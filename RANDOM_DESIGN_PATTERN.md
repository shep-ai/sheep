# Factory Method — A Creational Design Pattern

The Factory Method pattern defines an interface for creating an object, but lets subclasses
decide which class to instantiate. Factory Method lets a class defer instantiation to
subclasses.

---

## Overview

The Factory Method pattern is a **creational** design pattern from the Gang of Four (GoF)
catalog. It addresses a common problem: a class needs to create objects, but it cannot
anticipate the exact class of objects it must create. Hard-coding concrete class names
creates tight coupling and violates the Open/Closed Principle.

The pattern solves this by defining a method that returns an object. The base class
provides a default implementation or declares it abstract; subclasses override the method
to return the appropriate concrete type. The creating code depends only on the abstract
product interface, not on the concrete product classes.

This pattern is especially useful when object creation involves logic that varies by
subclass, when the exact type depends on configuration or runtime conditions, or when
you want to provide an extension point for subclass-based object creation.

---

## Structure

The Factory Method pattern involves four key participants:

- **Product** — The abstract interface or base class for the objects the factory creates.
  All concrete products implement this interface so the client can work with them
  interchangeably.

- **ConcreteProduct** — A specific implementation of the Product interface. Each
  ConcreteProduct is created by a corresponding ConcreteCreator.

- **Creator** — The class that declares the factory method. It may provide a default
  implementation that returns a default ConcreteProduct, or it may declare the method
  abstract. The Creator typically contains other methods that call the factory method.

- **ConcreteCreator** — A subclass of Creator that overrides the factory method to
  return an instance of a particular ConcreteProduct.

The relationship flows as follows:

1. The client calls the Creator's factory method (often indirectly through other methods)
2. The Creator delegates object creation to its subclass via the factory method
3. The ConcreteCreator returns the appropriate ConcreteProduct
4. The client uses the Product through its abstract interface

---

## When to Use

The Factory Method pattern is appropriate in the following scenarios:

- **Frameworks and libraries** — When a framework defines the skeleton of an algorithm
  but leaves object creation to client code. Document parsers, UI widget creation, and
  plugin systems often use this pattern so extensions can supply their own product types.

- **Class hierarchies with parallel product hierarchies** — When you have a Creator
  hierarchy and a Product hierarchy, and each Creator is responsible for creating a
  specific Product. A shipping company might have AirShippingCreator returning
  AirFreightProduct and SeaShippingCreator returning SeaFreightProduct.

- **Configuration-driven creation** — When the type of object to create depends on
  configuration, environment variables, or runtime discovery. A factory method can
  encapsulate the decision logic.

- **Testing and dependency injection** — When you need to substitute mock or stub
  implementations for testing. Overriding the factory method in a test subclass provides
  a clean way to inject test doubles without changing production code.

---

## Trade-offs

### Advantages

- **Loose coupling** — The client code depends only on the Product abstraction. It does
  not need to know the concrete product classes or how they are created. New product
  types can be added by introducing new Creator subclasses.

- **Open/Closed Principle** — The system is open for extension (add new ConcreteCreator
  and ConcreteProduct pairs) and closed for modification (existing Creator code remains
  unchanged).

- **Single responsibility** — Object creation logic is isolated in the factory method.
  The Creator can focus on other responsibilities while delegating instantiation to
  subclasses.

### Disadvantages

- **Proliferation of classes** — Each product type typically requires a corresponding
  Creator subclass. For simple cases with few variations, this overhead may not be
  justified.

- **Indirection** — Following the chain from Creator to ConcreteCreator to
  ConcreteProduct adds another layer of abstraction. This can make the flow harder to
  trace for developers new to the codebase.

- **Subclassing requirement** — The pattern requires extending the Creator class. In
  languages or scenarios where inheritance is constrained (e.g., final classes, single
  inheritance), Abstract Factory or Builder may be more flexible.

---

## Code Example

The following Python example demonstrates the Factory Method pattern. A `LogProcessor`
(Creator) defines a `create_parser()` factory method; `JsonLogProcessor` and
`XmlLogProcessor` (ConcreteCreators) override it to return the appropriate parser.

```python
from abc import ABC, abstractmethod


class LogParser(ABC):
    """Abstract Product: log parsing interface."""

    @abstractmethod
    def parse(self, raw: str) -> dict:
        pass


class JsonLogParser(LogParser):
    """ConcreteProduct: parses JSON-formatted logs."""

    def parse(self, raw: str) -> dict:
        import json
        return json.loads(raw)


class XmlLogParser(LogParser):
    """ConcreteProduct: parses XML-formatted logs."""

    def parse(self, raw: str) -> dict:
        import xml.etree.ElementTree as ET
        root = ET.fromstring(raw)
        return {child.tag: child.text for child in root}


class LogProcessor(ABC):
    """Creator: defines the factory method for log parsers."""

    @abstractmethod
    def create_parser(self) -> LogParser:
        pass

    def process(self, raw: str) -> dict:
        parser = self.create_parser()
        return parser.parse(raw)


class JsonLogProcessor(LogProcessor):
    """ConcreteCreator: produces JsonLogParser."""

    def create_parser(self) -> LogParser:
        return JsonLogParser()


class XmlLogProcessor(LogProcessor):
    """ConcreteCreator: produces XmlLogParser."""

    def create_parser(self) -> LogParser:
        return XmlLogParser()


if __name__ == "__main__":
    json_proc = JsonLogProcessor()
    result = json_proc.process('{"level": "info", "message": "started"}')
    print(result)

    xml_proc = XmlLogProcessor()
    result = xml_proc.process("<log><level>warning</level><message>retry</message></log>")
    print(result)
```

---

## Related Patterns

- **Abstract Factory** — Factory Method is often used to implement the methods of
  Abstract Factory. While Factory Method creates a single product, Abstract Factory
  creates families of related products.

- **Template Method** — Factory Method is a specialization of Template Method. The
  factory method is the step that varies, while the surrounding algorithm is fixed in
  the base class.

- **Prototype** — Instead of subclassing to get new product types, Prototype clones an
  existing instance. Use Prototype when the number of product classes is large or when
  products are configured at runtime.
