import sys
import os
import uuid
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'customer-support-agent')))
import config

import asyncio
import agent as agent_module #type: ignore

asyncio.run(agent_module.init_agent())
agent = agent_module.agent
retriever = agent_module.retriever


from deepeval import evaluate
from deepeval.evaluate import AsyncConfig
from deepeval.test_case import LLMTestCase
from deepeval.metrics import (
    FaithfulnessMetric,
    AnswerRelevancyMetric,
    ContextualRelevancyMetric,
    ContextualPrecisionMetric,
    ContextualRecallMetric,
)

# ---------------------------------------------------------
# Judge model  (provider configured in config.py)
# ---------------------------------------------------------

os.environ.setdefault("DEEPEVAL_PER_ATTEMPT_TIMEOUT_SECONDS_OVERRIDE", "2000")

JUDGE_MODEL = config.get_judge_model()

# ---------------------------------------------------------
# Test cases (Single-Turn RAG)
# ---------------------------------------------------------

json_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'Data-Generation', 'singleturn_goldens.json'))
TEST_CASES_DATA = []

try:
    with open(json_path, 'r') as f:
        TEST_CASES_DATA = json.load(f)
except FileNotFoundError:
    print(f"Could not find synthetic data at {json_path}. Please run golden_synthesis.py first.")

# ---------------------------------------------------------
# Patch the Retriever to capture individual text chunks
# ---------------------------------------------------------

captured_chunks = []
original_invoke = type(retriever).invoke

def patched_invoke(self, *args, **kwargs):
    docs = original_invoke(self, *args, **kwargs)
    # DeepEval RAG metrics require a list of individual text chunks, 
    # not a single concatenated string.
    captured_chunks.extend([doc.page_content for doc in docs])
    return docs

type(retriever).invoke = patched_invoke

# ---------------------------------------------------------
# Run the agent for a single turn
# ---------------------------------------------------------

def run_rag_test_case(item: dict) -> LLMTestCase:
    thread_id = str(uuid.uuid4())
    question = item["input"]
    expected_output = item["expected_output"]
    
    # Reset chunks for this specific run
    captured_chunks.clear()
    
    # Run agent
    result = agent.invoke(
        {"messages": [{"role": "user", "content": question}]},
        config={"configurable": {"thread_id": thread_id}},
    )
    
    actual_output = result["messages"][-1].content
    
    return LLMTestCase(
        input=question,
        actual_output=actual_output,
        expected_output=expected_output,
        retrieval_context=captured_chunks.copy()
    )


# ---------------------------------------------------------
# Metrics 
# ---------------------------------------------------------


metrics = [
    FaithfulnessMetric(
        threshold=0.7,
        model=JUDGE_MODEL,
        include_reason=True,
        async_mode=False,
    ),
    AnswerRelevancyMetric(
        threshold=0.7,
        model=JUDGE_MODEL,
        include_reason=True,
        async_mode=False,
    ),
    ContextualRelevancyMetric(
        threshold=0.7,
        model=JUDGE_MODEL,
        include_reason=True,
        async_mode=False,
    ),
    ContextualPrecisionMetric(
        threshold=0.7,
        model=JUDGE_MODEL,
        include_reason=True,
        async_mode=False,
    ),
    ContextualRecallMetric(
        threshold=0.7,
        model=JUDGE_MODEL,
        include_reason=True,
        async_mode=False,
    ),
]

test_cases = []

print("=" * 70)
print("Evaluating Single-Turn RAG Agent")
print("=" * 70)

for item in TEST_CASES_DATA:
    test_case = run_rag_test_case(item)
    test_cases.append(test_case)

if test_cases:
    evaluate(
        test_cases=test_cases,
        metrics=metrics, # type: ignore
        async_config=AsyncConfig(
            run_async=False,
            throttle_value=1,
            max_concurrent=1,
        ),
    )
else:
    print("No test cases generated.")