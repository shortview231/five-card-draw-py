import os
import tkinter as tk
from tkinter import messagebox

def load_card_images(root):
    card_images = {}

    card_path = "Assets/Cards take 2/kenney_playing-cards-pack/PNG/Cards (large)"
    
    suits = {
        'C': 'clubs',
        'D': 'diamonds',
        'H': 'hearts',
        'S': 'spades'
    }

    # ✅ Face cards use capital letters because your file is card_clubs_J.png etc.
    ranks = {
        '2': '02', '3': '03', '4': '04', '5': '05', '6': '06', '7': '07',
        '8': '08', '9': '09', '10': '10',
        'J': 'J', 'Q': 'Q', 'K': 'K', 'A': 'A'
    }

    for suit_code, suit_name in suits.items():
        for rank_code, rank_file in ranks.items():
            game_code = rank_code + suit_code  # "AC", "10S", etc.
            file_name = f"card_{suit_name}_{rank_file}.png"
            full_path = os.path.join(card_path, file_name)

            if os.path.exists(full_path):
                card_images[game_code] = tk.PhotoImage(file=full_path, master=root)
            else:
                print(f"[MISSING] {game_code} → {full_path}")

    # Load card back
    back_path = os.path.join(card_path, "card_back.png")
    if os.path.exists(back_path):
        card_images["BACK"] = tk.PhotoImage(file=back_path, master=root)
    else:
        print("[MISSING] BACK card image")

    print(f"[DEBUG] Loaded cards: {list(card_images.keys())}")
    return card_images

# === COLORS ===
POKER_GREEN = "#0b6623"
GOLD = "#FFD700"
WHITE = "#FFFFFF"
DARK_GRAY = "#222222"
LIGHT_GREY = "#CCCCCC"
BUTTON_BG = "#444444"
BUTTON_ACTIVE_BG = "#666666"

# === FONTS & DIMENSIONS ===
ENTRY_FONT = ("Helvetica", 14)
LABEL_FONT = ("Helvetica", 16)
TITLE_FONT = ("Courier New", 32, "bold")
SUBTITLE_FONT = ("Courier New", 24, "bold")
BUTTON_FONT = ("Helvetica", 18, "bold")
CARD_FONT = ("Helvetica", 14)

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720

# === POPUP UTILITY ===
def show_popup(title, message):
    messagebox.showinfo(title, message)
