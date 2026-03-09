# Legend of Elmwood Ghetto – Python Game

A **Legend of Zelda–inspired action adventure** built with **Python and Pygame**.
This project is a learning experiment focused on **game logic, sprite systems, world interaction, and event-driven programming** while creating a playable adventure inspired by the Elmwood concept map.

The game uses a **Zelda-style engine architecture** including player combat, enemy AI, tile maps, and UI systems.

---

# Important: Python Version

This project is designed to run using:

**Python 3.12**

Earlier Python versions may behave differently and older versions of the Zelda tutorial code may not run correctly without modifications.

Tested with:

* Python **3.12**
* Pygame **2.6+**

You can check your Python version with:

```
python --version
```

---

# Features

## Overworld Exploration

Explore a top-down overworld inspired by the Elmwood map.

Areas include:

* Courtyard training area
* Old Shophouses district
* Trade Post Road
* Elmwood Projects
* Ancient Cave dungeon
* Open Elmwood streets

The camera follows the player while exploring the map.

---

## Combat System

Real-time sword combat inspired by classic Zelda games.

Features include:

* Sword attack system
* Enemy damage and knockback
* Health system
* Enemy AI movement
* Dungeon boss encounter

Enemy types currently include:

* Lizalfos
* Street bandits
* Cave boss

---

## Player Systems

The player character includes:

* Health system
* Magic energy
* Experience points
* Level progression
* Rupee currency

Leveling increases player survivability and restores health.

---

## Magic System

The player can use a healing ability powered by magic energy.

Magic is limited and must be managed carefully during combat.

---

## Interactive World

The game includes several interactive systems:

NPC Characters
Players can talk to characters to receive hints.

Treasure Chests
Hidden chests contain rupees and relics.

Relic Progression
Three relics must be collected to unlock the final cave.

Trade System
Merchants can restore health for rupees.

---

# Main Quest

The core progression loop:

1. Train in the **Courtyard**
2. Explore Elmwood districts
3. Recover **three relics**
4. Unlock the **Ancient Cave**
5. Defeat the cave boss

The interface displays:

* Player health
* Magic energy
* Rupees
* Relic progress
* Current area
* Quest hint

---

# Controls

| Key                  | Action          |
| -------------------- | --------------- |
| W A S D / Arrow Keys | Move            |
| Space                | Sword attack    |
| E                    | Interact / talk |
| Left CTRL            | Magic heal      |
| Q                    | Change weapon   |
| M                    | Upgrade menu    |
| R                    | Restart game    |

---

# Running the Game

## 1. Install Python 3.12

Download Python:

https://www.python.org/downloads/

Verify installation:

```
python --version
```

You should see:

```
Python 3.12.x
```

---

## 2. Install Dependencies

Install Pygame:

```
pip install pygame
```

---

## 3. Run the Game

Navigate to the **Code** folder:

```
cd Zelda-with-Python-main/Code
```

Run the game:

```
python Main.py
```

The game window should open and begin the adventure.

---

# Technologies Used

* Python 3.12
* Pygame
* Sprite-based game engine
* Tile map world system
* Event-driven input
* Basic enemy AI
* Camera-follow rendering

---

# Future Improvements

Planned upgrades include:

* Custom Elmwood tile graphics
* More enemy types
* Inventory system
* Additional magic abilities
* Dialogue system
* Save / load system
* Sound effects and music
* Larger overworld
* Dungeon puzzles

---

# Author

**Logan Garth Goodwin**

IT and Cybersecurity student focused on building practical projects and learning through hands-on experimentation.

Interests include:

* networking
* cybersecurity
* system architecture
* programming
* game development experiments

LinkedIn
https://www.linkedin.com/in/logan-g-goodwin/

---

If you enjoy the project, feel free to fork the code and experiment with your own ideas.
