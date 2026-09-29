Q: Compare sub cancellation path in Acct Settings and access duration until cycle end.
A: Based on the information from our internal knowledge base, here is what I can tell you:

1. **Canceling Your Subscription:**
   - You can cancel your subscription by navigating to Account Settings -> ...

Q: How does Acme Corp secure resting data with 256-bit AES vs. transit data via TLS 1.3?
A: Based on the information gathered from various sources, Acme Corp uses AES-256 encryption for data at rest and TLS 1.3 for data in transit.

### Data at Rest (AES-256)
- Acme Corp encrypts all custome...

✨ You're running DeepEval's latest Format Adherence [GEval] Metric! (using gemini-3.1-flash-lite (Gemini), 
strict=False, async_mode=False)...
Direct use of automatic function calling (AFC) in Models.generate_content is not recommended. Instead, we        
recommend to use AFC in Chat.send_message. Similarly, direct use of AFC in Models.generate_content_stream is not 
recommended. Instead, we recommend to use AFC in Chat.send_message_stream.
[PostHog] Multiple active PostHog clients detected for the same project API key and host. Reuse one Posthog instance per app or process when possible to avoid competing background queues and missed shutdown flushes. Multiple clients are supported when intentional.

╭───────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ 🚀 DeepEval Evaluation Results                                                                                │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭───────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│                                                                                                               │
│  ❌ test_case_0                                                                                               │
│  ├──   Input:            Compare sub cancellation path in Acct Settings and access duration until cycle       │
│  │                       end.                                                                                 │
│  │     Actual Output:    Based on the information from our internal knowledge base, here is what I can        │
│  │                       tell you:                                                                            │
│  │                                                                                                            │
│  │                       1. **Canceling Your Subscription:**                                                  │
│  │                          - You can cancel your subscription by navigating to Account Settings ->           │
│  │                       Billing -> Cancel Subscription.                                                      │
│  │                          - Your access will remain active until the end of the current billing cycle.      │
│  │                                                                                                            │
│  │                       2. **Access Duration Until Cycle End:**                                              │
│  │                          - Once you cancel your subscription, your access will continue until the end      │
│  │                       of the current billing cycle. This means you will have full access to all            │
│  │                       features and services until the next scheduled billing date.                         │
│  │                                                                                                            │
│  │                       If you need further assistance or if there's anything specific you're looking for    │
│  │                       regarding these processes, please let me know!                                       │
│  └── Metrics                                                                                                  │
│       Status ┃ Metric                   ┃ Score ┃ Threshold ┃ Reason                                          │
│      ━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│        FAIL  │ Format Adherence [GEval] │ 0.30  │ 0.70      │ The response fails to provide a direct answer   │
│              │                          │       │           │ first, instead starting with an introductory    │
│              │                          │       │           │ sentence. It also fails to distinguish          │
│              │                          │       │           │ between internal knowledge and web search       │
│              │                          │       │           │ information as required by the evaluation       │
│              │                          │       │           │ steps.                                          │
│                                                                                                               │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭───────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ ✅ test_case_1 (Passed 1 metrics)                                                                             │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭───────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ Aggregate Metrics                                                                                             │
│                                                                                                               │
│  Metric                             ┃ Average Score       ┃ Pass Rate                              ┃ Total    │
│ ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━ │
│  Format Adherence [GEval]           │ 0.55                │ 50.00% | passed=1 | failed=1           │ 2        │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────╯


⚠ WARNING: No hyperparameters logged.
» Log hyperparameters to attribute prompts and models to your test runs.

================================================================================


✓ Evaluation completed 🎉! (time taken: 9.8s | token cost: 0.00041875 USD)
» Test Results (2 total tests):
   » Pass Rate: 50.0% | Passed: 1 | Failed: 1

 ================================================================================