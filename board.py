from __future__ import annotations
from abc import ABC, abstractmethod
from enum import IntEnum
import random


import numpy as np

from PIL import Image

class Player(IntEnum):
    BLUE = 1
    RED = 2
    GREEN = 3
    YELLOW = 4

class DiceResults(IntEnum):
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    PLACE_WALL = 5
    MOVE_MINOTAUR = 6

Position = tuple[int, int]

class BaseBoard(ABC):
    """
    Board tiles can be encoded in the binary: 0bGSPPPPAA
        - if G is 1, this is a goal tile for the player PPPP. If the LSB is 1, this tile has a hero (of the corresponding color)
        - if S is 1, this is a starting tile for the player PPPP. If the LSB is 1, this tile has a hero (of the corresponding color)
        - PPPP is a 4-bit number codifying the playr's number. This is a hero
        - if AA is 10 -> Minotaur
        - if AA is 01 -> HEDGE (immovable)
        - if AA is 11 -> WALL  (movable)
        - if 0, then it's a tile of grass
    """

    GOAL_TILE_MASK  = 0b10000000
    START_TILE_MASK = 0b01000000
    PLAYER_MASK     = 0b00111100
    SPECIAL_MASK    = 0b00000011

    def __init__(self, x_size: int, y_size: int, players: set[Player]):
        self.x_size = x_size
        self.y_size = y_size

        self.board = np.zeros((self.x_size, self.y_size), dtype=np.uint8)

        self.players = sorted(players, key=lambda p: p.value)
        self.turn: int = self.players[0]

    def import_from_image(self, filepath: str) -> None:
        if not filepath.endswith('.png'):
            raise ValueError(f"File {filepath} should have a .png extension.")

        image = Image.open(filepath)
        width, height = image.size
        if width != self.x_size or height != self.y_size:
            raise ValueError(f"Image ({filepath}) has size ({width}, {height}) but should be ({self.x_size}, {self.y_size})")

        flattened = image.get_flattened_data()
        for y in range(self.y_size):
            for x in range(self.x_size):
                n = y * self.x_size + x
                color = flattened[n]
                if not isinstance(color, tuple) or len(color) != 4:
                    raise TypeError(f"Image ({filepath}) has the wrong format (expected RGBA)")
                coord: int = 0

                # decode presence of colors as player
                if color[0] > 0:
                    if color[1] > 0:
                        coord |= Player.YELLOW << 2
                    else:
                        coord |= Player.RED << 2
                elif color[1] > 0:
                    coord |= Player.GREEN << 2
                elif color[2] > 0:
                    coord |= Player.BLUE << 2

                # decode the rest from the alpha channel like (255 - GSAA)
                alpha = 255 - color[3]
                alpha = ((alpha & 0b1100) << 5) | (alpha & 0b0011)
                coord |= alpha

                assert(coord <= 0xFF)

                self.board[x, y] = coord

    def initialize_board(self) -> None:
        pass

    def throw_dice(self) -> DiceResults:
        choices = list(DiceResults)
        return random.choice(choices)

    @abstractmethod
    def _move_piece(self, player: Player, origin: Position, destination: Position) -> bool:
        """Returns true if the move was legal"""

class Board2P(BaseBoard):
    def __init__(self, x_size: int, y_size: int):
        super().__init__(x_size, y_size, {Player.BLUE, Player.RED})

        self.board = [
            [0x91, 0x91,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0],
            [0x91,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0,    0],
            [    0,   0, 0x01, 0x01,    0,    0, 0x01,    0,    0, 0x01, 0x01,    0,    0,    0,    0,    0, 0x01, 0x01,    0,    0],
            [    0,    0, 0x01,    0,    0,    0, 0x01,    0,    0,    0,    0,    0,    0,   0,    0,    0, 0x01, 0x01]
        ]
