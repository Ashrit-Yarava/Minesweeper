import torch
import torch.nn as nn
import numpy as np
from make_guess import calculate_probabilities_for_indices, get_best_prediction
from play_until_guess import play_confirmed
from board import Board
from model import Model
from config import LENGTH, WIDTH, BOMB_COUNT


def generate_batch(batch_size, model):
    batch = []
    correct_labels = []
    board = Board(LENGTH, WIDTH, BOMB_COUNT)
    board.reveal(LENGTH // 2, WIDTH // 2)
    while len(batch) < batch_size:
        if not board.game_running:
            board = Board(LENGTH, WIDTH, BOMB_COUNT)
            board.reveal(LENGTH // 2, WIDTH // 2)
        play_confirmed(board)
        b, indices, predictions = calculate_probabilities_for_indices(model, board)

        for i, j in zip(b, indices):
            if len(batch) == batch_size:
                break
            batch.append(i)
            correct_labels.append(
                1.0 if board.board[j[0], j[1]] == -1 else 0.0  # 1 is safe, 0 is not safe.
            )

        guess = get_best_prediction(indices, predictions)
        board.reveal(guess[0], guess[1])

    return torch.concatenate(batch), torch.tensor(correct_labels).unsqueeze(-1)


if __name__ == "__main__":
    size = 16
    model = Model()
    batch, labels = generate_batch(size, model)

    print(batch.shape)
    print(labels.shape)
