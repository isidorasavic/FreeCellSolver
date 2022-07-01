from FileHandler import write_file


class Solution:
    solution = []  # solution je lista stanja od pocetka do kraja kao
    file = ""

    def __init__(self, last_state, file, solution_found):
        if solution_found is True:
            self.file = file
            self.extract_solution(last_state)
            self.print_solution()
            self.write_to_file()

    def extract_solution(self, last_state):
        parent = last_state
        while parent is not None:
            self.solution.append(parent)
            parent = parent.parent
        reversed(self.solution)
        del(self.solution[0])

    def print_solution(self):
        print("Total steps: " + str(len(self.solution)) + "\n")

    def write_to_file(self):
        write_file(self.file, self.solution)