class Player:
    def __init__(self, name, chips=100):
        self.name = name
        self.hand = []
        self.chips = chips
        self.current_bet = 0
        self.folded = False

    def bet(self, amount):
        if amount > self.chips:
            raise ValueError("Insufficient chips")
        self.chips -= amount
        self.current_bet += amount

    def fold(self):
        self.folded = True

    def reset_for_next_round(self):
        self.hand = []
        self.current_bet = 0
        self.folded = False

    def receive_cards(self, cards):
        self.hand.extend(cards)

    def discard_cards(self, cards):
        for card in cards:
            if card in self.hand:
                self.hand.remove(card)
            else:
                raise ValueError("Card not in hand")

    def discard_cards_by_indices(self, indices):
        for index in sorted(indices, reverse=True):
            if index < len(self.hand):
                del self.hand[index]
            else:
                raise ValueError("Index out of range")

    def show_hand(self):
        return [str(card) for card in self.hand]

    def __str__(self):
        return f"Player {self.name}: Chips: {self.chips}, Current Bet: {self.current_bet}, Hand: {self.show_hand()}, Folded: {self.folded}"
