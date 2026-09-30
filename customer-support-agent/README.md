# Customer Support Agent

                                           USER
                                            │
                                            ▼
                                   ┌─────────────────┐
                                   │  Support Agent  │
                                   │   LangChain     │
                                   └────────┬────────┘
                                            │
                                  decides which tool
                                            │
                  ┌──────────────────┬──────┴───────┬──────────────────┐
                  │                  │              │                  │
                  ▼                  ▼              ▼                  ▼
          ┌───────────────┐  ┌──────────────┐ ┌──────────────┐  ┌──────────────┐
          │ RAG Tool      │  │ Web Tool     │ │ Memory Tool  │  │ MCP Tools    │
          │               │  │              │ │              │  │              │
          │ BGE-M3        │  │ Tavily       │ │ LangGraph    │  │ FastMCP      │
          │      ↓        │  │      ↓       │ │    Store     │  │   Server     │
          │    Chroma     │  │    Web       │ │              │  │              │
          └───────┬───────┘  └──────┬───────┘ └──────┬───────┘  └──────┬───────┘
                  │                 │                │                 │
                  └─────────────────┴────────┬───────┴─────────────────┘
                                             ▼
                                    ┌─────────────────┐
                                    │    OpenRouter   │
                                    │   Chat Model    │
                                    └────────┬────────┘
                                             │
                                             ▼
                                           ANSWER

This directory contains an intelligent Agentic RAG implementation built using LangChain and LangGraph. It is a **Customer Support Agent** that answers user queries based on internal FAQs, checks external web services, manages support tickets, and maintains long-term memory about users.

## Architecture & Tools

The agent is driven by a chat model via OpenRouter and acts as a central decision-maker. It is equipped with several tools:

- **RAG Tool (`search_knowledge_base`)**: Queries an internal customer support FAQ stored in a Chroma vector database using BGE-M3 embeddings.
- **Web Tool (`search_web`)**: Queries the public internet using Tavily Search when the question requires external information (e.g., status pages, third-party subprocessor info).
- **Memory Tools (`remember_fact` & `recall_facts`)**: Utilizes LangGraph's `InMemoryStore` to store and retrieve long-term facts about the user across conversations (e.g., plan tier, name).

## MCP Server Integration

The agent integrates with a FastMCP server (`mcp_server.py`) which exposes external support utility tools over the `stdio` transport. 
Current mock tools provided by the MCP server include:
- `check_ticket_status`: Checks the status of an existing support ticket.
- `create_ticket`: Creates a new support ticket and assigns priority.

## Guardrails

The agent implements a dual-layer guardrail system in `guardrail.py` to ensure safe, on-topic interactions:
1. **Deterministic Guardrails (O(1))**: A fast, regex-based pre-guard that intercepts prompt injections (e.g., "ignore previous instructions") and PII leakage (e.g., "credit card") in milliseconds.
2. **LLM-as-a-Judge Guardrails**: If the fast check passes, a DeepEval `TopicalGuard` ensures the user is strictly asking about approved customer support topics (billing, bugs, data privacy, etc.) and blocks off-topic requests.

## Planning & Execution

The agent operates with a strict planning phase before taking any action. Based on its system prompt (`prompt1.txt`), it must explicitly state a complete, numbered, multi-step plan detailing which tools it will use and how it will analyze the retrieved information to resolve the request. The agent is instructed to strictly adhere to this plan and execute only the planned steps without deviating.

## Usage

First, ingest the knowledge base:
```bash
python ingest.py
```

Then, run the agent interactively via the CLI:
```bash
python agent.py
```

### The "All-In-One" Mega Query

To test all the capabilities of the agent at once (Memory, RAG, Web Search, and MCP tool usage), paste the following query into the CLI:

> *"Hi! First, please remember that I am an Enterprise plan user and my name is Alex. Next, can you check the status of my existing ticket TKT-9921? After that, please check your internal documents to tell me if my data is SOC 2 Type II compliant and if you share it with any third parties. Also, search the web to find out what year Stripe was founded, since I know they are one of your subprocessors. Finally, go ahead and create a new High priority ticket for me so I can speak to a human about upgrading my API limits."*

## Configuration

Make sure your `.env` file is properly configured with the necessary API keys:
- `OPENROUTER_API_KEY`
- `TAVILY_API_KEY`
- `CONFIDENTAI_API_KEY` (for DeepEval)

Model selection for the agent, embeddings, and judge is managed centrally in the `config.py` file located at the project root.