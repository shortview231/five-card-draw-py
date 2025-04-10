import os
import tkinter as tk
from PIL import Image, ImageTk
from gui_units import (
    POKER_GREEN, TITLE_FONT, BUTTON_FONT, WINDOW_WIDTH, WINDOW_HEIGHT, load_card_images
)

card_images = {}

def get_scaled_rotated_card(code, root, angle=0, scale=2.0):
    code = code.upper()

    card_path = "Assets/Cards take 2/kenney_playing-cards-pack/PNG/Cards (large)"
    suits = {'C': 'clubs', 'D': 'diamonds', 'H': 'hearts', 'S': 'spades'}
    ranks = {
        '2': '02', '3': '03', '4': '04', '5': '05', '6': '06', '7': '07',
        '8': '08', '9': '09', '10': '10',
        'J': 'J', 'Q': 'Q', 'K': 'K', 'A': 'A'
    }

    if code == "BACK":
        full_path = os.path.join(card_path, "card_back.png")
    else:
        rank = code[:-1].upper()
        suit = code[-1].upper()

        if suit not in suits or rank not in ranks:
            print(f"[ERROR] Invalid code: {code}")
            return None

        file_name = f"card_{suits[suit]}_{ranks[rank]}.png"
        full_path = os.path.join(card_path, file_name)

    if not os.path.exists(full_path):
        print(f"[ERROR] Missing file for card: {code} → {full_path}")
        return None

    pil_image = Image.open(full_path)
    w, h = pil_image.size
    pil_image = pil_image.resize((int(w * scale), int(h * scale)), Image.LANCZOS)

    if angle:
        pil_image = pil_image.rotate(angle, expand=True)

    return ImageTk.PhotoImage(pil_image, master=root)

def launch_game_screen(player_name, player_count):
    global card_images
    game_screen = tk.Toplevel()
    game_screen.title("Five Card Draw")
    game_screen.configure(bg=POKER_GREEN)
    game_screen.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
    game_screen.grab_set()

    card_images = load_card_images(game_screen)

    # === CPU 1 (Top Center) ===
    cpu1_frame = tk.Frame(game_screen, bg=POKER_GREEN)
    cpu1_frame.pack(pady=10)
    tk.Label(cpu1_frame, text="CPU 1", font=BUTTON_FONT, fg="white", bg=POKER_GREEN).pack()
    cpu1_cards_frame = tk.Frame(cpu1_frame, bg=POKER_GREEN)
    cpu1_cards_frame.pack()
    for i in range(5):
        card = get_scaled_rotated_card("BACK", game_screen, scale=1.2)
        if card:
            tk.Label(cpu1_cards_frame, image=card, bg=POKER_GREEN).pack(side="left", padx=5)
            card_images[f"CPU1_{i}"] = card

    # === CPU 2 (Left Vertical with Name on Left) ===
    cpu2_frame = tk.Frame(game_screen, bg=POKER_GREEN)
    cpu2_frame.place(relx=0.02, rely=0.25, anchor="nw")

    tk.Label(cpu2_frame, text="C\nP\nU\n2", font=BUTTON_FONT, fg="white", bg=POKER_GREEN, justify="center").pack(side="left", padx=(0, 10))

    cpu2_cards_frame = tk.Frame(cpu2_frame, bg=POKER_GREEN)
    cpu2_cards_frame.pack(side="left")
    for i in range(5):
        card = get_scaled_rotated_card("BACK", game_screen, angle=90, scale=1.2)
        if card:
            tk.Label(cpu2_cards_frame, image=card, bg=POKER_GREEN).pack(pady=2)
            card_images[f"CPU2_{i}"] = card

    # === CPU 3 (Right Vertical with Name on Right) ===
    cpu3_frame = tk.Frame(game_screen, bg=POKER_GREEN)
    cpu3_frame.place(relx=0.98, rely=0.25, anchor="ne")

    cpu3_cards_frame = tk.Frame(cpu3_frame, bg=POKER_GREEN)
    cpu3_cards_frame.pack(side="left")
    for i in range(5):
        card = get_scaled_rotated_card("BACK", game_screen, angle=270, scale=1.2)
        if card:
            tk.Label(cpu3_cards_frame, image=card, bg=POKER_GREEN).pack(pady=2)
            card_images[f"CPU3_{i}"] = card

    tk.Label(cpu3_frame, text="C\nP\nU\n3", font=BUTTON_FONT, fg="white", bg=POKER_GREEN, justify="center").pack(side="left", padx=(10, 0))

    # === PLAYER (Bottom Center, Full Size, All 5 Cards) ===
    player_frame = tk.Frame(game_screen, bg=POKER_GREEN)
    player_frame.place(relx=0.5, rely=0.92, anchor="center")
    player_cards_frame = tk.Frame(player_frame, bg=POKER_GREEN)
    player_cards_frame.pack()

    test_hand = ["7H", "10S", "KD", "AC", "9C"]
    for i, code in enumerate(test_hand):
        card = get_scaled_rotated_card(code, game_screen, scale=2.0)
        if card:
            tk.Label(player_cards_frame, image=card, bg=POKER_GREEN).pack(side="left", padx=5)
            card_images[f"PLAYER_{i}"] = card
        else:
            print(f"[ERROR] Couldn't load card for: {code}")

    tk.Label(player_frame, text=player_name, font=BUTTON_FONT, fg="white", bg=POKER_GREEN).pack(pady=(10, 0))

    # === Welcome Message ===
    welcome_label = tk.Label(
        game_screen,
        text=f"Welcome {player_name}! Total Players: {player_count}",
        font=TITLE_FONT,
        fg="white",
        bg=POKER_GREEN
    )
    welcome_label.pack(pady=30)

    def fade_welcome():
        welcome_label.destroy()

    game_screen.after(2000, fade_welcome)
