from State import State
from Card import Card
from Utils import Suits


def read_file(file_name):
    state = State()

    f = open("games\\" + file_name, "r")
    line = f.readline()

    num_of_cards = 0
    while line != "":
        brojac = 0
        cards = line.split(" ")
        print_string = ""
        for card in cards:
            num_of_cards += 1
            suit = card[0]
            number = card[1:]
            if number[-1:] == "\n":
                number = number[:-1]
            new_card = Card(suit, number)

            state.stacks[brojac].append(new_card)
            state.pair[new_card] = Suits.stack
            brojac += 1
            print_string += str(new_card)+" "
        # brojac += 1
        line = f.readline()
        print(print_string)

    Suits.N = num_of_cards / 4
    f.close()
    print("Number of cards: ", num_of_cards)

    return state


def write_file(file_name, solution):
    f = open("solutions\\" + file_name, "w")

    f.write(f"{len(solution)}\n")
    for state in solution:
        f.write(f"{state.move}\n")

    f.close()

