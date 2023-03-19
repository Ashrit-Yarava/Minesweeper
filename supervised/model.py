import torch
import torch.nn as nn
from board import Board
from typing import NamedTuple
from config import LENGTH, WIDTH


class Pointer(NamedTuple):
    x: int
    y: int


OBS_SPACE = [Board.DEFAULT, 0, 1, 2, 3, 4, 5, 6, 7, 8]


class Model(nn.Module):
    def __init__(self):
        super().__init__()

        self.layers = nn.Sequential(
            nn.Conv2d(len(OBS_SPACE) + 1, 128, 3),
            nn.ReLU(),
            nn.Conv2d(128, 256, 3),
            nn.ReLU(),
            nn.Conv2d(256, 256, 3),
            nn.ReLU(),
            nn.Conv2d(256, 256, 3),
            nn.ReLU(),
            nn.Conv2d(256, 256, 3),
            nn.ReLU(),
            nn.Conv2d(256, 10, 3),
            nn.ReLU(),
            nn.Flatten(),
            nn.Linear(8 * 8 * 10, 512),
            nn.ReLU(),
            nn.Linear(512, 2),
            nn.Softmax(dim=-1)
        )

    def forward(self, x):
        return self.layers(x)


if __name__ == "__main__":
    model = Model()

    board = torch.zeros((1, len(OBS_SPACE) + 1, LENGTH, WIDTH))

    print(model(board).shape)
