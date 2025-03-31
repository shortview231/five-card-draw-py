# ♠️ Five Card Draw Poker (Python Edition)

Welcome to **Five Card Draw**, a terminal + GUI-based poker game built entirely in Python from scratch.  
This project is part of a larger portfolio to demonstrate OOP mastery, data handling, and GUI design.

---

## 🎯 Project Overview

This is a fully playable CLI poker game modeled after classic **Five Card Draw** rules, now entering GUI development using **Tkinter**.

Built 100% modular with a focus on:
- Clean object-oriented design
- User-friendly gameplay
- Expandable features (GUI, AI betting logic, multiplayer, etc.)

---

## ✅ Current Features (Completed)

### 🧠 Core Game Logic:
- Full game loop: betting, discarding, drawing, and showdown
- OOP design with `Player`, `Deck`, and `Game` classes
- Basic CPU logic for betting & folding
- Hand evaluation system (`poker.py`) with ranking from High Card to Royal Flush
- Game loops automatically into new rounds

### 🖥️ CLI Game:
- Fully playable in the terminal
- Includes card handling, betting, and win detection

### 🧩 GUI Progress:
- Main Menu screen (Tkinter)
- Green poker felt background
- Royal Flush placeholder title
- Start Game popup with:
  - Name input
  - Player count selection (2–4 players)
- Buttons for "Start Game", "Rules", and "Exit"
- Modular GUI setup with reusable styles in `gui_units.py`

---

## 🛠️ To Do (Next Phases)

### Phase 2: GUI Game Window
- Build the game screen for displaying player hands
- Highlight/select cards to discard (keyboard support)
- Add betting and game flow with GUI buttons
- Handle win logic and reset in GUI

### Phase 3: Visual Polish
- Custom card visuals or font-based rendering
- Card animations (optional)
- Sound effects (chip sounds, win effects, etc.)

### Phase 4: Final Touches
- Responsive resolution scaling
- Final README polish with media
- Optional: Create an executable `.exe` or `.app` for easy sharing

---

## 🚀 How to Run

### Requirements:
- Python 3.10+
- No external libraries (pure Python + Tkinter)

### Run CLI Game:
```bash
python3 game.py
