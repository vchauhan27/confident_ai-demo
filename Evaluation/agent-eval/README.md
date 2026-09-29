# Agent Evaluation Framework

## Part 1: Trace-Based Metrics

These metrics analyze the entire execution trace (trajectory) of the agent, including its internal thought process and sequence of actions.

- **Task Completion (`TaskCompletionMetric`)**: Measures whether the agent ultimately completed the requested task successfully.
- **Step Efficiency (`StepEfficiencyMetric`)**: Evaluates whether the agent reached the goal using an optimal sequence of steps, penalizing unnecessary or redundant actions.
- **Plan Adherence (`PlanAdherenceMetric`)**: Measures how well the agent adhered to a logical plan or instructions during its execution loop.
- **Plan Quality (`PlanQualityMetric`)**: Assesses the quality, safety, and robustness of the agent's internal planning.

**Application**: A golden query is provided, such as *"What is the refund policy for the Enterprise plan, and can you check my ticket status?"* The agent is invoked with tracing enabled (`invoke_with_tracing`), capturing every intermediate step, thought, and tool call for the judge model to analyze.

## Part 2: Tool-Call-Based Metrics (Jev-as-a-Judge)

These metrics focus specifically on the agent's ability to select and use its available tools correctly. We have replaced the generative LLM-as-a-judge metrics (formerly `ToolCorrectnessMetric` and `ArgumentCorrectnessMetric`) with **JevEval** (`Tool Faithfulness`). 

By using Jev-as-a-Judge, tool evaluation relies on deterministic, mathematically traceable probability outputs rather than generative reasoning. The metric answers bounded questions:
- **(Noul)** Did every fact and figure in the output come from a tool?
- **(Noul)** Were the facts from tools reported accurately?
- **(Score)** How completely grounded is the output overall?
- **(Choice)** How did it handle information that the tools did not return?

**Application**: We define test cases that specify the `expected_tools` (e.g., `search_knowledge_base` followed by `check_ticket_status`). The script captures the tools the agent *actually* called and their arguments, evaluating their correctness strictly against the Jev logic.

## Example Output

## Troubleshooting & Common Pitfalls

### Agent State Memory Leakage (Cross-Contamination)
**Symptoms:** 
- The agent fails `StepEfficiencyMetric` or `PlanAdherenceMetric` with reasons indicating it was "answering unrelated questions" or "performing unnecessary web searches."
- In the DeepEval CLI output, the `Actual Output` trace for one test case includes the user's prompt or the agent's response from a *previous* test case.

**Cause:**
Agents built with short-term memory (e.g., LangGraph with `InMemorySaver`) track conversations via a `thread_id`. If multiple evaluation test cases are run sequentially using the same default `thread_id`, the agent remembers the entire conversation history from the previous tests. The judge model sees this inherited context, assumes the agent is hallucinating or executing irrelevant plans, and heavily penalizes the agent.

**Fix:**
This framework is configured to generate a unique `thread_id` using `uuid.uuid4()` for every test case execution inside the evaluation loop. This ensures each test case is run in complete isolation with a fresh memory state. 
```python
import uuid
import asyncio

async def main():
    for golden in trace_dataset.evals_iterator(metrics=trace_metrics):
        await invoke_with_tracing(golden.input, thread_id=str(uuid.uuid4()))
```

### JevEval "Tool Faithfulness" Fails but LLM Judge Passes
**Symptoms:** 
- A standard LLM-as-a-Judge (`Tool Correctness`) gives the agent a perfect score (1.0).
- However, JevEval (`Tool Faithfulness`) heavily penalizes the agent, claiming facts were "Mostly fabricated" or "stated_it_as_fact" (even when the agent answered correctly).

**Cause:**
- **Different Evaluation Scopes**: The LLM Judge (`Tool Correctness`) merely checks if the expected tool name was invoked (e.g., `search_knowledge_base`). It completely ignores whether the agent hallucinated in its final response. JevEval's Tool Faithfulness, on the other hand, strictly checks if the agent's final answer is grounded *only* in the facts returned by the tool.
- **Missing Tool Outputs**: If the evaluation script extracts `tools_called` but forgets to populate the `output` field of the `ToolCall`, JevEval assumes the tool returned *nothing*. Consequently, it treats every single fact in the agent's response as an ungrounded hallucination.
- **Pre-trained Knowledge**: If the agent ignores the tool's brief output and goes off-script to provide a highly detailed response using its pre-trained external knowledge, JevEval will correctly penalize it for bringing in ungrounded facts.

**Fix:**
Ensure that when constructing `ToolCall` objects for DeepEval, you map the actual execution result (e.g., the content from LangChain's `ToolMessage`) to the `output` field of the `ToolCall`.

```python
# First, map tool outputs by their tool_call_id
tool_outputs = {msg.tool_call_id: msg.content for msg in result["messages"] if hasattr(msg, 'tool_call_id') and msg.tool_call_id}

# Then attach them to the ToolCall object
for msg in result["messages"]:
    if hasattr(msg, 'tool_calls') and msg.tool_calls:
        for tc in msg.tool_calls:
            output = tool_outputs.get(tc.get('id'))
            tools_called.append(ToolCall(name=tc['name'], input_parameters=tc['args'], output=output))
```
