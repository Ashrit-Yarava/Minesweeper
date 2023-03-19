import numpy as np
from safe_finder import get_indices, get_bombs
from board import Board
from config import LENGTH, WIDTH, BOMB_COUNT


def smart_selectable(board):
    covered = np.argwhere((board == Board.DEFAULT))

    def neighbor_has_been_selected(x, y):
        return np.sum((Board.neighbors(board, x, y) >= 0)) != 0

    neighbor_indices = covered[np.vectorize(neighbor_has_been_selected)(covered[:, 0], covered[:, 1])]
    bomb_indices = get_bombs(board)

    bomb_indices = {(i[0], i[1]) for i in bomb_indices}
    neighbor_indices = [(i[0], i[1]) for i in neighbor_indices if (i[0], i[1]) not in bomb_indices]

    return np.array(neighbor_indices)


if __name__ == "__main__":
    board = Board(LENGTH, WIDTH, BOMB_COUNT)
    board.reveal(LENGTH // 2, WIDTH // 2)

    print(board)
    print(smart_selectable(board.user()))
