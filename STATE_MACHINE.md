# Sheep State Machine

```mermaid
stateDiagram-v2
    [*] --> Grazing
    Grazing --> Wandering : feels restless
    Wandering --> Grazing : finds good grass
    Wandering --> Shearing : farmer appears
    Shearing --> Sleeping : exhausted after shearing
    Sleeping --> Grazing : fully rested
    Sleeping --> [*] : winter comes
```
