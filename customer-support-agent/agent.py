import os
import sys
import asyncio
import warnings
from typing import Any

# Suppress SyntaxWarning from deepteam dependencies during import
warnings.filterwarnings("ignore", category=SyntaxWarning)

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import config

from pathlib import Path
from dotenv import load_dotenv

from langchain.agents import create_agent
from langchain.tools import tool, ToolRuntime
from langchain_openrouter import ChatOpenRouter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_tavily import TavilySearch
from langchain_mcp_adapters.client import MultiServerMCPClient
from guardrail import check_input, check_output

from dataclasses import dataclass
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.store.memory import InMemoryStore

# ---------------------------------------------------------
# Environment
# ---------------------------------------------------------

load_dotenv()

OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")
TAVILY_API_KEY = os.environ.get("TAVILY_API_KEY")

if not OPENROUTER_API_KEY:
    raise RuntimeError("OPENROUTER_API_KEY is not set.")

if not TAVILY_API_KEY:
    raise RuntimeError("TAVILY_API_KEY is not set.")

BASE_DIR = Path(__file__).resolve().parent
DB_DIR = BASE_DIR / "chroma_db"

# ---------------------------------------------------------
# 1. OpenRouter reasoning model
# ---------------------------------------------------------

model = config.get_agent_model()

# ---------------------------------------------------------
# 2. BGE-M3 embeddings
# ---------------------------------------------------------


class OpenRouterEmbeddings(OpenAIEmbeddings):
    def embed_documents(self, texts, chunk_size=None, **kwargs):
        embeddings = []
        for text in texts:
            response = self.client.create(model=self.model, input=text)
            embeddings.append(response.data[0].embedding)
        return embeddings

    def embed_query(self, text, **kwargs):
        response = self.client.create(model=self.model, input=text)
        return response.data[0].embedding


embeddings = OpenRouterEmbeddings(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,  # type: ignore
    model=config.embedding_model,
)

# ---------------------------------------------------------
# 3. Chroma vector database
# ---------------------------------------------------------

vectorstore = Chroma(
    collection_name="support_docs",
    persist_directory=str(DB_DIR),
    embedding_function=embeddings,
)

# short memory
checkpointer = InMemorySaver()

# ---------------------------------------------------------
# 4. Retriever
# ---------------------------------------------------------

retriever = vectorstore.as_retriever(search_kwargs={"k": 5})

# ---------------------------------------------------------
# 5. RAG tool
# ---------------------------------------------------------


@tool
def search_knowledge_base(query: str) -> str:
    """
    Search the internal knowledge base / support FAQ.

    Use this tool when the question concerns billing, technical
    issues, policies, or may be answered using FAQ documents.
    """

    documents = retriever.invoke(query)

    if not documents:
        return "No relevant internal documents were found."

    results = []

    for i, document in enumerate(documents, start=1):
        source = document.metadata.get("source", "unknown")

        results.append(
            f"""
SOURCE TYPE: INTERNAL KNOWLEDGE BASE
DOCUMENT: {i}
SOURCE: {source}

CONTENT:
{document.page_content}
"""
        )

    return "\n".join(results)


# ---------------------------------------------------------
# 6. Web search
# ---------------------------------------------------------

web_search = TavilySearch(max_results=5)


@tool
def search_web(query: str) -> str:
    """
    Search the public web.

    Use this tool for current, recent, external, or
    time-sensitive information that may not exist in
    the internal knowledge base.
    """

    result = web_search.invoke({"query": query})

    return str(result)

# ---------------------------------------------------------
# 7. MCP utility tools (word_count, format_citation) — served
#    by mcp_server.py, nothing to do with retrieval.
# ---------------------------------------------------------

mcp_client = MultiServerMCPClient(
    {
        "utils": {
            "transport": "stdio",
            "command": sys.executable,
            "args": [str(BASE_DIR / "mcp_server.py")],
        }
    }
)

mcp_tools = []

# long memory
store = InMemoryStore()


@dataclass
class Context:
    user_id: str


@tool
def remember_fact(fact: str, runtime: ToolRuntime[Context]) -> str:
    """
    Save a fact about the user or their preferences for future
    conversations (e.g. "prefers concise answers", "researching RAG systems").
    """
    if runtime.store is None:
        return "Memory store is not available."
    key = str(hash(fact))[:8]
    runtime.store.put(("user_facts", runtime.context.user_id), key, {"fact": fact})
    return "Saved."


@tool
def recall_facts(runtime: ToolRuntime[Context]) -> str:
    """Retrieve previously saved facts about the user."""
    if runtime.store is None:
        return "Memory store is not available."
    items = runtime.store.search(("user_facts", runtime.context.user_id))
    if not items:
        return "No saved facts about this user yet."
    return "\n".join(item.value["fact"] for item in items)


# ---------------------------------------------------------
# 8. Agent system prompt
# ---------------------------------------------------------

#   prompt1.txt -- original prompt (no explicit planning step)
#   prompt2.txt -- current prompt (adds a "state your plan" instruction)

PROMPT_PATH = BASE_DIR / "prompt1.txt"

SYSTEM_PROMPT = PROMPT_PATH.read_text(encoding="utf-8")

# ---------------------------------------------------------
# 9. Create agent
# ---------------------------------------------------------

agent: Any = None

async def init_agent():
    global mcp_tools, agent
    if agent is None:
        mcp_tools = await mcp_client.get_tools()
        agent = create_agent(
            model=model,
            tools=[
                search_knowledge_base,
                search_web,
                *mcp_tools,
                remember_fact,
                recall_facts,
            ],
            system_prompt=SYSTEM_PROMPT,
            checkpointer=checkpointer,
            store=store,
            context_schema=Context,
        )


# ---------------------------------------------------------
# 9b. Traced invocation helper (for DeepEval agentic metrics)
# ---------------------------------------------------------

async def invoke_with_tracing(question: str, thread_id: str = "default", user_id: str = "default", agent_instance=None):
    from deepeval.integrations.langchain import CallbackHandler
    
    await init_agent()

    # --- Input guardrail ---
    input_res = check_input(question)
    if not input_res["allowed"]:
        raise ValueError(
            "Input blocked by guardrails:\n" + str(input_res.get("message", "No reason provided."))
        )

    target_agent = agent_instance or agent

    result = await target_agent.ainvoke(
        {"messages": [{"role": "user", "content": question}]},
        config={
            "configurable": {"thread_id": thread_id},
            "callbacks": [CallbackHandler()],
        },
        context=Context(user_id=user_id),
    )

    # --- Output guardrail ---
    output_text = result["messages"][-1].content
    output_res = check_output(question, output_text)
    if not output_res["allowed"]:
        raise ValueError(
            "Output blocked by guardrails:\n" + str(output_res.get("message", "No reason provided."))
        )

    return result


# ---------------------------------------------------------
# 10. Run agent
# ---------------------------------------------------------


async def main():
    await init_agent()

    print("=" * 70)
    print("CUSTOMER SUPPORT AGENT")
    print("=" * 70)

    print("\nAvailable tools:")
    print("  - search_knowledge_base")
    print("  - search_web")
    for t in mcp_tools:
        print(f"  - {t.name} (MCP)")
    print("  - remember_fact")
    print("  - recall_facts")

    while True:
        print("\n" + "-" * 70)

        question = input("User request: ").strip()

        if not question:
            continue

        if question.lower() in {"exit", "quit"}:
            print("\nExiting.")
            break

        print("\nAgent is investigating...\n")

        try:
            input_res = check_input(question)
            if not input_res["allowed"]:
                print("=" * 70)
                print("BLOCKED: Input violated guardrails.")
                print("=" * 70)
                print(f"- {input_res.get('message', 'No reason provided.')}")
                continue

            result = await agent.ainvoke(
                {"messages": [{"role": "user", "content": question}]},
                config={"configurable": {"thread_id": "cli-session"}},
                context=Context(user_id="cli-user"),
            )

            output_text = result["messages"][-1].content
            output_res = check_output(question, output_text)
            
            if not output_res["allowed"]:
                print("=" * 70)
                print("BLOCKED: Output violated guardrails.")
                print("=" * 70)
                print(f"- {output_res.get('message', 'No reason provided.')}")
                continue

            print("=" * 70)
            print("ANSWER")
            print("=" * 70)
            print(output_text)

        except Exception as e:
            print("\nAgent error:")
            print(repr(e))


if __name__ == "__main__":
    asyncio.run(main())