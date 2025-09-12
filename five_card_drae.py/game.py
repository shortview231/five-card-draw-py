import random
from player import Player
from deck import Deck
from poker import evaluate_hand, get_hand_score

class Game:
    def __init__(self, total_players=4, starting_chips=100, player_name="You"):
        self.players = []
        self.pot = 0
        self.round_number = 0  # for tracking rounds played

        # Add human player first
        self.players.append(Player(player_name, chips=starting_chips))

        # CPU Names
        cpu_names = [
            "HHH", "Shawn Michaels", "Stone Cold", "The Rock",
            "Hulk Hogan", "Ric Flair", "Undertaker", "John Cena",
            "Roman Reigns", "Seth Rollins"
        ]

        cpu_count = total_players - 1
        selected_cpu_names = random.sample(cpu_names, cpu_count)

        for name in selected_cpu_names:
            self.players.append(Player(name, chips=starting_chips))

    def start_round(self):
        print("\n== Starting a New Round ==")
        self.round_number += 1
        self.pot = 0

        self.deck = Deck()
        self.deck.shuffle()

        for player in self.players:
            player.reset_for_next_round()

        for player in self.players:
            hand = self.deck.deal(5)
            player.receive_cards(hand)

    def betting_phase(self, bet_amount=10):
        for player in self.players:
            if player.folded:
                continue

            if player.name == self.players[0].name:
                decision = "bet"  # default GUI behavior for now
            else:
                hand_strength = evaluate_hand(player.hand)
                if hand_strength in ("Pair", "Two Pair", "Three of a Kind", "Straight", "Flush", "Full House", "Four of a Kind"):
                    decision = "bet"
                else:
                    decision = random.choices(["bet", "fold"], weights=[0.7, 0.3])[0]

            if decision == "bet":
                try:
                    player.bet(bet_amount)
                    self.pot += bet_amount
                except ValueError:
                    player.fold()
            else:
                player.fold()

    def draw_phase(self):
        for player in self.players:
            if player.folded:
                continue

            if player.name == self.players[0].name:
                pass  # GUI will handle card discard later
            else:
                discard_count = random.choice([0, 1, 2, 3])
                indices = random.sample(range(len(player.hand)), discard_count)
                player.discard_cards_by_indices(indices)
                new_cards = self.deck.deal(discard_count)
                player.receive_cards(new_cards)

    def showdown(self):
        active_players = [p for p in self.players if not p.folded]
        scored_players = [(player, get_hand_score(player.hand)) for player in active_players]
        scored_players.sort(key=lambda x: x[1], reverse=True)

        winner, _ = scored_players[0]
        winner.chips += self.pot
        self.pot = 0
        return winner.name

if __name__ == "__main__":
    print("🔧 Testing game.py in isolation...")

    game = Game(total_players=4, starting_chips=100, player_name="Tester")
    game.start_round()

    print("\n🃏 Players and Hands:")
    for p in game.players:
        print(f"{p.name} → {p.hand} (Chips: {p.chips})")

    game.betting_phase(bet_amount=10)
    game.draw_phase()
    game.betting_phase(bet_amount=20)

    winner = game.showdown()
    print(f"\n🏆 Winner: {winner}")
