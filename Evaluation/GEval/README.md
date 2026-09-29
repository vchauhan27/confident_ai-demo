# GEval Framework

This directory contains the evaluation suite for assessing the agent's output using custom LLM-as-a-judge criteria, built with [DeepEval's](https://github.com/confident-ai/deepeval) GEval metric.

## What is GEval?

**GEval = "Use an LLM to grade another LLM's output."**

You write your grading rubric in plain English, and a judge LLM reads the output and gives it a score from 0 to 1.

### How it works (3 steps)

1. **You describe what "good" looks like** in natural language (the `evaluation_steps`).
2. **The judge LLM reads the agent's output** and works through your steps one by one (chain-of-thought).
3. **It produces a score** (0–1). DeepEval uses the judge's token log-probabilities to calculate this, making it more reliable than just asking the LLM to say a number.

### GEval vs JevEval — Why not use Jev here?

While other parts of this repository have replaced generative evaluations with deterministic **JevEval** checks, the metrics in this directory explicitly require GEval.

**Why?**
Jev is a System One model built exclusively for *bounded, objective* decisions (like "did it use this specific tool?"). However, the metrics here (like Coherence or Memory Consistency) evaluate **subjective qualities** that require open-ended reasoning and nuance. Jev cannot and should not be used to interpret subjective flow, logical sense, or conversational tone. For those tasks, you *must* use an LLM-as-a-judge (GEval) that can walk through a chain of thought to arrive at a holistic score.

**How is JevEval different from G-Eval?**
GEval asks an LLM to draft evaluation steps from a criteria and then generate a score, and uses token probabilities to smooth that number. JevEval has no generative judge: you write the questions, Jev returns calibrated probabilities, and the score is a fixed weighted mean. Use G-Eval when you want the LLM to figure out the logic; use JevEval when you know what you want decided and want it decided the same way every run.

| | GEval | JevEval |
|---|---|---|
| **What it is** | A generative LLM acting as a judge | A System One model returning calibrated probabilities |
| **Best for** | Subjective qualities (coherence, tone) | Hard rules (hallucination checks, tool usage) |
| **How it scores** | Generates a chain-of-thought and smooths token probabilities | Maps discrete probability distributions to fixed math |

---

## Metrics Calculated

### 1. Format Adherence (`GEval.py`)

> **Question it answers:** "Did the agent structure its answer correctly?"

Checks whether the agent's response follows the expected structure — answer first, then explanation, with internal KB sources distinguished from web sources.

**Input:** One question → one answer (`LLMTestCase`)

### Summary

| File | What it grades | Single or Multi-turn |
|---|---|---|
| `GEval.py` | Is the answer **formatted** right? | Single-turn |

---

## How It Is Applied

For single-turn evaluations, we provide an `input` and capture the `actual_output`. DeepEval's GEval uses a judge LLM to score the output based on defined criteria and evaluation steps.

- `GEval.py` runs **Format Adherence**.

## Running

```bash
python GEval.py               # Format Adherence
```

## Example Output