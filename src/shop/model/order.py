"""
Domain models for order management.
The domain model represents the core business logic and entities.
Rule: The 'model' package MUST NOT depend on any other application package (ui, services, persistence, etc.).
"""

from dataclasses import dataclass
from typing import List

# ============================================================================
# ARCHITECTURE DEMO: Forbidden Dependency Check
# ----------------------------------------------------------------------------
# In a clean architecture / DDD onion architecture, domain models must remain
# pure POPOs (Plain Old Python Objects) and never import from services or adapters.
#
# UNCOMMENT the line below to simulate an architectural violation:
# When uncommented, running `pytest` will fail with an architectural violation!
# ============================================================================
# from shop.services.payment import PaymentService  # ❌ FORBIDDEN DEPENDENCY!


@dataclass
class OrderItem:
    sku: str
    quantity: int
    unit_price: float

    @property
    def total_price(self) -> float:
        return self.quantity * self.unit_price


@dataclass
class Order:
    order_id: str
    customer_id: str
    items: List[OrderItem]

    @property
    def total_amount(self) -> float:
        return sum(item.total_price for item in self.items)

    def is_valid_order(self) -> bool:
        return len(self.items) > 0 and self.total_amount > 0
