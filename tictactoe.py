"""
Tic Tac Toe Player
"""

import math
import copy
import numpy as np

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
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
    return max(count, key=count.get)

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    result = set()
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == EMPTY:
                result.add((i,j))
    return result


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    temp_board = copy.deepcopy(board)
    curr_player = player(board)
    i, j = action
    if temp_board[i][j] != EMPTY:
        raise Exception ('Not a valid move')
    else:
        temp_board[i][j] = curr_player
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


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    print('Terminal: ', board)
    e_count = 0
    for row in board:
        if row.count(EMPTY) != 0:
            e_count += 1
    if e_count != 0:
        return False
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    print('Utility: ', board)
    check_board = winner(board)
    print('Utility: ', check_board)
    if check_board == 'X':
        return 1
    elif check_board == 'O':
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if (terminal(board)):
        return None
    else:
        if player(board) == 'X':
            return min_value(board)
        elif player(board) == 'O':
            return max_value(board)


def max_value(board):
    if (terminal(board)):
        return utility(board)
    v = float("-inf")
    possibilities = actions(board)
    for places in possibilities:
        v = max(v, min_value(result(board, places)))
    return v

def min_value(board):
    if (terminal(board)):
        return utility(board)
    v = float("inf")
    possibilities = actions(board)
    for places in possibilities:
        v = min(v, max_value(result(board, places)))
    return v

test_board = [['X', 'O', 'O'], ['X', 'O', 'O'], ['X', 'X', EMPTY]]
print(max_value(test_board))


# get the min or max value from the respective functions, get the associated move and pass it on
