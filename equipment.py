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


def _count_items(player):
    """Все уникальные вещи у игрока: инвентарь + слоты (без дублей)."""
    seen = set()
    total = 0
    for it in player.inventory:
        if id(it) not in seen:
            seen.add(id(it))
            total += 1
    for it in player.slots.values():
        if it is not None and id(it) not in seen:
            seen.add(id(it))
            total += 1
    return total


def _is_two_handed(item):
    return item is not None and item.two_handed


def equip(player, item):
    """Надеть вещь из инвентаря. True — надели, False — не смогли."""
    before = _count_items(player)

    if item not in player.inventory:
        assert _count_items(player) == before
        return False

    if player.level < item.level_req:
        assert _count_items(player) == before
        return False

    slot = item.slot
    if slot not in SLOTS:
        assert _count_items(player) == before
        return False

    to_return = []

    if item.two_handed:
        returned_ids = set()
        for hand in HANDS:
            occupant = player.slots[hand]
            if occupant is not None and id(occupant) not in returned_ids:
                to_return.append(occupant)
                returned_ids.add(id(occupant))
            player.slots[hand] = None
        player.inventory.remove(item)
        player.slots["right_hand"] = item
        player.slots["left_hand"] = item
    else:
        occupant = player.slots[slot]
        if occupant is not None:
            to_return.append(occupant)
            player.slots[slot] = None
            if _is_two_handed(occupant):
                for hand in HANDS:
                    player.slots[hand] = None
        player.inventory.remove(item)
        player.slots[slot] = item

    for old in to_return:
        player.inventory.append(old)

    assert _count_items(player) == before
    return True


def unequip(player, slot):
    """Снять вещь из слота в инвентарь. True — сняли, False — слот пуст."""
    before = _count_items(player)

    if slot not in SLOTS:
        assert _count_items(player) == before
        return False

    item = player.slots[slot]
    if item is None:
        assert _count_items(player) == before
        return False

    if player.capacity <= len(player.inventory):
        player.inventory.pop()

    if _is_two_handed(item):
        for hand in HANDS:
            player.slots[hand] = None
        player.inventory.append(item)
    else:
        player.slots[slot] = None
        player.inventory.append(item)

    assert _count_items(player) == before
    return True


def total_power(player):
    """Сила всех надетых вещей. Сломанная вещь даёт 0."""
    seen = set()
    power = 0
    for item in player.slots.values():
        if item is None or id(item) in seen:
            continue
        seen.add(id(item))
        if item.durability > 0:
            power += item.power
    return power

sword = Item('sword', 'left_hand', power=100, two_handed=True)
femboy = Player('femboy', 3, inventory=[sword])

equip(femboy, sword)
print(femboy.inventory, femboy.slots)

unequip(femboy, 'left_hand')
print(femboy.inventory, femboy.slots)
