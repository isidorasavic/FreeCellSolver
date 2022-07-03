from Solver import FreeCell
from FileHandler import read_file


if __name__ == '__main__':
    file_name = "game3"
    initial_state, num_of_cards = read_file(f"{file_name}.txt")

    game = FreeCell(stacks=initial_state)

    solution = game.solve()

    print('Number of turns in solution:', len(solution))

    for i in range(len(solution)):
        state = solution[i]
        state.print_solution()
        print(f'--------------- {i+1}. move ---------------')

