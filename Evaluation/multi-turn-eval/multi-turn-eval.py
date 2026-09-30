"""
Runs 11 multi-turn DeepEval metrics, each against one golden conversation.
"""

import os
import re
import sys
import uuid
from pathlib import Path

# Increase DeepEval's execution timeout to prevent the 180s TimeoutError when running many metrics
os.environ.setdefault("DEEPEVAL_PER_ATTEMPT_TIMEOUT_SECONDS_OVERRIDE", "2000")

# ---------------------------------------------------------------------------
# Path setup (mirrors the pattern already used in agent.py / ingest.py)
# ---------------------------------------------------------------------------

THIS_DIR = Path(__file__).resolve().parent
ROOT_DIR = THIS_DIR.parent.parent          # repo root (where config.py lives)
RESEARCH_AGENT_DIR = ROOT_DIR / "customer-support-agent"

sys.path.append(str(ROOT_DIR))
sys.path.append(str(RESEARCH_AGENT_DIR))

import config  # noqa: E402  (root config.py)

import agent as agent_module # type: ignore
from agent import (  # type: ignore  # noqa: E402
    Context,
    search_knowledge_base,
    search_web,
    remember_fact,
    recall_facts,
)
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage  # noqa: E402

from deepeval.test_case import Turn, ConversationalTestCase, ToolCall  # noqa: E402
from deepeval.metrics import (  # noqa: E402
    TurnRelevancyMetric,
    RoleAdherenceMetric,
    KnowledgeRetentionMetric,
    ConversationCompletenessMetric,
    GoalAccuracyMetric,
    ToolUseMetric,
    TopicAdherenceMetric,
    TurnFaithfulnessMetric,
    TurnContextualPrecisionMetric,
    TurnContextualRecallMetric,
    TurnContextualRelevancyMetric,
)

EVAL_MODEL = config.get_judge_model()   # judge model object (provider set in config.py)


def make_metric(metric_cls, **kwargs):
    if EVAL_MODEL is not None:
        kwargs.setdefault("model", EVAL_MODEL)
    return metric_cls(**kwargs)


# ---------------------------------------------------------------------------
# Tool inventory (for ToolUseMetric's required `available_tools`)
# ---------------------------------------------------------------------------

# Tool inventory will be created in main after mcp_tools are loaded

# ---------------------------------------------------------------------------
# Helpers: run the live agent and turn its trace into DeepEval Turns
# ---------------------------------------------------------------------------

async def run_agent_turn(question: str, thread_id: str, user_id: str = "eval-user"):
    """Invoke the customer support agent once and return its full message trace."""
    result = await agent_module.agent.ainvoke(
        {"messages": [{"role": "user", "content": question}]},
        config={"configurable": {"thread_id": thread_id}},
        context=Context(user_id=user_id),
    )
    return result["messages"]


def extract_retrieval_context(tool_output: str):
    """
    Turn search_knowledge_base's formatted blob into a list of individual chunks.
    """
    if "No relevant internal documents were found." in tool_output:
        return [tool_output.strip()]

    chunks = re.split(r"\nSOURCE TYPE: INTERNAL KNOWLEDGE BASE", tool_output)
    contents = []
    for chunk in chunks:
        match = re.search(r"CONTENT:\s*(.+)", chunk, re.DOTALL)
        if match:
            contents.append(match.group(1).strip())

    return contents or [tool_output.strip()]


def build_multi_turns(messages):
    """
    Collapse a full LangGraph message trace into a sequence of DeepEval Turns,
    properly pairing Human and AI messages into the Conversational format.
    """
    turns = []
    current_user_msg = None
    current_ai_content = ""
    current_tools = []
    current_retrieval = []

    def flush_turn():
        if current_user_msg is not None:
            turns.append(Turn(role="user", content=current_user_msg))
            turns.append(Turn(
                role="assistant",
                content=current_ai_content.strip(),
                tools_called=current_tools if current_tools else None,
                retrieval_context=current_retrieval if current_retrieval else None,
            ))

    for msg in messages:
        if isinstance(msg, HumanMessage):
            flush_turn()
            if isinstance(msg.content, list):
                current_user_msg = " ".join(p.get("text", "") if isinstance(p, dict) else str(p) for p in msg.content)
            else:
                current_user_msg = str(msg.content)
            current_ai_content = ""
            current_tools = []
            current_retrieval = []
        elif isinstance(msg, AIMessage):
            if getattr(msg, "tool_calls", None):
                for tc in msg.tool_calls:
                    current_tools.append(
                        ToolCall(name=tc["name"], input_parameters=tc.get("args", {}) or {})
                    )
            if msg.content:
                if isinstance(msg.content, list):
                    content = " ".join(p.get("text", "") if isinstance(p, dict) else str(p) for p in msg.content)
                else:
                    content = msg.content
                current_ai_content += content + " "
        elif isinstance(msg, ToolMessage):
            if getattr(msg, "name", None) == "search_knowledge_base":
                current_retrieval.extend(extract_retrieval_context(str(msg.content)))

    flush_turn()
    return turns


from deepeval import evaluate
from deepeval.evaluate import AsyncConfig

async def get_conversation_turns(questions):
    thread_id = f"eval-multiturn-{uuid.uuid4().hex[:8]}"
    final_messages = []
    for q in questions:
        final_messages = await run_agent_turn(q, thread_id)
    return build_multi_turns(final_messages)

async def main():
    import asyncio
    import json
    await agent_module.init_agent()
    
    ALL_TOOLS = [search_knowledge_base, search_web, *agent_module.mcp_tools, remember_fact, recall_facts]
    AVAILABLE_TOOLS = [
        ToolCall(name=t.name, input_parameters={})
        for t in ALL_TOOLS
    ]

    print("Loading simulated multi-turn test case...")
    json_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'Data-Generation', 'multiturn_simulated_goldens.json'))
    
    simulated_questions = []
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            # Use the first simulated conversation, filter only the user's questions
            simulated_questions = [turn["content"] for turn in data[0]["turns"] if turn["role"] == "user"]
    except Exception as e:
        print(f"Warning: Could not load simulated goldens, falling back to hardcoded. Error: {e}")
        simulated_questions = [
            "What is retrieval augmented generation?",
            "And how does the BGE-M3 embedding model fit into it?"
        ]

    print("Generating conversation trace from agent...")
    turns = await get_conversation_turns(simulated_questions)

    test_case = ConversationalTestCase(
        turns=turns,
        chatbot_role=(
            "A customer support agent that answers questions using evidence from the "
            "internal knowledge base or the web. It does not role-play, "
            "make small talk, or claim to have personal experiences."
        ),
        expected_outcome=(
            "The assistant should state that ingestion uses the BGE-M3 "
            "embedding model served via OpenRouter, producing 1024-"
            "dimensional embeddings. "
            "The assistant should explain that documents are split using a "
            "RecursiveCharacterTextSplitter with chunk_size=800 and "
            "chunk_overlap=150."
        ),
    )

    metrics = [
        make_metric(TurnRelevancyMetric, threshold=0.5),
        make_metric(RoleAdherenceMetric, threshold=0.5),
        make_metric(KnowledgeRetentionMetric, threshold=0.5),
        make_metric(ConversationCompletenessMetric, threshold=0.5),
        make_metric(GoalAccuracyMetric, threshold=0.5),
        make_metric(ToolUseMetric, threshold=0.5, available_tools=AVAILABLE_TOOLS),
        make_metric(
            TopicAdherenceMetric,
            threshold=0.5,
            relevant_topics=[
                "retrieval augmented generation and RAG systems",
                "the internal research knowledge base and its documents",
                "citation formatting (APA/MLA)",
                "word counts, character counts, and reading time",
                "current AI/ML news or software releases found via web search",
            ],
        ),
        make_metric(TurnFaithfulnessMetric, threshold=0.5),
        make_metric(TurnContextualPrecisionMetric, threshold=0.5),
        make_metric(TurnContextualRecallMetric, threshold=0.5),
        make_metric(TurnContextualRelevancyMetric, threshold=0.5),
    ]

    print("Running multi-turn DeepEval metrics...")
    
    evaluate(
        test_cases=[test_case],
        metrics=metrics,
        async_config=AsyncConfig(
            run_async=False,
            throttle_value=1,
            max_concurrent=1,
        ),
    )

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
