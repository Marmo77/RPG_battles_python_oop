# items.py
class Item:
    def __init__(self, name: str, effect_type: str, value: int, quantity: int = 1):
        self.name = name
        self.effect_type = effect_type
        self.value = value
        self.quantity = quantity

    def __repr__(self):
        return f"{self.name}({self.effect_type}:{self.value} x{self.quantity})"


default_items = [
    Item("Mikstura Lecznicza", "heal", 20, 2),
    Item("Mikstura Tarczy", "shield", 20, 1),
    Item("Mikstura Wściekłości", "damage", 15, 1),
]
