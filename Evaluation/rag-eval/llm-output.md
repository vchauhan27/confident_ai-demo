Evaluating Single-Turn RAG Agent
======================================================================
✨ You're running DeepEval's latest Faithfulness Metric! (using openai/gpt-oss-120b (OpenRouter), strict=False, 
async_mode=False)...
✨ You're running DeepEval's latest Answer Relevancy Metric! (using openai/gpt-oss-120b (OpenRouter), strict=False, 
async_mode=False)...
✨ You're running DeepEval's latest Contextual Relevancy Metric! (using openai/gpt-oss-120b (OpenRouter), strict=False,
async_mode=False)...
✨ You're running DeepEval's latest Contextual Precision Metric! (using openai/gpt-oss-120b (OpenRouter), strict=False,
async_mode=False)...
✨ You're running DeepEval's latest Contextual Recall Metric! (using openai/gpt-oss-120b (OpenRouter), strict=False, 
async_mode=False)...
[PostHog] Multiple active PostHog clients detected for the same project API key and host. Reuse one Posthog instance per app or process when possible to avoid competing background queues and missed shutdown flushes. Multiple clients are supported when intentional.

╭─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ 🚀 DeepEval Evaluation Results                                                                                      │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│                                                                                                                     │
│  ❌ test_case_0                                                                                                     │
│  ├──   Input:              Compare sub cancellation path in Acct Settings and access duration until cycle end.      │
│  │     Actual Output:                                                                                               │
│  │                                                                                                                  │
│  │                         Based on our internal knowledge base, here's the information you requested:              │
│  │                                                                                                                  │
│  │                         ## Subscription Cancellation Path                                                        │
│  │                         You can cancel your subscription by navigating to:                                       │
│  │                         **Account Settings → Billing → Cancel Subscription**                                     │
│  │                                                                                                                  │
│  │                         ## Access Duration Until Cycle End                                                       │
│  │                         When you cancel your subscription, your access will remain active **until the end of     │
│  │                         the current billing cycle**. You will continue to have full access to all features       │
│  │                         and functionality until that date.                                                       │
│  │                                                                                                                  │
│  │                         ## Additional Information                                                                │
│  │                         - **Refunds**: We offer a 14-day money-back guarantee for all new subscriptions.         │
│  │                         After 14 days, we do not provide prorated refunds for canceled subscriptions.            │
│  │                         - **Payment Methods**: We accept all major credit cards (Visa, MasterCard, American      │
│  │                         Express) as well as PayPal and Apple Pay.                                                │
│  │                                                                                                                  │
│  │                         Is there anything else you'd like to know about the cancellation process or your         │
│  │                         subscription?                                                                            │
│  │     Expected Output:    To cancel your subscription, go to Account Settings -> Billing -> Cancel                 │
│  │                         Subscription. Your access will remain active until the end of the current billing        │
│  │                         cycle.                                                                                   │
│  └── Metrics                                                                                                        │
│       Status ┃ Metric               ┃ Score ┃ Threshold ┃ Reason                                                    │
│      ━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│        PASS  │ Faithfulness         │ 1.00  │ 0.70      │ The score is 1.00 because there are no contradi...        │
│        FAIL  │ Answer Relevancy     │ 0.43  │ 0.70      │ The score is 0.43 because the response included several   │
│              │                      │       │           │ unrelated statements—generic prefaces, money‑back         │
│              │                      │       │           │ guarantee details, refund policy, and payment method      │
│              │                      │       │           │ info—none of which address the requested comparison of    │
│              │                      │       │           │ the subscription cancellation path and access duration,   │
│              │                      │       │           │ limiting relevance.                                       │
│        FAIL  │ Contextual Relevancy │ 0.05  │ 0.70      │ The score is 0.05 because the retrieval context mostly    │
│              │                      │       │           │ contains unrelated statements—e.g., about money‑back      │
│              │                      │       │           │ guarantees, payment methods, data deletion, etc.—while    │
│              │                      │       │           │ only one line ('You can cancel your subscription by       │
│              │                      │       │           │ going to Account Settings -> Billing -> Cancel            │
│              │                      │       │           │ Subscription. Your access will remain active until the    │
│              │                      │       │           │ end of the current billing cycle.') actually addresses    │
│              │                      │       │           │ the cancellation path and access duration.                │
│        PASS  │ Contextual Precision │ 1.00  │ 0.70      │ The score is 1.00 because the first node (rank ...        │
│        PASS  │ Contextual Recall    │ 1.00  │ 0.70      │ The score is 1.00 because sentence 1 and senten...        │
│                                                                                                                     │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│                                                                                                                     │
│  ❌ test_case_1                                                                                                     │
│  ├──   Input:              How does Acme Corp secure resting data with 256-bit AES vs. transit data via TLS 1.3?    │
│  │     Actual Output:                                                                                               │
│  │                                                                                                                  │
│  │                         **Plan:**                                                                                │
│  │                                                                                                                  │
│  │                         1. Search the internal knowledge base for terms related to Acme Corp's data              │
│  │                         encryption policies: "256-bit AES", "TLS 1.3", "data at rest", "data in transit", and    │
│  │                         "security practices".                                                                    │
│  │                         2. Review the search results to understand how Acme Corp secures resting data and        │
│  │                         transit data.                                                                            │
│  │                         3. Compare the two methods: 256-bit AES for encryption of stored data, TLS 1.3 for       │
│  │                         encryption during transmission.                                                          │
│  │                         4. Formulate a clear, polite, and accurate response explaining the difference and how    │
│  │                         each is used, based on the retrieved information.                                        │
│  │                                                                                                                  │
│  │                         I'll now execute step 1 by searching the knowledge base.                                 │
│  │     Expected Output:    Acme Corp secures data at rest using industry-standard 256-bit AES encryption and        │
│  │                         data in transit using TLS 1.3.                                                           │
│  └── Metrics                                                                                                        │
│       Status ┃ Metric               ┃ Score ┃ Threshold ┃ Reason                                                    │
│      ━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│        PASS  │ Faithfulness         │ 1.00  │ 0.70      │ The score is 1.00 because there are no contradi...        │
│        PASS  │ Answer Relevancy     │ 1.00  │ 0.70      │ The score is 1.00 because the response directly...        │
│        FAIL  │ Contextual Relevancy │ 0.00  │ 0.70      │ The score is 0.00 because there are no statements in      │
│              │                      │       │           │ the retrieval context—neither irrelevant nor              │
│              │                      │       │           │ relevant—to address the question about Acme Corp's data   │
│              │                      │       │           │ security.                                                 │
│        FAIL  │ Contextual Precision │ 0.00  │ 0.70      │ The score is 0.00 because there are no retrieval nodes    │
│              │                      │       │           │ at all, so no relevant information can be ranked above    │
│              │                      │       │           │ any irrelevant content.                                   │
│        FAIL  │ Contextual Recall    │ 0.00  │ 0.70      │ The score is 0.00 because there are no retrieval          │
│              │                      │       │           │ context nodes to back up any part of the statement.       │
│                                                                                                                     │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ Aggregate Metrics                                                                                                   │
│                                                                                                                     │
│  Metric                          ┃ Average Score         ┃ Pass Rate                                    ┃ Total     │
│ ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━ │
│  Faithfulness                    │ 1.00                  │ 100.00% | passed=2 | failed=0                │ 2         │
│  Answer Relevancy                │ 0.71                  │ 50.00% | passed=1 | failed=1                 │ 2         │
│  Contextual Relevancy            │ 0.02                  │ 0.00% | passed=0 | failed=2                  │ 2         │
│  Contextual Precision            │ 0.50                  │ 50.00% | passed=1 | failed=1                 │ 2         │
│  Contextual Recall               │ 0.50                  │ 50.00% | passed=1 | failed=1                 │ 2         │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯


⚠ WARNING: No hyperparameters logged.
» Log hyperparameters to attribute prompts and models to your test runs.

================================================================================


✓ Evaluation completed 🎉! (time taken: 269.31s | token cost: 0.003892683 USD)
» Test Results (2 total tests):
   » Pass Rate: 0.0% | Passed: 0 | Failed: 2