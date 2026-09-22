from equipment import Item, Player, equip, unequip, total_power


def unique_items(player):
    seen = set()
    for it in player.inventory:
        seen.add(id(it))
    for it in player.slots.values():
        if it is not None:
            seen.add(id(it))
    return seen


def inventory_ids(player):
    return [id(it) for it in player.inventory]


def snapshot(player):
    return {
        "unique": unique_items(player),
        "inventory": inventory_ids(player),
    }


def assert_preserved(before, player):
    after = unique_items(player)
    assert after == before["unique"], (
        f"Инвариант нарушен: было {len(before['unique'])}, стало {len(after)}"
    )


def assert_no_duplicates(player):
    ids = inventory_ids(player)
    assert len(ids) == len(set(ids)), f"Дубликаты в инвентаре: {ids}"


def make_player(level=10):
    return Player("Тестировщик", level=level)


def make_item(name="Вещь", slot="right_hand", power=10, **kw):
    return Item(name, slot=slot, power=power, **kw)


def test_equip_simple():
    player = make_player()
    sword = make_item()
    player.inventory.append(sword)
    before = snapshot(player)

    assert equip(player, sword) is True
    assert_preserved(before, player)
    assert player.slots["right_hand"] is sword
    assert sword not in player.inventory


def test_equip_rejects():
    player = make_player(level=1)
    missing = make_item()
    low_level = make_item(level_req=5)
    unknown = make_item(slot="tail")
    player.inventory.extend([low_level, unknown])
    before = snapshot(player)

    assert equip(player, missing) is False
    assert equip(player, low_level) is False
    assert equip(player, unknown) is False
    assert_preserved(before, player)
    assert player.slots["right_hand"] is None


def test_equip_replaces_occupant():
    player = make_player()
    old = make_item("Старый шлем", slot="head")
    new = make_item("Новый шлем", slot="head")
    player.inventory.extend([old, new])

    equip(player, old)
    before = snapshot(player)

    assert equip(player, new) is True
    assert_preserved(before, player)
    assert player.slots["head"] is new
    assert old in player.inventory
    assert_no_duplicates(player)


def test_two_handed_occupies_both_hands():
    player = make_player()
    sword = make_item(two_handed=True, power=25)
    player.inventory.append(sword)
    before = snapshot(player)

    assert equip(player, sword) is True
    assert_preserved(before, player)
    assert player.slots["right_hand"] is sword
    assert player.slots["left_hand"] is sword
    assert total_power(player) == 25


def test_unequip_two_handed_frees_both_hands():
    player = make_player()
    sword = make_item(two_handed=True)
    player.inventory.append(sword)
    equip(player, sword)
    before = snapshot(player)

    assert unequip(player, "left_hand") is True
    assert_preserved(before, player)
    assert player.slots["right_hand"] is None
    assert player.slots["left_hand"] is None
    assert player.inventory.count(sword) == 1


def test_two_handed_replaces_two_handed():
    player = make_player()
    old = make_item("Старый", two_handed=True)
    new = make_item("Новый", two_handed=True)
    player.inventory.extend([old, new])
    equip(player, old)
    before = snapshot(player)

    assert equip(player, new) is True
    assert_preserved(before, player)
    assert player.slots["right_hand"] is new
    assert player.inventory.count(old) == 1
    assert_no_duplicates(player)


def test_one_handed_replaces_two_handed():
    player = make_player()
    great = make_item(two_handed=True)
    dagger = make_item("Кинжал", slot="left_hand")
    player.inventory.extend([great, dagger])
    equip(player, great)
    before = snapshot(player)

    assert equip(player, dagger) is True
    assert_preserved(before, player)
    assert player.slots["left_hand"] is dagger
    assert player.slots["right_hand"] is None
    assert great in player.inventory


def test_unequip_edge_cases():
    player = make_player()
    helmet = make_item(slot="head")
    player.inventory.append(helmet)
    equip(player, helmet)
    before = snapshot(player)

    assert unequip(player, "head") is True
    assert_preserved(before, player)
    assert unequip(player, "head") is False
    assert unequip(player, "tail") is False
    assert_preserved(before, player)


def test_power_rules():
    player = make_player()
    helmet = make_item("Шлем", slot="head", power=3)
    great = make_item(two_handed=True, power=25)
    broken = make_item("Сломанное", slot="ring_1", power=100)
    broken.durability = 0
    player.inventory.extend([helmet, great, broken])
    equip(player, helmet)
    equip(player, great)
    equip(player, broken)

    assert total_power(player) == 28


def test_invariant_mixed_operations():
    player = make_player()
    items = [
        make_item("Шлем", slot="head"),
        make_item("Меч", slot="right_hand"),
        make_item("Двуручник", two_handed=True),
        make_item("Кольцо", slot="ring_1"),
    ]
    player.inventory.extend(items)
    before = snapshot(player)

    equip(player, items[0])
    equip(player, items[1])
    equip(player, items[2])
    equip(player, items[3])
    equip(player, make_item("Призрак", slot="head"))
    unequip(player, "head")
    unequip(player, "head")
    unequip(player, "right_hand")
    unequip(player, "left_hand")

    assert_preserved(before, player)
    assert_no_duplicates(player)

tests = [v for k, v in sorted(globals().items())
         if k.startswith("test_") and callable(v)]
passed = 0
failed = []

for test in tests:
    try:
        test()
        passed += 1
        print(f"  OK   {test.__name__}")
    except AssertionError as e:
        failed.append((test.__name__, str(e)))
        print(f"  FAIL {test.__name__}: {e}")
    except Exception as e:
        failed.append((test.__name__, repr(e)))
        print(f"  ERR  {test.__name__}: {e!r}")

print(f"\nПройдено: {passed} / {len(tests)}")
if failed:
    for name, msg in failed:
        print(f"  - {name}: {msg}")
    raise SystemExit(1)
