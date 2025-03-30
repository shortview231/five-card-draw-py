import random
from player import Player
from deck import Deck
from poker import evaluate_hand, get_hand_score  # For hand logic


class Game:
    def __init__(self, total_players=4, starting_chips=100):
        self.players = []
        self.pot = 0

        user_name = input("Enter your name: ")
        self.players.append(Player(user_name, chips=starting_chips))

        cpu_names = [
            "HHH", "Shawn Michaels", "Stone Cold", "The Rock",
            "Hulk Hogan", "Ric Flair", "Undertaker", "John Cena",
            "Roman Reigns", "Seth Rollins"
        ]

        cpu_count = total_players - 1
        selected_cpu_names = random.sample(cpu_names, cpu_count)

        for name in selected_cpu_names:
            self.players.append(Player(name, chips=starting_chips))

        for player in self.players:
            print(f"- {player.name} (Chips: {player.chips})")

        print(f"\nThe game is ready. Starting pot: {self.pot} chips.")

    def start_round(self):
        print("\n== Starting a New Round ==")
        self.pot = 0

        self.deck = Deck()
        self.deck.shuffle()

        for player in self.players:
            player.reset_for_next_round()

        for player in self.players:
            hand = self.deck.deal(5)
            player.receive_cards(hand)
            print(f"{player.name}'s hand: {player.show_hand()}")

    def betting_phase(self, bet_amount=10):
        print(f"\n== Betting Phase ({bet_amount} chips) ==")

        for player in self.players:
            if player.folded:
                continue

            if player.name == self.players[0].name:
                decision = input(f"{player.name}, do you want to 'bet' or 'fold'? ").lower()
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
                    print(f"{player.name} bets {bet_amount} chips.")
                except ValueError as e:
                    print(f"Error: {e}. {player.name} cannot bet.")
                    player.fold()
            else:
                player.fold()
                print(f"{player.name} folds.")

    def draw_phase(self):
        print("\n== Draw Phase ==")

        for player in self.players:
            if player.folded:
                continue

            print(f"\n{player.name}'s current hand: {player.show_hand()}")

            if player.name == self.players[0].name:
                try:
                    indices = input("Enter indices of cards to discard (0-4, space-separated): ")
                    indices = [int(i) for i in indices.split() if i.isdigit()]
                    player.discard_cards_by_indices(indices)
                    new_cards = self.deck.deal(len(indices))
                    player.receive_cards(new_cards)
                    print(f"New hand: {player.show_hand()}")
                except Exception as e:
                    print(f"Error discarding cards: {e}")
            else:
                discard_count = random.choice([0, 1, 2, 3])
                indices = random.sample(range(len(player.hand)), discard_count)
                player.discard_cards_by_indices(indices)
                new_cards = self.deck.deal(discard_count)
                player.receive_cards(new_cards)
                print(f"{player.name} discards {discard_count} card(s).")

    def showdown(self):
        print("\n== Showdown ==")

        active_players = [p for p in self.players if not p.folded]

        for player in active_players:
            print(f"\n{player.name}'s hand: {player.show_hand()}")
            hand_type = evaluate_hand(player.hand)
            print(f"  => {hand_type}")

        scored_players = [(player, get_hand_score(player.hand)) for player in active_players]
        scored_players.sort(key=lambda x: x[1], reverse=True)

        winner, winning_score = scored_players[0]
        print(f"\n🏆 {winner.name} wins the pot of {self.pot} chips with a {evaluate_hand(winner.hand)}!")

        winner.chips += self.pot
        self.pot = 0


# ===== RUNNING THE GAME =====
if __name__ == "__main__":
    game = Game()

    while True:
        game.start_round()
        game.betting_phase(bet_amount=10)
        game.draw_phase()
        game.betting_phase(bet_amount=20)
        game.showdown()

        again = input("\nPlay another round? (y/n): ")
        if again.lower() != 'y':
            print("Thanks for playing!")
            break
