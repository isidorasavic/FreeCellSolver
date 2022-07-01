from Card import Card
from Solver import Solver
from FileHandler import read_file
from State import State

if __name__ == '__main__':
    initial_state = read_file("test1.txt")
    solver = Solver()
    solver.search(initial_state, "solution1.txt")

