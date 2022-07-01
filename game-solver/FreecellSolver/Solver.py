from time import *
from Utils import Suits
from Solution import Solution
from colorama import init, Fore, Back, Style


class Solver:

    nodes = None
    current_state = None

    def __init__(self):
        self.nodes = SortedNodesList()

    def search(self, initial_state, output_file):

        # mapa koja cuva cvorove koje smo obisli vec
        visited_states = {}

        solution_found = False

        num_of_searched_nodes = 0
        self.nodes.add_node(initial_state)

        print("Start searching......\n")

        current_node = None

        tic = time()  # merac vremena koje je proslo od pocetka resavanja igre
        toc = time()
        while  toc - tic < Suits.limit and self.nodes.size() != 0 and solution_found is False:  # toc - tic < Suits.limit and
            # trazimo sledeci cvor za analizu
            current_node = self.nodes.get_first()

            # ne obilazimo ga opet ako je vec obidjen
            if visited_states.get(current_node) is not None:
                continue
            # ako ga nismo obisli dodajemo ga u listu
            visited_states[current_node] = True

            # ako je stanje finalno zavrsavamo igru
            if current_node.is_solved():
                solution_found = True
                break
            else:
                # ako nismo nasli resenje pretrazujemo decu trenutnog stanja
                children = current_node.get_children()
                for child in children:
                    if visited_states.get(child) is None:
                        self.nodes.add_node(child)
                        # print(f"added node: {str(child)}")

                num_of_searched_nodes += 1
            if num_of_searched_nodes % 2 == 0:
                toc = time()
                print(f"time: {toc-tic}")

        Solution(current_node, output_file, solution_found)

        # for i in range(len(self.nodes.nodes)):
        #     print(str(self.nodes.nodes[i]))

        if solution_found:
            print(Fore.GREEN + "Solution found :)")
        else:
            print(Fore.RED + "Solution not found :(")
        print("Time elapsed: ", toc - tic)
        print("Nodes visited: ", len(visited_states))
        print("Nodes expanded: ", num_of_searched_nodes)
        print("Nodes in frontier: ", self.nodes.size())

        nodes = None
        current_node = None


# klasa koja ce da glumi TreeSet iz jave
class SortedNodesList:
    nodes = []

    def size(self):
        return len(self.nodes)

    def add_node(self, node):
        self.nodes.append(node)
        self.sort()

    def sort(self):
        for i in range(len(self.nodes)):

            # Find the minimum element in remaining
            # unsorted array
            min_idx = i
            for j in range(i + 1, len(self.nodes)):
                if self.nodes[min_idx].compare_to(self.nodes[j]) >= 0:
                    min_idx = j

            # Swap the found minimum element with
            # the first element
            self.nodes[i], self.nodes[min_idx] = self.nodes[min_idx], self.nodes[i]

    def get_first(self):
        node = self.nodes[0]
        self.nodes.remove(node)
        return node
