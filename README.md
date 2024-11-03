# Orderbook Handler Package

---

## Description:
The **orderbook_handler package** provides an efficient and standardized way of storing a sorted orderbook across multiple exchanges using a `SortedDict`. 
`OrderbookInterface`, `UpdateStrategyInterface`, and `TrackerInterface` provide a standardized way of managing an orderbook for cryptocurrency exchanges. 
You can implement exchange specific functionality for parsing orderbook updates with the update strategy, and ensuring validity of those updates
with the tracker interface. `OrderBookWrapper` implements `OrderbookInterface` with general methods that can be used across different platforms, but a final `Orderbook`
class must be created to implement exchange specific functionality. 

---

## Installation

### Requirements
- Python 3.8+
- `sortedcontainers` (for SortedDict)

You can install the required dependencies via `pip`:
```bash
pip install -r requirements.txt
```

---

## Usage

### Example implementation with Deribit:

***Deribit Book Stream Docs: https://docs.deribit.com/#book-instrument_name-interval***

Combing the UpdateStrategy, Tracker, and OrderbookWrapper to make DeribitOrderbook:
```python
from orderbook.orderbook_wrapper import OrderBookWrapper
from orderbook.update_strategy_interface import UpdateStrategyInterface
from orderbook.tracker_interface import TrackerInterface
import orderbook.constants as constants
from typing import Tuple, Optional


class DeribitUpdateStrategy(UpdateStrategyInterface):
    """
    DeribitUpdateStrategy is an implementation of UpdateStrategyInterface that handles order book data parsing specifically for Deribit.
    """

    def __init__(self):
        super().__init__()

    def parse_update(self, obj) -> Tuple[constants.BOOK_SIDE_UPDATE, constants.BOOK_SIDE_UPDATE]:
        return obj['params']['data'][constants.BookSide.BIDS.value], obj['params']['data'][constants.BookSide.ASKS.value]

    def normalize_size(self, price, size, size_flag) -> float:
        return size / price if size_flag else size  # futures sizes come in quote currency rather than base
    
    
class DeribitTracker(TrackerInterface):
    """
    DeribitTracker is an implementation of TrackerInterface that handles tracking order book updates specifically for Deribit.
    """
    def __init__(self):
        super().__init__()

    def initialize(self, obj) -> None:
        self.update_tracker(obj)

    def validate_update(self, obj) -> bool:
        if obj['params']['data']['prev_change_id'] == self.tracker['change_id']:
            # valid update, no messages skipped
            self.update_tracker(obj)  # ensure to update the tracker each time
            return True
        else:
            # there was a message skipped, clear data, and refresh book
            return False

    def update_tracker(self, obj) -> None:
        data = obj['params']['data']
        change_id = data['change_id']
        self.tracker.update({'prev_change_id': change_id if 'prev_change_id' not in data else data['prev_change_id'], 'change_id': change_id})


class DeribitOrderBook(OrderBookWrapper):
    """
    DeribitOrderBook is an implementation of OrderBookWrapper that handles order book updates specifically for Deribit.
    """

    def __init__(self, limit: int, size_flag: bool = False):
        super().__init__(limit, size_flag, DeribitUpdateStrategy(), DeribitTracker())

    def initialize(self, obj) -> constants.SORTED_BOOK:
        data = obj['params']['data']
        self.orderbook[constants.BookSide.BIDS.value].update({bid[1]: self.update_strategy.normalize_size(bid[1], bid[2], self.size_flag) for bid in data[constants.BookSide.BIDS.value] if bid[0] == 'new'})
        self.orderbook[constants.BookSide.ASKS.value].update({ask[1]: self.update_strategy.normalize_size(ask[1], ask[2], self.size_flag) for ask in data[constants.BookSide.ASKS.value] if ask[0] == 'new'})
        self.tracker.initialize(obj)
        return self.orderbook

    def update_orderbook_side(self, updates: constants.BOOK_SIDE_UPDATE, book_side: constants.BookSide) -> None:
        # update action: 'new' or 'change' (not 'delete')
        self.orderbook[book_side].update({update[1]: self.update_strategy.normalize_size(update[1], update[2], self.size_flag) for update in updates if update[0] != 'delete'})
        
        # remove action: 'delete' orders
        for price in [update[1] for update in updates if update[0] == 'delete']:
            self.orderbook[book_side].pop(price, None)

    def handler(self, obj) -> Optional[constants.SORTED_BOOK]:
        if self.tracker.validate_update(obj) is True:  # valid update, update book as normal
            self.update_book(obj)
            return self.orderbook
        else:  # invalid update, reset order book
            raise constants.InvalidOrderBookUpdate  # raise an error to reset the book
```

---

#### License
This package is licensed under the MIT License. See the LICENSE file for details.

----
### Updated local commit author to cheetah cat...