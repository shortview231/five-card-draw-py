# ♠️ Five Card Draw Poker (Python Edition)

Welcome to **Five Card Draw**, a poker game built entirely in Python.
It started as my **first ever Python project**, before I knew Git or GitHub — and has grown into a showcase of my **OOP design**, **CLI development**, and **early GUI experiments**.

This project is a **work in progress**: core game logic works, the CLI is playable, and the GUI is underway. The unfinished edges are intentional — they highlight my learning curve, problem-solving process, and commitment to building real projects.

---

## 🎯 Project Overview

Classic **Five Card Draw poker**, designed with:

* Clean object-oriented classes (`Card`, `Deck`, `Player`, `Game`)
* A playable CLI loop
* A GUI prototype using **Tkinter** (with future plans for polish)
* Expandable architecture for AI, betting, and more

---

## ✅ Current Features

### 🧠 Core Logic

* Deal phase: player + CPU receive 5 cards
* Player can **play or fold**
* Discard phase (WIP): GUI allows selection, but logic still forces discard
* Basic CPU behavior

### 🖥️ CLI Version

* Fully playable in terminal
* Card dealing, hand evaluation, and round resets

### 🎴 GUI Progress

* Main Menu screen (Tkinter)
* Poker felt background + Royal Flush placeholder title
* Start Game popup with:

  * Name input
  * Player count (2–4)
* Buttons for **Start Game**, **Rules**, **Exit**
* Modular GUI setup (`gui_units.py`)

---

## 🛠️ Work in Progress

### What works:

* Dealing, folding, discarding (partially), and restarting rounds
* CLI end-to-end play

### What I’m still fixing:

* GUI **discard logic**: need to allow “keep all cards”
* GUI **game screen**: show player + CPU hands properly
* Betting system (planned, not implemented yet)

---

## 📌 Roadmap

* [ ] Fix discard logic (don’t force discard)
* [ ] Expand GUI for full gameplay
* [ ] Add CPU strategy for discards/betting
* [ ] Hand evaluation tie-breaks
* [ ] Visual polish: custom cards, animations, chip sounds
* [ ] Package as `.exe` / `.app` for easy sharing

---

## 🚀 How to Run

### Requirements

* Python 3.10+
* Tkinter (comes standard)
* Pillow (for image scaling/rotation in GUI)

### Run CLI Game

```bash
python3 game.py
```

### Run GUI Prototype

```bash
python3 gui.py
```

---

## 📂 Folder Structure

```
five-card-draw-py/
│── src/
│   ├── card.py        # Card class
│   ├── deck.py        # Deck class
│   ├── player.py      # Player logic
│   ├── game.py        # CLI loop
│   └── gui.py         # GUI prototype
│
│── assets/
│   ├── screenshots/
│   │   ├── start.png
│   │   ├── deal.png
│   │   └── discard.png
│   └── cards/         # Card image assets
│
│── README.md
│── requirements.txt
```

---

## 📸 Screenshots *(to add)*

* Start Screen
* Deal Phase
* Discard Phase (WIP)

---

## ✍️ Author

**Robert Sory Jr. (RJ)**

* Portfolio: [shortview231.github.io](https://shortview231.github.io/)
* GitHub: [@shortview231](https://github.com/shortview231)
* LinkedIn: [Robert Sory Jr.](https://www.linkedin.com/in/robert-sory-1ab752213)
