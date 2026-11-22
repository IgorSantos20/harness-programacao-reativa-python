class Inventory:
    def __init__(self):
        self.stock = {"notebook": 10, "mouse": 50}

    def decrease_stock(self, item: str, qty: int):
        if self.stock.get(item, 0) < qty:
            raise ValueError("Estoque insuficiente")
        self.stock[item] -= qty


class Invoice:
    def __init__(self):
        self.total = 0.0

    def update_invoice(self, price: float, qty: int):
        # Passivo: aguarda comando remoto de outro módulo[cite: 8, 9]
        self.total += price * qty


class Cart:
    def __init__(self, invoice: Invoice, inventory: Inventory):
        self.items = []
        # VIOLAÇÃO ARQUITETURAL: Cart conhece e controla Invoice e Inventory[cite: 8, 48]
        self.invoice = invoice
        self.inventory = inventory

    def add_product(self, name: str, price: float, qty: int):
        self.items.append({"name": name, "price": price, "qty": qty})
        # Acoplamento imperativo direto ("este muda esse")[cite: 7, 8]
        self.inventory.decrease_stock(name, qty)
        self.invoice.update_invoice(price, qty)