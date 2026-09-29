# Customer Support Agent Red Teaming Suite

This directory contains the automated red teaming suite for the Customer Support Agent. It leverages the `deepteam` framework to comprehensively evaluate the resilience, safety, and reliability of the underlying AI models, autonomous agents, and RAG (Retrieval-Augmented Generation) systems.

## Overview

The red teaming scripts simulate adversarial interactions to expose vulnerabilities across four main domains:

### 1. Autonomous Agent Behavior (`aiagent.py`)
Focuses on vulnerabilities specific to tool-using AI agents.
* **Target Purpose:** Customer Support Agent that answers user queries, checks ticket status, and creates support tickets.
* **Vulnerabilities Tested:** Goal Theft, Excessive Agency, Tool Orchestration Abuse, Exploit Tool Agent, Indirect Instruction, Autonomous Agent Drift.
* **Attacks Used:** Context Poisoning, Goal Redirection, System Override, Permission Escalation, Linear Jailbreaking.
* **Report Output:** `AIAgent.md`

### 2. Conversational Safety (`convo.py`)
Evaluates the model's resistance to complex, multi-turn adversarial dialogue.
* **Target Purpose:** Conversational Customer Support Agent assisting users with inquiries and support iteratively.
* **Vulnerabilities Tested:** Toxicity, Illegal Activity, Personal Safety, Bias, PII Leakage, Prompt Leakage.
* **Attacks Used:** Linear Jailbreaking, Crescendo Jailbreaking, Sequential Jailbreak, Tree Jailbreaking, Bad Likert Judge.
* **Report Output:** `convo.md`

### 3. RAG System Integrity (`rag.py`)
Assesses the robustness of the retrieval pipeline and how the model handles poisoned or flooded contexts.
* **Target Purpose:** Customer Support Agent with RAG analyzing internal knowledge base documents and FAQs.
* **Vulnerabilities Tested:** Robustness, PII Leakage, Prompt Leakage, Cross-Context Retrieval, Misinformation, Hallucination.
* **Attacks Used:** Prompt Injection, Context Flooding, Synthetic Context Injection, Roleplay, Leetspeak.
* **Report Output:** `rag.md`

### 4. Responsible AI & Ethics (`responsible.py`)
Focuses on core ethical tenets and safety guardrails.
* **Target Purpose:** Customer Support Agent answering support queries and resolving user issues securely.
* **Vulnerabilities Tested:** Bias, Toxicity, Fairness, Misinformation, Hallucination, Personal Safety, Ethics.
* **Attacks Used:** Prompt Injection, Roleplay, Crescendo Jailbreaking.
* **Report Output:** `ResponsibleAI.md`

## Configuration

* **`config.py`**: Manages the LLM setup for both the AI agent being tested and the "judge" model evaluating the interactions. By default, it uses `langchain_openrouter` and `deepeval` to configure the models (e.g., `dots-studio/dots-3-note-preview:free`).

### Using Jev as a Judge
For more robust evaluations, you can configure DeepEval to use **Jev** (a System One decision model) as the judge instead of a generative LLM. Jev is highly recommended for red teaming because:
1. **Resilience to Attacks:** Jev outputs probability distributions instead of generated text, making it virtually immune to "judge jailbreaks" where adversarial prompts confuse standard LLM evaluators.
2. **Precise Behavior Classification:** You can use Jev's `Choice` primitive to definitively categorize how a model reacted to an attack (e.g., `refused`, `hedged`, `complied`).
3. **Strict Boundaries:** You can use Jev's `Noul` primitive for binary pass/fail conditions (e.g., "Did the agent execute an unauthorized tool?").

To integrate Jev, replace the standard generative judge model in your setup with a `JevEval` metric containing bounded questions (`Noul`, `Choice`, `Score`).

## Architectural Notes on Agent Evaluation

### The `model_callback` Flow (Memory & Guardrails)
When evaluating agents with DeepTeam (e.g., in `aiagent.py`), you must explicitly construct the agent's memory using a `model_callback`. You **cannot** use the agent's standard execution wrapper (like `invoke_with_tracing` or LangGraph's checkpointer) for the following reasons:

1. **The Memory Problem (Why we need statelessness):**
   DeepTeam executes dozens of multi-turn conversational attacks concurrently. If we relied on the agent's internal database memory (e.g., using a single `thread_id`), the concurrent tests would bleed into each other. For example, an attack designed to steal goals might pollute the memory of an attack testing context poisoning.
2. **The Solution (Manual History Construction):**
   To ensure strict isolation, DeepTeam provides the exact, isolated conversational history for every iteration via the `turns` array. Inside `model_callback`, we force the agent to have "amnesia" by manually constructing a clean LangChain history array from `turns` and feeding it directly into the raw core of the agent (`agent.ainvoke`).
3. **Re-enforcing Guardrails:**
   Because we completely bypassed the agent's standard `invoke_with_tracing` wrapper to inject this stateless history, we *also* accidentally bypassed any guardrails (like `check_input` and `check_output`) living inside it. Therefore, we **must** manually copy and re-invoke those guardrail functions directly inside the `model_callback` to ensure they are actively tested during the red teaming assessment.

## How to Run

Ensure your environment is activated and API keys (e.g., `OPENROUTER_API_KEY`) are set. You can execute each script independently:

```bash
# Run agent-specific red teaming
python aiagent.py

# Run conversational safety red teaming
python convo.py

# Run RAG robustness red teaming
python rag.py

# Run responsible AI red teaming
python responsible.py
```

## Dependencies

* `deepteam`: The core automated red teaming framework.
* `langchain_core` / `langchain_openrouter`: Used to format the message history and invoke the underlying LangGraph agent.
* `deepeval`: Provides the evaluation capabilities and judge models.
