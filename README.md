# ♠️ Five Card Draw Poker (Python Edition)

**Five Card Draw** started as my first Python project, before I knew Git or GitHub. It has grown into a small playable desktop game that preserves the original learning project while adding a finished Windows-classic edition.

## Windows Classic Edition

The revival build lives in `five_card_drae.py/windows_classic.py` and is designed to resemble a late-1990s/early-2000s Windows card game.

### Features

- Full five-card draw round loop
- Opening betting round
- Player fold/bet actions
- Select and replace 0–3 cards
- CPU discard strategy
- Final betting round
- Full showdown and tie handling
- Persistent chips between rounds
- Correct poker hand evaluation and tie breakers
- Classic gray Windows controls, blue title bar, menus, status bar, and green card table
- No external card-image assets required for the classic edition

### Run

```bash
cd five_card_drae.py
python3 windows_classic.py
```

The classic build uses only Python's standard-library Tkinter modules.

## Original Project

The repository intentionally keeps the earlier CLI and experimental image-based GUI because they show the project's development history.

### Core modules

- `deck.py` - 52-card deck and dealing
- `player.py` - player state, chips, folding and discarding
- `poker.py` - poker hand classification and full tie-breaking scores
- `game.py` - original reusable game engine
- `fcd_GUI/` - original Tkinter/table-image experiment
- `windows_classic.py` - finished classic desktop edition
- `test_poker.py` - regression tests for poker hand evaluation

## Tests

From `five_card_drae.py`:

```bash
python3 -m unittest test_poker.py
```

The regression suite covers all ten standard poker hand categories, ace-low straights, pair kicker tie breakers, and two-pair comparisons.

## Hand Ranking

1. Royal Flush
2. Straight Flush
3. Four of a Kind
4. Full House
5. Flush
6. Straight
7. Three of a Kind
8. Two Pair
9. Pair
10. High Card

## Original GUI Prototype

The earlier `fcd_GUI` implementation remains available for continued experimentation with card images and a four-seat felt-table layout. It is preserved rather than overwritten by the Windows Classic edition.

## Author

**Robert Sory Jr. (RJ)**

- Portfolio: https://shortview231.github.io/
- GitHub: @shortview231
