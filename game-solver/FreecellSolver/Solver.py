from copy import deepcopy
import itertools
from queue import PriorityQueue
import time
from Move import Move
from FinalCell import FinalCell
from Utils import Suits
from colorama import init, Fore, Back, Style


# board = Suits.stack
# foundation = Suits.final_field


class FreeCell:
    n_free_cells = 4
    suits = ['P', 'H', 'T', 'K']
    parent = None

    def __init__(self, stacks=None, final_cells=None, free_spaces=None):
        self.stacks = stacks
        self.final_cells = final_cells or [FinalCell(suit) for suit in self.suits]
        self.free_spaces = free_spaces or [None] * self.n_free_cells

    def __cmp__(self, other):
        if len(self.free_spaces) != other.free_spaces():
            return False

        for card in self.free_spaces:
            if other.free_spaces.count(card) == 0:
                return False

        for i in range(4):
            if len(self.final_cells[i]) != len(other.final_cells[i]):
                return False

            if len(self.final_cells[i]) != 0 and len(other.final_cells[i]) != 0:
                if self.final_cells[i][-1] != other.final_cells[i][-1]:
                    return False

        for stack in self.stacks:
            if len(stack) != 0:
                card = stact[-1]
                for other_stack in other.stacks:
                    if len(other_stack) == 0:
                        return False
                    else:
                        if other_stack[-1] != card:
                            return -1
        return True

    def get_potential_moves(self):
        all_moves = []

        empty_column_indices = []
        for column_index, column in enumerate(self.stacks):
            if column:
                card = column[-1]

                # da li moze bilo sta iz steka da se prebaci u finalno polje
                for final_cell_index, final_cell in enumerate(self.final_cells):
                    if final_cell.check_deposit(card):
                        new_move = Move(Suits.stack, column_index, Suits.final_field, final_cell_index)
                        all_moves.append(new_move)
                # da li ima neko prazno polje
                if None in self.free_spaces:
                    new_move = Move(Suits.stack, column_index, Suits.freecell, self.free_spaces.index(None))
                    all_moves.append(new_move)
            else:
                empty_column_indices.append(column_index)

        for column_index, column in enumerate(self.stacks):
            previous_card = None
            for card_index, card in enumerate(reversed(column)):
                move_depth = card_index + 1
                if move_depth > self.n_movable_cards():
                    break

                if previous_card and (card.get_color() == previous_card.get_color() or
                                      card.get_value() != previous_card.get_value() + 1):
                    break

                for to_col_index, to_column in enumerate(self.stacks):
                    if column_index == to_col_index:
                        continue
                    if to_column:
                        to_col_card = to_column[-1]
                        if card.get_color() != to_col_card.get_color() and \
                                card.get_value() == to_col_card.get_value() - 1:
                            all_moves.append(
                                Move(Suits.stack, column_index, Suits.stack, to_col_index, move_depth=move_depth))
                    else:
                        all_moves.append(
                            Move(Suits.stack, column_index, Suits.stack, to_col_index, move_depth=move_depth))
                previous_card = card

        for free_space_index, card in enumerate(self.free_spaces):
            if card is None:
                continue
            for to_col_index, to_column in enumerate(self.stacks):
                if to_column:
                    to_col_card = to_column[-1]
                    if card.get_color() != to_col_card.get_color() and card.get_value() == to_col_card.get_value() - 1:
                        all_moves.append(Move(Suits.freecell, free_space_index, Suits.stack, to_col_index))
                else:
                    all_moves.append(Move(Suits.freecell, free_space_index, Suits.stack, to_col_index))

        return sorted(all_moves, key=lambda m: (m.priority, -m.move_depth))

    def execute_move(self, move):

        # sa steka na stek
        if move.from_location == Suits.stack and move.to_location == Suits.stack:
            self.stacks[move.to_index].extend(self.stacks[move.from_index][-move.move_depth:])
            self.stacks[move.from_index] = self.stacks[move.from_index][:-move.move_depth:]
        # sa steka na prazno polje
        elif move.from_location == Suits.stack and move.to_location == Suits.freecell:
            self.free_spaces[move.to_index] = self.stacks[move.from_index][-move.move_depth]
            self.stacks[move.from_index] = self.stacks[move.from_index][:-move.move_depth:]
        # sa stela na finalno polje
        elif move.from_location == Suits.stack and move.to_location == Suits.final_field:
            self.final_cells[move.to_index].deposit(self.stacks[move.from_index][-move.move_depth])
            self.stacks[move.from_index] = self.stacks[move.from_index][:-move.move_depth:]
        # sa praznog polja na stek
        elif move.from_location == Suits.freecell and move.to_location == Suits.stack:
            self.stacks[move.to_index].append(self.free_spaces[move.from_index])
            self.free_spaces[move.from_index] = None
        # sa praznog polja na finalno polje
        elif move.from_location == Suits.freecell and move.to_location == Suits.final_field:
            self.final_cells[move.to_index].deposit(self.free_spaces[move.from_index][-move.move_depth])
            self.free_spaces[move.from_index] = None
        # sa finalnog polja na stek
        elif move.from_location == Suits.final_field and move.to_location == Suits.stack:
            self.stacks[move.from_index][-move.move_depth] = self.final_cells[move.from_index].withdraw()
        # sa finalnog polja na prazno polje
        elif move.from_location == Suits.final_field and move.to_location == Suits.freecell:
            self.free_spaces[move.to_index] = self.foundations[move.from_index].withdraw()
        else:
            raise Exception(f'error')

    def check_win(self):
        if self.free_spaces.count(None) != 4:
            return False

        for stack in self.stacks:
            if len(stack) != 0:
                return False
        return True

    def n_movable_cards(self):
        num_free_columns = sum(map(lambda col: len(col) == 0, self.stacks))
        num_free_spaces = self.free_spaces.count(None)
        return (2 ** num_free_columns) * (num_free_spaces + 1)

    def generate_hash(self):
        return hash(f"{str(self.free_spaces)} {str(self.final_cells)} {str(self.stacks)}")

    def print_solution(self):
        print(''.join("[ ]" if space is None else str(space) for space in self.free_spaces) + '|' + ''.join(
            str(f) for f in self.final_cells))
        print('=' * 25)
        max_len = 0
        for column in self.stacks:
            max_len = max(max_len, len(column))
        for row_index in range(max_len):
            row = []
            for column in self.stacks:
                if len(column) - 1 < row_index:
                    row.append(' ' * 3)
                else:
                    row.append(str(column[row_index]))
            print(''.join(row))

    def copy(self):
        return FreeCell(stacks=deepcopy(self.stacks), final_cells=deepcopy(self.final_cells),
                        free_spaces=deepcopy(self.free_spaces))

    def heuristic(self):
        score = 0
        for foundation in self.final_cells:
            top_card = foundation.peek()
            if top_card:
                score -= 100 * top_card.get_value()

        for free_space in self.free_spaces:
            if free_space is None:
                score -= 10

        for column in self.stacks:
            if column and column[0].get_value() == 13:
                score -= 5

        return score

    def solve(self):
        begin_time = time.time()
        visited = set()

        counter = itertools.count()
        pqueue = PriorityQueue()
        pqueue.put((1, 1, self.copy()))
        count = 0
        max_queue_size = 1
        while pqueue:
            max_queue_size = max(max_queue_size, pqueue.qsize())
            _, _, state = pqueue.get()
            state_hash = state.generate_hash()

            if state.check_win():
                print(f'Solved in {round(time.time() - begin_time, 2)} seconds')
                print(f'Expanded {count} nodes, with a maximum queue size of {max_queue_size}')
                solution = []
                parent = state.parent
                while parent:
                    solution.append(parent)
                    parent = parent.parent
                return list(reversed(solution))

            if state_hash in visited:
                continue
            #
            # if self in visited:
            #     continue

            visited.add(state_hash)
            # visited.add(self)
            potential_moves = state.get_potential_moves()
            for move in potential_moves:
                state_copy = state.copy()
                state_copy.parent = state
                state_copy.execute_move(move)
                clone_hash = state_copy.generate_hash()
                count += 1

                if clone_hash not in visited:
                    pqueue.put((state_copy.heuristic(), next(counter), state_copy))
        return False
