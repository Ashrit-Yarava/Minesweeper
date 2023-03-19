import numpy as np
from safe_finder import get_indices
from smart_selectable import smart_selectable
from board import Board
from config import LENGTH, WIDTH, BOMB_COUNT


def play_confirmed(board: Board):
    indices = get_indices(board.user())

    while len(indices) > 0:
        for (x, y) in indices:
            board.reveal(x, y)
        indices = get_indices(board.user())


if __name__ == "__main__":
    board = Board(LENGTH, WIDTH, BOMB_COUNT, render=True)
    board.reveal(LENGTH // 2, WIDTH // 2)

    play_confirmed(board)
    board.save_gif("game.gif")

    print(smart_selectable(board.user()))
