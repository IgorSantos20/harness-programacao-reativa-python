import reactivex as rx
from reactivex import operators as ops
from src.with_harness.events import ProductAddedEvent


class ReactiveInvoice:
    def __init__(self, cart_stream: rx.Observable[ProductAddedEvent]):
        self.total: float = 0.0
        # Transformação reativa pura (map) antes do side-effect (subscribe)[cite: 33, 44]
        self._subscription = cart_stream.pipe(
            ops.map(lambda ev: ev.unit_price * ev.quantity),
            ops.catch(lambda err, src: rx.empty()),
        ).subscribe(on_next=self._on_subtotal_calculated)

    def _on_subtotal_calculated(self, subtotal: float) -> None:
        self.total += subtotal


class ReactiveInventory:
    def __init__(self, cart_stream: rx.Observable[ProductAddedEvent]):
        self.stock = {"notebook": 10, "mouse": 50}
        self._subscription = cart_stream.pipe(
            ops.filter(lambda ev: ev.product_name in self.stock),
            ops.catch(lambda err, src: rx.empty()),
        ).subscribe(on_next=self._on_product_added)

    def _on_product_added(self, event: ProductAddedEvent) -> None:
        if self.stock[event.product_name] >= event.quantity:
            self.stock[event.product_name] -= event.quantity