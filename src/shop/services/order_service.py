"""
Order processing application service.
Rule: 'services' may import 'model' (entities) and 'adapters' / abstractions,
      but 'model' MUST NOT import 'services'.
"""

from shop.model.order import Order
from shop.services.payment import PaymentService
from shop.adapters.repository import InMemoryOrderRepository


class OrderService:
    def __init__(
        self,
        repository: InMemoryOrderRepository,
        payment_service: PaymentService,
    ) -> None:
        self.repository = repository
        self.payment_service = payment_service

    def process_order(self, order: Order) -> bool:
        if not order.is_valid_order():
            raise ValueError(f"Invalid order {order.order_id}")

        charged = self.payment_service.charge(order.customer_id, order.total_amount)
        if charged:
            self.repository.save(order)
            return True
        return False
