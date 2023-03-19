import numpy as np
from board import Board
from bomb_finder import get_bombs
from config import LENGTH, WIDTH, BOMB_COUNT


def get_indices(board):
    """
    Return a list of all the confirmed safe squares.

    :param board: The user view of the numpy array of the board. Ranged from (-1 $\to$ 8)
    :return: An array (N, 2) of indices.
    """

    l, w = board.shape

    bomb_indices = get_bombs(board)
    bomb_loc = np.zeros_like(board)

    for (x, y) in bomb_indices:
        bomb_loc[x, y] = 1

    indices = []
    for (x, y) in np.argwhere(board > 0):
        num_bombs = board[x, y] - np.sum(Board.neighbors(bomb_loc, x, y))
        neighboring_squares = np.sum(Board.neighbors(board, x, y) == Board.DEFAULT)
        if num_bombs == 0 and neighboring_squares > 0:
            possible = [
                [x - 1, y - 1], [x - 1, y], [x - 1, y + 1],
                [x, y - 1], [x, y + 1],
                [x + 1, y - 1], [x + 1, y], [x + 1, y + 1]
            ]
            for (xi, yi) in possible:
                if 0 <= xi < l and 0 <= yi < w and board[xi, yi] == Board.DEFAULT and bomb_loc[xi, yi] == 0:
                    indices.append((xi, yi))
    indices = np.unique(np.array(indices), axis=0)
    return indices


if __name__ == "__main__":
    board = Board(LENGTH, WIDTH, BOMB_COUNT, render=True)
    board.reveal(LENGTH // 2, WIDTH // 2)
    print(board)
    indices = get_indices(board.user())

    for (x, y) in indices:
        board.reveal(x, y)

    board.save_gif("game.gif")
