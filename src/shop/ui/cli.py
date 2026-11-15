"""
User interface / CLI / API entry points.
Rule: 'ui' is allowed to access 'services' and 'model'.
      However, 'model' or 'services' MUST NEVER access 'ui'.
"""

from shop.model.order import Order, OrderItem
from shop.services.order_service import OrderService
from shop.services.payment import PaymentService
from shop.adapters.repository import InMemoryOrderRepository


def run_cli_checkout_demo() -> None:
    repo = InMemoryOrderRepository()
    payment = PaymentService()
    service = OrderService(repository=repo, payment_service=payment)

    order = Order(
        order_id="ORD-42",
        customer_id="CUST-100",
        items=[OrderItem(sku="ROBOT-ARM-V1", quantity=1, unit_price=499.0)],
    )

    success = service.process_order(order)
    print(f"Order placement success: {success}")
