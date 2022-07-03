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

    def __init__(self, board=None, foundations=None, free_spaces=None):
        self.board = board
        self.foundations = foundations or [FinalCell(suit) for suit in self.suits]
        self.free_spaces = free_spaces or [None] * self.n_free_cells

    def get_potential_moves(self):
        all_moves = []

        empty_column_indices = []
        for column_index, column in enumerate(self.board):
            if column:
                card = column[-1]

                # see if you can move anything into the foundation
                for foundation_index, foundation in enumerate(self.foundations):
                    if foundation.check_deposit(card):
                        new_move = Move(Suits.stack, column_index, Suits.final_field, foundation_index)
                        all_moves.append(new_move)
                # you can add any cards to the free space
                if None in self.free_spaces:
                    # print(self.free_spaces)
                    new_move = Move(Suits.stack, column_index, Suits.freecell, self.free_spaces.index(None))
                    all_moves.append(new_move)
            else:
                empty_column_indices.append(column_index)

        for column_index, column in enumerate(self.board):
            previous_card = None
            for card_index, card in enumerate(reversed(column)):
                move_depth = card_index + 1
                if move_depth > self.n_movable_cards():
                    break

                if previous_card and (card.get_color() == previous_card.get_color() or
                                      card.get_value() != previous_card.get_value() + 1):
                    break

                for to_col_index, to_column in enumerate(self.board):
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
                # end of column loop

        for free_space_index, card in enumerate(self.free_spaces):
            if card is None:
                continue
            for to_col_index, to_column in enumerate(self.board):
                if to_column:
                    to_col_card = to_column[-1]
                    if card.get_color() != to_col_card.get_color() and card.get_value() == to_col_card.get_value() - 1:
                        all_moves.append(Move(Suits.freecell, free_space_index, Suits.stack, to_col_index))
                else:
                    all_moves.append(Move(Suits.freecell, free_space_index, Suits.stack, to_col_index))

        return sorted(all_moves, key=lambda m: (-m.move_depth, m.priority))

    def execute_move(self, move):

        if move.from_location == Suits.stack and move.to_location == Suits.stack:
            self.board[move.to_index].extend(self.board[move.from_index][-move.move_depth:])
            self.board[move.from_index] = self.board[move.from_index][:-move.move_depth:]
        elif move.from_location == Suits.stack and move.to_location == Suits.freecell:
            self.free_spaces[move.to_index] = self.board[move.from_index][-move.move_depth]
            self.board[move.from_index] = self.board[move.from_index][:-move.move_depth:]
        elif move.from_location == Suits.stack and move.to_location == Suits.final_field:
            self.foundations[move.to_index].deposit(self.board[move.from_index][-move.move_depth])
            self.board[move.from_index] = self.board[move.from_index][:-move.move_depth:]
        elif move.from_location == Suits.freecell and move.to_location == Suits.stack:
            self.board[move.to_index].append(self.free_spaces[move.from_index])
            self.free_spaces[move.from_index] = None
        elif move.from_location == Suits.freecell and move.to_location == Suits.final_field:
            self.foundations[move.to_index].deposit(self.free_spaces[move.from_index][-move.move_depth])
            self.free_spaces[move.from_index] = None
        elif move.from_location == Suits.final_field and move.to_location == Suits.stack:
            self.board[move.from_index][-move.move_depth] = self.foundations[move.from_index].withdraw()
        elif move.from_location == Suits.final_field and move.to_location == Suits.freecell:
            self.free_spaces[move.to_index] = self.foundations[move.from_index].withdraw()
        else:
            raise Exception(f'Invalid Move Type {move.move_type}')

    def check_win(self):
        return all(foundation.peek() and foundation.peek().get_value() == Suits.N for foundation in self.foundations)

    def n_movable_cards(self):
        num_free_columns = sum(map(lambda col: len(col) == 0, self.board))
        num_free_spaces = self.free_spaces.count(None)
        return (2 ** num_free_columns) * (num_free_spaces + 1)

    def generate_hash(self):
        return hash(f"{str(self.free_spaces)} {str(self.foundations)} {str(self.board)}")

    def print_solution(self):
        print(''.join("[ ]" if space is None else str(space) for space in self.free_spaces) + '|' + ''.join(
            str(f) for f in self.foundations))
        print('=' * 25)
        max_len = 0
        for column in self.board:
            max_len = max(max_len, len(column))
        for row_index in range(max_len):
            row = []
            for column in self.board:
                if len(column) - 1 < row_index:
                    row.append(' ' * 3)
                else:
                    row.append(str(column[row_index]))
            print(''.join(row))

    def copy(self):
        return FreeCell(board=deepcopy(self.board), foundations=deepcopy(self.foundations),
                        free_spaces=deepcopy(self.free_spaces))

    def heuristic(self):
        score = 0
        for foundation in self.foundations:
            top_card = foundation.peek()
            if top_card:
                score -= 100 * top_card.get_value()

        for free_space in self.free_spaces:
            if free_space is None:
                score -= 10

        for column in self.board:
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

            visited.add(state_hash)
            for move in state.get_potential_moves():
                state_copy = state.copy()
                state_copy.parent = state
                state_copy.execute_move(move)
                clone_hash = state_copy.generate_hash()
                count += 1

                if clone_hash not in visited:
                    pqueue.put((state_copy.heuristic(), next(counter), state_copy))
        return False
