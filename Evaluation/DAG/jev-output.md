╭───────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ 🚀 DeepEval Evaluation Results                                                                                │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭───────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│                                                                                                               │
│  ❌ conversational_test_case_0                                                                                │
│  ├── Conversation Turns                                                                                       │
│  │   ├── User: I've been using this service for three weeks and it's completely useless to me. I want my      │
│  │   │   money back immediately, so process the refund now.                                                   │
│  │   ├── Assistant: I understand your frustration. According to our refund policy, we offer a 14-day          │
│  │   │   money-back guarantee for all new subscriptions. Since you've been using the service for three        │
│  │   │   weeks, unfortunately, we do not provide prorated refunds for canceled subscriptions.                 │
│  │   │                                                                                                        │
│  │   │   If you believe there has been a significant issue that justifies a refund outside of our standard    │
│  │   │   policy, I can help you escalate this to a human agent who can review your case more thoroughly.      │
│  │   │   Would you like to proceed with creating a support ticket for this matter?                            │
│  │   │                                                                                                        │
│  │   │   Let me create a ticket for you now.                                                                  │
│  │   │                                                                                                        │
│  │   ├── Assistant: Thank you for your patience. I have created a ticket TKT-2170 for your request and it     │
│  │   │   will be reviewed by a human agent shortly. They will contact you to discuss your concerns and        │
│  │   │   determine the best course of action.                                                                 │
│  │   │                                                                                                        │
│  │   │   If there's anything else you need assistance with in the meantime, please let me know.               │
│  │   │                                                                                                        │
│  │   │   Best regards,                                                                                        │
│  │   │   [Your Name]                                                                                          │
│  │   ├── User: I don't care about your policy, this is ridiculous. Open a support ticket right now so I can   │
│  │   │   talk to a real person who can actually fix this.                                                     │
│  │   ├── Assistant: I understand your frustration and I apologize for any inconvenience you're experiencing.  │
│  │   │   Let's get this resolved as quickly as possible.                                                      │
│  │   │                                                                                                        │
│  │   │   I will create a support ticket with a higher priority to ensure a human agent can assist you         │
│  │   │   promptly. This should allow you to speak directly with someone who can address your concerns.        │
│  │   │                                                                                                        │
│  │   │   Let me create the ticket now.                                                                        │
│  │   │                                                                                                        │
│  │   │                                                                                                        │
│  │   └── Assistant: I have created a ticket TKT-8531 with a high priority to ensure a human agent reviews     │
│  │       your issue as soon as possible. They will be in touch with you shortly to address your concerns and  │
│  │       help resolve the problem.                                                                            │
│  │                                                                                                            │
│  │       If there's anything else you need assistance with, please let me know.                               │
│  │                                                                                                            │
│  │       Best regards,                                                                                        │
│  │       [Your Name]                                                                                          │
│  └── Metrics                                                                                                  │
│       Status ┃ Metric                              ┃ Score ┃ Threshold ┃ Reason                               │
│      ━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│        FAIL  │ Memory Recall Gate (Jev)            │ 0.00  │ 1.00      │ Decided by typesafe/jev-1.13         │
│              │ [Conversational JevEval]            │       │           │ (TypeSafe AI), minimum confidence    │
│              │                                     │       │           │ 0.92.                                │
│              │                                     │       │           │ 1. The assistant correctly           │
│              │                                     │       │           │ recalled and used the fact the       │
│              │                                     │       │           │ user shared in an earlier turn       │
│              │                                     │       │           │ (their name or research goal) when   │
│              │                                     │       │           │ answering a later, related           │
│              │                                     │       │           │ question. -> clearly fails           │
│              │                                     │       │           │ (P(yes)=0.04, confidence=0.92)       │
│              │                                     │       │           │ strict=fail                          │
│              │                                     │       │           │ Score: 0.00 (strict mode: at least   │
│              │                                     │       │           │ one applicable question failed).     │
│                                                                                                               │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭───────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ Aggregate Metrics                                                                                             │
│                                                                                                               │
│  Metric                                              ┃ Average Score  ┃ Pass Rate                    ┃ Total  │
│ ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━ │
│  Memory Recall Gate (Jev) [Conversational JevEval]   │ 0.00           │ 0.00% | passed=0 | failed=1  │ 1      │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────╯


⚠ WARNING: No hyperparameters logged.
» Log hyperparameters to attribute prompts and models to your test runs.

================================================================================


✓ Evaluation completed 🎉! (time taken: 0.48s | token cost: None)
» Test Results (1 total tests):
   » Pass Rate: 0.0% | Passed: 0 | Failed: 1

 ================================================================================