from Utils import Suits

class Move(object):
    from_location = None
    from_index = 0
    to_location = None
    to_index = 0
    move_depth = None
    priority = 0

    def __init__(self, from_location, from_index, to_location, to_index, move_depth=1):
        self.from_location = from_location
        self.from_index = from_index
        self.to_location = to_location
        self.to_index = to_index
        self.move_depth = move_depth
        move_cost = {
            Suits.stack: {
                Suits.stack: 5,
                Suits.final_field: 1,
                Suits.freecell: 7
            },
            Suits.freecell: {
                Suits.stack: 3,
                Suits.final_field: 2,
            },
            Suits.final_field: {
                Suits.stack: 10
            }
        }
        self.priority = move_cost[self.from_location][self.to_location]
