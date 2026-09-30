╭───────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ 🚀 DeepEval Evaluation Results                                                                                │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭───────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│                                                                                                               │
│  ❌ conversational_test_case_0                                                                                │
│  ├── Conversation Turns                                                                                       │
│  │   ├── User: I've been using this service for three weeks and it's completely useless to me. I want my      │
│  │   │   money back immediately, so process the refund now.                                                   │
│  │   ├── Assistant: I understand your frustration, and I apologize for any inconvenience you've experienced.  │
│  │   │   According to our refund policy, we offer a 14-day money-back guarantee for all new subscriptions.    │
│  │   │   Since you've been using the service for three weeks, unfortunately, we do not provide prorated       │
│  │   │   refunds for canceled subscriptions.                                                                  │
│  │   │                                                                                                        │
│  │   │   If you would like to proceed with canceling your subscription and requesting a refund, please        │
│  │   │   navigate to Account Settings -> Billing -> Cancel Subscription. Your access will remain active       │
│  │   │   until the end of the current billing cycle.                                                          │
│  │   │                                                                                                        │
│  │   │   Would you like me to guide you through the process or create a support ticket for you so that one    │
│  │   │   of our human agents can assist further?                                                              │
│  │   │                                                                                                        │
│  │   │   Let me know how you'd like to proceed.                                                               │
│  │   ├── User: I don't care about your policy, this is ridiculous. Open a support ticket right now so I can   │
│  │   │   talk to a real person who can actually fix this.                                                     │
│  │   └── Assistant: I've opened a support ticket for you, TKT-2357, with priority Medium. A human agent will  │
│  │       review your issue shortly and get back to you as soon as possible.                                   │
│  │                                                                                                            │
│  │       Thank you for bringing this to our attention. We apologize for any inconvenience and appreciate      │
│  │       your patience while we work on resolving your concern.                                               │
│  │                                                                                                            │
│  │       If you need any further assistance or have additional questions, feel free to ask.                   │
│  └── Metrics                                                                                                  │
│       Status ┃ Metric                    ┃ Score ┃ Threshold ┃ Reason                                         │
│      ━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│        PASS  │ Turn Relevancy            │ 1.00  │ 0.50      │ The score is 1.0 because there are no listed   │
│              │                           │       │           │ ir...                                          │
│        PASS  │ Role Adherence            │ 1.00  │ 0.50      │ The score is 1.0 because there were no         │
│              │                           │       │           │ out‑of‑c...                                    │
│        PASS  │ Knowledge Retention       │ 1.00  │ 0.50      │ The score is 1.00 because there are no         │
│              │                           │       │           │ attritio...                                    │
│        PASS  │ Conversation Completeness │ 0.50  │ 0.50      │ The score is 0.5 because the LLM response      │
│              │                           │       │           │ satis...                                       │
│        PASS  │ Goal Accuracy             │ 0.81  │ 0.50      │ The agent achieved a final combined score of   │
│              │                           │       │           │ 0....                                          │
│        PASS  │ Tool Use                  │ 0.62  │ 0.50      │ The agent passed because it consistently       │
│              │                           │       │           │ chose ...                                      │
│        FAIL  │ Topic Adherence           │ 0.00  │ 0.50      │ There were no question-answer pairs to         │
│              │                           │       │           │ evaluate. Please enable verbose logs to look   │
│              │                           │       │           │ at the evaluation steps taken                  │
│        PASS  │ Turn Faithfulness         │ 1.00  │ 0.50      │ The metric passed with a perfect score         │
│              │                           │       │           │ because ...                                    │
│        FAIL  │ Turn Contextual Precision │ 0.25  │ 0.50      │ The metric failed with a low score of 0.25     │
│              │                           │       │           │ because relevant nodes were consistently       │
│              │                           │       │           │ ranked below irrelevant ones, as the reasons   │
│              │                           │       │           │ show multiple interactions where the           │
│              │                           │       │           │ top‑ranked documents did not address the       │
│              │                           │       │           │ user’s query while the pertinent documents     │
│              │                           │       │           │ appeared later in the list, leading to poor    │
│              │                           │       │           │ contextual precision.                          │
│        FAIL  │ Turn Contextual Recall    │ 0.00  │ 0.50      │ The metric failed with a score of 0.0          │
│              │                           │       │           │ because none of the assistant's sentences      │
│              │                           │       │           │ could be linked to the provided retrieval      │
│              │                           │       │           │ context; the output discussed BGE‑M3           │
│              │                           │       │           │ embeddings, OpenRouter, and specific           │
│              │                           │       │           │ text‑splitter settings, which were absent      │
│              │                           │       │           │ from the context that only contained Acme      │
│              │                           │       │           │ Corp support FAQs, resulting in a complete     │
│              │                           │       │           │ lack of contextual recall.                     │
│        FAIL  │ Turn Contextual Relevancy │ 0.10  │ 0.50      │ The metric failed because the retrieved        │
│              │                           │       │           │ context was overwhelmingly irrelevant to the   │
│              │                           │       │           │ user's request for an immediate refund,        │
│              │                           │       │           │ containing mostly unrelated information        │
│              │                           │       │           │ about subscription cancellation, payment       │
│              │                           │       │           │ methods, and troubleshooting, with only a      │
│              │                           │       │           │ brief mention of a 14‑day money‑back           │
│              │                           │       │           │ guarantee that does not address the user's     │
│              │                           │       │           │ situation, resulting in a very low overall     │
│              │                           │       │           │ relevance score.                               │
│                                                                                                               │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭───────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ Aggregate Metrics                                                                                             │
│                                                                                                               │
│  Metric                             ┃ Average Score      ┃ Pass Rate                               ┃ Total    │
│ ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━ │
│  Turn Relevancy                     │ 1.00               │ 100.00% | passed=1 | failed=0           │ 1        │
│  Role Adherence                     │ 1.00               │ 100.00% | passed=1 | failed=0           │ 1        │
│  Knowledge Retention                │ 1.00               │ 100.00% | passed=1 | failed=0           │ 1        │
│  Conversation Completeness          │ 0.50               │ 100.00% | passed=1 | failed=0           │ 1        │
│  Goal Accuracy                      │ 0.81               │ 100.00% | passed=1 | failed=0           │ 1        │
│  Tool Use                           │ 0.62               │ 100.00% | passed=1 | failed=0           │ 1        │
│  Topic Adherence                    │ 0.00               │ 0.00% | passed=0 | failed=1             │ 1        │
│  Turn Faithfulness                  │ 1.00               │ 100.00% | passed=1 | failed=0           │ 1        │
│  Turn Contextual Precision          │ 0.25               │ 0.00% | passed=0 | failed=1             │ 1        │
│  Turn Contextual Recall             │ 0.00               │ 0.00% | passed=0 | failed=1             │ 1        │
│  Turn Contextual Relevancy          │ 0.10               │ 0.00% | passed=0 | failed=1             │ 1        │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────╯


⚠ WARNING: No hyperparameters logged.
» Log hyperparameters to attribute prompts and models to your test runs.

================================================================================


✓ Evaluation completed 🎉! (time taken: 450.78s | token cost: 0.007488171000000001 USD)
» Test Results (1 total tests):
   » Pass Rate: 0.0% | Passed: 0 | Failed: 1