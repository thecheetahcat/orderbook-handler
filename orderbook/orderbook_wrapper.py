from .orderbook_interface import OrderBookInterface
from .tracker_interface import TrackerInterface
from .update_strategy_interface import UpdateStrategyInterface
from .constants import BookSide
from abc import ABC
from sortedcontainers import SortedDict


class OrderBookWrapper(OrderBookInterface, ABC):
    def __init__(self, limit: int, size_flag: bool, update_strategy: UpdateStrategyInterface, tracker: TrackerInterface):
        super().__init__(limit, size_flag)
        self.update_strategy = update_strategy
        self.tracker = tracker

    def update_book(self, obj) -> None:
        bids, asks = self.update_strategy.parse_update(obj)
        self.update_orderbook_side(bids, BookSide.BIDS.value)
        self.update_orderbook_side(asks, BookSide.ASKS.value)
        self.maintain_book_limit()

    def maintain_book_limit(self) -> None:
        while len(self.orderbook[BookSide.BIDS.value]) > self.limit:
            self.orderbook[BookSide.BIDS.value].popitem(0)
        while len(self.orderbook[BookSide.ASKS.value]) > self.limit:
            self.orderbook[BookSide.ASKS.value].popitem(-1)

    def clear_data(self) -> None:
        self.orderbook[BookSide.BIDS.value] = SortedDict()
        self.orderbook[BookSide.ASKS.value] = SortedDict()
        self.tracker.clear_tracker()
