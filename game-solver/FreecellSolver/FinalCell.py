from colorama import init, Fore, Back, Style


class FinalCell(object):
    suit = ''  # K, P, H ili  T
    cards = []

    def __init__(self, suit):
        self.suit = suit
        self.cards = []

    def __str__(self):
        if len(self.cards) == 0:
            return "[]"
        return f"[{str(self.peek())[:-1]}]"

    # gledamo sta je poslednja dodata karta
    def peek(self):
        if len(self.cards) != 0:
            return self.cards[-1]
        return None

    def check_withdraw(self):
        return bool(self.cards)

    def check_deposit(self, card):
        if card.get_suit() == self.suit:
            if len(self.cards) == 0:
                if card.get_value() == 1:
                    return True
                else:
                    return False
            if card.get_value() == self.peek().get_value() + 1:
                return True
        return False

    def deposit(self, card):
        self.cards.append(card)

    def withdraw(self):
        return self.cards.pop()

    def ncards(self):
        return len(self.cards)
