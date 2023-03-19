"""
Plays one game of minesweeper with a passed in model and board.
The board must have the first move played already.
"""
import torch

from board import Board
from play_until_guess import play_confirmed
from supervised.make_guess import calculate_probabilities_for_indices, get_best_prediction
from model import Model
from config import LENGTH, WIDTH, BOMB_COUNT


def play_game(model, board):

    guesses_made = 0

    while board.game_running:
        play_confirmed(board)  # Play all the moves that are guarenteed.
        _, indices, predictions = calculate_probabilities_for_indices(model, board)
        guess = get_best_prediction(indices, predictions)
        guesses_made += 1
        # print(guess)
        board.reveal(guess[0], guess[1])

    return guesses_made


if __name__ == "__main__":
    board = Board(LENGTH, WIDTH, BOMB_COUNT, render=False)
    board.reveal(LENGTH // 2, WIDTH // 2)
    model = Model()
    model.load_state_dict(torch.load("checkpoints/state_dict.pt"))

    play_game(model, board)

    print(board)

    if board.game_won():
        print("Game Won!")

    # board.save_gif("game.gif")
