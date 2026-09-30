import sys
import os
import json
import asyncio
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
import config

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'customer-support-agent')))
import agent as agent_module  # type: ignore
from agent import Context  # type: ignore

from deepeval import evaluate
from deepeval.evaluate import AsyncConfig
from deepeval.test_case import Turn, ConversationalTestCase, MultiTurnParams
from deepeval.metrics import ConversationalJevEval
from deepeval.metrics import ConversationalJevEval
from deepeval.metrics.jev_eval import Noul
from deepeval.models.system_one.typesafe_model import TypeSafeModel

# ---------------------------------------------------------
# Judge model
# ---------------------------------------------------------

JUDGE_MODEL = config.get_judge_model()

# ---------------------------------------------------------
# Conversational JevEval metric (Replacing DAG)
# ---------------------------------------------------------

memory_recall_gate_metric = ConversationalJevEval(
    name="Memory Recall Gate (Jev)",
    system_one_model=TypeSafeModel(
        model="typesafe/jev-1.13",
        api_key=os.environ.get("OPENROUTER_API_KEY"),
        base_url="https://openrouter.ai/api",
    ),
    evaluation_params=[MultiTurnParams.CONTENT],
    questions=[
        Noul(
            "The assistant correctly recalled and used the fact the user "
            "shared in an earlier turn (their name or research goal) when "
            "answering a later, related question."
        )
    ],
    strict_mode=True,
)

# ---------------------------------------------------------
# Load Test Cases
# ---------------------------------------------------------

json_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'Data-Generation', 'multiturn_simulated_goldens.json'))
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        QUESTIONS = [turn["content"] for turn in data[0]["turns"] if turn["role"] == "user"]
except Exception as e:
    print(f"Could not load multiturn_simulated_goldens.json, falling back. Error: {e}")
    QUESTIONS = [
        "My name is Alex and I'm researching agentic RAG systems.",
        "Given what I just told you, what part of this knowledge base should I focus on first?",
    ]

async def run_conversation(questions, thread_id="jev-conversation-1"):
    await agent_module.init_agent()
    result = None
    for question in questions:
        result = await agent_module.agent.ainvoke(
            {"messages": [{"role": "user", "content": question}]},
            config={"configurable": {"thread_id": thread_id}},
            context=Context(user_id="eval-user"),
        )

    if result is None:
        return []
    return result["messages"]

def to_turns(messages):
    turns = []
    for message in messages:
        kind = type(message).__name__
        if kind == "HumanMessage":
            turns.append(Turn(role="user", content=message.content))
        elif kind == "AIMessage" and message.content:
            turns.append(Turn(role="assistant", content=message.content))
    return turns

async def main():
    messages = await run_conversation(QUESTIONS)
    turns = to_turns(messages)

    print("Conversation:")
    for turn in turns:
        print(f"  [{turn.role}] {turn.content[:150]}")
    print()

    convo_test_case = ConversationalTestCase(turns=turns)

    evaluate(
        test_cases=[convo_test_case],
        metrics=[memory_recall_gate_metric],
        async_config=AsyncConfig(
            run_async=False,
            throttle_value=1,
            max_concurrent=1,
        ),
    )

if __name__ == "__main__":
    asyncio.run(main())
