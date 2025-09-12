# 1. Imports and Globals
import sys
import os
import random
import tkinter as tk
from PIL import Image, ImageTk

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from gui_units import (
    POKER_GREEN, TITLE_FONT, BUTTON_FONT, WINDOW_WIDTH, WINDOW_HEIGHT, load_card_images
)
from game import Game
from poker import evaluate_hand

# Global Variables
game_screen = None
ard_images = {}
game = None
bet_button = None
fold_button = None
discard_button = None
player_labels = []
player_card_labels = {
    "CPU1": [],
    "CPU2": [],
    "CPU3": [],
    "PLAYER": []
}
current_turn_index = 0
turns_taken = 0
phase_label = None
player_cards_frame = None
selected_indices = set()
discard_used = False
# 2. Card Image Utility
def get_scaled_rotated_card(code, root, angle=0, scale=2.0):
    code = code.upper()
    card_path = "Assets/Cards take 2/kenney_playing-cards-pack/PNG/Cards (large)"
    suits = {'C': 'clubs', 'D': 'diamonds', 'H': 'hearts', 'S': 'spades'}
    ranks = {
        '2': '02', '3': '03', '4': '04', '5': '05', '6': '06', '7': '07',
        '8': '08', '9': '09', '10': '10', 'J': 'J', 'Q': 'Q', 'K': 'K', 'A': 'A'
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
# 3. Card Click + Discard Logic
def handle_card_click(event, idx):
    global selected_indices, discard_used
    if discard_used:
        return

    label = player_card_labels["PLAYER"][idx]
    if idx in selected_indices:
        selected_indices.remove(idx)
        label.config(highlightthickness=0, highlightbackground=POKER_GREEN)
        label.pack_configure(pady=0)
    elif len(selected_indices) < 3:
        selected_indices.add(idx)
        label.config(highlightbackground="red", highlightcolor="red", highlightthickness=2)
        label.pack_configure(pady=10)

def discard_selected_cards():
    global selected_indices, discard_used
    if discard_used or not selected_indices:
        return
    discard_used = True

    to_discard = sorted(selected_indices)
    selected_indices.clear()

    for i in reversed(to_discard):
        player_card_labels["PLAYER"][i].destroy()
        del player_card_labels["PLAYER"][i]
        del game.players[0].hand[i]

    new_cards = game.deck.deal(len(to_discard))
    game.players[0].receive_cards(new_cards)

    for i, card_str in zip(to_discard, new_cards):
        rank, _, suit = card_str.partition(" of ")
        code = rank + suit[0].upper()
        card_img = get_scaled_rotated_card(code, player_card_labels["PLAYER"][0].master, scale=2.0)
        if card_img:
            label = tk.Label(player_cards_frame, image=card_img, bg=POKER_GREEN, bd=0, relief="flat")
            label.pack(side="left", padx=5)
            label.bind("<Button-1>", lambda e, idx=i: handle_card_click(e, idx))
            player_card_labels["PLAYER"].insert(i, label)
            card_images[f"PLAYER_{i}"] = card_img

    for lbl in player_card_labels["PLAYER"]:
        lbl.unbind("<Button-1>")

    discard_button.place_forget()
# 4. Launch Game Screen Setup
def launch_game_screen(player_name, player_count):
    global card_images, game, bet_button, fold_button, discard_button
    global current_turn_index, turns_taken, player_labels, phase_label
    global player_cards_frame, selected_indices, discard_used

    selected_indices = set()
    discard_used = False

    game_screen = tk.Toplevel()
    game_screen.title("Five Card Draw")
    game_screen.configure(bg=POKER_GREEN)
    game_screen.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
    game_screen.grab_set()

    game = Game(total_players=player_count, player_name=player_name)
    game.start_round()
    card_images = load_card_images(game_screen)

    player_labels.clear()
    for v in player_card_labels.values():
        v.clear()

    # === CPU 1 ===
    cpu1_frame = tk.Frame(game_screen, bg=POKER_GREEN)
    cpu1_frame.pack(pady=10)
    cpu1_label = tk.Label(cpu1_frame, text=game.players[1].name, font=BUTTON_FONT, fg="white", bg=POKER_GREEN)
    cpu1_label.pack()
    player_labels.append(cpu1_label)

    cpu1_cards_frame = tk.Frame(cpu1_frame, bg=POKER_GREEN)
    cpu1_cards_frame.pack()
    for i in range(5):
        card = get_scaled_rotated_card("BACK", game_screen, scale=1.2)
        label = tk.Label(cpu1_cards_frame, image=card, bg=POKER_GREEN)
        label.pack(side="left", padx=5)
        player_card_labels["CPU1"].append(label)
        card_images[f"CPU1_{i}"] = card

    # === CPU 2 ===
    cpu2_frame = tk.Frame(game_screen, bg=POKER_GREEN)
    cpu2_frame.place(relx=0.02, rely=0.25, anchor="nw")
    cpu2_label = tk.Label(cpu2_frame, text="C\nP\nU\n2", font=BUTTON_FONT, fg="white", bg=POKER_GREEN, justify="center")
    cpu2_label.pack(side="left", padx=(0, 10))
    player_labels.append(cpu2_label)

    cpu2_cards_frame = tk.Frame(cpu2_frame, bg=POKER_GREEN)
    cpu2_cards_frame.pack(side="left")
    for i in range(5):
        card = get_scaled_rotated_card("BACK", game_screen, angle=90, scale=1.2)
        label = tk.Label(cpu2_cards_frame, image=card, bg=POKER_GREEN)
        label.pack(pady=2)
        player_card_labels["CPU2"].append(label)
        card_images[f"CPU2_{i}"] = card

    # === CPU 3 ===
    cpu3_frame = tk.Frame(game_screen, bg=POKER_GREEN)
    cpu3_frame.place(relx=0.98, rely=0.25, anchor="ne")
    cpu3_cards_frame = tk.Frame(cpu3_frame, bg=POKER_GREEN)
    cpu3_cards_frame.pack(side="left")
    for i in range(5):
        card = get_scaled_rotated_card("BACK", game_screen, angle=270, scale=1.2)
        label = tk.Label(cpu3_cards_frame, image=card, bg=POKER_GREEN)
        label.pack(pady=2)
        player_card_labels["CPU3"].append(label)
        card_images[f"CPU3_{i}"] = card
    cpu3_label = tk.Label(cpu3_frame, text="C\nP\nU\n3", font=BUTTON_FONT, fg="white", bg=POKER_GREEN)
    cpu3_label.pack(side="left", padx=(10, 0))
    player_labels.append(cpu3_label)
# 5. Player Hand, UI Setup, and Game HUD
    # === PLAYER FRAME ===
    player_frame = tk.Frame(game_screen, bg=POKER_GREEN)
    player_frame.place(relx=0.5, rely=0.92, anchor="center")
    player_cards_frame = tk.Frame(player_frame, bg=POKER_GREEN)
    player_cards_frame.pack()
    player_obj = game.players[0]

    for i, card_str in enumerate(player_obj.hand):
        rank, _, suit = card_str.partition(" of ")
        code = rank + suit[0].upper()
        card_img = get_scaled_rotated_card(code, game_screen, scale=2.0)
        if card_img:
            label = tk.Label(player_cards_frame, image=card_img, bg=POKER_GREEN, bd=0, relief="flat")
            label.pack(side="left", padx=5, pady=0)
            label.bind("<Button-1>", lambda e, idx=i: handle_card_click(e, idx))
            player_card_labels["PLAYER"].append(label)
            card_images[f"PLAYER_{i}"] = card_img

    player_label = tk.Label(player_frame, text=player_name, font=BUTTON_FONT, fg="white", bg=POKER_GREEN)
    player_label.pack(pady=(10, 0))
    player_labels.insert(0, player_label)

    # === DECK IN CENTER ===
    card = get_scaled_rotated_card("BACK", game_screen, scale=2.0)
    if card:
        deck_label = tk.Label(game_screen, image=card, bg=POKER_GREEN, borderwidth=0)
        deck_label.place(relx=0.5, rely=0.5, anchor="center")

    chip_label = tk.Label(game_screen, text=f"Chips: ${player_obj.chips}", font=BUTTON_FONT, fg="white", bg=POKER_GREEN)
    chip_label.place(relx=0.5, rely=0.5, x=-180, anchor="center")

    pot_label = tk.Label(game_screen, text=f"Pot: ${game.pot}", font=BUTTON_FONT, fg="white", bg=POKER_GREEN)
    pot_label.place(relx=0.5, rely=0.5, x=180, anchor="center")

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
# 6. Game Flow: Phases, Actions, and Buttons
    phase_label = tk.Label(game_screen, text="Discard Phase", font=TITLE_FONT, fg="white", bg=POKER_GREEN)

    def show_discard_phase():
        phase_label.pack(pady=30)
        discard_button.place(relx=0.5, rely=0.65, anchor="center")
        game_screen.after(2000, phase_label.destroy)

    def hide_buttons():
        bet_button.place_forget()
        fold_button.place_forget()

    def hide_folded_cards(player_key):
        for label in player_card_labels[player_key]:
            label.destroy()

    def get_next_index(current):
        next_index = (current + 1) % len(game.players)
        start = current
        while game.players[next_index].folded:
            next_index = (next_index + 1) % len(game.players)
            if next_index == start:
                return None
        return next_index

    def next_turn():
        global current_turn_index, turns_taken
        if turns_taken >= len(game.players):
            show_discard_phase()
            return

        for lbl in player_labels:
            lbl.config(fg="white")
        player_labels[current_turn_index].config(fg="red")

        player = game.players[current_turn_index]
        player_key = "PLAYER" if current_turn_index == 0 else f"CPU{current_turn_index}"

        if player == game.players[0]:
            bet_button.place(relx=0.65, rely=0.70, anchor="center")
            fold_button.place(relx=0.35, rely=0.70, anchor="center")
        else:
            hand_strength = evaluate_hand(player.hand)
            print(f"[DEBUG] {player.name} hand: {player.hand} → {hand_strength}")

            if hand_strength in ("Pair", "Two Pair", "Three of a Kind", "Straight", "Flush", "Full House", "Four of a Kind"):
                decision = "bet"
            else:
                decision = random.choices(["bet", "fold"], weights=[0.6, 0.4])[0]

            if decision == "bet":
                try:
                    player.bet(10)
                    game.pot += 10
                except ValueError:
                    player.fold()
                    hide_folded_cards(player_key)
            else:
                player.fold()
                hide_folded_cards(player_key)

            chip_label.config(text=f"Chips: ${game.players[0].chips}")
            pot_label.config(text=f"Pot: ${game.pot}")

            turns_taken += 1
            current_turn_index = get_next_index(current_turn_index)
            if current_turn_index is not None:
                game_screen.after(600, next_turn)
            else:
                show_discard_phase()

    def place_bet():
        global current_turn_index, turns_taken
        try:
            game.players[current_turn_index].bet(10)
            game.pot += 10
        except ValueError:
            game.players[current_turn_index].fold()
            hide_folded_cards("PLAYER")
        chip_label.config(text=f"Chips: ${game.players[0].chips}")
        pot_label.config(text=f"Pot: ${game.pot}")
        hide_buttons()
        turns_taken += 1
        current_turn_index = get_next_index(current_turn_index)
        if current_turn_index is not None:
            next_turn()
        else:
            show_discard_phase()

    def fold_action():
        global current_turn_index, turns_taken
        game.players[current_turn_index].fold()
        hide_folded_cards("PLAYER")
        hide_buttons()
        turns_taken += 1
        current_turn_index = get_next_index(current_turn_index)
        if current_turn_index is not None:
            next_turn()
        else:
            show_discard_phase()

    bet_button = tk.Button(
        game_screen, text="Bet ($10)", font=BUTTON_FONT,
        bg="#444", fg="white", command=place_bet
    )

    fold_button = tk.Button(
        game_screen, text="Fold", font=BUTTON_FONT,
        bg="#555", fg="white", command=fold_action
    )

    discard_button = tk.Button(
        game_screen, text="Discard Selected", font=BUTTON_FONT,
        bg="#333", fg="white", command=discard_selected_cards
    )

    current_turn_index = 0
    turns_taken = 0
    next_turn()
# 8. CPU Discard Phase
def cpu_discard_phase():
    for i, player in enumerate(game.players[1:], start=1):  # Skip player[0] (the human)
        if player.folded:
            continue

        discard_count = random.choice([0, 1, 2, 3])
        if discard_count == 0:
            print(f"[CPU {player.name}] Stands pat.")
            continue

        indices = random.sample(range(len(player.hand)), discard_count)
        player.discard_cards_by_indices(indices)
        new_cards = game.deck.deal(discard_count)
        player.receive_cards(new_cards)
        print(f"[CPU {player.name}] Discarded {discard_count} card(s) → New hand: {player.hand}")
# 9. Final Bet Phase Display (defined inside launch_game_screen)
    def show_final_bet_phase():
        final_phase_label = tk.Label(game_screen, text="Final Bet Phase", font=TITLE_FONT, fg="white", bg=POKER_GREEN)
        final_phase_label.pack(pady=30)

        def show_buttons():
            bet_button.place(relx=0.65, rely=0.70, anchor="center")
            fold_button.place(relx=0.35, rely=0.70, anchor="center")

        def fade_and_continue():
            final_phase_label.destroy()
            show_buttons()

        game_screen.after(2000, fade_and_continue)
# 10. Updated Discard Phase Logic (defined inside launch_game_screen)
    def show_discard_phase():
        phase_label.pack(pady=30)
        discard_button.place(relx=0.5, rely=0.65, anchor="center")

        def continue_after_discard():
            phase_label.destroy()
            cpu_discard_phase()
            show_final_bet_phase()

        game_screen.after(2000, continue_after_discard)

# 11. Discard Selected (Player, CPU, Final Phase Trigger - Styled Like Discard Phase)
def discard_selected_cards():
    global selected_indices, discard_used
    if discard_used or not selected_indices:
        return
    discard_used = True

    to_discard = sorted(selected_indices)
    selected_indices.clear()

    for i in reversed(to_discard):
        player_card_labels["PLAYER"][i].destroy()
        del player_card_labels["PLAYER"][i]
        del game.players[0].hand[i]

    new_cards = game.deck.deal(len(to_discard))
    game.players[0].receive_cards(new_cards)

    for i, card_str in zip(to_discard, new_cards):
        rank, _, suit = card_str.partition(" of ")
        code = rank + suit[0].upper()
        card_img = get_scaled_rotated_card(code, game_screen, scale=2.0)
        if card_img:
            label = tk.Label(player_cards_frame, image=card_img, bg=POKER_GREEN, bd=0, relief="flat")
            label.pack(side="left", padx=5)
            label.bind("<Button-1>", lambda e, idx=i: handle_card_click(e, idx))
            player_card_labels["PLAYER"].insert(i, label)
            card_images[f"PLAYER_{i}"] = card_img

    for lbl in player_card_labels["PLAYER"]:
        lbl.unbind("<Button-1>")

    discard_button.place_forget()

    # === CPU DISCARD ===
    cpu_discard_phase()

    # === Final Bet Phase Message (same structure as Discard Phase) ===
    final_label = tk.Label(game_screen, text="Final Bet Phase", font=TITLE_FONT, fg="white", bg=POKER_GREEN)
    final_label.pack(pady=30)

    def reveal_final_buttons():
        final_label.destroy()
        bet_button.place(relx=0.65, rely=0.70, anchor="center")
        fold_button.place(relx=0.35, rely=0.70, anchor="center")

    game_screen.after(2000, reveal_final_buttons)
