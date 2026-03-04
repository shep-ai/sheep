# ATM State Machine

This diagram models the states of an Automated Teller Machine (ATM). The machine begins idle, accepts a card, prompts for a PIN (retrying on wrong entry), authenticates the user, dispenses cash, and ejects the card before returning to idle.

```mermaid
stateDiagram-v2
    [*] --> Idle

    Idle --> CardInserted : insertCard
    CardInserted --> PINEntry : cardAccepted
    PINEntry --> PINEntry : wrongPIN
    PINEntry --> Authenticated : correctPIN
    PINEntry --> EjectCard : maxAttemptsReached
    Authenticated --> Dispensing : requestCash
    Dispensing --> EjectCard : cashDispensed
    Authenticated --> EjectCard : cancel
    EjectCard --> Idle : cardRemoved
```
