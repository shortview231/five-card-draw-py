import random
import tkinter as tk
from tkinter import messagebox

from deck import Deck
from player import Player
from poker import evaluate_hand, get_hand_score


WIN_BG = "#c0c0c0"
WIN_DARK = "#808080"
WIN_LIGHT = "#ffffff"
WIN_SHADOW = "#404040"
TITLE_BLUE = "#000080"
FELT = "#007000"
CARD_BG = "#ffffff"
CARD_RED = "#b00000"
CARD_BLACK = "#101010"

SUIT_SYMBOLS = {
    "Hearts": "♥",
    "Diamonds": "♦",
    "Clubs": "♣",
    "Spades": "♠",
}


class ClassicButton(tk.Button):
    def __init__(self, master, **kwargs):
        kwargs.setdefault("bg", WIN_BG)
        kwargs.setdefault("activebackground", WIN_LIGHT)
        kwargs.setdefault("relief", "raised")
        kwargs.setdefault("bd", 2)
        kwargs.setdefault("font", ("MS Sans Serif", 10))
        kwargs.setdefault("padx", 8)
        kwargs.setdefault("pady", 3)
        super().__init__(master, **kwargs)


class FiveCardDrawClassic:
    def __init__(self, root):
        self.root = root
        self.root.title("Five Card Draw - Windows Classic Edition")
        self.root.geometry("980x690")
        self.root.minsize(900, 650)
        self.root.configure(bg=WIN_BG)

        self.player = Player("Player", 100)
        self.cpu = Player("Computer", 100)
        self.deck = None
        self.pot = 0
        self.selected = set()
        self.phase = "idle"
        self.round_number = 0

        self._build_menu()
        self._build_ui()
        self.new_session()

    def _build_menu(self):
        menu = tk.Menu(self.root)
        game_menu = tk.Menu(menu, tearoff=0)
        game_menu.add_command(label="New Game", command=self.new_session)
        game_menu.add_command(label="New Round", command=self.start_round)
        game_menu.add_separator()
        game_menu.add_command(label="Exit", command=self.root.destroy)
        menu.add_cascade(label="Game", menu=game_menu)

        help_menu = tk.Menu(menu, tearoff=0)
        help_menu.add_command(label="Poker Hands", command=self.show_rules)
        help_menu.add_command(label="About", command=self.show_about)
        menu.add_cascade(label="Help", menu=help_menu)
        self.root.config(menu=menu)

    def _build_ui(self):
        outer = tk.Frame(self.root, bg=WIN_BG, bd=3, relief="raised")
        outer.pack(fill="both", expand=True, padx=8, pady=8)

        title = tk.Frame(outer, bg=TITLE_BLUE, height=28)
        title.pack(fill="x")
        tk.Label(
            title,
            text=" Five Card Draw",
            bg=TITLE_BLUE,
            fg="white",
            font=("MS Sans Serif", 11, "bold"),
            anchor="w",
        ).pack(side="left", fill="x", expand=True, padx=2, pady=3)

        status_bar = tk.Frame(outer, bg=WIN_BG, bd=1, relief="sunken")
        status_bar.pack(side="bottom", fill="x")
        self.status_var = tk.StringVar(value="Ready")
        tk.Label(
            status_bar,
            textvariable=self.status_var,
            bg=WIN_BG,
            anchor="w",
            font=("MS Sans Serif", 9),
        ).pack(fill="x", padx=4, pady=2)

        toolbar = tk.Frame(outer, bg=WIN_BG, bd=1, relief="raised")
        toolbar.pack(fill="x", padx=4, pady=(4, 2))
        ClassicButton(toolbar, text="New Round", command=self.start_round).pack(side="left", padx=3, pady=3)
        ClassicButton(toolbar, text="Rules", command=self.show_rules).pack(side="left", padx=3, pady=3)
        self.phase_var = tk.StringVar(value="Waiting")
        tk.Label(
            toolbar,
            textvariable=self.phase_var,
            bg=WIN_BG,
            font=("MS Sans Serif", 10, "bold"),
        ).pack(side="right", padx=8)

        self.table = tk.Frame(outer, bg=FELT, bd=3, relief="sunken")
        self.table.pack(fill="both", expand=True, padx=5, pady=5)

        self.cpu_name = tk.StringVar(value="Computer")
        self.cpu_info = tk.StringVar(value="Chips: $100")
        tk.Label(
            self.table,
            textvariable=self.cpu_name,
            bg=FELT,
            fg="white",
            font=("MS Sans Serif", 13, "bold"),
        ).pack(pady=(18, 2))
        tk.Label(
            self.table,
            textvariable=self.cpu_info,
            bg=FELT,
            fg="white",
            font=("MS Sans Serif", 10),
        ).pack()

        self.cpu_cards_frame = tk.Frame(self.table, bg=FELT)
        self.cpu_cards_frame.pack(pady=8)

        center = tk.Frame(self.table, bg=FELT)
        center.pack(fill="x", pady=18)
        self.pot_var = tk.StringVar(value="Pot: $0")
        self.message_var = tk.StringVar(value="Welcome to Five Card Draw")
        tk.Label(
            center,
            textvariable=self.pot_var,
            bg=FELT,
            fg="#ffff00",
            font=("MS Sans Serif", 14, "bold"),
        ).pack()
        tk.Label(
            center,
            textvariable=self.message_var,
            bg=FELT,
            fg="white",
            font=("MS Sans Serif", 11),
            wraplength=760,
        ).pack(pady=8)

        self.player_cards_frame = tk.Frame(self.table, bg=FELT)
        self.player_cards_frame.pack(pady=8)

        self.player_info = tk.StringVar(value="Player - Chips: $100")
        tk.Label(
            self.table,
            textvariable=self.player_info,
            bg=FELT,
            fg="white",
            font=("MS Sans Serif", 13, "bold"),
        ).pack(pady=(2, 12))

        controls = tk.Frame(outer, bg=WIN_BG, bd=2, relief="raised")
        controls.pack(fill="x", padx=5, pady=(0, 5))
        self.bet_button = ClassicButton(controls, text="Bet $10", command=self.player_bet)
        self.fold_button = ClassicButton(controls, text="Fold", command=self.player_fold)
        self.draw_button = ClassicButton(controls, text="Draw Selected", command=self.player_draw)
        self.stand_button = ClassicButton(controls, text="Stand Pat", command=self.player_stand)
        for button in (self.bet_button, self.fold_button, self.draw_button, self.stand_button):
            button.pack(side="left", padx=5, pady=6)

    def new_session(self):
        self.player.chips = 100
        self.cpu.chips = 100
        self.round_number = 0
        self.start_round()

    def start_round(self):
        if self.player.chips <= 0 or self.cpu.chips <= 0:
            self.new_session()
            return

        self.round_number += 1
        self.deck = Deck()
        self.deck.shuffle()
        self.pot = 0
        self.selected.clear()
        self.player.reset_for_next_round()
        self.cpu.reset_for_next_round()
        self.player.receive_cards(self.deck.deal(5))
        self.cpu.receive_cards(self.deck.deal(5))
        self.phase = "opening_bet"
        self.message_var.set(f"Round {self.round_number}. Bet $10 to stay in, or fold.")
        self.status_var.set("Opening betting round")
        self._refresh(reveal_cpu=False)
        self._set_controls(bet=True, fold=True)

    def _set_controls(self, *, bet=False, fold=False, draw=False, stand=False):
        states = {
            self.bet_button: bet,
            self.fold_button: fold,
            self.draw_button: draw,
            self.stand_button: stand,
        }
        for button, enabled in states.items():
            button.config(state="normal" if enabled else "disabled")

    def _card_widget(self, master, card, hidden=False, index=None):
        if hidden:
            text = "░░░\n░░░\n░░░"
            fg = TITLE_BLUE
        else:
            rank, suit = card.split(" of ")
            symbol = SUIT_SYMBOLS[suit]
            text = f"{rank}\n{symbol}\n{rank}"
            fg = CARD_RED if suit in {"Hearts", "Diamonds"} else CARD_BLACK

        selected = index is not None and index in self.selected
        label = tk.Label(
            master,
            text=text,
            width=7,
            height=5,
            bg="#ffffcc" if selected else CARD_BG,
            fg=fg,
            font=("Courier New", 14, "bold"),
            bd=3,
            relief="sunken" if selected else "raised",
        )
        if index is not None:
            label.bind("<Button-1>", lambda _event, i=index: self.toggle_card(i))
        return label

    def _refresh(self, reveal_cpu=False):
        for frame in (self.cpu_cards_frame, self.player_cards_frame):
            for child in frame.winfo_children():
                child.destroy()

        for card in self.cpu.hand:
            self._card_widget(self.cpu_cards_frame, card, hidden=not reveal_cpu).pack(side="left", padx=5)

        for i, card in enumerate(self.player.hand):
            self._card_widget(self.player_cards_frame, card, index=i).pack(side="left", padx=5)

        self.pot_var.set(f"Pot: ${self.pot}")
        self.player_info.set(f"{self.player.name} - Chips: ${self.player.chips}")
        self.cpu_info.set(f"Chips: ${self.cpu.chips}")
        phase_names = {
            "opening_bet": "Opening Bet",
            "draw": "Draw Phase",
            "final_bet": "Final Bet",
            "showdown": "Showdown",
            "idle": "Waiting",
        }
        self.phase_var.set(phase_names.get(self.phase, self.phase.title()))

    def toggle_card(self, index):
        if self.phase != "draw":
            return
        if index in self.selected:
            self.selected.remove(index)
        elif len(self.selected) < 3:
            self.selected.add(index)
        else:
            self.status_var.set("You may discard at most three cards")
        self._refresh(reveal_cpu=False)

    def _take_bet(self, player, amount=10):
        amount = min(amount, player.chips)
        if amount <= 0:
            return False
        player.bet(amount)
        self.pot += amount
        return True

    def player_bet(self):
        if self.phase not in {"opening_bet", "final_bet"}:
            return
        if not self._take_bet(self.player, 10):
            self.player_fold()
            return

        if self.phase == "opening_bet":
            self._cpu_opening_action()
        else:
            self._cpu_final_action()

    def player_fold(self):
        self.player.fold()
        self.cpu.chips += self.pot
        won = self.pot
        self.pot = 0
        self.phase = "showdown"
        self.message_var.set(f"You folded. Computer wins ${won}.")
        self.status_var.set("Round complete")
        self._set_controls()
        self._refresh(reveal_cpu=True)

    def _cpu_opening_action(self):
        strength = evaluate_hand(self.cpu.hand)
        strong = strength != "High Card"
        if strong or random.random() < 0.72:
            self._take_bet(self.cpu, 10)
            self.phase = "draw"
            self.message_var.set("Select up to three cards to replace, or stand pat.")
            self.status_var.set("Click cards to select them")
            self._set_controls(draw=True, stand=True)
            self._refresh(reveal_cpu=False)
        else:
            self.cpu.fold()
            self.player.chips += self.pot
            won = self.pot
            self.pot = 0
            self.phase = "showdown"
            self.message_var.set(f"Computer folds. You win ${won}.")
            self.status_var.set("Round complete")
            self._set_controls()
            self._refresh(reveal_cpu=True)

    def player_draw(self):
        if self.phase != "draw":
            return
        indices = sorted(self.selected, reverse=True)
        self.selected.clear()
        count = len(indices)
        if count:
            self.player.discard_cards_by_indices(indices)
            self.player.receive_cards(self.deck.deal(count))
        self._cpu_draw()
        self._begin_final_bet(count)

    def player_stand(self):
        if self.phase != "draw":
            return
        self.selected.clear()
        self._cpu_draw()
        self._begin_final_bet(0)

    def _cpu_draw(self):
        score = evaluate_hand(self.cpu.hand)
        if score in {"Straight", "Flush", "Full House", "Four of a Kind", "Straight Flush", "Royal Flush"}:
            discard_count = 0
        elif score in {"Three of a Kind", "Two Pair"}:
            discard_count = 1
        elif score == "Pair":
            discard_count = 3
        else:
            discard_count = random.choice([2, 3])

        if discard_count:
            indices = random.sample(range(5), discard_count)
            self.cpu.discard_cards_by_indices(indices)
            self.cpu.receive_cards(self.deck.deal(discard_count))
        self.cpu_last_draw = discard_count

    def _begin_final_bet(self, player_draw_count):
        self.phase = "final_bet"
        self.message_var.set(
            f"You drew {player_draw_count}. Computer drew {self.cpu_last_draw}. Bet $10 for showdown, or fold."
        )
        self.status_var.set("Final betting round")
        self._set_controls(bet=True, fold=True)
        self._refresh(reveal_cpu=False)

    def _cpu_final_action(self):
        strength = evaluate_hand(self.cpu.hand)
        continue_probability = {
            "High Card": 0.55,
            "Pair": 0.80,
            "Two Pair": 0.95,
        }.get(strength, 1.0)

        if random.random() <= continue_probability and self._take_bet(self.cpu, 10):
            self.showdown()
        else:
            self.cpu.fold()
            self.player.chips += self.pot
            won = self.pot
            self.pot = 0
            self.phase = "showdown"
            self.message_var.set(f"Computer folds on the final bet. You win ${won}.")
            self.status_var.set("Round complete")
            self._set_controls()
            self._refresh(reveal_cpu=True)

    def showdown(self):
        self.phase = "showdown"
        player_score = get_hand_score(self.player.hand)
        cpu_score = get_hand_score(self.cpu.hand)
        player_name = evaluate_hand(self.player.hand)
        cpu_name = evaluate_hand(self.cpu.hand)
        pot = self.pot

        if player_score > cpu_score:
            self.player.chips += pot
            result = f"You win ${pot} with {player_name}. Computer had {cpu_name}."
        elif cpu_score > player_score:
            self.cpu.chips += pot
            result = f"Computer wins ${pot} with {cpu_name}. You had {player_name}."
        else:
            player_share = pot // 2
            cpu_share = pot - player_share
            self.player.chips += player_share
            self.cpu.chips += cpu_share
            result = f"Tie: {player_name}. Pot split ${player_share}/${cpu_share}."

        self.pot = 0
        self.message_var.set(result)
        self.status_var.set("Round complete. Choose New Round to continue.")
        self._set_controls()
        self._refresh(reveal_cpu=True)

    def show_rules(self):
        messagebox.showinfo(
            "Poker Hands",
            "Five Card Draw\n\n"
            "1. Royal Flush\n"
            "2. Straight Flush\n"
            "3. Four of a Kind\n"
            "4. Full House\n"
            "5. Flush\n"
            "6. Straight\n"
            "7. Three of a Kind\n"
            "8. Two Pair\n"
            "9. Pair\n"
            "10. High Card\n\n"
            "After the opening bet, select up to three cards to replace. "
            "A final betting round is followed by the showdown."
        )

    def show_about(self):
        messagebox.showinfo(
            "About Five Card Draw",
            "Five Card Draw - Windows Classic Edition\n"
            "A revival of Robert Sory Jr.'s first Python project."
        )


def main():
    root = tk.Tk()
    FiveCardDrawClassic(root)
    root.mainloop()


if __name__ == "__main__":
    main()
