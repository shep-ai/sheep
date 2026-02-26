# State Machine: Traffic Light

A traffic light cycles through Red, Green, and Yellow states in a continuous loop.

```mermaid
stateDiagram-v2
    [*] --> Red
    Red --> Green : Go
    Green --> Yellow : Slow down
    Yellow --> Red : Stop
```
