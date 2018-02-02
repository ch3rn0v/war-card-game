"""
Implements War, the card game.
"""

RANKS = '2 3 4 5 6 7 8 9 10 J Q K A'.split(' ')  # from lower to higher.

# Deck has:
# A cards
# M deal shuffled cards

# Player has:
# A Stack
# A Hand (basic list of Cards)
# M Draw another card
# M Grab cards to the bottom of the stack (face down) on battle/war win

# Card has:
# A Value
# A Face status (face up or face down)
# M Comparison method. Takes in another card, answers whether this card is of a higher, lower or of the same value

# Announcer has:
# M Announce the message to the output stream

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

# Players:
# Player
# Machine


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


class Game():
    """
    Initiates the game engine for War, the card game.
    """

    notificator = None
    game_is_going = False
    winner = None
    player_hand_size = 0
    machine_hand_size = 0

    GAME_STARTED_MSG = "Welcome to War. Don't be scared, it's just a card game.\n\
    And you have no choice.\n"
    MACHINE_HAS_WON_MSG = "Player has no cards left. Machine has won the game."
    PLAYER_HAS_WON_MSG = "Machine has no cards left. Player has won the game."

    def __init__(self, notificator):
        self.notificator = notificator
        self.start()

    def start(self):
        """
        Starts the game.
        """

        self.game_is_going = True
        self.notificator.announce(self.GAME_STARTED_MSG)
        # call Deck to shuffle and deal the cards
        # set the hand sizes to the half of the amount the Deck dealt to the players

    def check_if_anyone_won(self):
        """
        At every step of the game it counts each player's cards in the stack
        after the cards that were in the hands have been distributed.
        Whoever has none cards left, loses.
        """

        if self.game_is_going:
            if self.player_hand_size == 0:
                self.notificator.announce(self.MACHINE_HAS_WON_MSG)
            elif self.machine_hand_size == 0:
                self.notificator.announce(self.PLAYER_HAS_WON_MSG)


NOTIFICATOR = Notificator()
NOTIFICATOR.announce('Hello from Notificator')
