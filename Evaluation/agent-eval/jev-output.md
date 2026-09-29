Evaluating Jev Tool Faithfulness...
✨ You're running DeepEval's latest Tool Faithfulness [JevEval] Metric! (using typesafe/jev-1.13 (TypeSafe AI), 
strict=False, async_mode=True)...
[PostHog] Multiple active PostHog clients detected for the same project API key and host. Reuse one Posthog instance per app or process when possible to avoid competing background queues and missed shutdown flushes. Multiple clients are supported when intentional.

╭─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ 🚀 DeepEval Evaluation Results                                                                                      │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│                                                                                                                     │
│  ❌ test_case_0                                                                                                     │
│  ├──   Input:            A frustrated customer contacts the Acme Corp support agent regarding a subscription        │
│  │                       refund after three weeks, learns that prorated refunds are unavailable, and                │
│  │                       subsequently requests to open a ticket to speak with a human agent.                        │
│  │     Actual Output:                                                                                               │
│  │                                                                                                                  │
│  │                       I've created a support ticket for you with the ID **TKT-5386** and assigned it a high      │
│  │                       priority. A human agent will review your case shortly and will contact you to discuss      │
│  │                       your subscription refund request.                                                          │
│  │                                                                                                                  │
│  │                       Is there anything else I can help you with while you wait for their response?              │
│  └── Metrics                                                                                                        │
│       Status ┃ Metric                      ┃ Score ┃ Threshold ┃ Reason                                             │
│      ━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│        FAIL  │ Tool Faithfulness [JevEval] │ 0.39  │ 0.50      │ Decided by typesafe/jev-1.13 (TypeSafe AI),        │
│              │                             │       │           │ minimum confidence 0.53.                           │
│              │                             │       │           │ 1. Every fact and figure in actual_output          │
│              │                             │       │           │ appears in the output of a tool in tools_called.   │
│              │                             │       │           │ -> clearly fails (P(yes)=0.12, confidence=0.76,    │
│              │                             │       │           │ weight=2)                                          │
│              │                             │       │           │ 2. actual_output reports every value returned in   │
│              │                             │       │           │ tools_called accurately. -> likely holds           │
│              │                             │       │           │ (P(yes)=0.80, confidence=0.60)                     │
│              │                             │       │           │ 3. How much of actual_output is grounded in        │
│              │                             │       │           │ tools_called? -> "Mostly grounded" (expected       │
│              │                             │       │           │ level=0.78 of 1.00, confidence=0.61)               │
│              │                             │       │           │ 4. What did actual_output do with information      │
│              │                             │       │           │ the tools did not return? -> "stated_it_as_fact"   │
│              │                             │       │           │ (P=0.63, confidence=0.53)                          │
│              │                             │       │           │ Score: 0.39 (weighted mean of 4 applicable         │
│              │                             │       │           │ questions).                                        │
│                                                                                                                     │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ ✅ test_case_1 (Passed 1 metrics)                                                                                   │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ Aggregate Metrics                                                                                                   │
│                                                                                                                     │
│  Metric                                  ┃ Average Score       ┃ Pass Rate                               ┃ Total    │
│ ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━ │
│  Tool Faithfulness [JevEval]             │ 0.64                │ 50.00% | passed=1 | failed=1            │ 2        │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯


⚠ WARNING: No hyperparameters logged.
» Log hyperparameters to attribute prompts and models to your test runs.

================================================================================


✓ Evaluation completed 🎉! (time taken: 0.51s | token cost: None)
» Test Results (2 total tests):
   » Pass Rate: 50.0% | Passed: 1 | Failed: 1

 ================================================================================

» Want to share evals with your team, or a place for your test cases to live? ❤️ 🏡
  » Run 'deepeval view' to analyze and save testing results on Confident AI.