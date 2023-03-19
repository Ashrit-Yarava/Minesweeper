"""
Implement Minesweeper in Numpy.

Board:
* __init__(length, width, bomb, render): Initialize the board with the given parameters.
* __str__(): Get a string representation of the board.
* squares_remaining(): Get the number of squares that are remaining on the board to be checked.
* game_won(): Check whether the game is won.
* reveal(): Reveal a given square.
* convert_to_image(): Generate an image representation of the board.
* user(): Get a view of the board without the bombs labeled.
* selectable(): Get an array of the selectable values.
* selectable_near_revealed(): Get an array of the indices that are next to revealed neighbors. (Includes bombs).
* save_gif(filename): If render is true, save a gif of the board until it's current state.
"""

import numpy as np
from PIL import Image
from collections import namedtuple
from config import LENGTH, WIDTH, BOMB_COUNT

Pointer = namedtuple("Pointer", ("x", "y"))


class Board:
    DEFAULT = -1
    BOMB = -2

    def __init__(self, l, w, b, render=False):
        """
        Initialize the board.
        :param l: Length
        :param w: Wdith
        :param b: Number of bombs
        :param render: Whether to save an array of the images of the board.
        """
        self.l = l
        self.w = w
        self.b = b
        self.render = render

        self.moves = 0
        self.game_running = True

        self.board = np.zeros((self.l, self.w)) + Board.DEFAULT
        self.render_images = []

    def __str__(self):
        text = "    "
        for i in range(self.l):
            char_to_print = f"{i:^1}"
            text += f"{char_to_print}   "
        text += ("\n  " + ("-" * 4) * self.l + "-") + "\n"
        row_num = 0
        for rows in self.board:

            text += f"{row_num} | "
            row_num += 1
            for col in rows:

                if int(col) == Board.DEFAULT:
                    char_to_print = f"{' ':^1}"
                elif int(col) == Board.BOMB:
                    char_to_print = f"{'⚐':^1}"
                elif int(col) == 0:
                    char_to_print = f"{'O':^1}"
                else:
                    char_to_print = f"{int(col):^1}"

                text += f"{char_to_print} | "

            text += "\n  " + ("-" * 4) * self.l + "-\n"
        return text

    def _valid(self, x: int, y: int):
        """
        Check if the given index is a valid index.
        :param x: The row
        :param y: The column.
        :return: True if valid, false if invalid and not in range.
        """
        return 0 <= x < self.l and 0 <= y < self.w

    @staticmethod
    def neighbors(board, x, y):
        """
        Static method that takes an arbitary board and the index to return the neighbors of.

        :param board: The board.
        :param x: The row
        :param y: The column.
        :return: A numpy array of the neighbors in 8 directions.
        """
        l, w = board.shape
        return board[max(0, x - 1):min(l, x + 2), max(0, y - 1):min(w, y + 2)]

    def _adj(self, x: int, y: int):
        """
        Get the neighbors around the given x and y.
        :param x: The row
        :param y: The column
        :return:
        """
        return self.board[max(0, x - 1):min(self.l, x + 2), max(0, y - 1):min(self.w, y + 2)]

    def squares_remaining(self):
        """
        The number of squares that are still to be revealed.
        :return: The squares that are still to be revealed.
        """
        return np.sum((self.board == Board.DEFAULT))

    def game_won(self):
        """
        Check whether the game is won.
        :return: True if no squares are left, False if the game is still running.
        """
        return self.squares_remaining() == 0

    def reveal(self, x: int, y: int):
        """
        Reveal the selected square. End game if it is a bomb, and reveal adjacent squares.
        :param x: The row
        :param y: The column
        """

        def _reveal(xi, yi):
            if (not self._valid(xi, yi)
                    or self.board[xi, yi] >= 0
                    or self.board[xi, yi] in [Board.BOMB]):
                return
            # Set the total to the sum of the bombs and the labeled bombs.
            self.board[xi, yi] = np.sum(self._adj(xi, yi) == Board.BOMB)

            if self.render:
                self.render_images.append(Image.fromarray(self.convert_to_image()))

            # Reveal the neighbors.
            if self.board[xi, yi] == 0:
                _reveal(xi - 1, yi - 1)
                _reveal(xi + 1, yi + 1)
                _reveal(xi + 1, yi - 1)
                _reveal(xi - 1, yi + 1)
                _reveal(xi, yi - 1)
                _reveal(xi, yi + 1)
                _reveal(xi - 1, yi)
                _reveal(xi + 1, yi)

        if not self._valid(x, y) or self.board[x, y] >= 0 or not self.game_running:
            return

        self.moves += 1

        if self.board[x, y] == Board.BOMB:
            self.game_running = False
            return

        if self.moves == 1:
            probs = np.ones_like(self.board)
            probs[max(0, x - 1):min(self.l, x + 2), max(0, y - 1):min(self.w, y + 2)] = 0
            probs[:, :] = 1 / np.count_nonzero(probs)
            probs[max(0, x - 1):min(self.l, x + 2), max(0, y - 1):min(self.w, y + 2)] = 0
            probs = probs.flatten()

            shape = self.board.shape
            temp = self.board.flatten()
            temp[np.random.choice(temp.shape[0], self.b,
                                  replace=False, p=probs)] = Board.BOMB
            temp = temp.reshape(shape)
            self.board = temp

        _reveal(x, y)

        if self.game_won():
            self.game_running = False

    def convert_to_image(self):
        """
        Return an image representation of the board.
        :return: Numpy array of 3 Dimensions (l, w, 3)
        """
        b = self.board
        colored_image = np.zeros((b.shape[0], b.shape[1], 3))
        colored_image[b == Board.BOMB] = np.array((102, 0, 0))  # Bombs
        colored_image[b == Board.DEFAULT] = np.array((255, 255, 255))  # Default.
        colored_image[b == 0] = np.array((235, 235, 235))  # 0.
        colored_image[b == 1] = np.array((224, 224, 224))  # 1.
        colored_image[b == 2] = np.array((192, 192, 192))  # 2.
        colored_image[b == 3] = np.array((160, 160, 160))  # 3.
        colored_image[b == 4] = np.array((128, 128, 128))  # 4.
        colored_image[b == 5] = np.array((96, 96, 96))  # 5.
        colored_image[b == 6] = np.array((64, 64, 64))  # 6.
        colored_image[b == 7] = np.array((50, 50, 50))  # 7.
        colored_image[b == 8] = np.array((25, 25, 25))  # 8.
        colored_image = colored_image / 255
        colored_image = colored_image.repeat(50, axis=0).repeat(50, axis=1)
        colored_image = np.pad(colored_image, [(1, 1), (1, 1), (0, 0)], mode='constant')
        colored_image = (colored_image * 255).astype(np.uint8)
        return colored_image

    def user(self):
        """
        Get a user view of the board that hides all the bombs.

        :return: The user view of the board.
        """
        b = np.array(self.board)
        b[b == Board.BOMB] = Board.DEFAULT
        return b

    def selectable(self):
        """
        Get a list of all the selectable spots as indices.

        :return: The indices (N, 2) array.
        """
        return np.argwhere((self.user() == Board.DEFAULT))

    def selectable_near_revealed(self):
        """
        Get a list of indices of the squares that are adjacent to the current squares.

        :return: A 2d array of (x, 2) where each row is a unique index.
        """
        covered = self.selectable()

        def neighbor_has_been_selected(x, y):
            return np.sum((self._adj(x, y) >= 0)) != 0

        return covered[np.vectorize(neighbor_has_been_selected)(covered[:, 0], covered[:, 1])]

    def save_gif(self, filename):
        """
        Save the gif to the file.

        :param filename: The filename to save to.
        """

        if self.render and len(self.render_images) > 0:
            self.render_images[0].save(filename, save_all=True, append_images=self.render_images[1:], duration=120)


if __name__ == "__main__":
    board = Board(LENGTH, WIDTH, BOMB_COUNT)
    board.reveal(5, 5)
    print(board)
    print(f"Smartly selectable squares: {len(board.selectable_near_revealed())}")
