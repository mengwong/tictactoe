"""
Tic Tac Toe Player
"""

import math
import copy
import numpy as np

X = "X"
O = "O"
EMPTY = None

def stars(depth):
    return "*"*depth

def show(name, board, depth=0):
    print(stars(depth), name + ":")
    for row in board:
        print(" "*(depth+1), end="")
        print (row)

def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board, depth):
    """
    Returns player who has the next turn on a board.
    """
    if (board == initial_state()):
        return 'X'
    count = {'X': 0, 'O': 0}
    for row in board:
        if row.count(None) < len(row):
            count['O'] += row.count('O')
            count['X'] += row.count('X')
    toreturn = 'X' if count['X'] < count['O'] else 'O'
    print("next move, player " + toreturn)
    return toreturn

def actions(board, depth):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    result = set()
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == EMPTY:
                result.add((i,j))
    print(f"actions = {result}")
    return result


def result(board, action, depth):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    temp_board = copy.deepcopy(board)
    curr_player = player(board,depth)
    print("the current player is " + curr_player)
    i, j = action
    if temp_board[i][j] != EMPTY:
        raise Exception ('Not a valid move')
    else:
        temp_board[i][j] = curr_player
    show("result", temp_board, 0)
    return temp_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    np_board = np.array(board)
    pos = ['X', 'O']
    for p in pos:
        # check rows
        if (np.all(np_board == p, axis=1).any()):
            return p
        # check columns
        elif (np.all(np_board == p, axis=0).any()):
            return p
        # check diagonals
        elif (np.all(np.diag(np_board) == p)):
            return p
        # check flipped diagonals
        elif (np.all(np.fliplr(np_board).diagonal() == p)):
            return p
        else:
            return None


def terminal(board, depth):
    """
    Returns True if game is over, False otherwise.
    """
#    show('Terminal', board)
    e_count = 0
    for row in board:
        if row.count(EMPTY) != 0:
            e_count += 1
    if e_count != 0:
        print("are we terminal? no")
        return False
    print("are we terminal? yes")
    return True


def utility(board, depth):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    show('Utility', board, 0)
    check_board = winner(board)
    print(check_board)
    if check_board == 'X':
        print(stars(depth), 'We have a Winner! X wins.')
        return 1
    elif check_board == 'O':
        print(stars(depth), 'We have a Winner! X wins.')
        return -1
    else:
        print(stars(depth), 'A curious game, Professor Falken. The only winning move is not to play.')
        return 0


def minimax(board, depth):
    """
    Returns the optimal action for the current player on the board.
    """
    show("minimax: what is the minimax value of this board?", board, depth)
    if (terminal(board,depth)):
        print(stars(depth), "minimax: board is terminal; returning none.")
        return None
    else:
        if player(board,depth) == 'X':
            print(stars(depth), "minimax: player X goes next, so returning max_value.")
            return max_value(board, depth+1)
        elif player(board,depth) == 'O':
            print(stars(depth), "minimax: player O goes next, so returning min_value.")
            return min_value(board, depth+1)


def max_value(board, depth):
    show ("max_value: what is the max value of this board?", board, depth)
    if (terminal(board, depth)):
        ub = utility(board, depth)
        print (stars(depth), "max_value: board is terminal. returning utility of the board, which is " + str(ub))
        return ub
    v = float("-inf")
    possibilities = actions(board, depth)
    print("max_value: considering " + str(len(possibilities)) + " possibilities.")
    p = player(board,depth)
    for places in possibilities:
        print(stars(depth), f"max_value: what if {p} plays " + str(places) + "?")
        v = max(v, min_value(result(board, places, depth+1), depth+1))
        print(stars(depth), f"max_value:      if {p} plays " + str(places) + ", the max_value is " + str(v))
    return v

def min_value(board, depth):
    show ("min_value: what is the min value of this board?", board, depth)
    if (terminal(board,depth)):
        ub = utility(board, depth)
        print (stars(depth), "min_value: board is terminal. returning utility of the board, which is " + str(ub))
        return ub
    v = float("inf")
    possibilities = actions(board, depth)
    print("min_value: considering " + str(len(possibilities)) + " possibilities.")
    p = player(board,depth)
    for places in possibilities:
        print(stars(depth), f"min_value: what if {p} plays " + str(places) + "?")
        v = min(v, max_value(result(board, places, depth+1), depth+1))
        print(stars(depth), f"min_value:      if {p} plays " + str(places) + ", the min_value is " + str(v))
    return v

test_board = [['X', 'O', 'O'],
              ['O', 'O', EMPTY],
              ['X', 'X', EMPTY]]
print(minimax(test_board, 2))


# get the min or max value from the respective functions, get the associated move and pass it on
