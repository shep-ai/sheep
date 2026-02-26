# Observer Pattern

## Category

Behavioral — Gang of Four (GoF)

## Intent

Define a one-to-many dependency between objects so that when one object changes state,
all its dependents are notified and updated automatically.

The Observer pattern solves the problem of keeping multiple objects in sync with a
single source of truth without creating tight coupling between them. Without it, a
subject would need to know about every dependent object and call each one directly,
making the system brittle and hard to extend.

## Structure

The pattern involves two roles:

- **Subject** (also called Publisher or Observable): Maintains a list of observers and
  provides methods to register, remove, and notify them. When its state changes, it
  calls a notification method that iterates over all registered observers.
- **Observer** (also called Subscriber or Listener): Defines an interface with an
  update method. Concrete observers implement this interface and react to state changes
  in whatever way is appropriate for their purpose.

The subject and its observers interact through this interface only, so neither side
needs to know the concrete type of the other. New observer types can be added without
modifying the subject.

## Example

A stock ticker application is a classic use case. The ticker (subject) holds the current
price of a stock. Multiple displays — a web dashboard, a mobile app, and an alert service
— all register as observers. When the price updates, the ticker notifies each display
automatically. Each display then refreshes its view independently.

The same pattern appears throughout software: UI frameworks use it for event listeners
(a button notifying click handlers), messaging systems use it as publish/subscribe
infrastructure, and reactive programming libraries build their entire model around it.
