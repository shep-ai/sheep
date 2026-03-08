# Singleton Pattern — A Creational Design Pattern

The Singleton pattern ensures a class has only one instance and provides a global
point of access to it.

---

## Overview

The Singleton pattern is a **creational** design pattern from the Gang of Four (GoF)
catalog. It restricts instantiation of a class to a single object, which is useful when
exactly one instance is needed to coordinate actions across a system — such as a
configuration manager, connection pool, or logging service.

---

## Structure

- **Singleton** — A class that holds a reference to its sole instance in a class-level
  attribute. It provides a class method (or overrides `__new__`) that returns the
  existing instance or creates one if none exists. The constructor is effectively
  hidden from external callers.

---

## When to Use

- **Configuration management** — A single config object loaded once and shared across
  the application.
- **Database connection pools** — One pool manages all connections rather than creating
  competing pools.
- **Logging** — A single logger instance ensures consistent output formatting and
  destination across all modules.

---

## Trade-offs

### Advantages

- **Controlled access** — Guarantees a single instance, preventing conflicting state.
- **Lazy initialization** — The instance is created only when first requested.
- **Global access point** — Any part of the codebase can reach the instance without
  passing it through every function call.

### Disadvantages

- **Hidden dependencies** — Code that uses the Singleton has an implicit dependency
  that is not visible in function signatures.
- **Testing difficulty** — Global state persists between tests unless explicitly reset,
  making isolated unit testing harder.
- **Concurrency concerns** — In multithreaded environments, the creation step must be
  synchronized to avoid creating multiple instances.

---

## Code Example

```python
class Singleton:
    """Thread-unsafe Singleton for simplicity."""

    _instance = None

    def __new__(cls) -> "Singleton":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        self.value: str = "default"


if __name__ == "__main__":
    a = Singleton()
    b = Singleton()
    a.value = "updated"
    print(a is b)      # True
    print(b.value)      # updated
```
