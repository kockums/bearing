from typing import Any, Callable, List


class ListenerMixin:
    """
    A mixin class that adds event listener functionality to classes. It
    allows classes to register, remove, and notify listeners about specific
    events or changes.

    This mixin is designed to be used with other classes to provide a
    standardized approach to event handling and notifications.

    Attributes:
        _listeners (List[Callable]): A list of callback functions that are
            notified upon events.
    """

    def __init__(self):
        """
        Initializes the mixin with an empty list of listeners.
        """
        self._listeners: List[Callable] = []

    def add_listener(self, listener: Callable[[Any], None]):
        """
        Registers a new listener for event notifications.

        Parameters:
            listener: A callable to be invoked when notifying listeners.
        """
        self._listeners.append(listener)

    def remove_listener(self, listener: Callable[[Any], None]):
        """
        Removes a previously registered listener.

        Parameters:
            listener: The callable to be removed from the list of listeners.
        """
        self._listeners.remove(listener)

    def notify_listeners(self, *args, **kwargs):
        """
        Notifies all registered listeners, passing along any arguments.

        Parameters:
            *args: Positional arguments to pass to the listeners.
            **kwargs: Keyword arguments to pass to the listeners.
        """
        for listener in self._listeners:
            listener(*args, **kwargs)
