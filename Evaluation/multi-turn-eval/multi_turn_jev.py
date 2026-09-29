"""
Runs Multi-turn DeepEval Jev metrics against one golden conversation.
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
RESEARCH_AGENT_DIR = ROOT_DIR / "research-agent"

sys.path.append(str(ROOT_DIR))
sys.path.append(str(RESEARCH_AGENT_DIR))

import config  # noqa: E402  (root config.py)

import agent as agent_module # type: ignore
from agent import (  # type: ignore  # noqa: E402
    Context,
)
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage  # noqa: E402

from deepeval.test_case import Turn, ConversationalTestCase, ToolCall, MultiTurnParams  # noqa: E402
from deepeval.metrics.jev_eval import Noul, Score, Choice  # noqa: E402
from deepeval.metrics import ConversationalJevEval
from deepeval.models.system_one.typesafe_model import TypeSafeModel

EVAL_MODEL = config.get_judge_model()   # judge model object (provider set in config.py)

# ---------------------------------------------------------------------------
# Helpers: run the live agent and turn its trace into DeepEval Turns
# ---------------------------------------------------------------------------

async def run_agent_turn(question: str, thread_id: str, user_id: str = "eval-user"):
    """Invoke the research agent once and return its full message trace."""
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
    thread_id = f"eval-jev-{uuid.uuid4().hex[:8]}"
    final_messages = []
    for q in questions:
        final_messages = await run_agent_turn(q, thread_id)
    return build_multi_turns(final_messages)

async def main():
    import asyncio
    import json
    await agent_module.init_agent()

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
    )

    # 1. Tool Use Jev Eval
    tool_use_jev = ConversationalJevEval(
        name="Tool Use (Jev)",
        system_one_model=TypeSafeModel(
            model="typesafe/jev-1.13",
            api_key=os.environ.get("OPENROUTER_API_KEY"),
            base_url="https://openrouter.ai/api",
        ),
        evaluation_params=[MultiTurnParams.TOOLS_CALLED],
        questions=[
            Noul("The assistant called a tool rather than guessing the answer from memory.", weight=2),
            Score(
                "How appropriate was the tool choice?",
                levels=["Irrelevant tool", "Wrong tool", "Sub-optimal tool", "Perfect tool"],
            ),
            Choice(
                "What did the assistant do if the correct tool was not available?",
                options={
                    "hallucinated_a_tool": 0.0,
                    "apologized": 1.0,
                    "tool_was_available": None,
                }
            )
        ],
        include_reason=True
    )

    # 2. Turn Faithfulness Jev Eval
    turn_faithfulness_jev = ConversationalJevEval(
        name="Turn Faithfulness (Jev)",
        system_one_model=TypeSafeModel(
            model="typesafe/jev-1.13",
            api_key=os.environ.get("OPENROUTER_API_KEY"),
            base_url="https://openrouter.ai/api",
        ),
        evaluation_params=[MultiTurnParams.RETRIEVAL_CONTEXT],
        questions=[
            Noul("Every fact stated by the assistant appears in the retrieval_context.", weight=2),
            Score(
                "How much of the assistant's claims are grounded in the retrieval_context?",
                levels=["Fabricated", "Mostly fabricated", "Mostly grounded", "Fully grounded"],
            ),
            Choice(
                "What did the assistant do when asked for information not present in the retrieval_context?",
                options={
                    "flagged_it_as_unknown": 1.0,
                    "hedged_it": 0.5,
                    "stated_it_as_fact": 0.0,
                    "nothing_missing": None
                }
            )
        ],
        include_reason=True
    )

    print("Running multi-turn Jev metrics...")

    evaluate(
        test_cases=[test_case],
        metrics=[tool_use_jev, turn_faithfulness_jev],
        async_config=AsyncConfig(
            run_async=False,
            throttle_value=1,
            max_concurrent=1,
        ),
    )

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
