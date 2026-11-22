from dataclasses import dataclass


@dataclass(frozen=True)
class ProductAddedEvent:
    product_name: str
    unit_price: float
    quantity: int