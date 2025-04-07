"""
    Containing all the settings required for the pygame GUI in main.py.
"""

# COLORS (r, g, b)
WHITE = (255, 255, 255)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
MENU_COLOR = (60, 60, 60)

# Game settings
WIDTH = 500
HEIGHT = 600
FPS = 60
title = "AI Trained Tic-Tac-Toe"
BGCOLOUR = DARKGREY

TILESIZE = 120
BOARD_SIZE = 3

MARGIN_X = int((WIDTH - (BOARD_SIZE * TILESIZE)) / 2)
MARGIN_Y = int((HEIGHT - (BOARD_SIZE * TILESIZE)) / 2)


def board_to_pixel(x: int, y: int) -> tuple[int, int]:
    """
    Returns the board coordinates as pixel coordinates.
    """
    return MARGIN_X + TILESIZE * x, MARGIN_Y + TILESIZE * y
