import cardDeck as deck
import unittest as test
from copy import copy, deepcopy


class CardTest(test.TestCase):
    def setUp(self):
        self.test_card = deck.Card("Hearts", "2")

    def testInit(self):
        """Tests to check if the suit/value is correct"""
        self.assertEqual(self.test_card.suit, "Hearts")
        self.assertEqual(self.test_card.value, "2")

    def reprTest(self):
        self.assertEqual(self.test_card.__repr__(), "2 of Hearts")


class DeckTest(test.TestCase):
    def setUp(self):
        self.test_deck = deck.Deck()

    def testInit(self):
        self.assertEqual(
            self.test_deck.count(), 52, "The constructor didn't make 52 cards"
        )
    
    def testRepr(self):
        self.assertEqual(self.test_deck.__repr__(), "Deck of 52 cards")
        self.test_deck.cards.pop()
        self.assertEqual(self.test_deck.__repr__(), "Deck of 51 cards")

    def testCount(self):
        self.test_deck.cards.pop()
        self.assertEqual(
            self.test_deck.count(), 51, "The card list should have 51 cards by now"
        )

    def testShuffle(self):
        deck_copy = deepcopy(self.test_deck)
        self.test_deck.shuffle()
        self.assertNotEqual(
            deck_copy,
            self.test_deck,
            "The shuffle method didn't change the order",
        )
        self.test_deck.cards.pop()
        with self.assertRaises(ValueError):
            self.test_deck.shuffle()

    def testSufficientDeal(self):
        cards = self.test_deck.deal_hand(10)
        self.assertEqual(len(cards),10)
        self.assertEqual(self.test_deck.count(),42)
        card = self.test_deck.deal_card()
        self.assertIsInstance(card,deck.Card)
        self.assertEqual(self.test_deck.count(),41)

    def testInsufficientDeal(self):
        """This tests the deal methods, and also if the deck has 52 cards"""
        self.test_deck.deal_hand(52)
        self.assertEqual(
            self.test_deck.count(),
            0,
            "There were more than 52 cards in the deck",
        )
        with self.assertRaises(ValueError):
            self.test_deck.deal_card()
        with self.assertRaises(ValueError):
            self.test_deck.deal_hand(5)


if __name__ == "__main__":
    test.main()
