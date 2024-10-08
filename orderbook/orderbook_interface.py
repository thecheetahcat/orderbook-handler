from abc import ABC, abstractmethod
from sortedcontainers import SortedDict
from constants import SORTED_BOOK, BookSide
from typing import Any, Optional


class OrderBookInterface(ABC):
    """
    OrderBookInterface is an abstract base class that defines a common interface for order book updates.

    This interface ensures that any order book implementation for different exchanges will have a consistent set of methods
    for initializing, handling, maintaining, and clearing the order book.

    Attributes:
        orderbook (SORTED_BOOK): A dictionary to store the order book information.
        limit (int): The maximum number of orders to maintain in the book.
        size_flag (bool): Flag for size normalization in the update strategy. For example, Deribit inverse contracts have size
            in quote currency, but in linear contracts, they have size in base currency. The flag can indicate whether to normalize
            to base currency or not.
    """
    def __init__(self, limit: int, size_flag: bool):
        """
        Initializes the OrderBook with an empty order book dictionary.
        """
        self.orderbook: SORTED_BOOK = {BookSide.BIDS.value: SortedDict(), BookSide.ASKS.value: SortedDict()}
        self.limit = limit
        self.size_flag = size_flag

    @abstractmethod
    def initialize(self, obj) -> SORTED_BOOK:
        """
        Initializes the order book for a given symbol with a snapshot of data.
        This method processes the initial snapshot of order book data (bids and asks) and updates the order book accordingly.

        :param obj: The object containing the order book update information.
        :return: A dictionary representing the updated order book.
        """
        raise NotImplementedError

    @abstractmethod
    def handler(self, obj) -> Optional[SORTED_BOOK]:
        """
        Handles new updates to the order book.
        This method is responsible for processing incoming order book updates.
        It validates the update, clears data if necessary, and applies the update to the order book.

        :param obj: The object containing the order book update information.
        :return: The updated order book, or None if the update was skipped.
        """
        raise NotImplementedError

    @abstractmethod
    def update_book(self, obj) -> None:
        """
        Updates the order book for a given symbol based on the provided update object.
        This method parses the update using the strategy and then updates both sides of the book.

        :param obj: The object containing the order book update information.
        :return: None.
        """
        raise NotImplementedError

    @abstractmethod
    def update_orderbook_side(self, updates: Any, book_side: BookSide) -> None:
        """
        Batch updates a specific side (bids or asks) of the order book.

        :param updates: The order book update information.
        :param book_side: The side of the book to update (either 'bids' or 'asks').
        :return: None.
        """
        raise NotImplementedError

    @abstractmethod
    def maintain_book_limit(self) -> None:
        """
        Maintains the maximum limit of orders for both the bid and ask sides of the order book.
        This method ensures that the number of orders does not exceed the specified limit.

        :return: None.
        """
        raise NotImplementedError

    @abstractmethod
    def clear_data(self) -> None:
        """
        Clears all data from the order book for a specific symbol, including both bids and asks.

        :return: None.
        """
        raise NotImplementedError
