"""Payment processing service."""


class PaymentService:
    """Simulates payment gateway integration."""

    def charge(self, customer_id: str, amount: float) -> bool:
        print(f"Charging customer {customer_id} EUR {amount:.2f}")
        return True

