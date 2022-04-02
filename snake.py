#!/usr/bin/env python3
import sys
import time
from collections import deque
from random import randint
from threading import Thread
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
options.hardware_mapping = "adafruit-hat"  # If you have an Adafruit HAT: 'adafruit-hat'

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


try:
    # noinspection PyUnresolvedReferences
    import keyboard

    mode = "keyboard"
except ImportError:
    import sshkeyboard

    mode = "ssh"


class QuickKill(Exception):
    pass


class Snake:
    def __init__(self, matrix: RGBMatrix, color: Color, blank: Color):
        self.pos: deque[Pixel] = deque([Pixel(0, 1), Pixel(1, 1)])
        self.matrix: RGBMatrix = matrix
        self.color: Color = color
        self.blank = blank
        self.direction: Literal["w", "a", "s", "d"] = "d"

    def set_direction(self, key):
        if mode == "keyboard":
            key = key.name
        print(key)
        if key in "wasd":
            self.direction = key

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

    def move(self):
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

        self.pos.pop()
        if head in self.pos:
            raise QuickKill("Dead")

        self.pos.appendleft(head)


try:
    print("Press CTRL-C to stop.")
    snek = Snake(matrix, color=(255, 255, 255), blank=(0, 0, 0))
    if mode == "keyboard":
        for dir_ in "wasd":
            keyboard.on_press_key(dir_, snek.set_direction)
    else:
        thread = Thread(
            target=sshkeyboard.listen_keyboard, kwargs=dict(on_press=snek.set_direction)
        )
        thread.start()

    apple = Pixel(randint(0, matrix.width - 1), randint(0, matrix.height - 1))
    matrix.SetPixel(apple.x, apple.y, 255, 0, 0)
    print(apple)

    while True:
        snek.move()
        snek.draw_step()

        if snek.pos[0] == apple:
            snek.grow()
            apple = Pixel(randint(0, matrix.width - 1), randint(0, matrix.height - 1))
            matrix.SetPixel(apple.x, apple.y, 255, 0, 0)
            print(apple)
        time.sleep(0.1)


except (KeyboardInterrupt, QuickKill):
    print("kill1")
    if mode == "ssh":
        sshkeyboard.stop_listening()
    # noinspection PyUnboundLocalVariable
    print("kill2")
    sys.exit(0)
