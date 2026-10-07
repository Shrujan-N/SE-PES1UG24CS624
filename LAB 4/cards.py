import random

RANKS = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
SUITS = ["C", "D", "H", "S"]

class Deck:
    def __init__(self):
        self.reset()

    def reset(self):
        """Creates a full 52-card deck and shuffles it."""
        self.cards = [(rank, suit) for suit in SUITS for rank in RANKS]
        random.shuffle(self.cards)

    def draw(self):
        # If the deck becomes empty during gameplay, auto-replenish & reshuffle
        # seamlessly without breaking the game or crashing.
        if not self.cards:
            print("\n[Deck empty! Reshuffling new deck...]")
            self.reset()
        return self.cards.pop()

def hand_value(hand):
    """
    # TASK 1: Correct Ace Scoring Logic
    # Calculates hand value dynamically. Aces count as 11 when total <= 21,
    # but reduce to 1 (value -= 10) as long as total exceeds 21.
    """
    value = 0
    aces = 0

    for card in hand:
        rank = card[0]
        if rank == "A":
            aces += 1
            value += 11
        elif rank in {"J", "Q", "K"}:
            value += 10
        else:
            value += int(rank)

    # Reduce Ace from 11 to 1 dynamically if busting
    while value > 21 and aces > 0:
        value -= 10
        aces -= 1

    return value