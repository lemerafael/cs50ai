"""
Tic Tac Toe Player
"""

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
    count = 0
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] is not None:
                count = count + 1
    if count % 2 == 0:
        output = X
    else:
        output = O
    return output
        
            
def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    output = set()
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] is None:
                output.add((i, j))
    return output


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if action[0] < 0 or action[0] > len(board) or action[1] < 0 or action[1] > len(board):
        raise IndexError
    if board[action[0]][action[1]] is not None:
        raise ValueError
    next_player = player(board)
    board_copy = copy.deepcopy(board)
    board_copy[action[0]][action[1]] = next_player
    return board_copy


def horizontal_winner(board):
    """
    Returns the winner of the board in a horizontal line, if any.
    """
    winner = None
    for i in range(3):
        tentative = EMPTY
        if winner is not EMPTY:
            break
        for j in range(3):
            if not is_line_valid(i, j, tentative, board):
                break
            elif j == 2:
                winner = tentative
            else:
                tentative = board[i][j]
    return winner


def vertical_winner(board):
    """
    Returns the winner of the board in a vertical line, if any.
    """
    winner = None
    for j in range(3):
        tentative = None
        if winner is not EMPTY:
            break
        for i in range(3):
            if not is_line_valid(i, j, tentative, board):
                break
            elif i == 2:
                winner = tentative
            else:
                tentative = board[i][j]
    return winner


def diagonal_winner(board):
    """
    Returns the winner of the board in a diagonal line, if any.
    """
    winner = None
    tentative = None
    for i in range(3):
        if not is_line_valid(i, i, tentative, board):
            break
        elif i == 2:
            winner = tentative
        else:
            tentative = board[i][i]
    tentative = None
    if winner is None:
        j = 0
        for i in range(2, -1, -1):
            if not is_line_valid(i, j, tentative, board):
                break
            elif j == 2:
                winner = tentative
            else:
                tentative = board[i][j]
            j = j + 1
    return winner


def is_line_valid(line, column, tentative, board):
    """
    Return whether the line is valid to find a tentative winner.
    """
    output = False
    is_first_element = line == 0 or column == 0
    is_empty = board[line][column] is EMPTY
    is_same_as_tentative = board[line][column] == tentative
    if (tentative is None and is_first_element and not is_empty) or (not is_empty and is_same_as_tentative):
        output = True
    return output


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    output = horizontal_winner(board)
    if output is None:
        output = vertical_winner(board)
    if output is None:
        output = diagonal_winner(board)
    return output


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    output = False
    if winner(board) is not None or len(actions(board)) == 0:
        output = True
    return output
    

def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    output = 0
    the_winner = winner(board)
    if the_winner == X:
        output = 1
    elif the_winner == O:
        output = -1
    return output


def max_value(board):
    """
    Recursive function to return the max value.
    """
    if terminal(board):
        return utility(board)
    v = -math.inf
    for action in actions(board):
        v = max(v, min_value(result(board, action)))
    return v


def max_board(board):
    """
    Returns the action that has the path with the max value.
    """
    values = {}
    for action in actions(board):
        cur_result = result(board, action)
        values[action] = min_value(cur_result)
    return max(values.items(), key=lambda values: values[1])[0]


def min_value(board):
    """
    Recursive function to return the min value.
    """
    if terminal(board):
        return utility(board)
    v = math.inf
    for action in actions(board):
        v = min(v, max_value(result(board, action)))
    return v


def min_board(board):
    """
    Returns the action that has the path with the min value.
    """
    values = {}
    for action in actions(board):
        cur_result = result(board, action)
        values[action] = max_value(cur_result)
    return min(values.items(), key=lambda values: values[1])[0]


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    result = None
    if not terminal(board):
        if player(board) == X:
            result = max_board(board)
        elif player(board) == O:
            result = min_board(board)
    return result        
