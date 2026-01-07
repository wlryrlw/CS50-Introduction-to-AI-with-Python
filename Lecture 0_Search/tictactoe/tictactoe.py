"""
Tic Tac Toe Player
"""

from typing import Any


import math
import copy

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
    nx = 0
    no = 0
    
    for row in board:
        for col in row:
            if col == X:
                nx += 1
            elif col == O:
                no += 1

    if nx == no:
        return X
    else:
        return O
 

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    set_actions = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                set_actions.add((i, j))
    return set_actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if action not in actions(board):
        raise ValueError
    
    new_board = copy.deepcopy(board)
    new_board[action[0]][action[1]] = player(board)

    return new_board

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for row in board:
        if row[0] == row[1] == row[2] != EMPTY:
            return row[0]

    for j in range(3):
        if board[0][j] == board[1][j] == board[2][j] != EMPTY:
            return board[0][j]

    if board[0][0] == board[1][1] == board[2][2] != EMPTY:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != EMPTY:
        return board[0][2]

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board):
        return True

    if all(cell != EMPTY for row in board for cell in row):
        return True
        
    return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    win = winner(board)
    if win == X:
        return 1
    elif win == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None

    if player(board) == X:
        return max_value(board)[1]
    else:
        return min_value(board)[1]


def max_value(board):
    """
    Returns (value, action) for the maximizing player.
    """
    if terminal(board):
        return (utility(board), None)
    
    best_action = None
    v = -math.inf
    for action in actions(board):
        min_val = min_value(result(board, action))[0]
        if min_val > v:
            v = min_val
            best_action = action
    return (v, best_action)


def min_value(board):
    """
    Returns (value, action) for the minimizing player.
    """
    if terminal(board):
        return (utility(board), None)
    
    best_action = None
    v = math.inf
    for action in actions(board):
        max_val = max_value(result(board, action))[0]
        if max_val < v:
            v = max_val
            best_action = action
    return (v, best_action)