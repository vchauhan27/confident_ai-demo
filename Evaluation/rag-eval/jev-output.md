======================================================================
Evaluating Single-Turn RAG Agent with JevEval
======================================================================
✨ You're running DeepEval's latest RAG Faithfulness [JevEval] Metric! (using typesafe/jev-1.13 (TypeSafe AI), 
strict=False, async_mode=False)...
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
│  │                         Based on the information from our knowledge base, here's a comparison of the             │
│  │                         subscription cancellation path and access duration:                                      │
│  │                                                                                                                  │
│  │                         ## Cancellation Path                                                                     │
│  │                         - **Location**: Account Settings → Billing → Cancel Subscription                         │
│  │                         - **Process**: Navigate through these specific menu items to access the cancellation     │
│  │                         option                                                                                   │
│  │                         - **Accessibility**: This is the standard, self-service path available to all users      │
│  │                                                                                                                  │
│  │                         ## Access Duration Until Cycle End                                                       │
│  │                         - **Duration**: Your access remains active until the end of the current billing cycle    │
│  │                         - **Implication**: You continue to have full access to all features and services         │
│  │                         throughout the remainder of your paid period                                             │
│  │                         - **No Immediate Loss**: Cancellation doesn't result in immediate loss of access         │
│  │                                                                                                                  │
│  │                         ## Key Comparison Points                                                                 │
│  │                         1. **Timing**: The cancellation path is immediate (you can cancel anytime), but the      │
│  │                         access duration extends to your cycle end date                                           │
│  │                         2. **Function**: The cancellation path stops future billing, while the access            │
│  │                         duration defines how long you keep using the service                                     │
│  │                         3. **User Experience**: You can cancel now and continue using the service without        │
│  │                         interruption until your billing period naturally concludes                               │
│  │                                                                                                                  │
│  │                         This means you can cancel your subscription at any point through the Account Settings    │
│  │                         path, and you'll maintain full access to all features until your current billing         │
│  │                         cycle ends, after which your account will be downgraded to the free tier (if             │
│  │                         available) or closed.                                                                    │
│  │     Expected Output:    To cancel your subscription, go to Account Settings -> Billing -> Cancel                 │
│  │                         Subscription. Your access will remain active until the end of the current billing        │
│  │                         cycle.                                                                                   │
│  └── Metrics                                                                                                        │
│       Status ┃ Metric                     ┃ Score ┃ Threshold ┃ Reason                                              │
│      ━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│        FAIL  │ RAG Faithfulness [JevEval] │ 0.24  │ 0.50      │ Decided by typesafe/jev-1.13 (TypeSafe AI),         │
│              │                            │       │           │ minimum confidence 0.68.                            │
│              │                            │       │           │ 1. Every fact and figure in actual_output appears   │
│              │                            │       │           │ in the retrieval_context. -> likely fails           │
│              │                            │       │           │ (P(yes)=0.16, confidence=0.68, weight=2)            │
│              │                            │       │           │ 2. How much of actual_output is grounded in the     │
│              │                            │       │           │ retrieval_context? -> "Mostly grounded" (expected   │
│              │                            │       │           │ level=0.63 of 1.00, confidence=0.86)                │
│              │                            │       │           │ 3. What did actual_output do with information the   │
│              │                            │       │           │ user asked for that was not present in the          │
│              │                            │       │           │ retrieval_context? -> "stated_it_as_fact"           │
│              │                            │       │           │ (P=0.91, confidence=0.87)                           │
│              │                            │       │           │ Score: 0.24 (weighted mean of 3 applicable          │
│              │                            │       │           │ questions).                                         │
│                                                                                                                     │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│                                                                                                                     │
│  ❌ test_case_1                                                                                                     │
│  ├──   Input:              How does Acme Corp secure resting data with 256-bit AES vs. transit data via TLS 1.3?    │
│  │     Actual Output:                                                                                               │
│  │                                                                                                                  │
│  │                         Based on my research, I can provide you with a comprehensive explanation of how Acme     │
│  │                         Corp secures both resting and transit data using industry-standard encryption            │
│  │                         methods.                                                                                 │
│  │                                                                                                                  │
│  │                         ## Data at Rest: 256-Bit AES Encryption                                                  │
│  │                                                                                                                  │
│  │                         Acme Corp uses **Advanced Encryption Standard (AES) with 256-bit keys** to protect       │
│  │                         data when it's stored on our servers. Here's how this works:                             │
│  │                                                                                                                  │
│  │                         ### Technical Implementation:                                                            │
│  │                         - **Symmetric Block Cipher**: AES-256 is a symmetric encryption algorithm, meaning       │
│  │                         the same key is used for both encryption and decryption                                  │
│  │                         - **14 Rounds of Encryption**: The algorithm processes data in 14 rounds of              │
│  │                         substitution, permutation, and mixing operations                                         │
│  │                         - **Key Expansion**: The initial 256-bit key is expanded into multiple round keys        │
│  │                         through a key schedule process                                                           │
│  │                         - **Block Processing**: Data is divided into 128-bit blocks, each processed              │
│  │                         independently                                                                            │
│  │                                                                                                                  │
│  │                         ### Security Benefits:                                                                   │
│  │                         - **Massive Key Space**: With 2^256 possible keys, brute-force attacks are               │
│  │                         computationally infeasible                                                               │
│  │                         - **Industry Standard**: AES-256 is approved by the U.S. government for classified       │
│  │                         data                                                                                     │
│  │                         - **Hardware Encryption**: Many implementations use dedicated AES engines in storage     │
│  │                         controllers, protecting data even if physical media is stolen                            │
│  │                         - **Compliance**: Supports SOC 2 Type II and GDPR requirements for data protection       │
│  │                                                                                                                  │
│  │                         ## Data in Transit: TLS 1.3                                                              │
│  │                                                                                                                  │
│  │                         For data moving between your devices and our servers, Acme Corp implements               │
│  │                         **Transport Layer Security (TLS) version 1.3**, the latest and most secure version of    │
│  │                         the TLS protocol.                                                                        │
│  │                                                                                                                  │
│  │                         ### Technical Implementation:                                                            │
│  │                         - **1-RTT Handshake**: TLS 1.3 completes the initial connection setup in just one        │
│  │                         round trip (vs. 2-RTT in TLS 1.2), reducing latency by 50-100ms                          │
│  │                         - **Perfect Forward Secrecy**: Each session uses unique encryption keys, ensuring        │
│  │                         that even if a key is compromised later, past sessions remain secure                     │
│  │                         - **Encrypted Handshake**: Most of the handshake process itself is encrypted,            │
│  │                         protecting sensitive information like server certificates                                │
│  │                         - **Modern Cipher Suites**: Only supports strong cipher suites like AES-GCM and          │
│  │                         ChaCha20-Poly1305                                                                        │
│  │                                                                                                                  │
│  │                         ### Security Benefits:                                                                   │
│  │                         - **End-to-End Encryption**: All data transmitted over the network is encrypted and      │
│  │                         authenticated                                                                            │
│  │                         - **Protection Against Attacks**: Prevents eavesdropping, tampering, and                 │
│  │                         man-in-the-middle attacks                                                                │
│  │                         - **Future-Proof**: Designed with cryptographic agility to adapt to emerging threats     │
│  │                         - **Performance**: Faster connection establishment while maintaining highest security    │
│  │                         standards                                                                                │
│  │                                                                                                                  │
│  │                         ## How They Work Together                                                                │
│  │                                                                                                                  │
│  │                         Acme Corp employs a **defense-in-depth strategy** where both encryption methods          │
│  │                         complement each other:                                                                   │
│  │                                                                                                                  │
│  │                         1. **Layered Protection**: Data is protected both while being transmitted (TLS 1.3)      │
│  │                         and while stored (AES-256)                                                               │
│  │                         2. **Compliance Alignment**: Together, these technologies help meet SOC 2 Type II and    │
│  │                         GDPR requirements                                                                        │
│  │                         3. **Comprehensive Coverage**: Ensures security across all data states - at rest, in     │
│  │                         transit, and during processing                                                           │
│  │                                                                                                                  │
│  │                         This dual-layer approach means that even if one protection layer were compromised,       │
│  │                         the other would still safeguard your data. For example, if someone intercepted           │
│  │                         network traffic, they would only see encrypted data. If they somehow gained physical     │
│  │                         access to our servers, the stored data would still be encrypted with AES-256.            │
│  │                                                                                                                  │
│  │                         Both technologies represent the current industry standard for enterprise-grade data      │
│  │                         protection and are continuously monitored and updated to maintain the highest            │
│  │                         security posture.                                                                        │
│  │     Expected Output:    Acme Corp secures data at rest using industry-standard 256-bit AES encryption and        │
│  │                         data in transit using TLS 1.3.                                                           │
│  └── Metrics                                                                                                        │
│       Status ┃ Metric                     ┃ Score ┃ Threshold ┃ Reason                                              │
│      ━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│        FAIL  │ RAG Faithfulness [JevEval] │ 0.10  │ 0.50      │ Decided by typesafe/jev-1.13 (TypeSafe AI),         │
│              │                            │       │           │ minimum confidence 0.86.                            │
│              │                            │       │           │ 1. Every fact and figure in actual_output appears   │
│              │                            │       │           │ in the retrieval_context. -> clearly fails          │
│              │                            │       │           │ (P(yes)=0.03, confidence=0.94, weight=2)            │
│              │                            │       │           │ 2. How much of actual_output is grounded in the     │
│              │                            │       │           │ retrieval_context? -> "Mostly fabricated"           │
│              │                            │       │           │ (expected level=0.34 of 1.00, confidence=0.89)      │
│              │                            │       │           │ 3. What did actual_output do with information the   │
│              │                            │       │           │ user asked for that was not present in the          │
│              │                            │       │           │ retrieval_context? -> "stated_it_as_fact"           │
│              │                            │       │           │ (P=0.90, confidence=0.86)                           │
│              │                            │       │           │ Score: 0.10 (weighted mean of 3 applicable          │
│              │                            │       │           │ questions).                                         │
│                                                                                                                     │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ Aggregate Metrics                                                                                                   │
│                                                                                                                     │
│  Metric                                 ┃ Average Score        ┃ Pass Rate                               ┃ Total    │
│ ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━ │
│  RAG Faithfulness [JevEval]             │ 0.17                 │ 0.00% | passed=0 | failed=2             │ 2        │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯


⚠ WARNING: No hyperparameters logged.
» Log hyperparameters to attribute prompts and models to your test runs.

================================================================================


✓ Evaluation completed 🎉! (time taken: 1.23s | token cost: None)
» Test Results (2 total tests):
   » Pass Rate: 0.0% | Passed: 0 | Failed: 2

 ================================================================================

» Want to share evals with your team, or a place for your test cases to live? ❤️ 🏡
  » Run 'deepeval view' to analyze and save testing results on Confident AI.