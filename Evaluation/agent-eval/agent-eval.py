import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
import config

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'research-agent')))
from agent import agent, invoke_with_tracing, Context  # type: ignore

from deepeval.dataset import EvaluationDataset, Golden, get_current_golden
from deepeval.test_case import ToolCall
from deepeval.tracing import observe, update_current_span
from typing import List
from deepeval.metrics import (
    TaskCompletionMetric,
    StepEfficiencyMetric,
    PlanAdherenceMetric,
    PlanQualityMetric,
    ToolCorrectnessMetric,
    ArgumentCorrectnessMetric,
    # JevEval,
    # BaseMetric
)
# from deepeval.metrics.jev_eval import Noul, Score, Choice
# from deepeval.test_case import SingleTurnParams

# Judge model
JUDGE_MODEL = config.get_judge_model()

# ---------------------------------------------------------
# Define all metrics
# ---------------------------------------------------------

trace_metrics = [
    TaskCompletionMetric(threshold=0.7, model=JUDGE_MODEL, async_mode=False),
    StepEfficiencyMetric(threshold=0.7, model=JUDGE_MODEL, async_mode=False),
    PlanAdherenceMetric(threshold=0.7, model=JUDGE_MODEL, async_mode=False),
    PlanQualityMetric(threshold=0.7, model=JUDGE_MODEL, async_mode=False),
]

tool_metrics = [
    ToolCorrectnessMetric(threshold=0.7, model=JUDGE_MODEL, include_reason=True, async_mode=False),
    ArgumentCorrectnessMetric(threshold=0.7, model=JUDGE_MODEL, include_reason=True, async_mode=False)
]

# ---------------------------------------------------------
# Run agent evaluation
# ---------------------------------------------------------

import json

json_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'Data-Generation', 'multiturn_goldens.json'))
goldens_list = []

try:
    with open(json_path, 'r') as f:
        agent_data = json.load(f)
        for item in agent_data:
            goldens_list.append(
                Golden(
                    input=item["scenario"],
                    # Since these are factual questions, we expect the agent to search its knowledge base
                    expected_tools=[
                        ToolCall(name="search_knowledge_base", input_parameters={})
                    ],
                    multimodal=False
                )
            )
except FileNotFoundError:
    print(f"Could not find synthetic data at {json_path}.")

trace_dataset = EvaluationDataset(goldens=goldens_list)

print("=" * 70)
print("Evaluating Agentic Metrics (Trajectory + Component-level)")
print("=" * 70)

import asyncio
import uuid

@observe(type="tool")
def register_tool_call(tool_name, tool_args):
    update_current_span(name=tool_name, input=tool_args)

@observe(type="llm", metrics=tool_metrics)
async def call_agent_observed(user_input: str, thread_id: str):
    # Execute the trace
    result = await invoke_with_tracing(user_input, thread_id=thread_id)
    
    # Extract actual output from LangGraph's result
    output_text = result["messages"][-1].content if result.get("messages") else ""
    
    # Register tool calls as child spans so DeepEval recognizes them for the LLM span
    tools_called = []
    for msg in result.get("messages", []):
        if hasattr(msg, 'tool_calls') and msg.tool_calls:
            for tc in msg.tool_calls:
                register_tool_call(tc['name'], tc['args'])
                
                # Match tool call ID to the tool execution output
                output = ""
                for m in result.get("messages", []):
                    if getattr(m, "type", "") == "tool" and getattr(m, "tool_call_id", "") == tc.get("id"):
                        output = str(m.content)
                        break
                        
                tools_called.append(ToolCall(name=tc['name'], input_parameters=tc['args'], output=output))
    
    # Supply extracted fields to the span for the component-level metrics to evaluate
    golden = get_current_golden()
    if golden and golden.expected_tools:
        update_current_span(
            input=user_input,
            output=output_text,
            expected_tools=golden.expected_tools,
            tools_called=tools_called
        )
        
    return result

async def main():
    for golden in trace_dataset.evals_iterator(metrics=trace_metrics): # type: ignore
        await call_agent_observed(golden.input, str(uuid.uuid4()))

if __name__ == "__main__":
    asyncio.run(main())
