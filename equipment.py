"""Экипировка. Здесь ты пишешь новую систему.

Классы Item и Player трогать не надо: их держит остальной сервер, и менять
поля нельзя. Твоя работа — три функции внизу.
"""

SLOTS = ("head", "body", "right_hand", "left_hand", "ring_1", "ring_2")
# Не отдельное хранилище: просто два ключа из SLOTS, чтобы не писать их руками.
HANDS = ("right_hand", "left_hand")


class Item:
    """Вещь. Класс достался от старой системы."""

    def __init__(self, name, slot, power=0, durability=100, level_req=1,
                 two_handed=False):
        self.name = name
        self.slot = slot
        self.power = power
        self.durability = durability
        self.level_req = level_req
        self.two_handed = two_handed

    def __bool__(self):
        # Валера: «удобно же — if item: значит вещь целая»
        return self.durability > 0

    def __repr__(self):
        return f"<{self.name} {self.slot} dur={self.durability}>"


class Player:
    def __init__(self, name, level=1, inventory=None, capacity=20):
        self.name = name
        self.level = level
        self.inventory = list(inventory) if inventory else []
        self.capacity = capacity
        self.slots = {slot: None for slot in SLOTS}

    def __repr__(self):
        return f"<{self.name} lvl={self.level} inv={len(self.inventory)}>"


def equip(player, item):
    """Надеть вещь из инвентаря. True — надели, False — не смогли."""
    raise NotImplementedError


def unequip(player, slot):
    """Снять вещь из слота в инвентарь. True — сняли, False — слот пуст."""
    raise NotImplementedError


def total_power(player):
    """Сила всех надетых вещей. Сломанная вещь даёт 0."""
    raise NotImplementedError
