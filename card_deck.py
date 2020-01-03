from random import shuffle
from itertools import product
import functools
import copy


@functools.total_ordering
class Card:
    """codes a card"""

    valid_suits = ("Hearts", "Diamonds", "Clubs", "Spades")
    valid_values = (
        "A",
        "2",
        "3",
        "4",
        "5",
        "6",
        "7",
        "8",
        "9",
        "10",
        "J",
        "Q",
        "K",
    )

    def __init__(self, suit, value):
        if suit not in Card.valid_suits:
            raise ValueError("Invalid suit!")
        self.suit = suit
        if value not in Card.valid_values:
            raise ValueError("Invalid number!")
        self.value = value

    def __repr__(self):
        return str(self.value) + " of " + str(self.suit)

    #        return f"{self.value} of {self.suit}"

    # Implementing == and < for usage of @functools.total_ordering
    def __eq__(self, other):
        if self.value == other.value:
            return self.suit == other.suit
        return self.value == other.value

    def __lt__(self, other):
        if self.value == other.value:
            return self.suit < other.suit
        return self.value < other.value


class Deck:
    """codes a pack of 52 card combinations"""

    _full_deck = product(Card.valid_suits, Card.valid_values)

    @classmethod
    def make_deck(cls, source):
        return (Card(s, v) for s, v in source)

    def __init__(self):
        deck = copy.copy(Deck._full_deck)
        self.cards = list(Deck.make_deck(deck))

    def count(self):
        return len(self.cards)

    def __repr__(self):
        return "Deck of " + str(self.count()) + " cards"
        # return f"Deck of {self.count()} cards"

    def _deal(self, number):
        cards_to_deal = []
        if self.count() == 0:
            raise ValueError("All cards have been dealt")
        if number > self.count():
            number = self.count()
        while number > 0:
            number -= 1
            cards_to_deal.append(self.cards.pop())
        return cards_to_deal

    def __eq__(self, other):
        return all(s == o for s in self.cards for o in other.cards)

    def shuffle(self):
        if sorted(self.cards) != sorted(Deck.make_deck(Deck._full_deck)):
            raise ValueError("Only full decks can be shuffled")
        shuffle(self.cards)
        return self.cards

    def deal_card(self):
        return self._deal(1)[0]

    def deal_hand(self, cards):
        return self._deal(cards)


if __name__ == "__main__":
    d = Deck()
    d.shuffle()
    cards = d._deal(20)
    print(cards, len(cards))
