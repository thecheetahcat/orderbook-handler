from abc import ABC, abstractmethod
from typing import Dict, Any


class TrackerInterface(ABC):
    """
    TrackerInterface is an abstract base class that defines a common interface for tracking order book updates.

    This interface ensures that any tracker implementation for different exchanges will have a consistent set of methods
    for initializing, validating, updating, and clearing the tracking information related to order book updates.

    Attributes:
        tracker (Dict): A dictionary to store tracking information for each symbol.
    """
    def __init__(self):
        """
        Initializes the TrackerInterface with an empty tracking dictionary.
        """
        self.tracker = {}

    @abstractmethod
    def initialize(self, obj) -> Any:
        """
        Initialize the tracker with any sequence id's.

        :param obj: The object containing the new order book data.
        :return: Any.
        """
        raise NotImplementedError

    @abstractmethod
    def validate_update(self, obj) -> Any:
        """
        Validate each order book update.

        :param obj: The object containing the new order book data.
        :return: Any.
        """
        raise NotImplementedError

    @abstractmethod
    def update_tracker(self, obj) -> Any:
        """
        Update the tracker with new sequence id's

        :param obj: The object containing the new order book data.
        :return: Any.
        """
        raise NotImplementedError

    def clear_tracker(self) -> None:
        """
        Helper method to clear the tracker for a given symbol.

        :return: None.
        """
        self.tracker = {}
