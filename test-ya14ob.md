## Idempotence

Idempotence is a property of operations that produce the same result regardless of how many times they are executed, making systems more resilient to retries and duplicate requests. In distributed systems and APIs, idempotent operations are critical because network failures often trigger automatic retries, which could otherwise lead to unintended side effects like duplicate transactions. By designing APIs with idempotent semantics, developers can build more reliable systems that gracefully handle failures without requiring clients to implement complex deduplication logic.
