import pytest
from dataclasses import FrozenInstanceError
from src.with_harness.cart_stream import CartController
from src.with_harness.consumers import ReactiveInvoice, ReactiveInventory
from src.with_harness.events import ProductAddedEvent


def test_event_immutability():
    ev = ProductAddedEvent("notebook", 3500.0, 1)
    with pytest.raises(FrozenInstanceError):
        ev.quantity = 5  # type: ignore


def test_reactive_propagation_to_multiple_consumers():
    cart = CartController()
    invoice = ReactiveInvoice(cart.stream)
    inventory = ReactiveInventory(cart.stream)

    # Emite eventos no stream do carrinho
    cart.add_product("notebook", 3500.0, 2)
    cart.add_product("mouse", 150.0, 3)

    # Verifica auto-atualização independente dos consumidores[cite: 21]
    assert invoice.total == (3500.0 * 2) + (150.0 * 3)
    assert inventory.stock["notebook"] == 8
    assert inventory.stock["mouse"] == 47


def test_stream_error_resilience():
    cart = CartController()
    invoice = ReactiveInvoice(cart.stream)

    # Entrada inválida dispara on_error no stream, tratado reativamente sem quebrar a aplicação[cite: 45]
    cart.add_product("notebook", -100.0, 1)
    assert invoice.total == 0.0