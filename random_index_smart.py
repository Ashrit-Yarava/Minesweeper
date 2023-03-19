"""
When given the choice, just select a random square to reveal.
"""

import numpy as np
from board import Board
from play_until_guess import play_confirmed
from smart_selectable import smart_selectable
from tqdm import tqdm
from config import LENGTH, WIDTH, BOMB_COUNT


def random_guess(board):
    indices = smart_selectable(board.user())
    if len(indices) == 0:
        indices = board.selectable()
    choice = indices[np.random.choice(len(indices), 1)][0]
    board.reveal(choice[0], choice[1])


def random_guess_normal(board):
    indices = smart_selectable(board.user())
    if len(indices) == 0:
        indices = board.selectable()
    index = min(max(0, int(np.random.normal(len(indices) // 2, len(indices) // 4, size=1))), len(indices) - 1)
    choice = indices[index]
    board.reveal(choice[0], choice[1])


if __name__ == "__main__":

    NUM_GAMES = 100
    GAMES_WON = 0

    for _ in tqdm(range(NUM_GAMES)):
        board = Board(LENGTH, WIDTH, BOMB_COUNT, render=False)
        board.reveal(LENGTH // 2, WIDTH // 2)
        while board.game_running:
            play_confirmed(board)
            if not board.game_running:
                break
            random_guess(board)
        # if board.game_won():
        #     GAMES_WON += 1
        #     board.save_gif("game.gif")

    print(f"{GAMES_WON} / {NUM_GAMES} => {round(GAMES_WON / NUM_GAMES, 4) * 100}")