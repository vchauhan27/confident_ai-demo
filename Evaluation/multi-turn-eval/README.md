# Multi-Turn Evaluation

This directory evaluates the agent's behavior **across a full conversation**, not just a single Q&A pair. It runs 11 [DeepEval](https://github.com/confident-ai/deepeval) conversational metrics, each tested against one golden question.

## How it works

1. Each golden question is sent to the live agent on a fresh `thread_id`
2. The agent's full message trace (user turn, tool calls, AI response) is collapsed into DeepEval `Turn` objects
3. A judge LLM scores the conversation using the specified metric

All 11 metrics run sequentially in a single script.

---

## Metrics

### Conversation-level (how the agent behaves overall)

| # | Metric | What it checks | Golden question strategy |
|---|---|---|---|
| 1 | **Turn Relevancy** | Is the response relevant to what the user asked? | Straightforward knowledge question |
| 2 | **Role Adherence** | Does the agent stay in its defined role? | Asks the agent to break character ("chat casually about your weekend") |
| 3 | **Knowledge Retention** | Does the agent remember facts the user shared in the same turn? | User shares name + research goal, then asks a question |
| 4 | **Conversation Completeness** | Did the agent address all parts of the user's request? | Two-part question (explain a concept + format a citation) |
| 5 | **Goal Accuracy** | Did the agent accomplish the user's task? | Clear, verifiable task (count words in a sentence) |
| 6 | **Tool Use (Jev)** | Did the agent call the right tools? Evaluated deterministically with Jev. | Task that should use a specific MCP tool |
| 7 | **Topic Adherence** | Did the agent stay on-topic? | Deliberately off-topic request ("recommend a pizza place") |

### RAG-quality per turn (how well the agent uses retrieved context)

| # | Metric | What it checks |
|---|---|---|
| 8 | **Turn Faithfulness (Jev)** | Is the answer supported by what was retrieved? Evaluated deterministically with Jev. |
| 9 | **Turn Contextual Precision** | Are the most relevant retrieved chunks ranked highest? |
| 10 | **Turn Contextual Recall** | Did the retrieval find all the information needed for the expected answer? |
| 11 | **Turn Contextual Relevancy** | Are the retrieved chunks actually relevant to the question? |

> Metrics 9 and 10 require an `expected_outcome` to compare against. Metrics 8 and 11 only need the `retrieval_context` that the agent naturally produces.

---

## Key helpers in the code

- **`run_agent_turn(question, thread_id)`** — Invokes the agent once and returns its full message trace
- **`build_turns(messages, question)`** — Collapses a LangGraph message trace into two DeepEval `Turn`s (one user, one assistant) with `tools_called` and `retrieval_context` attached
- **`run_case(label, question, metric)`** — Runs the agent → builds turns → measures the metric → prints results

## Running

```bash
python multi_turn_metrics.py
```

Prints a summary table at the end:

```
SUMMARY
======================================================================
TurnRelevancyMetric                 0.85
RoleAdherenceMetric                 1.0
KnowledgeRetentionMetric            0.9
...
```
