"""
Persistence adapters and repository abstractions.
Rule: The 'adapters' (or 'persistence') package may import from 'model',
      but 'services' or 'model' should not depend directly on concrete database adapters.
"""

from typing import Dict, Optional
from shop.model.order import Order


class InMemoryOrderRepository:
    """Stores orders in an in-memory dictionary (simulating a database adapter)."""

    def __init__(self) -> None:
        self._storage: Dict[str, Order] = {}

    def save(self, order: Order) -> None:
        self._storage[order.order_id] = order

    def find_by_id(self, order_id: str) -> Optional[Order]:
        return self._storage.get(order_id)

