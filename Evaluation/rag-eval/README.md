# RAG Evaluation Framework

This directory contains the evaluation suite for the Retrieval-Augmented Generation (RAG) pipeline, built using [DeepEval](https://github.com/confident-ai/deepeval). It uses a judge LLM (e.g., Gemini Flash) to grade the information retrieval process and the generation of the final answer.

## Metrics Calculated

- **Answer Relevancy (`AnswerRelevancyMetric`)**: Evaluates whether the agent's final generated answer is directly relevant to the user's question, avoiding tangential or unhelpful information.
- **Faithfulness (Jev-as-a-Judge)**: Measures whether the final answer is faithful to the retrieved context. We replaced the generative `TurnFaithfulnessMetric` with `ConversationalJevEval` so that hallucinations (claims not supported by retrieved documents) are penalized based on deterministic probability outcomes (`Noul`, `Score`, and `Choice` primitives).
- **Contextual Relevancy (`ContextualRelevancyMetric`)**: Assesses if the retrieved documents themselves are actually relevant to the question asked.
- **Contextual Precision (`ContextualPrecisionMetric`)**: Measures the ranking quality of the retrieved contexts-specifically, whether the most highly relevant chunks are ranked at the top.
- **Contextual Recall (`ContextualRecallMetric`)**: Evaluates if the retriever successfully found all the necessary information required to answer the question.

## How It Is Applied

We provide a set of test cases with an `input` (the question) and an `expected_output`. For example: 
*"What is the refund policy for the Enterprise plan, and can you check my ticket status?"* 

The script runs the agent to capture the `actual_output` and the `retrieval_context` (the exact document chunks the agent fetched). DeepEval then compares the actual output and context against the expected output to calculate the metrics.

## Example Output

