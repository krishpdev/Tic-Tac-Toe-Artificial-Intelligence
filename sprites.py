"""
    Contains all the sprites or 2D objects needed to display the Tic-Tac-Toe board in main.py
"""

import pygame
from settings import *


class Icon:
    """
    Icon class represents a simple icon (text) displayed on the board.

    Instance Attributes:
    - x: The x-coordinate of the icon's position
    - y: The y-coordinate of the icon's position
    - text: The text displayed on the icon
    """
    x: int
    y: int
    text: str

    def __init__(self, x: int, y: int, text: str) -> None:
        self.x, self.y = x, y
        self.text = text

    def draw(self, screen: pygame.Surface) -> None:
        """
        Draws the icon (text) on the screen.
        """
        font = pygame.font.SysFont("Consolas", 70)
        text = font.render(self.text, True, WHITE)
        font_size = font.size(self.text)
        draw_x = self.x + (TILESIZE / 2) - font_size[0] / 2
        draw_y = self.y + (TILESIZE / 2) - font_size[1] / 2
        screen.blit(text, (draw_x, draw_y))


class Board:
    """
    Board class represents the game board where the icons are placed.

    Instance Attributes:
        - board_list: A 2D list representing the game board; each element is either an empty string or a player mark

    """

    board_list: list[list[str]]

    def __init__(self) -> None:
        self.board_list = [["" for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

    def draw_board(self, screen: pygame.Surface) -> None:
        """
        Draws the grid lines on the game board.
        """
        for row in range(0, TILESIZE * 2, TILESIZE):
            pygame.draw.line(screen, WHITE,
                             (MARGIN_X + row + TILESIZE, MARGIN_Y),
                             (MARGIN_X + row + TILESIZE, MARGIN_Y + BOARD_SIZE * TILESIZE), 4)
        for col in range(0, TILESIZE * 2, TILESIZE):
            pygame.draw.line(screen, WHITE,
                             (MARGIN_X, MARGIN_Y + col + TILESIZE),
                             (MARGIN_X + BOARD_SIZE * TILESIZE, MARGIN_Y + col + TILESIZE), 4)

    def is_clicked(self, mouse_x: int, mouse_y: int) -> tuple[int | None, int | None]:
        """
        Checks if a cell on the board has been clicked.
        """
        for row in range(len(self.board_list)):
            for col in range(len(self.board_list[row])):
                x, y = board_to_pixel(col, row)
                if x <= mouse_x <= x + TILESIZE and y <= mouse_y <= y + TILESIZE and self.board_list[row][col] == "":
                    return row, col
        return None, None

    def is_board_full(self) -> bool:
        """
        Checks if the game board is full (no empty cells)
        """
        return not any("" in row for row in self.board_list)


class UIElement:
    """
        UIElement class represents a general UI element, such as labels or other text elements.

        Instance Attributes:
            - x: The x-coordinate of the element's position
            - y: The y-coordinate of the element's position
    """
    x: int
    y: int
    text: str

    def __init__(self, x: int, y: int, text: str) -> None:
        self.x, self.y = x, y
        self.text = text

    def draw(self, screen: pygame.Surface, font_size: int) -> None:
        """
        Draws the text provided on the screen.
        """
        font = pygame.font.SysFont("Consolas", font_size)
        text = font.render(self.text, True, WHITE)
        screen.blit(text, (self.x, self.y))
