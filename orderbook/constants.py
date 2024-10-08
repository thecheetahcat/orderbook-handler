from enum import Enum
from sortedcontainers import SortedDict
from typing import List, Dict, Union


# ---------- book side ---------- #
class BookSide(Enum):
    BIDS = "bids"
    ASKS = "asks"


BOOK_SIDE_UPDATE = List[List[Union[str, float]]]
SORTED_BOOK = Dict[BookSide, SortedDict]


# ---------- errors ---------- #
class InvalidOrderBookUpdate(Exception):
    """
    Exception raised when an order book update is invalid.
    """
    pass
