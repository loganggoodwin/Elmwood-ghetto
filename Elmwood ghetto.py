#!/usr/bin/env python3
"""
Elmwood Ghetto (Text RPG) - turn-based fantasy/D&D-style.
- 10 turns per day
- Village hub
- Monsters, loot, XP, leveling
- PvP: Hot-seat local duel OR Arena AI "players"
"""

from __future__ import annotations
import random
import sys
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

# ----------------------------
# Utility
# ----------------------------

def clamp(n: int, lo: int, hi: int) -> int:
    return max(lo, min(hi, n))

def roll(a: int, b: int) -> int:
    return random.randint(a, b)

def pct(p: int) -> bool:
    return roll(1, 100) <= p

def ask(prompt: str, valid: Optional[List[str]] = None) -> str:
    while True:
        s = input(prompt).strip()
        if not valid:
            return s
        if s.lower() in valid:
            return s.lower()
        print(f"Choose one of: {', '.join(valid)}")

def press() -> None:
    input("\n(press Enter) ")

# ----------------------------
# Items / Gear
# ----------------------------

@dataclass
class Item:
    name: str
    kind: str  # "weapon", "armor", "potion", "junk"
    value: int
    dmg_min: int = 0
    dmg_max: int = 0
    armor: int = 0
    heal: int = 0
    rarity: str = "Common"  # Common/Uncommon/Rare/Epic

WEAPONS = [
    Item("Rusty Dagger", "weapon", value=6, dmg_min=1, dmg_max=4, rarity="Common"),
    Item("Peasant Spear", "weapon", value=10, dmg_min=2, dmg_max=6, rarity="Common"),
    Item("Short Sword", "weapon", value=18, dmg_min=3, dmg_max=8, rarity="Uncommon"),
    Item("Reaper's Cleaver", "weapon", value=35, dmg_min=5, dmg_max=10, rarity="Rare"),
    Item("Mythic Oakblade", "weapon", value=80, dmg_min=8, dmg_max=14, rarity="Epic"),
]

ARMORS = [
    Item("Cloth Tunic", "armor", value=6, armor=1, rarity="Common"),
    Item("Leather Jerkin", "armor", value=14, armor=2, rarity="Uncommon"),
    Item("Chain Shirt", "armor", value=30, armor=3, rarity="Rare"),
    Item("Knight's Cuirass", "armor", value=70, armor=5, rarity="Epic"),
]

POTIONS = [
    Item("Small Healing Potion", "potion", value=10, heal=12, rarity="Common"),
    Item("Healing Potion", "potion", value=22, heal=25, rarity="Uncommon"),
    Item("Greater Healing Potion", "potion", value=45, heal=45, rarity="Rare"),
]

JUNK = [
    Item("Rat Tail", "junk", value=2, rarity="Common"),
    Item("Goblin Tooth", "junk", value=3, rarity="Common"),
    Item("Silver Locket", "junk", value=15, rarity="Uncommon"),
    Item("Ancient Coin", "junk", value=25, rarity="Rare"),
]

def weighted_choice(choices: List[Tuple[object, int]]):
    total = sum(w for _, w in choices)
    r = random.randint(1, total)
    upto = 0
    for obj, w in choices:
        upto += w
        if upto >= r:
            return obj
    return choices[-1][0]

def random_loot() -> Optional[Item]:
    """
    Drops are intentionally modest to keep progression steady.
    """
    # chance for any loot
    if not pct(65):
        return None

    # rarity weights
    rarity = weighted_choice([
        ("Common", 70),
        ("Uncommon", 20),
        ("Rare", 9),
        ("Epic", 1),
    ])

    pool: List[Item] = []
    pool += [i for i in WEAPONS if i.rarity == rarity]
    pool += [i for i in ARMORS if i.rarity == rarity]
    pool += [i for i in POTIONS if i.rarity == rarity]
    pool += [i for i in JUNK if i.rarity == rarity]

    if not pool:
        # fallback: common junk
        pool = [i for i in JUNK if i.rarity == "Common"]

    return random.choice(pool)

# ----------------------------
# Creatures / Player
# ----------------------------

@dataclass
class Stats:
    max_hp: int
    hp: int
    atk: int       # to-hit bonus / attack skill
    defense: int   # damage mitigation baseline (not armor item)
    crit: int      # % crit chance

@dataclass
class Character:
    name: str
    level: int = 1
    xp: int = 0
    gold: int = 15
    stats: Stats = field(default_factory=lambda: Stats(max_hp=30, hp=30, atk=2, defense=1, crit=5))
    weapon: Item = field(default_factory=lambda: WEAPONS[0])
    armor: Item = field(default_factory=lambda: ARMORS[0])
    inventory: List[Item] = field(default_factory=list)
    kills: int = 0
    days_survived: int = 1

    def armor_value(self) -> int:
        return self.stats.defense + (self.armor.armor if self.armor else 0)

    def damage_roll(self) -> int:
        w = self.weapon
        base = roll(w.dmg_min, w.dmg_max) + self.stats.atk
        if pct(self.stats.crit):
            base += roll(2, 6)
            print("  ⚔️  Critical strike!")
        return base

    def xp_to_next(self) -> int:
        # fast early leveling, slows later
        return 25 + (self.level - 1) * 20

    def add_xp(self, amount: int) -> None:
        self.xp += amount
        while self.xp >= self.xp_to_next():
            self.xp -= self.xp_to_next()
            self.level_up()

    def level_up(self) -> None:
        self.level += 1
        hp_gain = roll(6, 10)
        atk_gain = 1 if pct(70) else 0
        def_gain = 1 if pct(55) else 0
        crit_gain = 1 if pct(35) else 0
        self.stats.max_hp += hp_gain
        self.stats.hp = self.stats.max_hp
        self.stats.atk += atk_gain
        self.stats.defense += def_gain
        self.stats.crit = clamp(self.stats.crit + crit_gain, 1, 25)
        print(f"\n✨ LEVEL UP! You are now level {self.level}.")
        print(f"  +{hp_gain} Max HP, +{atk_gain} ATK, +{def_gain} DEF, +{crit_gain} CRIT")
        press()

    def heal_full(self) -> None:
        self.stats.hp = self.stats.max_hp

@dataclass
class Enemy:
    name: str
    level: int
    stats: Stats
    gold_drop: Tuple[int, int]
    xp_drop: Tuple[int, int]

    def armor_value(self) -> int:
        return self.stats.defense

    def damage_roll(self) -> int:
        base = roll(1, 6) + self.stats.atk
        if pct(self.stats.crit):
            base += roll(1, 6)
            # enemy crit message kept small to avoid spam
        return base

MONSTERS = [
    ("Sewer Rat", 1),
    ("Bog Goblin", 1),
    ("Warg Pup", 2),
    ("Grave Skeleton", 2),
    ("Bandit Raider", 3),
    ("Ogre Brute", 4),
    ("Night Hag", 5),
    ("Forest Troll", 6),
]

def spawn_monster(player_level: int, day: int) -> Enemy:
    # scale enemy level around player + day drift
    base = player_level + (day // 3)
    lvl = clamp(base + roll(-1, 1), 1, 12)

    # choose a monster name somewhat appropriate
    name, min_lvl = random.choice(MONSTERS)
    if lvl < min_lvl:
        lvl = min_lvl

    max_hp = 18 + lvl * 6 + roll(-2, 6)
    atk = 1 + (lvl // 2)
    defense = (lvl // 3)
    crit = clamp(3 + lvl // 4, 3, 15)

    e = Enemy(
        name=f"{name} (Lv {lvl})",
        level=lvl,
        stats=Stats(max_hp=max_hp, hp=max_hp, atk=atk, defense=defense, crit=crit),
        gold_drop=(3 + lvl, 8 + lvl * 2),
        xp_drop=(10 + lvl * 2, 18 + lvl * 3),
    )
    return e

def spawn_ai_player(player: Character) -> Enemy:
    # AI "player" in the arena
    lvl = clamp(player.level + roll(-1, 2), 1, 20)
    max_hp = 26 + lvl * 7 + roll(-4, 8)
    atk = 2 + (lvl // 2)
    defense = 1 + (lvl // 3)
    crit = clamp(5 + lvl // 3, 5, 20)
    alias = random.choice(["Marauder", "Duelist", "Sellsword", "Outlaw Knight", "Rogue Captain"])
    name = f"{alias} (Lv {lvl})"
    return Enemy(
        name=name,
        level=lvl,
        stats=Stats(max_hp=max_hp, hp=max_hp, atk=atk, defense=defense, crit=crit),
        gold_drop=(10 + lvl, 20 + lvl * 3),
        xp_drop=(18 + lvl * 3, 30 + lvl * 4),
    )

# ----------------------------
# Combat
# ----------------------------

def hit_chance(attacker_atk: int, defender_level: int) -> int:
    # simple: base 70% + atk bonus - level drift
    return clamp(70 + attacker_atk * 3 - defender_level * 2, 35, 90)

def apply_damage(raw: int, armor: int) -> int:
    # armor reduces damage but never below 1
    reduced = raw - roll(0, armor)
    return max(1, reduced)

def combat(player: Character, enemy: Enemy) -> bool:
    """
    Returns True if player wins, False if player loses (dies).
    """
    print(f"\n⚔️  Encounter: {enemy.name}")
    while player.stats.hp > 0 and enemy.stats.hp > 0:
        print(f"\n{player.name}: {player.stats.hp}/{player.stats.max_hp} HP   "
              f"||   {enemy.name}: {enemy.stats.hp}/{enemy.stats.max_hp} HP")
        print("Actions: [a]ttack  [p]otion  [r]un")
        choice = ask("> ", valid=["a", "p", "r"])

        if choice == "p":
            potions = [i for i in player.inventory if i.kind == "potion"]
            if not potions:
                print("You have no potions.")
            else:
                print("Potions:")
                for idx, it in enumerate(potions, 1):
                    print(f"  {idx}. {it.name} (+{it.heal} HP)")
                s = ask("Use which potion #? (or 'b' to back) ").lower()
                if s == "b":
                    continue
                if not s.isdigit() or not (1 <= int(s) <= len(potions)):
                    print("Invalid choice.")
                else:
                    it = potions[int(s) - 1]
                    player.stats.hp = clamp(player.stats.hp + it.heal, 0, player.stats.max_hp)
                    player.inventory.remove(it)
                    print(f"You drink {it.name}.")
        elif choice == "r":
            if pct(45):
                print("🏃 You escaped!")
                return True  # treat escape as "survived" (no loot/xp)
            print("You failed to escape!")
        else:  # attack
            chance = hit_chance(player.stats.atk, enemy.level)
            if pct(chance):
                raw = player.damage_roll()
                dmg = apply_damage(raw, enemy.armor_value())
                enemy.stats.hp -= dmg
                print(f"You hit for {dmg} damage.")
            else:
                print("You miss.")

        if enemy.stats.hp <= 0:
            break

        # enemy turn
        chance_e = hit_chance(enemy.stats.atk, player.level)
        if pct(chance_e):
            raw = enemy.damage_roll()
            dmg = apply_damage(raw, player.armor_value())
            player.stats.hp -= dmg
            print(f"The enemy hits you for {dmg} damage.")
        else:
            print("The enemy misses.")

    if player.stats.hp <= 0:
        print("\n💀 You were defeated.")
        return False

    # rewards
    g = roll(*enemy.gold_drop)
    xp = roll(*enemy.xp_drop)
    player.gold += g
    player.kills += 1
    print(f"\n🏆 Victory! You gain {xp} XP and {g} gold.")
    player.add_xp(xp)

    loot = random_loot()
    if loot:
        print(f"🎒 Loot found: {loot.rarity} {loot.name}")
        player.inventory.append(loot)
    else:
        print("No loot this time.")

    press()
    return True

# ----------------------------
# Town / Shop / Inventory
# ----------------------------

def show_character(player: Character) -> None:
    print(f"\n=== {player.name} ===")
    print(f"Level {player.level}  XP {player.xp}/{player.xp_to_next()}  Gold {player.gold}")
    print(f"HP {player.stats.hp}/{player.stats.max_hp}  ATK {player.stats.atk}  DEF {player.stats.defense}  CRIT {player.stats.crit}%")
    print(f"Weapon: {player.weapon.name} ({player.weapon.dmg_min}-{player.weapon.dmg_max})")
    print(f"Armor : {player.armor.name} (+{player.armor.armor} armor)")
    print(f"Kills: {player.kills}  Days survived: {player.days_survived}")

def list_inventory(player: Character) -> None:
    print("\n=== Inventory ===")
    if not player.inventory:
        print("(empty)")
        return
    for idx, it in enumerate(player.inventory, 1):
        extra = ""
        if it.kind == "weapon":
            extra = f" dmg {it.dmg_min}-{it.dmg_max}"
        elif it.kind == "armor":
            extra = f" armor +{it.armor}"
        elif it.kind == "potion":
            extra = f" heal +{it.heal}"
        print(f"{idx}. [{it.rarity}] {it.name} ({it.kind}) value {it.value}{extra}")

def equip_menu(player: Character) -> None:
    while True:
        list_inventory(player)
        print("\nEquip: [w]eapon  [a]rmor  [b]ack")
        c = ask("> ", valid=["w", "a", "b"])
        if c == "b":
            return
        if c == "w":
            weapons = [it for it in player.inventory if it.kind == "weapon"]
            if not weapons:
                print("No weapons to equip.")
                continue
            for i, it in enumerate(weapons, 1):
                print(f"{i}. {it.name} ({it.dmg_min}-{it.dmg_max})")
            s = ask("Equip which weapon #? ").strip()
            if s.isdigit() and 1 <= int(s) <= len(weapons):
                new = weapons[int(s) - 1]
                player.inventory.remove(new)
                player.inventory.append(player.weapon)
                player.weapon = new
                print(f"Equipped {new.name}.")
            else:
                print("Invalid.")
        else:
            armors = [it for it in player.inventory if it.kind == "armor"]
            if not armors:
                print("No armor to equip.")
                continue
            for i, it in enumerate(armors, 1):
                print(f"{i}. {it.name} (+{it.armor})")
            s = ask("Equip which armor #? ").strip()
            if s.isdigit() and 1 <= int(s) <= len(armors):
                new = armors[int(s) - 1]
                player.inventory.remove(new)
                player.inventory.append(player.armor)
                player.armor = new
                print(f"Equipped {new.name}.")
            else:
                print("Invalid.")

def sell_menu(player: Character) -> None:
    while True:
        sellables = [it for it in player.inventory if it.kind in ("junk", "weapon", "armor")]
        if not sellables:
            print("\nYou have nothing to sell.")
            press()
            return
        print("\n=== Sell Items ===")
        for idx, it in enumerate(sellables, 1):
            print(f"{idx}. [{it.rarity}] {it.name} ({it.kind}) value {it.value}")
        print("Type item # to sell, or 'b' to back.")
        s = ask("> ").lower()
        if s == "b":
            return
        if not s.isdigit() or not (1 <= int(s) <= len(sellables)):
            print("Invalid.")
            continue
        it = sellables[int(s) - 1]
        player.inventory.remove(it)
        player.gold += it.value
        print(f"Sold {it.name} for {it.value} gold.")

def buy_menu(player: Character) -> None:
    # rotating daily shop stock would be cool; for now, static but simple
    stock = []
    stock += random.sample(POTIONS, k=min(2, len(POTIONS)))
    stock += random.sample(WEAPONS, k=2)
    stock += random.sample(ARMORS, k=1)

    while True:
        print(f"\n=== Market Stall (Gold: {player.gold}) ===")
        for idx, it in enumerate(stock, 1):
            extra = ""
            if it.kind == "weapon":
                extra = f" dmg {it.dmg_min}-{it.dmg_max}"
            elif it.kind == "armor":
                extra = f" armor +{it.armor}"
            elif it.kind == "potion":
                extra = f" heal +{it.heal}"
            print(f"{idx}. [{it.rarity}] {it.name} ({it.kind}) - {it.value}g{extra}")
        print("Buy item #, or 'b' back.")
        s = ask("> ").lower()
        if s == "b":
            return
        if not s.isdigit() or not (1 <= int(s) <= len(stock)):
            print("Invalid.")
            continue
        it = stock[int(s) - 1]
        if player.gold < it.value:
            print("Not enough gold.")
            continue
        player.gold -= it.value
        player.inventory.append(it)
        print(f"Bought {it.name}.")

# ----------------------------
# PvP (local hot-seat)
# ----------------------------

def make_player_for_duel(label: str) -> Character:
    name = ask(f"Enter name for {label}: ").strip() or label
    c = Character(name=name)
    # a little boost so duels are fun
    c.weapon = random.choice(WEAPONS[:3])
    c.armor = random.choice(ARMORS[:2])
    c.stats.max_hp = 34
    c.stats.hp = 34
    c.stats.atk = 3
    c.stats.defense = 2
    c.stats.crit = 6
    c.gold = 0
    return c

def duel(p1: Character, p2: Character) -> Character:
    print(f"\n🥊 Duel: {p1.name} vs {p2.name}")
    attacker, defender = p1, p2
    while p1.stats.hp > 0 and p2.stats.hp > 0:
        print(f"\n{p1.name}: {p1.stats.hp}/{p1.stats.max_hp} HP  ||  {p2.name}: {p2.stats.hp}/{p2.stats.max_hp} HP")
        print(f"{attacker.name}'s turn: [a]ttack  [p]otion  (or just attack)")
        c = ask("> ", valid=["a", "p"])
        if c == "p":
            pots = [i for i in attacker.inventory if i.kind == "potion"]
            if not pots:
                print("No potions.")
            else:
                it = pots[0]
                attacker.inventory.remove(it)
                attacker.stats.hp = clamp(attacker.stats.hp + it.heal, 0, attacker.stats.max_hp)
                print(f"{attacker.name} drinks {it.name}.")
        else:
            chance = hit_chance(attacker.stats.atk, defender.level)
            if pct(chance):
                raw = attacker.damage_roll()
                dmg = apply_damage(raw, defender.armor_value())
                defender.stats.hp -= dmg
                print(f"{attacker.name} hits for {dmg} damage.")
            else:
                print(f"{attacker.name} misses.")
        attacker, defender = defender, attacker

    winner = p1 if p1.stats.hp > 0 else p2
    print(f"\n🏅 {winner.name} wins the duel!")
    return winner

# ----------------------------
# Game Loop
# ----------------------------

def new_day(player: Character) -> None:
    player.days_survived += 1
    player.heal_full()
    # small daily stipend to keep things moving
    stipend = 3 + (player.level // 2)
    player.gold += stipend
    print(f"\n🌅 Day {player.days_survived} begins. You rest to full HP and receive {stipend} gold for odd jobs around Elmwood.")
    press()

def village_menu(player: Character, day: int, turns_left: int) -> str:
    print("\n==============================")
    print(f"🏘️  Elmwood Ghetto - Village Day {day} | Turns left: {turns_left}/10")
    print("==============================")
    show_character(player)
    print("\nChoose:")
    print("  1) Hunt monsters (1 turn)")
    print("  2) Arena (fight AI players) (1 turn)")
    print("  3) Market (buy) (1 turn)")
    print("  4) Sell items (1 turn)")
    print("  5) Inventory / Equip (free)")
    print("  6) Local PvP duel (free)")
    print("  7) End day early")
    print("  8) Quit")

    return ask("> ").strip()

def main() -> None:
    random.seed()

    print("=== Elmwood Ghetto (Text RPG) ===")
    print("A grimy little medieval village where peasants dream of glory.\n")

    name = ask("Name your character: ").strip()
    if not name:
        name = "Nameless Peasant"

    player = Character(name=name)
    # starter potion
    player.inventory.append(POTIONS[0])

    day = 1
    turns = 10

    while True:
        if turns <= 0:
            new_day(player)
            day += 1
            turns = 10

        choice = village_menu(player, day, turns)

        if choice == "1":
            turns -= 1
            enemy = spawn_monster(player.level, day)
            ok = combat(player, enemy)
            if not ok:
                print("\nGame Over. Your legend ends in the mud.")
                return

        elif choice == "2":
            turns -= 1
            enemy = spawn_ai_player(player)
            ok = combat(player, enemy)
            if not ok:
                print("\nGame Over. The arena claims another soul.")
                return

        elif choice == "3":
            turns -= 1
            buy_menu(player)

        elif choice == "4":
            turns -= 1
            sell_menu(player)

        elif choice == "5":
            list_inventory(player)
            equip_menu(player)

        elif choice == "6":
            print("\nLocal PvP Duel (hot-seat). This does not cost turns.")
            p2 = make_player_for_duel("Challenger")
            # give each duelist one small potion to keep it spicy
            player.inventory.append(POTIONS[0])
            p2.inventory.append(POTIONS[0])
            # copy player to avoid messing campaign stats/HP too hard
            p1 = Character(
                name=player.name,
                level=player.level,
                xp=player.xp,
                gold=player.gold,
                stats=Stats(player.stats.max_hp, player.stats.max_hp, player.stats.atk, player.stats.defense, player.stats.crit),
                weapon=player.weapon,
                armor=player.armor,
                inventory=[i for i in player.inventory if i.kind == "potion"][:1],
            )
            winner = duel(p1, p2)
            if winner.name == p1.name:
                reward = 12 + player.level * 2
                print(f"{player.name} earns {reward} XP for the win.")
                player.add_xp(reward)
            else:
                print(f"{player.name} learns a painful lesson. No XP gained.")
            press()

        elif choice == "7":
            turns = 0

        elif choice == "8":
            print("Goodbye.")
            return

        else:
            print("Invalid choice.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nExiting...")
        sys.exit(0)