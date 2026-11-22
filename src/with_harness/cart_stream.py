import reactivex as rx
from reactivex.subject import Subject
from src.with_harness.events import ProductAddedEvent


class CartController:
    def __init__(self):
        # Sink privado: apenas o produtor emite eventos[cite: 22, 24]
        self._cart_subject: Subject[ProductAddedEvent] = Subject()

    @property
    def stream(self) -> rx.Observable[ProductAddedEvent]:
        # Expõe apenas o Observable (somente leitura)[cite: 26]
        return self._cart_subject.pipe()

    def add_product(self, name: str, price: float, qty: int) -> None:
        if qty <= 0 or price < 0:
            self._cart_subject.on_error(ValueError("Quantidade ou preço inválido"))
            return
        event = ProductAddedEvent(product_name=name, unit_price=price, quantity=qty)
        self._cart_subject.on_next(event)