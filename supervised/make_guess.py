import torch
import torch.nn as nn
import numpy as np
from play_until_guess import play_confirmed
from smart_selectable import smart_selectable
from board import Board
from supervised.model import OBS_SPACE, Model
from config import LENGTH, WIDTH, BOMB_COUNT


def generate_input_matrix(board, pointer_index):
    shape = board.shape
    b = np.array(board) + np.abs(Board.DEFAULT)
    b = (np.arange(len(OBS_SPACE)) == b[..., None] - 1)
    b = torch.from_numpy(b)
    b = b.permute(2, 0, 1)
    pointer_layer = torch.zeros(shape)
    pointer_layer[int(pointer_index[0]), int(pointer_index[1])] = 1.0
    pointer_layer = pointer_layer.unsqueeze(0)
    return torch.concatenate((b, pointer_layer)).unsqueeze(0)


def calculate_probabilities_for_indices(model, board: Board):
    indices = smart_selectable(board.user())
    if len(indices) == 0:
        indices = board.selectable()
    batch = []
    for index in indices:
        batch.append(generate_input_matrix(board.user(), index))
    x = torch.concatenate(batch)
    with torch.no_grad():
        predictions = model(x)
    return batch, indices, predictions


def get_best_prediction(i, p):
    return i[torch.argmax(p[:, 0])]


if __name__ == "__main__":
    model = Model()
    board = Board(LENGTH, WIDTH, BOMB_COUNT)
    board.reveal(LENGTH // 2, WIDTH // 2)
    play_confirmed(board)
    batch, indices, preds = calculate_probabilities_for_indices(model, board)
    print(len(batch), batch[0].shape)
    print(preds.shape)
    print(f"Best Guess: {get_best_prediction(indices, preds)}")
