import numpy as np

from board import Board
from play_until_guess import play_confirmed
from naiveprob.calculate_matrix import calculate_matrix, make_best_choice
from config import LENGTH, WIDTH, BOMB_COUNT


def play_game(board: Board):
    """
    Plays a game with the given board.

    :param board: The board to play on.
    """

    while board.game_running:
        play_confirmed(board)

        if not board.game_running:
            return

        indices, probabilities = calculate_matrix(board.user())

        if len(indices) == 0:
            # There are no logical squares to choose, make a random guess.
            indices = board.selectable()
            random_guess = np.random.choice(np.arange(len(indices)), size=1)[0]
            board.reveal(indices[random_guess][0], indices[random_guess][1])
        else:
            index = make_best_choice(indices, probabilities)
            board.reveal(index[0], index[1])


if __name__ == "__main__":
    board = Board(LENGTH, WIDTH, BOMB_COUNT)
    board.reveal(LENGTH // 2, WIDTH // 2)

    play_game(board)

    print(board.game_won())