# Evaluation Suite for Customer Support Agent

This directory contains a comprehensive evaluation suite built with [DeepEval](https://github.com/confident-ai/deepeval) to rigorously test the **Customer Support Agent**.

The suite is broken down into specific evaluation domains to test different components of the agent's architecture (RAG, agentic planning, multi-turn conversation, and deterministic gating).

---

## 🏗️ Architecture Evaluated

The agent being evaluated is a LangChain/LangGraph-based **Customer Support Agent** equipped with:
- **RAG Tool (`search_knowledge_base`)**: BGE-M3 embeddings over a Chroma vector DB.
- **Web Tool (`search_web`)**: Tavily public web search.
- **Memory Tools (`remember_fact` & `recall_facts`)**: LangGraph `InMemoryStore` for long-term user facts.
- **MCP Utility Tools**: FastMCP tools (e.g., `check_ticket_status`, `create_ticket`).

---

## 📁 Evaluation Modules

### 1. Agent Evaluation (`agent-eval/`)
Evaluates the core reasoning and tool-calling capabilities of the agent.
- **Trace-Based Metrics**: Analyzes the execution trace (`TaskCompletionMetric`, `StepEfficiencyMetric`, `PlanAdherenceMetric`, `PlanQualityMetric`).
- **Tool-Call-Based Metrics (Jev-as-a-Judge)**: Deterministically evaluates tool faithfulness using JevEval primitives (`Noul`, `Choice`) instead of generative LLM-as-a-judge.

### 2. RAG Evaluation (`rag-eval/`)
Evaluates the retrieval pipeline and the groundedness of single-turn answers.
- **Metrics**: `AnswerRelevancyMetric`, `ConversationalJevEval` (for Faithfulness), `ContextualRelevancyMetric`, `ContextualPrecisionMetric`, `ContextualRecallMetric`.

### 3. Multi-Turn Evaluation (`multi-turn-eval/`)
Evaluates the agent's behavior across a full conversation (e.g., simulating a frustrated user).
- **Conversation-level**: `TurnRelevancyMetric`, `RoleAdherenceMetric`, `KnowledgeRetentionMetric`, `ConversationCompletenessMetric`, `GoalAccuracyMetric`.
- **RAG-quality per turn**: Assesses retrieval quality at specific turns in the conversation.

### 4. Strict Gates Framework (`DAG/`)
Compares generative LLM DAGs (DeepAcyclicGraphs) against **JevEval**.
- Evaluates specific hard rules (e.g., "Memory Recall Gate") deterministically, checking if the agent successfully remembered information from previous turns.

### 5. GEval Custom Prompts (`GEval/`)
Uses an LLM-as-a-judge for subjective, format-related grading.
- **Format Adherence**: Validates if the agent's response follows the expected markdown structure, separates internal KB sources from web sources, etc.

---

## 🚀 Running the Evaluations

Each subdirectory contains its own test scripts. Make sure your `.env` file at the root is configured with `OPENROUTER_API_KEY` and `TAVILY_API_KEY` before running the evals. DeepEval results will be output to the console and can be integrated with Confident AI.
