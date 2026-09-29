Running multi-turn Jev metrics...
✨ You're running DeepEval's latest Tool Use (Jev) [Conversational JevEval] Metric! (using typesafe/jev-1.13 
(TypeSafe AI), strict=False, async_mode=False)...
✨ You're running DeepEval's latest Turn Faithfulness (Jev) [Conversational JevEval] Metric! (using
typesafe/jev-1.13 (TypeSafe AI), strict=False, async_mode=False)...
[PostHog] Multiple active PostHog clients detected for the same project API key and host. Reuse one Posthog instance per app or process when possible to avoid competing background queues and missed shutdown flushes. Multiple clients are supported when intentional.

╭───────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ 🚀 DeepEval Evaluation Results                                                                                │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭───────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│                                                                                                               │
│  ❌ conversational_test_case_0                                                                                │
│  ├── Conversation Turns                                                                                       │
│  │   ├── User: I've been using this service for three weeks and it's completely useless to me. I want my      │
│  │   │   money back immediately, so process the refund now.                                                   │
│  │   ├── Assistant: Thank you for reaching out to us. According to our refund policy, we offer a 14-day       │
│  │   │   money-back guarantee for all new subscriptions. Since you've been using the service for three        │
│  │   │   weeks, we unfortunately do not provide prorated refunds for canceled subscriptions.                  │
│  │   │                                                                                                        │
│  │   │   If you believe there has been a significant issue with the service that justifies a refund, I would  │
│  │   │   be happy to escalate this to our support team for further review. Would you like to create a         │
│  │   │   support ticket so we can look into this more closely?                                                │
│  │   │                                                                                                        │
│  │   │   Let me know how you'd like to proceed.                                                               │
│  │   ├── User: I don't care about your policy, this is ridiculous. Open a support ticket right now so I can   │
│  │   │   talk to a real person who can actually fix this.                                                     │
│  │   └── Assistant: I've created a support ticket for you, TKT-4075, with a Medium priority. A human agent    │
│  │       will review your issue shortly and get back to you as soon as possible.                              │
│  │                                                                                                            │
│  │       Thank you for bringing this to our attention. We value your feedback and will do our best to assist  │
│  │       you.                                                                                                 │
│  └── Metrics                                                                                                  │
│       Status ┃ Metric                             ┃ Score ┃ Threshold ┃ Reason                                │
│      ━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│        PASS  │ Tool Use (Jev) [Conversational     │ 0.95  │ 0.50      │ Decided by typesafe/jev-1.13          │
│              │ JevEval]                           │       │           │ (TypeSafe AI), min...                 │
│        FAIL  │ Turn Faithfulness (Jev)            │ 0.36  │ 0.50      │ Decided by typesafe/jev-1.13          │
│              │ [Conversational JevEval]           │       │           │ (TypeSafe AI), minimum confidence     │
│              │                                    │       │           │ 0.54.                                 │
│              │                                    │       │           │ 1. Every fact stated by the           │
│              │                                    │       │           │ assistant appears in the              │
│              │                                    │       │           │ retrieval_context. -> likely fails    │
│              │                                    │       │           │ (P(yes)=0.23, confidence=0.54,        │
│              │                                    │       │           │ weight=2)                             │
│              │                                    │       │           │ 2. How much of the assistant's        │
│              │                                    │       │           │ claims are grounded in the            │
│              │                                    │       │           │ retrieval_context? -> "Mostly         │
│              │                                    │       │           │ grounded" (expected level=0.63 of     │
│              │                                    │       │           │ 1.00, confidence=0.65)                │
│              │                                    │       │           │ 3. What did the assistant do when     │
│              │                                    │       │           │ asked for information not present     │
│              │                                    │       │           │ in the retrieval_context? -> not      │
│              │                                    │       │           │ applicable (not applicable,           │
│              │                                    │       │           │ confidence=0.86)                      │
│              │                                    │       │           │ Score: 0.36 (weighted mean of 2       │
│              │                                    │       │           │ applicable questions).                │
│                                                                                                               │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭───────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ Aggregate Metrics                                                                                             │
│                                                                                                               │
│  Metric                                             ┃ Average Score  ┃ Pass Rate                     ┃ Total  │
│ ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━ │
│  Tool Use (Jev) [Conversational JevEval]            │ 0.95           │ 100.00% | passed=1 | failed=0 │ 1      │
│  Turn Faithfulness (Jev) [Conversational JevEval]   │ 0.36           │ 0.00% | passed=0 | failed=1   │ 1      │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────╯


⚠ WARNING: No hyperparameters logged.
» Log hyperparameters to attribute prompts and models to your test runs.

================================================================================


✓ Evaluation completed 🎉! (time taken: 0.89s | token cost: None)
» Test Results (1 total tests):
   » Pass Rate: 0.0% | Passed: 0 | Failed: 1

 ================================================================================