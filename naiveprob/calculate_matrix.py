import sys
from typing import Tuple

import numpy as np

from board import Board
from config import LENGTH, WIDTH, BOMB_COUNT
from play_until_guess import play_confirmed
from bomb_finder import get_bombs
from smart_selectable import smart_selectable


def get_neighbor_indices(x, y):
    return {
        (x - 1, y - 1), (x - 1, y), (x - 1, y + 1),
        (x    , y - 1),             (x    , y + 1),
        (x + 1, y - 1), (x + 1, y), (x + 1, y + 1),
    }


def calculate_matrix(board: np.ndarray) -> tuple[set, np.ndarray]:
    """
    Return a matrix of probabilities for all the smartly selectable squares.

    :param board: The user view of the board.
    :return: A matrix with the summed probabilities.
    """

    probabilities = np.zeros_like(board)
    indicies = {(i[0], i[1]) for i in smart_selectable(board)}
    bombs = {(i[0], i[1]) for i in get_bombs(board)}

    for (x, y) in np.argwhere(board > 0):  # Get revealed squares.
        neighbors = get_neighbor_indices(x, y)
        num_bombs = board[x, y] - len(bombs.intersection(neighbors))
        num_selectable = len(indicies.intersection(neighbors))

        for (xi, yi) in indicies.intersection(neighbors):
            probabilities[xi, yi] += num_bombs / num_selectable
    return indicies, np.array([probabilities[i[0], i[1]] for i in indicies])


def make_best_choice(indices, probabilities):
    max_prob = np.min(probabilities)
    best_idx = np.argwhere(probabilities == max_prob)

    if len(best_idx) > 1:
        best_idx = np.random.choice(np.squeeze(best_idx, -1), size=1)[0]
    else:
        best_idx = best_idx[0][0]

    return list(indices)[best_idx]


if __name__ == "__main__":
    board = Board(LENGTH, WIDTH, BOMB_COUNT)
    board.reveal(5 // 2, 5 // 2)
    play_confirmed(board)

    if not board.game_won():
        print(board)
        print(make_best_choice(*calculate_matrix(board.user())))