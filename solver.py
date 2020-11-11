class state:
    board = []
    path = []
    cost = 0
    cursor = -1

def is_solved(state):
    return state.board == [1,2,3,4,5,6,7,0] or state.board == [1,3,5,7,2,4,6,0]

def moves(state):
    new_states = []
    new_states.append(regular_moves(state))
    new_states.append(wrapping_moves(state))
    new_states.append(diagonal_moves(state))




