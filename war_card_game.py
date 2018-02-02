"""
Implements War, the card game.
"""

from random import shuffle

RANKS = '2 3 4 5 6 7 8 9 10 J Q K A'.split(' ')  # from lower to higher.

# The deck has 52 cards. The deck is shuffled, then each player gets 26 cards to start, face down.
# Both players take a card from the top of their stacks. They simultaneously turn the cards face up. Thus a "battle" starts.
#   If one card's value is higher than the other, the owner of that card grabs them both and stores them on the bottom of their stack.
#   If both cards' value is equal, a "war" begins.
#       Both players place the next three cards of their stack face down. And another card (the following one from top of their stack) face up.
#       The owner of the higher face-up card wins the 'war' and adds all 10 cards on the table to the bottom of their deck.
#       If the face-up cards are again equal then the battle repeats with another set of two face-down and two face-up cards.
#       This repeats until one player's face-up card is higher than their opponent's.
# If the player rans out of cards, the game ends.
# The winner is the one who accumulated all the cards.


class Notificator():
    """
    Use it to create a notification engine.
    For now the only possible output stream is the default one.
    The input message must be string.
    """

    def __init__(self):
        pass

    def announce(self, message):
        """
        Announces the message to the Notificator's output channel.
        """

        if isinstance(message, str):
            print(message)
        else:
            raise TypeError("Notificator's input must be of type string.")


class Card():
    """
    Represents the Card entity. It has value and comparison method.
    """

    value = ''

    def __init__(self, value):
        if isinstance(value, str):
            if value in RANKS:
                self.value = value
            else:
                raise ValueError(
                    "Card's value must be one of these values: 2, 3, 4, 5, 6, 7, 8, 9, 10, J, Q, K, A.")
        else:
            raise TypeError("Card's value must be of type string.")

    def __str__(self):
        return self.value

    def __repr__(self):
        return self.value

    # Todo: define comparison to another Card


class Deck():
    """
    Represents the collection of 52 Cards. On initialization the cards are in order.
    To shuffle the Cards call shuffle(). To deal all the cards call deal_cards().
    It doesn't take Cards' suits into consideration since it's irrelevant for the game.
    """

    cards = []

    def __init__(self):
        self.reset()

    def shuffle(self):
        """
        Shuffles the list of cards.
        """

        shuffle(self.cards)

    def deal_cards(self):
        """
        Returns a list of two lists of Cards.
        The cards are drawn from the deck and evenly splitted between the two lists.
        The deck becomes empty after calling this method. Call reset() to reset the deck.
        """

        FIRST_HAND = self.cards[:26]
        SECOND_HAND = self.cards[26:]
        self.cards = []
        return [FIRST_HAND, SECOND_HAND]

    def reset(self):
        # RANKS is a list of all possible card values, there are 13 of them.
        # The deck has 4 suits of 13 cards each.
        for i in range(len(RANKS) * 4):
            c = Card(RANKS[i % 13])
            self.cards.append(c)

    def __str__(self):
        return "{}".format(self.cards)


class Hand():
    """
    Represents a hand of cards.
    """

    cards = []

    def __init__(self, cards):
        if all(isinstance(card, Card) for card in cards):
            self.cards = cards
        else:
            raise TypeError(
                "Hand's cards must be a list of objects of class Card.")

    def is_empty(self):
        return len(self.cards) == 0

    def draw_cards(self, number_of_cards_to_draw):
        """
        Draw number_of_cards_to_draw from the hand
        """
        # Todo: define drawing a card
        pass

    # Todo: define cards addition to the bottom of the hand

    def __str__(self):
        return "{}".format(self.cards)


class Game():
    """
    Initiates the game engine for War, the card game.
    """

    notificator = None
    deck = None
    game_is_going = False
    player_hand = None
    machine_hand = None

    GAME_STARTED_MSG = "Welcome to War. Don't be scared, it's just a card game.\n\
And you have no choice.\n"
    MACHINE_HAS_WON_MSG = "Player has no cards left. Machine has won the game."
    PLAYER_HAS_WON_MSG = "Machine has no cards left. Player has won the game."

    def __init__(self):
        self.notificator = Notificator()
        self.deck = Deck()
        # Todo: initialize hands here, populate them in the start() method
        self.start()

    def start(self):
        """
        Starts the game.
        """

        self.game_is_going = True
        self.notificator.announce(self.GAME_STARTED_MSG)
        self.deck.shuffle()
        shuffled_cards = self.deck.deal_cards()
        self.player_hand = Hand(shuffled_cards[0])
        self.machine_hand = Hand(shuffled_cards[1])
        self.conduct_game()

        # print(self.player_hand)
        # print(self.machine_hand)

    def conduct_game(self):
        self.check_if_anyone_won()
        # the battle begins:
        # grab a card from machine's stack to machine's hand
        # grab a card from player's stack to player's stack
        # players_card = self.player_hand.draw_cards(1)
        # machines_card = self.machine_hand.draw_cards(1)
        # compare cards
        # if the cards are different the upper hand gets both. They go to the bottom of the stack
        # else the war begins: each player grabs four more cards, three face down and one face up
        #     again, if they are different the upper hand gets all 10 cards. They go to the bottom of the stack
        #     else (if the face-up cards are again equal) the battle repeats with another set of two face-down and two face-up cards.
        #     this repeats until one player's face-up card is higher than their opponent's.

    def check_if_anyone_won(self):
        """
        At every step of the game it counts each player's cards in the stack
        after the cards that were in the hands have been distributed.
        Whoever has none cards left, loses.
        """

        if self.game_is_going:
            if self.player_hand.is_empty == 0:
                self.notificator.announce(self.MACHINE_HAS_WON_MSG)
                self.game_is_going = False
            elif self.machine_hand.is_empty == 0:
                self.notificator.announce(self.PLAYER_HAS_WON_MSG)
                self.game_is_going = False


GAME = Game()

# ---
# Test a deck of cards:
# ---
# print("Initializing test deck.")
# TEST_DECK = Deck()
# print(TEST_DECK)
# print("Shuffling test deck.")
# TEST_DECK.shuffle()
# print(TEST_DECK)
# print("Dealing cards from the test deck.")
# TEST_HANDS = TEST_DECK.deal_cards()
# print("Test deck remainder:")
# print(TEST_DECK)
# print("Test hands contents:")
# print(TEST_HANDS)
# print("First hand's len: {}".format(len(TEST_HANDS[0])))
# print("Second hand's len: {}".format(len(TEST_HANDS[1])))
