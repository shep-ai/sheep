# Strategy Pattern — A Behavioral Design Pattern

The Strategy pattern defines a family of algorithms, encapsulates each one, and makes
them interchangeable so that the algorithm can vary independently from the clients that
use it.

---

## Overview

The Strategy pattern is a **behavioral** design pattern from the Gang of Four (GoF)
catalog. It addresses a common problem in software design: when a class needs to perform
a task in multiple ways, hard-coding one approach creates inflexible code where adding or
changing an algorithm requires modifying the class itself.

The Strategy pattern solves this by extracting each algorithm into its own class — a
**Strategy** — and giving the client a reference to a Strategy object. The client
delegates the task to the Strategy, and a different Strategy can be swapped in at runtime
without changing the client. This separates the concern of *what to do* from *how to do it*.

This pattern is especially useful when behavior must be selected dynamically based on
user input, configuration, or runtime conditions — for example, choosing a payment method
at checkout, selecting a sorting algorithm based on data size, or picking a compression
codec based on file type.

---

## Structure

The Strategy pattern involves three participants:

- **Strategy** — An abstract interface or base class that defines the algorithm's
  contract. All concrete strategies implement this interface, giving the Context a
  uniform way to invoke any algorithm without knowing its implementation details.

- **ConcreteStrategy** — A specific implementation of the Strategy interface. Each
  ConcreteStrategy encapsulates a distinct algorithm or behavior. Concrete strategies
  are interchangeable as long as they satisfy the Strategy interface.

- **Context** — The object that holds a reference to a Strategy and delegates work to
  it. The Context does not implement the algorithm itself; instead, it calls the
  Strategy's method. The active Strategy can be changed at any time.

The relationship flows as follows:

1. The client selects a ConcreteStrategy and passes it to the Context
2. The Context calls the Strategy's method when the task must be performed
3. The ConcreteStrategy executes the algorithm and returns the result
4. Swapping strategies requires only passing a different ConcreteStrategy to the Context

---

## When to Use

The Strategy pattern is appropriate in the following scenarios:

- **Multiple payment methods** — When an e-commerce checkout must support credit card,
  PayPal, bank transfer, and other methods that share a common interface but differ in
  how they process transactions. Each method is a strategy; the checkout is the context.

- **Pluggable sorting or search algorithms** — When a collection class needs to support
  different sorting strategies (by price, rating, or distance) without the collection
  knowing which algorithm is active. The active strategy can be changed at query time.

- **File export formats** — When an application must export data as JSON, CSV, or XML
  and the format is chosen at runtime based on user preference. Each exporter is an
  independent strategy with the same interface.

- **Validation and business rule engines** — When input validation or pricing rules vary
  by user tier, region, or product type, and each rule set can be encapsulated as a
  strategy assigned to the validator at runtime rather than embedded in a single class.

---

## Trade-offs

### Advantages

- **Open/Closed Principle** — New algorithms can be added as new ConcreteStrategy
  classes without modifying the Context or existing strategies. The system is open for
  extension and closed for modification.

- **Eliminates conditional logic** — Replacing large `if/elif` chains with polymorphic
  strategy objects makes the Context cleaner and easier to understand. Each algorithm
  lives in its own focused, testable class.

- **Runtime algorithm swapping** — The active strategy can be changed dynamically
  during the lifetime of a Context object, enabling behavior that adapts to user actions
  or configuration changes without recreating the Context.

### Disadvantages

- **Increased number of classes** — Each algorithm requires its own class. For simple
  cases with only two or three variations, the overhead of an interface plus multiple
  classes may outweigh the flexibility gained.

- **Client must know which strategy to choose** — The client or a factory must decide
  which ConcreteStrategy to select. If not carefully encapsulated, the conditional
  logic that Strategy was meant to eliminate reappears in the client.

---

## Code Example

The following Python example demonstrates the Strategy pattern using `abc.ABC` to define
the Strategy interface explicitly. A `Checkout` context delegates payment processing to
whichever `PaymentStrategy` is active, allowing the payment method to be switched at
runtime without modifying the Checkout class.

```python
from abc import ABC, abstractmethod


class PaymentStrategy(ABC):
    """Abstract Strategy interface for payment processing."""

    @abstractmethod
    def pay(self, amount: float) -> None:
        pass


class CreditCardPayment(PaymentStrategy):
    def __init__(self, last_four: str) -> None:
        self._last_four = last_four

    def pay(self, amount: float) -> None:
        print(f"Charged ${amount:.2f} to card ending in {self._last_four}")


class PayPalPayment(PaymentStrategy):
    def __init__(self, email: str) -> None:
        self._email = email

    def pay(self, amount: float) -> None:
        print(f"Sent ${amount:.2f} via PayPal to {self._email}")


class BankTransferPayment(PaymentStrategy):
    def __init__(self, account: str) -> None:
        self._account = account

    def pay(self, amount: float) -> None:
        print(f"Transferred ${amount:.2f} to account {self._account}")


class Checkout:
    """Context: delegates payment processing to a PaymentStrategy."""

    def __init__(self, strategy: PaymentStrategy) -> None:
        self._strategy = strategy

    def set_payment_strategy(self, strategy: PaymentStrategy) -> None:
        self._strategy = strategy

    def complete_purchase(self, amount: float) -> None:
        self._strategy.pay(amount)


if __name__ == "__main__":
    checkout = Checkout(CreditCardPayment("1234"))
    checkout.complete_purchase(99.99)

    checkout.set_payment_strategy(PayPalPayment("user@example.com"))
    checkout.complete_purchase(49.95)

    checkout.set_payment_strategy(BankTransferPayment("GB29NWBK60161331926819"))
    checkout.complete_purchase(299.00)
```
