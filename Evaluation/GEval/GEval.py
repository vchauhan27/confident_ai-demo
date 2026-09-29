import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
import config

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'research-agent')))
import agent as agent_module  # type: ignore
from agent import Context  # type: ignore

from deepeval import evaluate
from deepeval.evaluate import AsyncConfig
from deepeval.test_case import LLMTestCase, SingleTurnParams
from deepeval.metrics import GEval


# ---------------------------------------------------------
# Judge model  (provider configured in config.py)
# ---------------------------------------------------------

JUDGE_MODEL = config.get_judge_model()

# ---------------------------------------------------------
# G-Eval metric
# ---------------------------------------------------------
# Checks a subjective quality that no other metric covers: does the
# answer actually follow the format rules laid out in the system prompt
# (answer first, then reasoning, then distinguish internal vs web
# sources)?

format_adherence_metric = GEval(
    name="Format Adherence",
    evaluation_steps=[
        "Check whether the answer is given first, before any explanation.",
        "Check whether reasoning or evidence is explained after the answer.",
        "Check whether internal knowledge base info is clearly distinguished "
        "from web search info, when both are used in the answer.",
        "Penalize heavily if the answer does not follow this structure.",
    ],
    evaluation_params=[
        SingleTurnParams.INPUT,
        SingleTurnParams.ACTUAL_OUTPUT,
    ],
    threshold=0.7,
    model=JUDGE_MODEL,
    async_mode=False,
)


# ---------------------------------------------------------
# Test cases
# ---------------------------------------------------------

import json

json_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'Data-Generation', 'singleturn_goldens.json'))
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        QUESTIONS = [item["input"] for item in data]
except Exception as e:
    print(f"Could not load singleturn_goldens.json, falling back to hardcoded. Error: {e}")



import asyncio

async def run_agent(question: str, thread_id: str) -> str:
    await agent_module.init_agent()
    result = await agent_module.agent.ainvoke(
        {"messages": [{"role": "user", "content": question}]},
        config={"configurable": {"thread_id": thread_id}},
        context=Context(user_id="eval-user"),
    )
    return result["messages"][-1].content


async def generate_test_cases():
    cases = []
    for i, question in enumerate(QUESTIONS):
        # Use a unique thread_id per question to prevent cross-contamination
        # from the checkpointer's conversation history.
        actual_output = await run_agent(question, thread_id=f"geval-eval-{i}")

        print(f"Q: {question}")
        print(f"A: {actual_output[:200]}...\n")

        cases.append(
            LLMTestCase(
                input=question,
                actual_output=actual_output,
            )
        )
    return cases

test_cases = asyncio.run(generate_test_cases())

evaluate(
    test_cases=test_cases,
    metrics=[format_adherence_metric],
    async_config=AsyncConfig(
        run_async=False,
        throttle_value=1,
        max_concurrent=1,
    ),
)