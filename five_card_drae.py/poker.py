from collections import Counter

RANK_VALUES = {
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
    "A": 14,
}

HAND_RANKS = {
    "High Card": 1,
    "Pair": 2,
    "Two Pair": 3,
    "Three of a Kind": 4,
    "Straight": 5,
    "Flush": 6,
    "Full House": 7,
    "Four of a Kind": 8,
    "Straight Flush": 9,
    "Royal Flush": 10,
}

# Backwards-compatible aliases for older modules.
rank_values = RANK_VALUES
hand_ranks = HAND_RANKS


def _parse_hand(hand):
    if len(hand) != 5:
        raise ValueError("A poker hand must contain exactly five cards")

    ranks = []
    suits = []
    for card in hand:
        parts = card.split(" of ")
        if len(parts) != 2:
            raise ValueError(f"Invalid card format: {card!r}")
        rank, suit = parts
        if rank not in RANK_VALUES:
            raise ValueError(f"Invalid card rank: {rank!r}")
        ranks.append(rank)
        suits.append(suit)
    return ranks, suits


def _straight_high(values):
    unique = sorted(set(values))
    if unique == [2, 3, 4, 5, 14]:
        return 5
    if len(unique) == 5 and unique[-1] - unique[0] == 4:
        return unique[-1]
    return None


def evaluate_hand(hand):
    """Return the conventional name of a five-card poker hand."""
    ranks, suits = _parse_hand(hand)
    values = [RANK_VALUES[rank] for rank in ranks]
    counts = Counter(values)
    count_pattern = sorted(counts.values(), reverse=True)
    flush = len(set(suits)) == 1
    straight_high = _straight_high(values)

    if flush and straight_high == 14 and set(values) == {10, 11, 12, 13, 14}:
        return "Royal Flush"
    if flush and straight_high is not None:
        return "Straight Flush"
    if count_pattern == [4, 1]:
        return "Four of a Kind"
    if count_pattern == [3, 2]:
        return "Full House"
    if flush:
        return "Flush"
    if straight_high is not None:
        return "Straight"
    if count_pattern == [3, 1, 1]:
        return "Three of a Kind"
    if count_pattern == [2, 2, 1]:
        return "Two Pair"
    if count_pattern == [2, 1, 1, 1]:
        return "Pair"
    return "High Card"


def get_hand_score(hand):
    """Return a sortable tuple that fully breaks ties between poker hands."""
    ranks, _ = _parse_hand(hand)
    values = [RANK_VALUES[rank] for rank in ranks]
    counts = Counter(values)
    hand_type = evaluate_hand(hand)
    category = HAND_RANKS[hand_type]
    straight_high = _straight_high(values)

    if hand_type in {"Royal Flush", "Straight Flush", "Straight"}:
        return (category, straight_high)

    if hand_type == "Four of a Kind":
        four = max(value for value, count in counts.items() if count == 4)
        kicker = max(value for value, count in counts.items() if count == 1)
        return (category, four, kicker)

    if hand_type == "Full House":
        trips = max(value for value, count in counts.items() if count == 3)
        pair = max(value for value, count in counts.items() if count == 2)
        return (category, trips, pair)

    if hand_type == "Three of a Kind":
        trips = max(value for value, count in counts.items() if count == 3)
        kickers = sorted((value for value, count in counts.items() if count == 1), reverse=True)
        return (category, trips, *kickers)

    if hand_type == "Two Pair":
        pairs = sorted((value for value, count in counts.items() if count == 2), reverse=True)
        kicker = max(value for value, count in counts.items() if count == 1)
        return (category, *pairs, kicker)

    if hand_type == "Pair":
        pair = max(value for value, count in counts.items() if count == 2)
        kickers = sorted((value for value, count in counts.items() if count == 1), reverse=True)
        return (category, pair, *kickers)

    return (category, *sorted(values, reverse=True))
