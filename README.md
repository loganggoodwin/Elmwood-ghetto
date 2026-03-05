# Elmwood Ghetto

*A Turn-Based Text RPG for Python*

## Overview

**Elmwood Ghetto** is a text-based, turn-based fantasy RPG inspired by classic tabletop games and early computer RPGs. The game takes place in a gritty medieval peasant village where players fight monsters, gain experience, collect loot, and survive day-to-day life in a harsh fantasy world.

Players create a character, battle enemies, visit the village market, and grow stronger over time. Each in-game day provides **10 turns**, requiring players to carefully choose how to spend their time.

This project is designed to be **simple, expandable, and beginner-friendly**, making it a good starting point for experimenting with Python game development.

---

## Features

### Character Creation

* Choose your character name
* Begin as a peasant adventurer
* Gain experience and level up

### Turn-Based Gameplay

* Each in-game day contains **10 turns**
* Actions consume turns (combat, market visits, etc.)
* Rest and recover at the start of each new day

### Combat System

* Fight monsters such as:

  * Sewer Rats
  * Goblins
  * Skeletons
  * Bandits
  * Trolls
* Critical hits
* Armor damage reduction
* Escape mechanics

### Experience & Leveling

* Earn **XP** for defeating enemies
* Level up to increase:

  * Health
  * Attack
  * Defense
  * Critical chance

### Loot System

Enemies can drop:

* Weapons
* Armor
* Potions
* Random treasure items

Loot rarity levels include:

* Common
* Uncommon
* Rare
* Epic

### Village Hub

Players can visit the village between battles to:

* Fight monsters
* Enter the arena
* Buy items from the market
* Sell loot
* Equip gear
* Duel other players locally

### PvP Duels

Local **hot-seat PvP mode** allows two players to duel using turn-based combat.

---

## Requirements

* Python **3.9 or newer**
* No external libraries required

The game runs entirely using Python’s standard library.

---

## Installation

Clone the repository:

```bash
git clone https://github.com/loganggoodwin/Elmwood-ghetto.git
```

Navigate to the folder:

```bash
cd Elmwood-ghetto
```

Run the game:

```bash
python elmwood_ghetto.py
```

---

## Example Gameplay

```
=== Elmwood Ghetto ===
A grimy little medieval village where peasants dream of glory.

Name your character: Rowan

Village Day 1 | Turns left: 10

1) Hunt monsters
2) Arena
3) Market
4) Sell items
5) Inventory
6) PvP duel
7) End day
8) Quit
```

---

## Project Structure

```
Elmwood-ghetto
│
├── elmwood_ghetto.py
├── README.md
└── LICENSE
```

Future versions may include:

```
Elmwood-ghetto
│
├── game/
│   ├── combat.py
│   ├── enemies.py
│   ├── items.py
│   ├── world.py
│   └── player.py
│
├── elmwood_ghetto.py
└── README.md
```

---

## Planned Features

Future improvements may include:

* Character classes (Warrior, Rogue, Mage)
* Magic spells and abilities
* Quests and storylines
* Save/load game system
* Expanded world map
* Multiplayer combat system
* Procedural dungeon generation
* Boss monsters
* Reputation system for villages

---

## Contributing

Contributions are welcome.

You can help by:

* Adding monsters
* Expanding loot tables
* Improving combat mechanics
* Creating quests
* Improving balance

To contribute:

1. Fork the repository
2. Create a new branch
3. Submit a pull request

---

## License

This project is open source and released under the **MIT License**.

---

## Author

Created by **Logan Garth Goodwin**

GitHub:
https://github.com/loganggoodwin

Repository:
https://github.com/loganggoodwin/Elmwood-ghetto

---

## Final Notes

This project is meant to be **fun, expandable, and easy to modify**. The code is intentionally straightforward so developers can experiment with mechanics, combat systems, and game design ideas.

Welcome to **Elmwood Ghetto** — where peasants fight monsters and legends begin.
