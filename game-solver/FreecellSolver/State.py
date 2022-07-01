from collections import deque
import copy

import Utils
from Utils import *


def get_worth_of_card_reversed(card):
    return abs(Suits.N - card.get_value())


def wrong_order_of_cards_penalty(stack):
    penalty = 0
    difference = 0
    if len(stack) > 0:
        for i in range(len(stack) - 1):
            difference = stack[i].get_value() - stack[i+1].get_value()
            if (stack[i].get_color() == stack[i+1].get_color() and difference == 1) is False:
                penalty += 1
    return penalty


class State:
    freecells = []  # lista za karte koje se nalaze u 4 slobodna polja
    final_fields = []  # lista za karte koje su slozene u finalna polja
    stacks = []  # lista karata u 8 kolona
    pair = {}  # recnik karata i gde se nalaze
    move = ""  # potez koji je doveo do ovog stanja

    _g = 0
    _h = 0
    _f = 0

    parent = None  # predhodno stanje

    def __init__(self):
        self.freecells = []
        self.final_fields = []
        self.stacks = []
        # dodajemo cetiri steka za cetiri finalna polja, i 8 stekova za kolone karata
        for i in range(4):
            self.final_fields.append(deque())
            self.stacks.append(deque())
            self.stacks.append(deque())

    def __str__(self):
        ret_val = ""
        ret_val += "State:\n"

        ret_val += f"Freecells: {str(self.freecells)} \n"
        ret_val += "\n"
        ret_val += "Foundations: \n"
        for stack in self.final_fields:
            ret_val += f"{str(stack)}\n"
        ret_val += "Stacks: \n"
        stack_num = 1
        for stack in self.stacks:
            ret_val += f"Stack num {stack_num}  "
            for card in stack:
                ret_val += f" {str(card)} "
            ret_val += "\n"
            stack_num += 1

        if self.get_f() > 0:
            ret_val += f"F: {self.get_f()}\n"

        if self.get_g() > 0:
            ret_val += f"G: {self.get_g()}\n"
        if self.get_h() > 0:
            ret_val += f"H: {self.get_g()}\n "

        ret_val += "End of state"

        return ret_val

    def __hash__(self):
        ret_tuple = tuple(self.freecells)
        for field in self.final_fields:
            lista = []
            for card in field:
                lista.append(card)
            ret_tuple += tuple(lista)
        for stack in self.stacks:
            lista = []
            for card in stack:
                lista.append(card)
            ret_tuple += tuple(lista)
        lista = None
        return hash(ret_tuple)

    # poredimo dva stanja da li su ista
    def __eq__(self, state2):
        if state2 is None:
            return False
        if len(self.freecells) != len(state2.freecells):
            return False

        # proveravamo da li su karte u slobodnim poljima iste, nije bitno koja je gde
        for card in self.freecells:
            if state2.freecells.count(card) == 0:
                return False

        # sad proveravamo da li su u finalnim poljima iste karte
        for i in range(4):
            if len(self.final_fields[i]) != len(state2.final_fields[i]):
                return False
            for card in self.final_fields[i]:
                if state2.final_fields[i].count(card) == 0:
                    return False

        # na kraju proveravamo da li su u svih 8 kolona iste karte
        for i in range(8):
            if len(self.stacks[i]) != len(state2.stacks[i]):
                return False

            if len(self.stacks[i]) != 0 and len(state2.stacks[i]) != 0 and self.stacks[i][-1] != state2.stacks[i][-1]:
                return False

        return True

    def compare_to(self, other):
        if self.get_f() > other.get_f():
            return 1
        elif self.get_f() < other.get_f():
            return -1

        else:
            if self.get_g() < other.get_g():
                return -1
        return 1

    # metoda za poredjenje dva stanja
    #  0 ako su ista
    # -1 ako je self manji od state2
    #  1 ako je state2 manji od self

    # metoda za kopiranje stanja
    def __copy__(self):
        state = State()

        for card in self.freecells:
            state.freecells.append(copy.copy(card))
            state.pair[card] = Suits.freecell

        for i in range(4):
            for card in self.final_fields[i]:
                state.final_fields[i].append(copy.copy(card))
                state.pair[card] = Suits.final_field

        for i in range(8):
            for card in self.stacks[i]:
                state.stacks[i].append(copy.copy(card))
                state.pair[card] = Suits.stack

        return state

    def move_to_freecell(self, card):
        self.remove_card_from_position(card)

        self.freecells.append(card)
        self.pair[card] = Suits.freecell
        return True

    def move_to_stack(self, card, stack_id):
        self.remove_card_from_position(card)

        self.stacks[stack_id].append(card)
        self.pair[card] = Suits.stack
        return True

    def move_to_final_field(self, card, field_id):
        self.remove_card_from_position(card)

        self.final_fields[field_id].append(card)
        self.pair[card] = Suits.final_field
        return True

    def freecell_can_move(self):
        return len(self.freecells) < 4

    def final_field_can_move(self, card, final_field_id):
        if len(self.final_fields[final_field_id]) == 0 and card.get_value() == 1:
            return True

        if len(self.final_fields[final_field_id]) != 0 and \
                card.is_larger_and_same_suit(self.final_fields[final_field_id][-1]):
            return True

        return False

    def stack_can_move(self, card, stack_id):
        if len(self.stacks[stack_id]) == 0:
            return True
        if card.is_smaller_and_diff_color(self.stacks[stack_id][-1]):
            return True
        return False

    def is_solved(self):
        if len(self.freecells) != 0:
            return False

        for i in range(8):
            if len(self.stacks[i]) != 0:
                return False

        for i in range(4):
            previous_card = None
            for card in self.final_fields[i]:
                if previous_card is None:
                    previous_card = card
                else:
                    if previous_card.get_suit() != card.get_suit() or previous_card.get_value() >= card.get_value():
                        return False

        return True

    # TODO: pop() ili remove(card)
    def remove_card_from_position(self, card):
        if self.pair[card] == Suits.freecell:
            self.freecells.remove(card)
        elif self.pair[card] == Suits.stack:
            for stack in self.stacks:
                if len(stack) != 0 and stack[-1] == card:
                    stack.pop()
                    break
        elif self.pair[card] == Suits.final_field:
            final_field = Utils.get_final_field(self, card.get_suit())
            final_field.remove(card)

    # pronalazimo sve poteze koji su moguci da se izvrse iz trenutnog stanja
    # za svaki potez zapravo pravimo novo stanje i stavljamo ga u listu
    # lista ovde nece biti doubly-linked-list kao u javi, ali valjda ce raditi svakako
    def get_children(self):
        children = []  # lista u kojoj ce se cuvati stanja
        children = children + self.get_states_from_final_cell_to_other()
        children = children + self.get_states_from_stack_to_other()
        children = children + self.get_states_from_freecell_to_other()
        return children

    def expanded_to_freecell(self, card):
        child_state = None
        if self.freecell_can_move():
            child_state = copy.copy(self)
            child_state.move_to_freecell(card)
            child_state.parent = self
            child_state.set_h(self.heuristics_function())
            child_state.set_f(self)
            child_state.move = f"{Suits.freecell} {str(card)}"
        return child_state

    def expanded_to_final_cell(self, card, final_cell_id):
        child_state = None
        if self.final_field_can_move(card, final_cell_id):
            child_state = copy.copy(self)
            child_state.move_to_final_field(card, final_cell_id)
            child_state.parent = self
            child_state.set_h(self.heuristics_function())
            child_state.set_f(self)
            child_state.move = f"{Suits.final_field} {str(card)}"
        return child_state

    def get_states_from_final_cell_to_other(self):
        children = []
        # prolazimo kroz 4 finalna polja
        for i in range(4):
            if len(self.final_fields[i]) == 0:  # ako je polje prazno idemo dalje
                continue

            card_to_move = copy.copy(self.final_fields[i][-1])
            a_state = self.expanded_to_freecell(card_to_move)

            if a_state is not None:
                children.append(a_state)

            has_moved_to_new_stack = False
            for j in range(8):
                if self.stack_can_move(card_to_move, j):
                    if len(self.stacks[j]) == 0 and has_moved_to_new_stack:
                        continue

                    child_state = copy.copy(self)
                    child_state.move_to_stack(card_to_move, j)
                    child_state.set_parent(self)
                    child_state.set_h(child_state.heuristics_function())
                    child_state.set_f(child_state)

                    if len(self.stacks[j]) == 0:
                        child_state.move = f"{Suits.newstack} {str(card_to_move)}"
                        has_moved_to_new_stack = True
                    else:
                        child_state.move = f"{Suits.stack} {str(card_to_move)} {str(self.stacks[j][-1])}"
                    children.append(child_state)
                    child_state = None

        return children

    def get_states_from_stack_to_other(self):
        children = []
        for i in range(8):
            if len(self.stacks[i]) == 0:
                continue
            card_to_move = copy.copy(self.stacks[i][-1])

            has_moved_to_new_stack = False

            child_state = None

            child_state = self.expanded_to_final_cell(card_to_move, Utils.get_final_field_id(self, card_to_move.get_suit()))

            if child_state is not None:
                children.append(child_state)

            child_state = None

            for j in range(8):
                if i == j:
                    continue
                if len(self.stacks[i]) == 1 and len(self.stacks[j]) == 0:
                    continue
                if self.stack_can_move(card_to_move, j):
                    if len(self.stacks[j]) == 0 and has_moved_to_new_stack:
                        continue

                    child_state = copy.copy(self)
                    child_state.move_to_stack(card_to_move, j)
                    child_state.set_parent(self)
                    child_state.set_h(child_state.heuristics_function())
                    child_state.set_f(child_state)
                    if len(self.stacks[j]) == 0:
                        child_state.move = Suits.newstack + " " + str(card_to_move)
                        has_moved_to_new_stack = True
                    else:
                        child_state.move = Suits.stack + " " + str(card_to_move) + " " + str(self.stacks[j][-1])

                    children.append(child_state)
                    child_state = None

            child_state = self.expanded_to_freecell(card_to_move)
            if child_state is not None:
                children.append(child_state)

        return children

    def get_states_from_freecell_to_other(self):
        children = []
        if len(self.freecells) == 0:
            return children

        for card in self.freecells:
            card_to_move = copy.copy(card)
            has_moved_to_new_stack = False

            child_state = self.expanded_to_final_cell(card_to_move, Utils.get_final_field_id(self, card_to_move.get_suit()))

            if child_state is not None:
                children.append(child_state)

            child_state = None

            for i in range(8):
                if self.stack_can_move(card_to_move, i):
                    if len(self.stacks[i]) == 0 and has_moved_to_new_stack:
                        continue

                    child_state = copy.copy(self)

                    child_state.move_to_stack(card_to_move, i)
                    child_state.set_parent(self)
                    child_state.set_h(child_state.heuristics_function())
                    child_state.set_f(child_state)
                    if len(self.stacks[i]) == 0:
                        child_state.move = Suits.newstack + " " + str(card_to_move)
                        has_moved_to_new_stack = True
                    else:
                        child_state.move = Suits.stack + " " + str(card_to_move) + " " + str(self.stacks[i][-1])

                    children.append(child_state)
                    child_state = None

            return children

    def heuristics_function(self):
        cards_not_in_final_cells_score = 0
        cards_wrong_order_score = 0

        for card in self.freecells:
            cards_not_in_final_cells_score += get_worth_of_card_reversed(card)

        for stack in self.stacks:
            for card in stack:
                cards_not_in_final_cells_score += get_worth_of_card_reversed(card)

        for stack in self.stacks:
            cards_wrong_order_score += wrong_order_of_cards_penalty(stack)

        return abs(0.95 * cards_not_in_final_cells_score + 0.05 * cards_wrong_order_score)

    def set_f(self, state):
        self._f = state.get_h() + state.get_g()
        # pass

    def set_parent(self, parent):
        self.parent = parent
        self.set_g(parent.get_g() + 1)

    def set_h(self, h):
        self._h = h

    def get_h(self):
        return self._h

    def set_g(self, g):
        self._g = g

    def get_g(self):
        return self._g

    def get_f(self):
        return self._f


