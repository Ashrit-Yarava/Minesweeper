import numpy as np
from board import Board
from config import LENGTH, WIDTH, BOMB_COUNT


def get_bombs(board):
    """
    Return a list of all the confirmed bombs.

    :param board: The user view of the numpy array of the board. Ranged from (-1 $\to$ 8)
    :return: An array (N, 2) of indices.
    """

    l, w = board.shape
    indices = []
    for (x, y) in np.argwhere(board > 0):
        num_bombs = board[x, y]
        neighboring_squares = np.sum(Board.neighbors(board, x, y) == Board.DEFAULT)
        if num_bombs == neighboring_squares:
            possible = [
                [x - 1, y - 1], [x - 1, y], [x -1, y + 1],
                [x, y - 1], [x, y + 1],
                [x + 1, y - 1], [x + 1, y], [x + 1, y + 1]
            ]
            for (xi, yi) in possible:
                if 0 <= xi < l and 0 <= yi < w and board[xi, yi] == Board.DEFAULT:
                    indices.append((xi, yi))
    indices = np.unique(np.array(indices), axis=0)
    return indices


def smart_selectable(board):
    covered = np.argwhere((board == Board.DEFAULT))

    def neighbor_has_been_selected(x, y):
        return np.sum((Board.neighbors(board, x, y) >= 0)) != 0

    neighbor_indices = covered[np.vectorize(neighbor_has_been_selected)(covered[:, 0], covered[:, 1])]
    bomb_indices = get_bombs(board)

    neighbor_indices = {(i[0], i[1]) for i in neighbor_indices}
    bomb_indices = {(i[0], i[1]) for i in bomb_indices}

    print(neighbor_indices)
    print(bomb_indices)

    return neighbor_indices - bomb_indices


if __name__ == "__main__":
    board = Board(LENGTH, WIDTH, BOMB_COUNT)
    board.reveal(LENGTH // 2, WIDTH // 2)
    print(board)

    print(get_bombs(board.user()))
    smart_selectable(board.user())
