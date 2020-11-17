import copy
import time

class MoveType:
    REGULAR = 1
    WRAP = 2
    DIAGONAL = 3

class State:
    board = []
    path = []
    cost = 0
    cursor = -1
    history = []

    def __init__(self, board, path, cost, cursor, history):
        if len(board) != 8:
            raise Exception("Bad Board: wrong length") 
        self.board = board.copy()
        self.path = path.copy()
        self.cost = cost
        if cursor < 0 or cursor > 7:
            for n in range(8):
                if self.board[n] == 0:
                    self.cursor = n
                    break
        else:
            self.cursor = cursor
        self.history = history.copy()
    
    def __str__(self):
        return f'\nboard: {self.board}\npath: {self.path}\ncost: {self.cost}\ncursor: {self.cursor}\nhistory: {self.history}\n'

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        if isinstance(other, State):
            return self.board == other.board and self.path == other.path and self.history == other.history
        return False

    def move(self, swap_position, move_type):
        self.history.append(self.board.copy())
        swap_value = self.board[swap_position]
        self.path.append(swap_value)
        self.cost += move_type
        self.board[self.cursor], self.board[swap_position] = self.board[swap_position], self.board[self.cursor]
        self.cursor = swap_position

def is_solved(state):
    return state.board == [1,2,3,4,5,6,7,0] or state.board == [1,3,5,7,2,4,6,0]

def moves(state):
    new_states = []
    new_states.extend(regular_moves(state))
    new_states.extend(wrapping_moves(state))
    new_states.extend(diagonal_moves(state))

    new_states = cleanup_moves(new_states)

    return new_states

def regular_moves(state):
    if state.cursor == 0:
        new_state_1 = State(state.board, state.path, state.cost, state.cursor, state.history)
        new_state_1.move(state.cursor+1, MoveType.REGULAR)
        
        new_state_2 = State(state.board, state.path, state.cost, state.cursor, state.history)
        new_state_2.move(state.cursor+4, MoveType.REGULAR)
        return [new_state_1, new_state_2]
    if state.cursor == 1 or state.cursor == 2:
        new_state_1 = State(state.board, state.path, state.cost, state.cursor, state.history)
        new_state_1.move(state.cursor-1, MoveType.REGULAR)
        
        new_state_2 = State(state.board, state.path, state.cost, state.cursor, state.history)
        new_state_2.move(state.cursor+1, MoveType.REGULAR)

        new_state_3 = State(state.board, state.path, state.cost, state.cursor, state.history)
        new_state_3.move(state.cursor+4, MoveType.REGULAR)
        return [new_state_1, new_state_2, new_state_3]
    if state.cursor == 3:
        new_state_1 = State(state.board, state.path, state.cost, state.cursor, state.history)
        new_state_1.move(state.cursor-1, MoveType.REGULAR)
        
        new_state_2 = State(state.board, state.path, state.cost, state.cursor, state.history)
        new_state_2.move(state.cursor+4, MoveType.REGULAR)
        return [new_state_1, new_state_2]
    if state.cursor == 4:
        new_state_1 = State(state.board, state.path, state.cost, state.cursor, state.history)
        new_state_1.move(state.cursor+1, MoveType.REGULAR)
        
        new_state_2 = State(state.board, state.path, state.cost, state.cursor, state.history)
        new_state_2.move(state.cursor-4, MoveType.REGULAR)
        return [new_state_1, new_state_2]
    if state.cursor == 5 or state.cursor == 6:
        new_state_1 = State(state.board, state.path, state.cost, state.cursor, state.history)
        new_state_1.move(state.cursor-1, MoveType.REGULAR)
        
        new_state_2 = State(state.board, state.path, state.cost, state.cursor, state.history)
        new_state_2.move(state.cursor+1, MoveType.REGULAR)

        new_state_3 = State(state.board, state.path, state.cost, state.cursor, state.history)
        new_state_3.move(state.cursor-4, MoveType.REGULAR)
        return [new_state_1, new_state_2, new_state_3]
    if state.cursor == 7:
        new_state_1 = State(state.board, state.path, state.cost, state.cursor, state.history)
        new_state_1.move(state.cursor-1, MoveType.REGULAR)
        
        new_state_2 = State(state.board, state.path, state.cost, state.cursor, state.history)
        new_state_2.move(state.cursor-4, MoveType.REGULAR)
        return [new_state_1, new_state_2]

def wrapping_moves(state):
    if state.cursor == 0 or state.cursor == 4:
        new_state_1 = State(state.board, state.path, state.cost, state.cursor, state.history)
        new_state_1.move(state.cursor+3, MoveType.WRAP)
        return [new_state_1]
    if state.cursor == 3 or state.cursor == 7:
        new_state_1 = State(state.board, state.path, state.cost, state.cursor, state.history)
        new_state_1.move(state.cursor-3, MoveType.WRAP)
        return [new_state_1]
    return []

def diagonal_moves(state):
    if state.cursor == 0:
        new_state_1 = State(state.board, state.path, state.cost, state.cursor, state.history)
        new_state_1.move(state.cursor+5, MoveType.DIAGONAL)
        
        new_state_2 = State(state.board, state.path, state.cost, state.cursor, state.history)
        new_state_2.move(state.cursor+7, MoveType.DIAGONAL)
        return [new_state_1, new_state_2]
    if state.cursor == 1 or state.cursor == 2:
        new_state_1 = State(state.board, state.path, state.cost, state.cursor, state.history)
        new_state_1.move(state.cursor+3, MoveType.DIAGONAL)
        
        new_state_2 = State(state.board, state.path, state.cost, state.cursor, state.history)
        new_state_2.move(state.cursor+5, MoveType.DIAGONAL)
        return [new_state_1, new_state_2]
    if state.cursor == 3:
        new_state_1 = State(state.board, state.path, state.cost, state.cursor, state.history)
        new_state_1.move(state.cursor+1, MoveType.DIAGONAL)
        
        new_state_2 = State(state.board, state.path, state.cost, state.cursor, state.history)
        new_state_2.move(state.cursor+3, MoveType.DIAGONAL)
        return [new_state_1, new_state_2]
    if state.cursor == 4:
        new_state_1 = State(state.board, state.path, state.cost, state.cursor, state.history)
        new_state_1.move(state.cursor-1, MoveType.DIAGONAL)
        
        new_state_2 = State(state.board, state.path, state.cost, state.cursor, state.history)
        new_state_2.move(state.cursor-3, MoveType.DIAGONAL)
        return [new_state_1, new_state_2]
    if state.cursor == 5 or state.cursor == 6:
        new_state_1 = State(state.board, state.path, state.cost, state.cursor, state.history)
        new_state_1.move(state.cursor-3, MoveType.DIAGONAL)
        
        new_state_2 = State(state.board, state.path, state.cost, state.cursor, state.history)
        new_state_2.move(state.cursor-5, MoveType.DIAGONAL)
        return [new_state_1, new_state_2]
    if state.cursor == 7:
        new_state_1 = State(state.board, state.path, state.cost, state.cursor, state.history)
        new_state_1.move(state.cursor-5, MoveType.DIAGONAL)
        
        new_state_2 = State(state.board, state.path, state.cost, state.cursor, state.history)
        new_state_2.move(state.cursor-7, MoveType.DIAGONAL)
        return [new_state_1, new_state_2]

def cleanup_moves(new_states):
    clean_states = []
    for state in new_states:
        is_clean = True
        for old_state in state.history:
            if board_equals(old_state, state.board):
                is_clean = False
        if is_clean:
            clean_states.append(state)
    return clean_states

def board_equals(board_a, board_b):
    for i in range(8):
        if board_a[i] != board_b[i]:
            return False
    return True

def ucs(puzzle):
    search_path = []
    start_time = time.time()

    initial_state = State(puzzle, [], 0, -1, [])
    open_list = [initial_state]
    closed_list = []

    def h_uniform(state):
        return state.cost

    while len(open_list) > 0:
        open_list.sort(key=h_uniform)
        current_node = copy.deepcopy(open_list.pop(0))
        search_path.append(copy.deepcopy(current_node))

        if is_solved(current_node):
            return (current_node, search_path, (time.time() - start_time))

        if time.time() - start_time > 60:
            return (search_path)
        closed_list.append(current_node)

        new_nodes = moves(current_node)

        for new_node in new_nodes:
            in_closed_list = False
            for closed_node in closed_list:
                if board_equals(closed_node.board, new_node.board):
                    in_closed_list = True
                    if new_node.cost < closed_node.cost:
                        closed_node = new_node
                        break
            
            in_open_list = False
            for open_node in open_list:
                if board_equals(open_node.board, new_node.board):
                    in_open_list = True
                    if new_node.cost < open_node.cost:
                        open_node = new_node
                        break
            
            if not in_open_list and not in_closed_list:
                open_list.append(new_node)
    
    return []

def gbfs(puzzle, h):
    search_path = []
    start_time = time.time()
    initial_state = State(puzzle, [], 0, -1, [])
    
    open_list = [initial_state]
    closed_list = []

    while len(open_list) > 0:
        open_list.sort(key=h)
        current_node = copy.deepcopy(open_list.pop(0))
        search_path.append(copy.deepcopy(current_node))

        if is_solved(current_node):
            return (current_node, search_path, (time.time() - start_time))

        if time.time() - start_time > 60:
            return (search_path)

        closed_list.append(current_node)
        new_nodes = moves(current_node)

        for new_node in new_nodes:
            if new_node not in open_list and new_node not in closed_list:
                open_list.append(new_node)
    
    return []

def a_star(puzzle, h):
    search_path = []
    start_time = time.time()

    initial_state = State(puzzle, [], 0, -1, [])
    open_list = [initial_state]
    closed_list = []

    def h_star(state):
        return h(state) + state.cost

    while len(open_list) > 0:
        open_list.sort(key=h_star)
        current_node = copy.deepcopy(open_list.pop(0))
        search_path.append(copy.deepcopy(current_node))

        if is_solved(current_node):
            return (current_node, search_path, (time.time() - start_time))

        if time.time() - start_time > 60:
            return (search_path)
            
        closed_list.append(current_node)

        new_nodes = moves(current_node)

        for new_node in new_nodes:
            in_closed_list = False
            for closed_node in closed_list:
                if board_equals(closed_node.board, new_node.board):
                    in_closed_list = True
                    if new_node.cost < closed_node.cost:
                        closed_node = new_node
                        break
            
            in_open_list = False
            for open_node in open_list:
                if board_equals(open_node.board, new_node.board):
                    in_open_list = True
                    if new_node.cost < open_node.cost:
                        open_node = new_node
                        break
            
            if not in_open_list and not in_closed_list:
                open_list.append(new_node)
    
    return []

def h0(state):
    if state.cursor == 7:
        return 1
    else:
        return 0            

def h1(state):
    return min(board_difference(state.board, [1,2,3,4,5,6,7,0]), board_difference(state.board, [1,3,5,7,2,4,6,0]))

def h2(state):
    return min(manning_distance(state.board, [1,2,3,4,5,6,7,0]), manning_distance(state.board, [1,3,5,7,2,4,6,0]))

def manning_distance(board_a, solution):
    distance = 0
    for i in range(8):
        curr = board_a[i]
        t = 0
        for s in range(8):
            if solution[s] == curr:
                t = s
                break
        
        if i < 4 and t < 4:
            distance += (abs(i-t))
        elif i > 3 and t > 3:
            distance += (abs(i-t))
        else:
            i = i % 4
            t = t % 4
            distance +=(abs(i-t) + 1)
    return distance

# Testing shows that ignoring zero is actually worse
def board_difference(board_a, board_b, ignore_zero = False):
    difference = 0
    for i in range(8):
        if board_a[i] == 0 and not ignore_zero:
            continue
        if board_a[i] != board_b[i]:
            difference += 1
    return difference

def solve(puzzle):
    print("UCS")
    print(ucs(puzzle))

    print("GBFS h1")
    print(gbfs(puzzle, h1))

    print("A* h1")
    print(a_star(puzzle, h1))

    print("GBFS h2")
    print(gbfs(puzzle, h2))

    print("A* h2")
    print(a_star(puzzle, h2))

def main():
    print("Solutions for [3, 0, 1, 4, 2, 6, 5, 7]")
    solve([3, 0, 1, 4, 2, 6, 5, 7])
    
    print("Solutions for [6, 3, 4, 7, 1, 2, 5, 0]")
    solve([6, 3, 4, 7, 1, 2, 5, 0])
    
    print("Solutions for [1, 0, 3, 6, 5, 2, 7, 4]")
    solve([1, 0, 3, 6, 5, 2, 7, 4])

if __name__ == "__main__":
    main()