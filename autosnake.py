#!/usr/bin/env python3
import time
from collections import deque
from random import choice, randint
from typing import Literal

try:
    from rgbmatrix import RGBMatrix, RGBMatrixOptions
except ImportError:
    from RGBMatrixEmulator import RGBMatrix, RGBMatrixOptions

# Configuration for the matrix
options = RGBMatrixOptions()
options.rows = 32
options.cols = 64
options.chain_length = 1
options.parallel = 1
options.hardware_mapping = "adafruit-hat"

matrix = RGBMatrix(options=options)

# noinspection PyTypeHints
char = Literal[tuple(range(256))]
Color = tuple[char, char, char]


class Pixel:
    def __init__(self, x, y):
        self.x: int = x
        self.y: int = y

    def copy(self):
        return self.__class__(self.x, self.y)

    def __repr__(self):
        return f"<Pixel(x={self.x}, y={self.y})>"

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            raise ValueError  # Should make good error message sometime
        return self.x == other.x and self.y == other.y


class QuickKill(Exception):
    pass


class Snake:
    def __init__(self, matrix: RGBMatrix, color: Color, blank: Color, bias: int = 0):
        self.pos: deque[Pixel] = deque([Pixel(0, 1), Pixel(1, 1)])
        self.matrix: RGBMatrix = matrix
        self.color: Color = color
        self.blank: Color = blank
        self.bias: int = bias

        self.directions = ["w", "a", "s", "d"]
        self.direction: Literal["w", "a", "s", "d"] = "d"

    def grow(self):
        self.pos.append(self.pos[-1])

    def draw(self):
        for block in self.pos:
            self.matrix.SetPixel(block.x, block.y, *self.color)

    def draw_step(self):
        last = self.pos[-1]
        self.matrix.SetPixel(last.x, last.y, *self.blank)

        head = self.pos[0]
        matrix.SetPixel(head.x, head.y, *self.color)

    def move(self, apple: Pixel):
        """Moves the snake one step"""
        self.smart_move(apple=apple)
        head = self.pos[0].copy()

        if self.direction == "a":
            head.x -= 1
        elif self.direction == "d":
            head.x += 1
        elif self.direction == "w":
            head.y -= 1
        elif self.direction == "s":
            head.y += 1

        # Cool loop logic
        head.x = head.x % self.matrix.width
        head.y = head.y % self.matrix.height

        self.pos.pop()  # remove tail
        if head in self.pos:
            raise QuickKill("Head touched body")

        self.pos.appendleft(head)

    def smart_move(self, apple: Pixel):
        """prevents the snake from moving into itself"""
        head = self.pos[0]
        valid_directions = []

        # generate a list of valid directions, where the snake won't move into itself
        for direction in self.directions:
            new = head.copy()
            if direction == "a":
                new.x -= 1
            elif direction == "d":
                new.x += 1
            elif direction == "w":
                new.y -= 1
            elif direction == "s":
                new.y += 1

            new.x = new.x % self.matrix.width
            new.y = new.y % self.matrix.height

            if new not in self.pos:
                valid_directions.append(direction)

        # add a bias to the apple
        if apple.x < head.x and "a" in valid_directions:
            [valid_directions.append("a") for _ in range(self.bias)]
        if apple.x > head.x and "d" in valid_directions:
            [valid_directions.append("d") for _ in range(self.bias)]
        if apple.y < head.y and "w" in valid_directions:
            [valid_directions.append("w") for _ in range(self.bias)]
        if apple.y > head.y and "s" in valid_directions:
            [valid_directions.append("s") for _ in range(self.bias)]

        # add a bias to the current direction
        if self.direction in valid_directions:
            valid_directions.append(self.direction)

        if not valid_directions:
            raise QuickKill("No valid directions")

        self.direction = choice(valid_directions)
        return valid_directions


print("Press CTRL-C to stop.")
snek = Snake(matrix, color=(255, 255, 255), blank=(0, 0, 0), bias=10)

apple = Pixel(randint(0, matrix.width - 1), randint(0, matrix.height - 1))
matrix.SetPixel(apple.x, apple.y, 255, 0, 0)
print(apple)

while True:
    try:
        snek.move(apple)
    except QuickKill:
        print("Game over")
        time.sleep(600)  # let the user see the snake
        break
    snek.draw_step()

    if snek.pos[0] == apple:
        snek.grow()
        apple = Pixel(randint(0, matrix.width - 1), randint(0, matrix.height - 1))
        matrix.SetPixel(apple.x, apple.y, 255, 0, 0)
        print(apple)
    time.sleep(0.1)
