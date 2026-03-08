# Singleton Pattern — A Creational Design Pattern

The Singleton pattern restricts the instantiation of a class to a single object and provides
a global point of access to that instance.

---

## Overview

The Singleton pattern is a **creational** design pattern from the Gang of Four (GoF) catalog.
It addresses a common problem in software design: when certain resources should exist in only
one instance throughout the application's lifetime, but multiple parts of the code need access
to that instance.

Hard-coding a single global instance creates rigid, inflexible code where the instance
initialization is scattered and difficult to test. The Singleton pattern solves this by
centralizing instance creation and ensuring that only one instance can ever exist. It does
this through a static method (or in Python, a decorator or class method) that returns the
single instance, creating it on first access if necessary (lazy initialization).

This pattern is widely used for resources that are expensive to create, should be shared
across the application, or must maintain consistent state: logging systems, configuration
managers, database connection pools, and thread pools. However, the pattern is also
controversial because it introduces global state, which can complicate testing and hide
dependencies between components.

---

## Structure

The Singleton pattern involves one primary participant:

- **Singleton** — The class that restricts instantiation to a single instance. It typically
  holds a private class-level reference to the single instance and provides a public method
  (often named `instance()` or accessed through a decorator) that returns that instance.
  The constructor or instantiation mechanism is private or restricted to prevent direct
  instantiation outside the pattern.

- **Client** — Any part of the application that needs to access the singleton instance.
  Rather than creating a new instance, the client calls the Singleton's access method to
  get the shared instance.

The relationship is straightforward:

1. The Singleton class stores the single instance at the class level
2. When a client requests access, the Singleton returns the shared instance
3. If the instance does not yet exist, it is created on first access (lazy initialization)
4. All subsequent requests return the same instance

---

## When to Use

The Singleton pattern is appropriate in the following scenarios:

- **Logging systems** — An application-wide logger that all components write to. Using
  Singleton ensures all log messages go to the same destination and the logger is
  initialized only once, avoiding multiple file handles or duplicate log streams.

- **Configuration managers** — Application configuration loaded from files at startup and
  accessed throughout the application. Singleton ensures the configuration is loaded once,
  remains consistent across all components, and is available globally without passing it
  as a parameter through every function.

- **Database connection pools** — A single pool managing a limited set of database
  connections. Singleton ensures that the pool is created once, connection resources are
  properly managed and reused, and all code accesses the same pool rather than creating
  multiple competing pools.

---

## Trade-offs

### Advantages

- **Controlled single instance** — The pattern guarantees that only one instance exists,
  preventing accidental duplication of resources and ensuring consistent shared state.

- **Lazy initialization** — The instance is created only when first needed, reducing startup
  time and resource consumption for singletons that may not be used in every execution path.

- **Global point of access** — Code anywhere in the application can easily access the
  instance without needing to pass it through multiple function parameters or constructor
  chains, simplifying call signatures.

### Disadvantages

- **Hidden global state** — The Singleton is implicitly available globally, creating hidden
  dependencies. Code reading a function cannot tell from its signature that it depends on
  the Singleton, making reasoning about dependencies difficult.

- **Testing challenges** — Tests must account for shared state across test cases. If the
  Singleton is not reset between tests, one test's behavior can affect another. Mocking a
  Singleton can be awkward since the global instance must be replaced, and cleanup is often
  error-prone.

- **Thread-safety complexity** — Ensuring the single instance is created safely in
  multi-threaded environments requires synchronization mechanisms (locks), which add
  complexity and can introduce performance bottlenecks through lock contention.

- **Hides dependencies** — Dependency injection is generally preferred over Singleton because
  it makes dependencies explicit. A Singleton-dependent class is harder to instantiate
  independently or in different configurations.

---

## Code Example

The following Python example demonstrates the Singleton pattern using a decorator-based
approach. The `@singleton` decorator wraps a class and ensures only one instance exists,
with thread-safe initialization using `threading.Lock`.

```python
import threading
from typing import Any


def singleton(cls: type) -> Any:
    """Decorator that restricts a class to a single instance.

    Thread-safe using a lock to prevent race conditions during the
    first instantiation in multi-threaded environments.
    """
    instances = {}
    lock = threading.Lock()

    def get_instance(*args: Any, **kwargs: Any) -> Any:
        """Return the single instance, creating it on first access."""
        if cls not in instances:
            with lock:
                # Double-check locking: verify instance wasn't created
                # by another thread while waiting for the lock
                if cls not in instances:
                    instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance


@singleton
class Logger:
    """Example: A thread-safe application-wide logger."""

    def __init__(self) -> None:
        self.messages: list[str] = []

    def log(self, message: str) -> None:
        """Add a message to the log."""
        print(f"[LOG] {message}")
        self.messages.append(message)

    def get_all_messages(self) -> list[str]:
        """Return all logged messages."""
        return self.messages


if __name__ == "__main__":
    # Both calls return the same instance
    logger1 = Logger()
    logger2 = Logger()

    assert logger1 is logger2, "Instances are not the same!"

    # All log messages go to the same instance
    logger1.log("Application started")
    logger2.log("Processing request")

    # Both loggers reflect the same state
    print(f"Total messages: {len(logger1.get_all_messages())}")
    print(f"Logger1 messages: {logger1.get_all_messages()}")
    print(f"Logger2 messages: {logger2.get_all_messages()}")
```
