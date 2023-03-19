import numpy as np
from tqdm import tqdm

from board import Board
from naiveprob.play_game import play_game
from config import LENGTH, WIDTH, BOMB_COUNT


if __name__ == "__main__":
    games_won = 0
    games = 10

    for i in tqdm(range(games)):
        board = Board(LENGTH, WIDTH, BOMB_COUNT, render=True)
        board.reveal(LENGTH // 2, WIDTH // 2)

        play_game(board)

        if board.game_won():
            games_won += 1
            board.save_gif(f"samples/{i}.gif")

    print(f"Games Won: {games_won} / {games} => {round(games_won / games * 100, 4)}%")