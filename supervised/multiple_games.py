import torch
import numpy as np
from tqdm import tqdm

from board import Board
from play_until_guess import play_confirmed
from supervised.make_guess import calculate_probabilities_for_indices, get_best_prediction
from model import Model
from supervised.play_game import play_game
from config import LENGTH, WIDTH, BOMB_COUNT


def get_game_score(model):
    board = Board(LENGTH, WIDTH, BOMB_COUNT)
    board.reveal(LENGTH // 2, WIDTH // 2)
    guesses = play_game(model, board)
    return board.game_won(), guesses


if __name__ == "__main__":
    games_won = 0
    games = 100
    guesses_list = []
    winning_game_guesses = []
    model = Model()
    model.load_state_dict(torch.load("checkpoints/state_dict.pt"))

    for _ in tqdm(range(games)):
        victory, guesses = get_game_score(model)
        guesses_list.append(guesses)
        if victory:
            winning_game_guesses.append(guesses)
            games_won += 1

    print(f"Statistics: {games_won} / {games} => {round(games_won / games, 4) * 100}")
    print(f"Average Number of Guesses: {np.mean(np.array(guesses_list))}")
    print(f"Average Number of Guesses in won games: {np.mean(np.array(winning_game_guesses))}")
