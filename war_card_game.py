"""
Implements War, the card game.
"""

from random import shuffle

RANKS = '2 3 4 5 6 7 8 9 10 J Q K A'.split(' ')  # From lower to higher.


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

    def __lt__(self, other):
        return RANKS.index(self.value) < RANKS.index(other.value)

    def __le__(self, other):
        return RANKS.index(self.value) <= RANKS.index(other.value)

    def __eq__(self, other):
        return RANKS.index(self.value) == RANKS.index(other.value)

    def __ne__(self, other):
        return RANKS.index(self.value) != RANKS.index(other.value)

    def __gt__(self, other):
        return RANKS.index(self.value) > RANKS.index(other.value)

    def __ge__(self, other):
        return RANKS.index(self.value) >= RANKS.index(other.value)


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
        """
        Resets the deck to its initial state.
        """

        # RANKS is a list of all possible card values; there are 13 of them.
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

    # Top of the hand is indexed as self.cards[0]. Bottom is at the self.cards[-1].

    def __init__(self, cards=None):
        if cards and all(isinstance(card, Card) for card in cards):
            self.cards = cards
        elif not cards:
            self.cards = []
        else:
            raise TypeError(
                "Hand's cards must be a list of objects of class Card.")

    def is_empty(self):
        """
        Returns True if the hand has no cards left.
        """

        return len(self.cards) == 0

    def draw_cards(self, number_of_cards_to_draw):
        """
        Draws number_of_cards_to_draw from the top of the hand.
        """

        if number_of_cards_to_draw > len(self):
            raise IndexError(
                "Index out of range. Tried to draw {}. The hand has only {} cards.".format(number_of_cards_to_draw, len(self)))
        else:
            drawn_cards = self.cards[:number_of_cards_to_draw]
            del self.cards[:number_of_cards_to_draw]
            return drawn_cards

    def add_cards(self, cards_to_add):
        """
        Adds cards_to_add to the bottom of the Hand.
        cards_to_add must be a list of objects of class Card.
        """

        if all(isinstance(card, Card) for card in cards_to_add):
            self.cards += cards_to_add
        else:
            raise TypeError(
                "Hand's cards must be a list of objects of class Card.")

    def __str__(self):
        return "{}".format(self.cards)

    def __len__(self):
        return len(self.cards)


class Game():
    """
    The game engine for War, the card game.
    Automatically starts the game upon initialization.
    """

    GAME_STARTED_MSG = "Welcome to War. Don't be scared, it's just a card game.\n\
And you have no choice.\n"
    MACHINE_HAS_WON_MSG = "Player has no cards left. Machine has won the game."
    PLAYER_HAS_WON_MSG = "Machine has no cards left. Player has won the game."

    def __init__(self):
        self.notificator = Notificator()
        self.deck = Deck()
        self.player_hand = Hand()
        self.machine_hand = Hand()
        self.start()

    def start(self):
        """
        Starts the game.
        """

        self.game_is_going = True
        self.notificator.announce(self.GAME_STARTED_MSG)
        self.deck.shuffle()
        two_sets_of_shuffled_cards = self.deck.deal_cards()
        self.player_hand.add_cards(two_sets_of_shuffled_cards[0])
        self.machine_hand.add_cards(two_sets_of_shuffled_cards[1])
        self.total_rounds_counter = 0
        self.particular_war_rounds_counter = 0
        self.conduct_game()

    def conduct_game(self):
        """
        Main game loop.
        """

        while self.game_is_going:
            self.conduct_next_round()

    def conduct_next_round(self, cards_in_bank=None):
        """
        Executes a single round of the game.
        Verifies if there is a winner. And calls itself in cases of war.
        """

        print("Round {} has begun.".format(self.total_rounds_counter))
        print("Player  has {} cards left.".format(len(self.player_hand)))
        print("Machine has {} cards left.".format(len(self.machine_hand)))
        self.total_rounds_counter += 1

        # If the war didn't end on its first round, then the second and all the other rounds of this
        # particular war should draw 2 face down cards and 2 face up cards instead of 3 and 1 respectively.

        count_of_cards_to_draw_face_up = 1
        if self.particular_war_rounds_counter < 2:
            count_of_cards_to_draw_face_down = 3
        else:
            count_of_cards_to_draw_face_down = 1

        # Draw face down cards (only in case of war).
        if cards_in_bank is not None:
            self.particular_war_rounds_counter += 1
            try:
                player_cards_drawn_face_down = self.player_hand.draw_cards(
                    count_of_cards_to_draw_face_down)
            except IndexError:
                # If the player doesn't have enough cards, the machine has won.
                self.announce_winner('M')
                return
            try:
                machine_cards_drawn_face_down = self.machine_hand.draw_cards(
                    count_of_cards_to_draw_face_down)
            except IndexError:
                # If the machine doesn't have enough cards, the player has won.
                self.announce_winner('P')
                return

        # Draw face up cards.
        try:
            player_cards_drawn_face_up = self.player_hand.draw_cards(
                count_of_cards_to_draw_face_up)
        except IndexError:
            # If the player doesn't have enough cards, the machine has won.
            self.announce_winner('M')
            return
        try:
            machine_cards_drawn_face_up = self.machine_hand.draw_cards(
                count_of_cards_to_draw_face_up)
        except IndexError:
            # If the machine doesn't have enough cards, the player has won.
            self.announce_winner('P')
            return

        # Don't bother trying to gather drawn cards if we already know a winner.
        if self.game_is_going:
            if cards_in_bank is None:
                cards_in_bank = player_cards_drawn_face_up + machine_cards_drawn_face_up
            else:
                cards_in_bank += player_cards_drawn_face_down + player_cards_drawn_face_up + \
                    machine_cards_drawn_face_down + machine_cards_drawn_face_up

            shuffle(cards_in_bank)  # To avoid endless wars.

            # If cards' values are different give both cards to winner.
            if player_cards_drawn_face_up[-1] < machine_cards_drawn_face_up[-1]:
                self.machine_hand.add_cards(cards_in_bank)
                cards_in_bank = []
                self.particular_war_rounds_counter = 0
            elif player_cards_drawn_face_up[-1] > machine_cards_drawn_face_up[-1]:
                self.player_hand.add_cards(cards_in_bank)
                cards_in_bank = []
                self.particular_war_rounds_counter = 0
            else:
                self.conduct_next_round(cards_in_bank)

    def announce_winner(self, winner):
        """
        Announces winner.
        Winner can either be the Player (winner == 'P') or the Machine (winner == 'M').
        """

        if winner == "P":
            self.notificator.announce(self.PLAYER_HAS_WON_MSG)
        elif winner == "M":
            self.notificator.announce(self.MACHINE_HAS_WON_MSG)
        else:
            raise ValueError(
                "Winner can either be the Player (winner == 'P') or the Machine (winner == 'M').")
        self.game_is_going = False


GAME = Game()
