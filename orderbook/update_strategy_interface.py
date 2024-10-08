from abc import ABC, abstractmethod
from typing import Tuple


class UpdateStrategyInterface(ABC):
    """
    UpdateStrategyInterface is an abstract base class that defines a common interface for parsing
    and normalizing order book updates.

    This interface ensures that any strategy implementation for different exchanges will have
    a consistent set of methods for parsing update objects and normalizing order sizes.

    Implementing classes will provide specific logic based on the data format of different exchanges.
    """
    @abstractmethod
    def parse_update(self, obj) -> Tuple:
        """
        Parse the object to extract bid and ask updates.

        :param obj: The object containing the new order book data.
        :return: A tuple containing the bid and ask updates.
        """
        raise NotImplementedError

    @abstractmethod
    def normalize_size(self, price, size, size_flag) -> float:
        """
        Normalize the size of the order.

        :param price: The price of the order.
        :param size: The size of the order.
        :param size_flag: Indicates the need to normalize to base currency or not.
        :return: The size in a normalized float value.
        """
        raise NotImplementedError
