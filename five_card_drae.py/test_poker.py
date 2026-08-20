import unittest

from poker import evaluate_hand, get_hand_score


class PokerEvaluationTests(unittest.TestCase):
    def test_all_hand_categories(self):
        cases = {
            "Royal Flush": ["10 of Hearts", "J of Hearts", "Q of Hearts", "K of Hearts", "A of Hearts"],
            "Straight Flush": ["5 of Spades", "6 of Spades", "7 of Spades", "8 of Spades", "9 of Spades"],
            "Four of a Kind": ["A of Hearts", "A of Diamonds", "A of Clubs", "A of Spades", "2 of Hearts"],
            "Full House": ["K of Hearts", "K of Diamonds", "K of Clubs", "4 of Spades", "4 of Hearts"],
            "Flush": ["2 of Clubs", "5 of Clubs", "8 of Clubs", "J of Clubs", "K of Clubs"],
            "Straight": ["6 of Hearts", "7 of Diamonds", "8 of Clubs", "9 of Spades", "10 of Hearts"],
            "Three of a Kind": ["Q of Hearts", "Q of Diamonds", "Q of Clubs", "3 of Spades", "8 of Hearts"],
            "Two Pair": ["J of Hearts", "J of Diamonds", "4 of Clubs", "4 of Spades", "9 of Hearts"],
            "Pair": ["10 of Hearts", "10 of Diamonds", "3 of Clubs", "6 of Spades", "K of Hearts"],
            "High Card": ["2 of Hearts", "5 of Diamonds", "8 of Clubs", "J of Spades", "K of Hearts"],
        }
        for expected, hand in cases.items():
            with self.subTest(expected=expected):
                self.assertEqual(evaluate_hand(hand), expected)

    def test_wheel_straight(self):
        hand = ["A of Hearts", "2 of Diamonds", "3 of Clubs", "4 of Spades", "5 of Hearts"]
        self.assertEqual(evaluate_hand(hand), "Straight")
        self.assertEqual(get_hand_score(hand)[1], 5)

    def test_pair_kicker_breaks_tie(self):
        stronger = ["A of Hearts", "A of Clubs", "K of Hearts", "7 of Clubs", "2 of Hearts"]
        weaker = ["A of Diamonds", "A of Spades", "Q of Hearts", "7 of Diamonds", "2 of Clubs"]
        self.assertGreater(get_hand_score(stronger), get_hand_score(weaker))

    def test_two_pair_high_pair_breaks_tie(self):
        kings = ["K of Hearts", "K of Clubs", "4 of Hearts", "4 of Clubs", "2 of Hearts"]
        queens = ["Q of Hearts", "Q of Clubs", "J of Hearts", "J of Clubs", "A of Hearts"]
        self.assertGreater(get_hand_score(kings), get_hand_score(queens))


if __name__ == "__main__":
    unittest.main()
