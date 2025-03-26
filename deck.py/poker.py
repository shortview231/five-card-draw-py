from collections import Counter

rank_values = {
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "10": 10,
    "J": 11,
    "Q": 12,
    "K": 13,
    "A": 14
}

hand_ranks = {
    "High Card": 1,
    "Pair": 2,
    "Two Pair": 3,
    "Three of a Kind": 4,
    "Straight": 5,
    "Flush": 6,
    "Full House": 7,
    "Four of a Kind": 8,
    "Straight Flush": 9,
    "Royal Flush": 10
}

def evaluate_hand(hand):
    pass 
    ranks = [card.split()[0] for card in hand]
    suits = [card.split()[-1] for card in hand]
    rank_counts = Counter(ranks)
    suit_counts = Counter(suits)

    sorted_ranks = sorted([rank_values[r] for r in ranks])

    is_straight = (
        len(set(sorted_ranks)) == 5 and max(sorted_ranks) == 4
    ) or set(["A", "2", "3", "4", "5"]).issubset(set(ranks))
   
    if 2 in rank_counts.values():
        return "Pair"
    elif 3 in rank_counts.values():
        return "Three of a Kind"
    elif 4 in rank_counts.values():
        return "Four of a kind"
    elif list(rank_counts.values()). count(2) == 2:
        return "Two Pair"
    elif 3 in rank_counts.values() and 2 in rank_counts.values():
        return "Full House"
    elif len(suit_counts) ==1 and set(ranks) == set(["10", "J", "Q", "K", "A"]):
        return "Royal Flush"
    elif 5 in suit_counts.values() and is_straight:
        return "Straight Flush"
    elif is_straight:
        return "straight"
    elif 5 in suit_counts.values():
        return "Flush"

def get_hand_score(hand):
    hand_type = evaluate_hand(hand)
    score = hand_ranks[hand_type]
    sorted_card_values = sorted([rank_values[card.split()[0]] for card in hand], reverse=True)
    return (score, sorted_card_values)