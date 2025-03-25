import random

class Deck:
    def __init__(self):
        ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
        suits = ["Hearts", "Diamonds", "Clubs", "Spades"]
        self.cards = [f"{rank} of {suit}" for suit in suits for rank in ranks]

    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self, num_cards):
        dealt_cards = self.cards[:num_cards]
        self.cards = self.cards[num_cards:]
        return dealt_cards


# ===== TESTING BLOCK =====
if __name__ == "__main__":
    deck = Deck()
    print("Deck created with", len(deck.cards), "cards.")

    print("\nShuffling deck...")
    deck.shuffle()

    print("\nDealing 5 cards:")
    hand = deck.deal(5)
    for card in hand:
        print("  ", card)

    print("\nCards left in deck:", len(deck.cards))
