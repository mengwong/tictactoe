"""
Tic Tac Toe Player
"""

# usage:              python tictactoe.py > log.org
# to view the log,    emacs log.org
# and press TAB judiciously

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

def other_p(p):
    if p == 'X': return 'O'
    else:        return 'X'
        
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
    toreturn = 'X' if count['X'] <= count['O'] else 'O'
    print("count O = " + str(count['O']) + "; count X = " + str(count['X']) + "; next move, player " + toreturn)
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


def winner(board, depth):
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
        
    return None


def terminal(board, depth):
    """
    Returns True if game is over, False otherwise.

    TODO: we're terminal if winner()
    """
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
    # show('Utility', board, 0)
    check_board = winner(board, depth)
    print(check_board)
    if check_board == 'X':
        print(stars(depth), 'We have a Winner! X wins.')
        return 1
    elif check_board == 'O':
        print(stars(depth), 'We have a Winner! O wins.')
        return -1
    else:
        print(stars(depth), 'A curious game, Professor Falken. The only winning move is not to play.')
        return 0


def minimax(board, depth, p=None):
    """
    Returns the optimal action for the current player on the board.

    We recurse until we bottom out at a terminal state.

    The terminal state could be X wins, O wins, or neither wins. We associate a utility function with that state.

    Assuming we are X and we win with 1:

    Every future move can be evaluated to a range of outcomes in {-1:n, 0:n, 1:n}.

    Order moves by:

    If a winning move is available, play it; the utility is nonzero.
    {-1:0, 0:0, 1: >0}

    If only a terminal draw is available, play that.
    Exclude all moves which lead to the other player winning.
    Play any move that prevents the other player from winning.
    {-1:0, 0: >0}

    Otherwise, be a good sport and lose
    {-1:>0}

    Let's return the best move and the utility as a tuple
    """
    p = p or player(board,depth)
    show("minimax: what should " + p + " play, given this board?", board, depth)
    if (terminal(board,depth)):
        print(stars(depth), "minimax: board is terminal; returning none.")
        return None
    else:
        possibilities = actions(board, depth)
        outcome = {}
        for places in possibilities:
            print(stars(depth+1), f"minimax: what if {p} plays " + str(places) + "?")
            nextmove = result(board, places, depth+1)
            if winner(nextmove,depth+2):
                outcome[places] = utility(nextmove, depth+1)
                print(stars(depth+2), f"minimax:     if {p} plays " + str(places) + f" then somebody wins with utility {outcome[places]}")
                if p == 'X' and outcome[places] == 1:
                    print(stars(depth), "X wins with " + str(places))
                    return places, outcome[places]
                elif p == 'O' and outcome[places] == -1:
                    print(stars(depth), "O wins with " + str(places))
                    return places, outcome[places]
            if terminal(nextmove,depth+2):
                print(stars(depth+2), f"minimax:      if {p} plays " + str(places) + " then it's a draw. fine by us.")
                return places, 0

            # non-leaf; run further minimax and collate the results
            print(stars(depth+2), f"minimax:      if {p} plays " + str(places) + " we recurse to the best submove for " + other_p(p))
            subresult, outcome[places] = minimax(nextmove, depth+2)
            print(stars(depth+2), f"minimax:      if {p} plays " + str(places) + " the best submove for " + other_p(p) + " is " + str(subresult))
            print(stars(depth+2), f"minimax:      hence we record utility of " + str(outcome[places]) + " for " + p + " playing " + str(places))

        print(stars(depth), p + " is considering options...")
        print(outcome)
        
        # choose the optimal action
        for places in outcome:
            print(f"recap: {places} has utilities {outcome[places]}")
        maxplay = max(outcome, key=outcome.get)
        minplay = min(outcome, key=outcome.get)
        if p == 'X':
            print(stars(depth), f"recap: correct play for X is {maxplay} with utility " + str(outcome[maxplay]))
            return maxplay, outcome[maxplay]
        else:
            print(stars(depth), f"recap: correct play for O is {minplay} with utility " + str(outcome[minplay]))
            return minplay, outcome[minplay]
            


test_board = [['X', 'O', EMPTY],
              ['O', EMPTY, EMPTY],
              ['X', 'X', EMPTY]]
print(minimax(test_board, 2))


# get the min or max value from the respective functions, get the associated move and pass it on
