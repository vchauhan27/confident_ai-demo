# About — Research Agent

A comprehensive reference covering everything the research agent does: what it requires, how it thinks, which tools it calls, what memory it holds, and what it returns.

---

## Table of Contents

1. [Purpose](#1-purpose)
2. [What It Requires](#2-what-it-requires)
3. [Architecture at a Glance](#3-architecture-at-a-glance)
4. [Tools](#4-tools)
5. [Input & Output](#5-input--output)
6. [Reasoning & Planning](#6-reasoning--planning)
7. [Memory](#7-memory)
8. [Guardrails](#8-guardrails)
9. [Turn Flow — Step by Step](#9-turn-flow--step-by-step)
10. [Models & Configuration](#10-models--configuration)

---

## 1. Purpose

The research agent is an **evidence-driven question-answering system**.  
Its sole job is to answer questions accurately by retrieving real evidence from one or more sources before responding. It is explicitly **not** a general-purpose chatbot — it does not generate opinions, give advice, or answer out-of-scope questions.

Designed for:
- Deep factual lookup across internal document collections and the public web
- Academic citation and bibliography formatting
- Text measurement (word count, reading time)
- Persistent user preference memory across conversations

---

## 2. What It Requires

### API Keys (`.env`)

| Key | Purpose |
|---|---|
| `OPENROUTER_API_KEY` | Powers the agent chat model and the judge model via OpenRouter |
| `TAVILY_API_KEY` | Powers live web search via Tavily |
| `CONFIDENTAI_API_KEY` | Required by DeepEval for evaluation and guardrail scoring |

### Infrastructure

| Component | Technology |
|---|---|
| Vector database | **Chroma** — persisted locally at `research-agent/chroma_db/` |
| Embedding model | **BGE-M3** (`baai/bge-m3`) via OpenRouter — 1024-dimensional dense vectors |
| Agent / LLM runtime | **LangChain + LangGraph** |
| MCP utility server | **FastMCP** over `stdio` transport |

### Python Dependencies (key packages)

```
langchain, langgraph, langchain-openrouter, langchain-chroma
langchain-openai, langchain-tavily, langchain-mcp-adapters
deepeval, deepteam
mcp (FastMCP)
```

---

## 3. Architecture at a Glance

```
                          USER INPUT
                              │
                   ┌──────────▼──────────┐
                   │   Input Guardrail   │  ← PromptInjectionGuard
                   │                     │  ← TopicalGuard
                   └──────────┬──────────┘
                              │  (safe input passes)
                   ┌──────────▼──────────┐
                   │   Research Agent    │  ← Dots-3-Note (OpenRouter)
                   │   (LangChain +      │  ← System prompt (prompt1.txt)
                   │    LangGraph DAG)   │  ← Short-term memory (InMemorySaver)
                   └──┬──┬──┬──┬────────┘
                      │  │  │  │
          ┌───────────┘  │  │  └──────────────┐
          ▼              ▼  ▼                  ▼
  ┌──────────────┐  ┌─────────┐  ┌──────────────────────┐
  │retrieve_docs │  │search_  │  │  MCP Tools (FastMCP) │
  │              │  │web      │  │  ┌──────────────────┐ │
  │ BGE-M3 →     │  │         │  │  │  word_count      │ │
  │ Chroma DB    │  │ Tavily  │  │  │  format_citation │ │
  └──────┬───────┘  └────┬────┘  │  └──────────────────┘ │
         │               │       └──────────┬─────────────┘
         └───────────────┴──────────────────┘
                              │
                    ┌─────────▼─────────┐
                    │ LLM synthesises   │
                    │ answer from       │
                    │ retrieved evidence│
                    └─────────┬─────────┘
                              │
                   ┌──────────▼──────────┐
                   │  Output Guardrail   │  ← HallucinationGuard
                   │                     │  ← PrivacyGuard
                   └──────────┬──────────┘
                              │  (safe output passes)
                           ANSWER
```

---

## 4. Tools

The agent chooses tools autonomously based on the question. It is instructed to use the **minimum necessary** set of tools per turn.

### 4.1 `retrieve_documents` — RAG Tool

| Property | Detail |
|---|---|
| **What it does** | Semantic search over the internal Chroma vector database |
| **When used** | Question concerns internal documentation, knowledge base content, or the agent's own architecture |
| **Embedding** | BGE-M3 via OpenRouter (1024-dim dense vectors) |
| **Top-k** | Returns top **5** most relevant document chunks |
| **Output** | Formatted block per document: source file name + page content |

```
SOURCE TYPE: INTERNAL KNOWLEDGE BASE
DOCUMENT: 1
SOURCE: /path/to/doc.pdf

CONTENT:
<chunk text>
```

---

### 4.2 `search_web` — Web Search Tool

| Property | Detail |
|---|---|
| **What it does** | Live search of the public internet |
| **When used** | Current/time-sensitive info, recent software releases, or when the KB has no answer |
| **Provider** | Tavily Search API |
| **Max results** | 5 results per query |
| **Output** | Raw Tavily result object stringified (URLs + content snippets) |

---

### 4.3 `word_count` — MCP Tool *(mandatory)*

| Property | Detail |
|---|---|
| **What it does** | Counts words, characters, and estimates reading time |
| **When used** | **Always** — agent must never answer word/character-count questions from its own knowledge |
| **Transport** | `stdio` via FastMCP server (`mcp_server.py`) |
| **Input** | `text: str` |
| **Output** | `Words: N / Characters: N / Estimated reading time: N min (at 200 wpm)` |

---

### 4.4 `format_citation` — MCP Tool *(mandatory)*

| Property | Detail |
|---|---|
| **What it does** | Formats citations in APA or MLA style |
| **When used** | **Always** — agent must never generate citation strings itself |
| **Transport** | `stdio` via FastMCP server (`mcp_server.py`) |
| **Inputs** | `author`, `year`, `title`, `source`, `style` (`"apa"` or `"mla"`, default `"apa"`) |
| **Output** | Formatted citation string, e.g.: `Smith, J. (2023). Title. Journal.` |

---

### 4.5 `remember_fact` — Long-term Memory Write

| Property | Detail |
|---|---|
| **What it does** | Saves a fact about the user to the in-memory store |
| **When used** | User states a preference or shares something important about themselves |
| **Storage** | LangGraph `InMemoryStore` keyed by `(user_facts, user_id)` |
| **Input** | `fact: str` |
| **Output** | `"Saved."` |

---

### 4.6 `recall_facts` — Long-term Memory Read

| Property | Detail |
|---|---|
| **What it does** | Retrieves all saved facts about the current user |
| **When used** | Agent wants to personalise its response using stored preferences |
| **Storage** | LangGraph `InMemoryStore` |
| **Input** | *(none — uses `user_id` from runtime context)* |
| **Output** | Newline-separated list of stored facts, or `"No saved facts about this user yet."` |

---

## 5. Input & Output

### Input

The agent accepts a **natural language question or instruction** from the user.

```
Research question: What is retrieval-augmented generation and how does it work?
```

| Field | Type | Description |
|---|---|---|
| `messages` | `list[dict]` | `[{"role": "user", "content": question}]` |
| `thread_id` | `str` | Identifies the conversation session for short-term memory |
| `user_id` | `str` | Identifies the user for long-term memory lookups |

**Before the input reaches the agent**, the input guardrail runs:
- **PromptInjectionGuard** — detects attempts to hijack the agent's instructions
- **TopicalGuard** — rejects off-topic requests (e.g. "write me a poem", "plan my vacation")

If either guard is breached, the question is **blocked** and never reaches the agent.

### Output

The agent returns a structured LangGraph result. The final message content (the answer) is extracted as:

```python
result["messages"][-1].content
```

**After the output is generated**, the output guardrail runs:
- **HallucinationGuard** — compares the answer against the retrieved evidence to detect fabricated facts
- **PrivacyGuard** — detects PII that may have leaked in from retrieved documents or web content

If either guard is breached, the answer is **suppressed** and a violation report is shown instead.

### Answer Format (enforced by system prompt)

```
1. The answer itself — given first, directly.
2. Reasoning / evidence — sources cited and reasoning explained.
3. Source distinction — internal KB results clearly separated from web results.
```

---

## 6. Reasoning & Planning

The agent uses **explicit planning** before every tool call. This is enforced by the system prompt:

> *"Before calling any tool, briefly state in one or two sentences what you intend to do and why."*

Example planning step visible in the response:

> *"I will check the internal knowledge base first because this question concerns the agent's own architecture. If the KB has no answer I will fall back to a web search."*

This means **every agent turn contains visible reasoning** — tool selection rationale is never hidden inside the model's silent chain-of-thought.

### Tool Selection Policy

| Rule | Detail |
|---|---|
| Minimum tools | Use the smallest set needed to answer reliably |
| No auto-double-call | Do not automatically call both `retrieve_documents` and `search_web` |
| MCP tools are mandatory | `word_count` and `format_citation` must always be called for their respective tasks — no exceptions |
| No invention | If retrieval returns nothing, say so — never fabricate sources |
| Source disagreement | If internal KB and web disagree, state the disagreement explicitly |

---

## 7. Memory

The agent has **two separate memory systems**:

### Short-term (Conversation Memory)

| Property | Detail |
|---|---|
| **Implementation** | LangGraph `InMemorySaver` (checkpointer) |
| **Scope** | Within a single session, identified by `thread_id` |
| **What it stores** | Full message history for the current thread |
| **Persistence** | In-process only — lost when the process restarts |
| **Purpose** | Multi-turn conversations — the agent remembers what was said earlier in the same session |

### Long-term (User Fact Memory)

| Property | Detail |
|---|---|
| **Implementation** | LangGraph `InMemoryStore` |
| **Scope** | Across sessions, keyed by `user_id` |
| **What it stores** | Explicit facts saved by the agent via `remember_fact` (e.g. `"prefers concise answers"`, `"researching RAG systems"`) |
| **Persistence** | In-process only — lost when the process restarts |
| **Purpose** | Personalisation — the agent recalls user preferences in future turns |

> **Note:** Both memory systems are currently in-process (`InMemory*`). For production persistence, replace with a database-backed checkpointer and store (e.g. `PostgresSaver`, `RedisStore`).

---

## 8. Guardrails

Guardrails run on **every invocation** — both in the CLI `main()` loop and in `invoke_with_tracing()`.

### Input Guards

| Guard | What it detects | Action on breach |
|---|---|---|
| `PromptInjectionGuard` | Attempts to override the system prompt or hijack agent behaviour | Block + print violation |
| `TopicalGuard` | Questions outside the research agent's allowed topic scope | Block + print violation |

**Allowed topics** (TopicalGuard):
- Research questions and factual inquiries
- Internal knowledge base retrieval
- Web search and current events lookup
- Document summarisation and synthesis
- Comparison of sources or concepts
- Citation and reference formatting (APA / MLA)
- Word count, character count, reading time
- Bibliography and source management
- Questions about the agent itself or its tools
- User preferences and personalisation
- General conversational acknowledgments (yes, no, hi, thank you…)
- Generic clarifying questions (why, how, what, when, where, which)

### Output Guards

| Guard | What it detects | Action on breach |
|---|---|---|
| `HallucinationGuard` | Fabricated facts not grounded in retrieved evidence | Suppress output + print violation |
| `PrivacyGuard` | PII leaking from retrieved documents or web content | Suppress output + print violation |

### Breach Handling

```
======================================================================
BLOCKED: Input violated guardrails.
======================================================================
- [TopicalGuard]: The question is outside the agent's permitted topics.
```

The agent never proceeds if the input is blocked. If the output is blocked, the answer is withheld and the user sees only the violation report.

---

## 9. Turn Flow — Step by Step

```
User types question
        │
        ▼
[1] Input Guardrail
    ├── PromptInjectionGuard evaluates question
    └── TopicalGuard evaluates question
        │
        ├── BREACHED → Print violation, skip to next question
        └── SAFE ↓
        │
        ▼
[2] Agent receives question
    Short-term memory (InMemorySaver) provides prior conversation turns
        │
        ▼
[3] Agent states plan (explicit, visible)
    e.g. "I will search the internal KB first..."
        │
        ▼
[4] Agent calls tools (one or more, minimum necessary)
    ┌────────────────────┬─────────────────────────────────┐
    │ retrieve_documents │ search_web                      │
    │ (internal KB)      │ (public web via Tavily)         │
    ├────────────────────┴─────────────────────────────────┤
    │ word_count         │ format_citation                  │
    │ (MCP — mandatory)  │ (MCP — mandatory)                │
    ├────────────────────┴─────────────────────────────────┤
    │ remember_fact      │ recall_facts                    │
    │ (long-term write)  │ (long-term read)                 │
    └──────────────────────────────────────────────────────┘
        │
        ▼
[5] Agent synthesises answer from retrieved evidence
    Applies evidence rules:
    - No invention
    - Source distinction (internal vs web)
    - Explicit disagreement if sources conflict
        │
        ▼
[6] Output Guardrail
    ├── HallucinationGuard compares answer to evidence
    └── PrivacyGuard scans for PII
        │
        ├── BREACHED → Print violation, withhold answer
        └── SAFE ↓
        │
        ▼
[7] Answer printed to user
    Format: Answer → Reasoning/Evidence → Source distinction
```

---

## 10. Models & Configuration

All model selection is centralised in [`config.py`](../config.py) at the project root.

| Model role | Model | Provider | Settings |
|---|---|---|---|
| **Agent / chat model** | `dots-studio/dots-3-note-preview:free` | OpenRouter | temperature 0.3 |
| **Embedding model** | `baai/bge-m3` | OpenRouter | 1024-dim dense vectors |
| **Judge model** (guardrails) | `dots-studio/dots-3-note-preview:free` | OpenRouter | temperature 0 |

> The Dots-3-Note model is a 16B-active-parameter mixture-of-experts (280B total) suited for reasoning, long-context processing, and multi-step agent workflows. Temperature 0 is used for the judge to ensure deterministic safety verdicts.

### Environment Variables Required

```dotenv
OPENROUTER_API_KEY=sk-or-...
TAVILY_API_KEY=tvly-...
CONFIDENTAI_API_KEY=...
```
