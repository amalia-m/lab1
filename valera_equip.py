"""Экипировка. Старая версия, тестовый сервер.

Автор: Валера. Поддержка: никто.

Файл нужен только затем, чтобы воспроизвести дюп. Чинить его не надо —
новую систему ты пишешь в equipment.py с нуля.
"""

SLOTS = ("head", "body", "right_hand", "left_hand", "ring_1", "ring_2")


class Item:
    def __init__(self, name, slot, power=0, durability=100, level_req=1,
                 two_handed=False):
        self.name = name
        self.slot = slot
        self.power = power
        self.durability = durability
        self.level_req = level_req
        self.two_handed = two_handed

    def __bool__(self):
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


def _drop(items, item):
    """Список без этой вещи.

    Исходный список не трогаем: на него могли остаться ссылки в других
    системах, а нам тут ничего чужого ломать не надо.
    """
    kept = []
    for existing in items:
        if existing is not item:
            kept.append(existing)
    return kept


def equip(player, item):
    if item.slot not in SLOTS:
        return False
    if player.level < item.level_req:
        return False

    inventory = _drop(player.inventory, item)
    old = player.slots[item.slot]
    if old:
        inventory.append(old)
    player.slots[item.slot] = item
    return True


def unequip(player, slot):
    item = player.slots[slot]
    if item is None:
        return False
    player.inventory.append(item)
    player.slots[slot] = None
    return True


def total_power(player):
    power = 0
    for item in player.slots.values():
        if item:
            power += item.power
    return power
