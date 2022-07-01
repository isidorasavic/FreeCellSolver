class Suits:
    karo = 0
    pik = 1
    tref = 2
    herc = 3

    final_field = "final_field"
    stack = "stack"
    freecell = "freecell"
    newstack = "newstack"

    black = "black"
    red = "red"

    limit = 300  # igra ce da se resava maks ovoliko sekundi

    N = 0


def get_final_field(state, suit):
    final_field = None
    if suit == "K":
        final_field = state.final_fields[Suits.karo]
    elif suit == "P":
        final_field = state.final_fields[Suits.pik]
    elif suit == "T":
        final_field = state.final_fields[Suits.tref]
    elif suit == "H":
        final_field = state.final_fields[Suits.herc]
    else:
        raise Exception("Invalid suit!")

    return final_field


def get_final_field_id(state, suit):
    final_field_id = -1
    if suit == "K":
        final_field_id = Suits.karo
    elif suit == "P":
        final_field_id = Suits.pik
    elif suit == "T":
        final_field_id = Suits.tref
    elif suit == "H":
        final_field_id = Suits.herc
    else:
        raise Exception("Invalid suit!")

    return final_field_id
