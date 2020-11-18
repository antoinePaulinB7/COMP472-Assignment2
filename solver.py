import copy
import time
import os
import sys
import random

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
        self.path.append((swap_value, move_type))
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

    def g_uniform(state):
        return state.cost

    while len(open_list) > 0:
        open_list.sort(key=g_uniform)
        current_node = copy.deepcopy(open_list.pop(0))
        
        g_value = current_node.cost
        h_value = 0
        f_value = g_value+h_value
        search_path.append((f_value, g_value, h_value, copy.deepcopy(current_node.board)))

        if is_solved(current_node):
            return (current_node, search_path, (time.time() - start_time))

        if time.time() - start_time > 60:
            return [(search_path)]
        
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

        g_value = 0
        h_value = h(current_node)
        f_value = g_value+h_value
        search_path.append((f_value, g_value, h_value, copy.deepcopy(current_node.board)))

        if is_solved(current_node):
            return (current_node, search_path, (time.time() - start_time))

        if time.time() - start_time > 60:
            return [(search_path)]

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

        g_value = current_node.cost
        h_value = h(current_node)
        f_value = g_value+h_value
        search_path.append((f_value, g_value, h_value, copy.deepcopy(current_node.board)))

        if is_solved(current_node):
            return (current_node, search_path, (time.time() - start_time))

        if time.time() - start_time > 60:
            return [(search_path)]
            
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

def solve_and_output(puzzle, puzzle_number = "test"):
    print("solving with ucs...")
    output_files(ucs(puzzle), puzzle_number, "ucs")
    
    print("solving with gbfs h1...")
    output_files(gbfs(puzzle, h1), puzzle_number, "gbfs-h1")

    print("solving with astar h1...")
    output_files(a_star(puzzle, h1), puzzle_number, "astar-h1")
    
    print("solving with gbfs h2...")
    output_files(gbfs(puzzle, h2), puzzle_number, "gbfs-h2")

    print("solving with astar h2...")
    output_files(a_star(puzzle, h2), puzzle_number, "astar-h2")


def output_files(result, puzzle_number, algo, directory = "results/"):
    puzzle_number = str(puzzle_number)

    if not os.path.exists(directory):
        os.makedirs(directory)

    f_solution = open(directory+puzzle_number+"_"+algo+"_solution.txt", "w")
    f_search = open(directory+puzzle_number+"_"+algo+"_search.txt", "w")

    solution = None
    search_path = []
    time_to_solve = 0

    if len(result) == 3:
        solution = result[0]
        search_path = result[1]
        time_to_solve = result[2]
    elif len(result) == 1:
        search_path = result[0]
        solution = None
    else:
        f_solution.close()
        f_search.close()

        print(solution)
        print("Solution is malformed")

        return

    if solution is None:
        f_solution.write("no solution")
    else:
        board_string = board_to_str(solution.history[0])
        f_solution.write("%d %d %s\n" % (0, 0, board_string))

        index = 1

        for (tile, cost) in solution.path:
            if index < len(solution.history):
                board_string = board_to_str(solution.history[index])
            else:
                board_string = board_to_str(solution.board)
            f_solution.write("%d %d %s\n" % (tile, cost, board_string))
            index += 1
        
        f_solution.write("%d %f" % (solution.cost, time_to_solve))

    for (f, g, n, board) in search_path:
        f_search.write("%d %d %d %s\n" % (f, g, n, board_to_str(board)))

    f_solution.close()
    f_search.close()

def board_to_str(board):
    string = ""

    for i in range(len(board) - 1):
        string += str(board[i]) + " "
    string += str(board[-1])

    return string

def str_to_board(string):
    board = [int(i) for i in string.split() if i.isdigit()]

    if len(board) == 8:
        return board
    else:
        return None

def solve_from_file(filename):
    file = open(filename, "r")

    puzzle_number = 0

    for (i, puzzle_str) in enumerate(file):
        print("Solving " + puzzle_str)
        solve_and_output(str_to_board(puzzle_str), i)

def validate_puzzle(puzzle):
    valid = True
    error = ""
    if len(puzzle) != 8:
        error += "wrong length\n"
        valid = False
    
    tester = [0, 0, 0, 0, 0, 0, 0, 0]
    
    for i in puzzle:
        tester[i] += 1

    for i in range(len(tester)):
        if tester[i] != 1:
            valid = False
            error += ("Number of %d: %d\n" % (i, tester[i]))

    if valid:
        print("Puzzle is valid")
    else:
        print("Puzzle is invalid!")
        print(error)

    return valid

def generate_puzzles(filename, quantity = 50):
    puzzle = [1, 2, 3, 4, 5, 6, 7, 0]
    
    file = open(filename, "w")

    print("Generating puzzle and writing file")
    for i in range(quantity):
        random.shuffle(puzzle)
        print(puzzle)
        file.write(board_to_str(puzzle)+"\n")

    file.close()
    

def main():
    # print("Solutions for [3, 0, 1, 4, 2, 6, 5, 7]")
    # solve([3, 0, 1, 4, 2, 6, 5, 7])
    
    # print("Solutions for [6, 3, 4, 7, 1, 2, 5, 0]")
    # solve([6, 3, 4, 7, 1, 2, 5, 0])
    
    # print("Solutions for [1, 0, 3, 6, 5, 2, 7, 4]")
    # solve([1, 0, 3, 6, 5, 2, 7, 4])

    # print(board_to_str([1, 0, 3, 6, 5, 2, 7, 4]))
    if len(sys.argv) == 1:
        print("Running samples")
        solve_from_file("samplePuzzles.txt")
    elif len(sys.argv) == 2:
        if os.path.isfile(sys.argv[1]):
            solve_from_file(sys.argv[1])
        else:
            generate_puzzles(sys.argv[1])
            solve_from_file(sys.argv[1])
    elif len(sys.argv) == 3:
        generate_puzzles(sys.argv[1], int(sys.argv[2]))
        solve_from_file(sys.argv[1])
    elif len(sys.argv) == 10:
        filename = sys.argv[1]
        puzzle_cli = sys.argv[2:]
        puzzle = []

        for i in range(8):
            puzzle.append(int(puzzle_cli[i]))

        if validate_puzzle(puzzle):
            solve_and_output(puzzle, filename)
    else:
        print(sys.argv)
        print("arguments invalid")
        

if __name__ == "__main__":
    main()