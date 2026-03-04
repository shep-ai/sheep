# Door Lock State Machine

```mermaid
stateDiagram-v2
    [*] --> Locked
    Locked --> Unlocked : unlock
    Unlocked --> Locked : lock
```
