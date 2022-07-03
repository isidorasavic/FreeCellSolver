# herc = H
# pik = P
# tref = T
# karo = K

from Utils import Suits
from colorama import init, Fore, Back, Style


class Card:
    _suit = None
    _value = -1
    _color = None

    def __init__(self, suit, value):
        self.set_value(value)
        self._suit = suit

        if suit == "H" or suit == "K":
            self._color = Suits.red
        elif suit == "P" or suit == "T":
            self._color = Suits.black
        else:
            raise Exception("Invalid suit!")

        if ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"].count(value) == 0:
            raise Exception(f"Invalid value: {value}")

    def get_value(self):
        return self._value

    def set_value(self, value):
        if ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"].count(value) == 0:
            raise Exception("Invalid value!")
        self._value = get_num_value(value)

    def get_suit(self):
        return self._suit

    def set_suit(self, suit):
        if ["H", "P", "K", "T"].count(suit) == 0:
            raise Exception("Invalid value!")
        self._suit = suit

    def get_color(self):
        return self._color

    def set_color(self, color):
        if [Suits.black, Suits.red].count(color) == 0:
            raise Exception("Invalid color!")
        self._color = color

    def __str__(self):
        suit_symbol = ""
        if self._suit == 'H':
            suit_symbol = Fore.RED+'♥'+Fore.RESET
        if self._suit == 'T':
            suit_symbol = Fore.BLACK+'♣'+Fore.RESET
        if self._suit == 'K':
            suit_symbol = Fore.RED+'♦'+Fore.RESET
        if self._suit == 'P':
            suit_symbol = Fore.BLACK+'♠'+Fore.RESET
        return str(self._value)+suit_symbol+" "

    def __eq__(self, card2):
        if card2 is None:
            return False
        return self.get_color() == card2.get_color() and self.get_suit() == card2.get_suit() and \
            self.get_value() == card2.get_value()

    def __copy__(self):
        return Card(self._suit, get_str_value(self._value))

    # def is_larger_and_same_suit(self, card2):
    #     return self._suit == card2.get_suit() and self.get_value() - 1 == card2.get_value()
    #
    # def is_smaller_and_diff_color(self, card2):
    #     return self.get_color() != card2.get_color() and self.get_value() + 1 == card2.get_value()

    def __hash__(self):
        return hash((self._color, self._suit, self._value))


def get_num_value(value_str):
    if value_str == "A":
        return 1
    elif value_str == "J":
        return 11
    elif value_str == "Q":
        return 12
    elif value_str == "K":
        return 13
    else:
        return int(value_str)


def get_str_value(value_num):
    if value_num == 1:
        return "A"
    elif value_num == 11:
        return "J"
    elif value_num == 12:
        return "Q"
    elif value_num == 13:
        return "K"
    else:
        return str(value_num)
