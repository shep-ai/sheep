# Observer Pattern — A Behavioral Design Pattern

The Observer pattern defines a one-to-many dependency between objects so that when one
object changes state, all its dependents are notified and updated automatically.

---

## Overview

The Observer pattern is a **behavioral** design pattern from the Gang of Four (GoF) catalog.
It addresses a fundamental problem in software design: how to maintain consistency between
related objects without making them tightly coupled.

In many systems, a change in one object requires other objects to react. For example, when
a data model changes, multiple views displaying that data need to refresh. Hard-coding these
dependencies creates rigid, brittle code where adding a new dependent means modifying the
source object.

The Observer pattern solves this by introducing a subscription mechanism. The object that
holds the state (the **Subject**) maintains a list of dependents (the **Observers**) and
notifies them automatically when its state changes. Observers can be added or removed at
runtime without modifying the Subject, enabling a loosely coupled design where neither side
needs to know the concrete details of the other.

This pattern is sometimes referred to as the **Publish-Subscribe** mechanism, though the
classic GoF Observer is synchronous and direct, while Pub/Sub systems often introduce a
message broker for further decoupling.

---

## Structure

The Observer pattern involves four key participants:

- **Subject (Observable)** — The object that holds state and maintains a list of observers.
  It provides methods to attach, detach, and notify observers. When its state changes, it
  iterates through its observer list and calls each observer's update method.

- **Observer** — An abstract interface or base class that defines the `update()` method.
  All concrete observers implement this interface so the Subject can notify them without
  knowing their specific types.

- **ConcreteSubject** — A specific implementation of the Subject that stores the state of
  interest. When this state changes, it triggers notification to all registered observers.

- **ConcreteObserver** — A specific implementation of the Observer interface. It registers
  with a ConcreteSubject and implements the `update()` method to synchronize its own state
  with the Subject's state.

The relationships between participants follow a simple flow:

1. ConcreteObservers register themselves with the ConcreteSubject
2. When the ConcreteSubject's state changes, it calls `notify()`
3. `notify()` iterates through all registered observers and calls `update()` on each
4. Each ConcreteObserver responds to the update according to its own logic

---

## When to Use

The Observer pattern is appropriate in the following scenarios:

- **Event-driven UI systems** — When a data model changes and multiple UI components
  (charts, tables, summaries) need to refresh independently. GUI frameworks like Qt,
  Swing, and reactive frontend libraries all use variations of this pattern.

- **Monitoring and logging** — When system metrics change and multiple consumers need to
  react: a dashboard display, an alerting service, and a log aggregator can all observe
  the same metric source without knowing about each other.

- **Stock price or data feeds** — When a real-time data source (stock ticker, sensor
  readings, weather data) has multiple subscribers that each process the data differently:
  one may display it, another may store it, and a third may trigger trading rules.

- **Configuration change propagation** — When application configuration is updated at
  runtime and multiple components need to adapt their behavior. Each component observes
  the configuration store and reacts to relevant changes.

- **Message notification systems** — When an event occurs (new user signup, order placed,
  payment received) and multiple downstream services need to be informed: sending a
  welcome email, updating analytics, provisioning resources.

---

## Trade-offs

### Advantages

- **Loose coupling** — The Subject only knows that its observers implement the Observer
  interface. It does not need to know their concrete classes, what they do with the data,
  or how many there are. This makes it easy to add new observer types without modifying
  existing code.

- **Open/Closed Principle** — New observers can be introduced without changing the Subject
  or other existing observers. The system is open for extension but closed for modification.

- **Dynamic relationships** — Observers can be attached and detached at runtime, allowing
  the set of dependents to change as the application evolves during execution.

- **Broadcast communication** — A single state change automatically propagates to all
  interested parties without the Subject needing to manage individual notifications.

### Disadvantages

- **Unexpected cascading updates** — If observers themselves trigger state changes, this
  can create chains of updates that are difficult to trace, debug, and reason about.
  Circular dependencies between observers can cause infinite loops.

- **Memory leaks from forgotten observers** — If observers register but are never
  detached (especially in long-running applications), they remain in memory as long as
  the Subject holds a reference to them. This is known as the "lapsed listener" problem.

- **Notification ordering is undefined** — The GoF pattern does not specify the order
  in which observers are notified. If observers depend on being called in a particular
  sequence, this pattern alone does not guarantee it.

- **Performance cost with many observers** — Notifying a large number of observers
  synchronously can introduce latency. Each observer's update method runs in sequence,
  and a slow observer delays all subsequent notifications.

---

## Code Example

The following Python example demonstrates the Observer pattern using `abc.ABC` to define
the Observer interface explicitly. A `WeatherStation` (ConcreteSubject) notifies multiple
display observers when temperature data changes.

```python
from abc import ABC, abstractmethod


class Observer(ABC):
    """Abstract Observer interface."""

    @abstractmethod
    def update(self, temperature: float) -> None:
        """Receive updated state from the subject."""
        pass


class Subject:
    """Base Subject that manages observer registration and notification."""

    def __init__(self) -> None:
        self._observers: list[Observer] = []

    def attach(self, observer: Observer) -> None:
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer: Observer) -> None:
        self._observers.remove(observer)

    def notify(self) -> None:
        for observer in self._observers:
            observer.update(self.temperature)


class WeatherStation(Subject):
    """ConcreteSubject that tracks temperature readings."""

    def __init__(self) -> None:
        super().__init__()
        self._temperature: float = 0.0

    @property
    def temperature(self) -> float:
        return self._temperature

    @temperature.setter
    def temperature(self, value: float) -> None:
        self._temperature = value
        self.notify()


class PhoneDisplay(Observer):
    """ConcreteObserver that shows temperature on a phone screen."""

    def update(self, temperature: float) -> None:
        print(f"Phone Display: {temperature:.1f}°C")


class DesktopWidget(Observer):
    """ConcreteObserver that shows temperature in a desktop widget."""

    def update(self, temperature: float) -> None:
        print(f"Desktop Widget: {temperature:.1f}°C")


class TemperatureLogger(Observer):
    """ConcreteObserver that logs temperature readings."""

    def __init__(self) -> None:
        self.log: list[float] = []

    def update(self, temperature: float) -> None:
        self.log.append(temperature)
        print(f"Logger: recorded {temperature:.1f}°C (total entries: {len(self.log)})")


if __name__ == "__main__":
    station = WeatherStation()

    phone = PhoneDisplay()
    widget = DesktopWidget()
    logger = TemperatureLogger()

    station.attach(phone)
    station.attach(widget)
    station.attach(logger)

    station.temperature = 22.5
    print()
    station.temperature = 18.3
    print()

    station.detach(widget)
    station.temperature = 25.0
```

---

## Related Patterns

- **Mediator** — While Observer establishes direct one-to-many communication between a
  Subject and its Observers, the Mediator pattern centralizes communication through a
  mediator object. Use Mediator when many-to-many interactions become too complex for
  direct Observer relationships.

- **Publish-Subscribe** — An evolution of Observer that introduces a message broker or
  event bus between publishers and subscribers. This adds full decoupling (publishers
  and subscribers do not reference each other at all) and often supports asynchronous,
  distributed communication.

- **Event Sourcing** — Complements Observer by persisting the sequence of state-change
  events rather than just the current state. Observers can replay events to reconstruct
  state, which is useful in audit logging and temporal queries.
