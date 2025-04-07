from __future__ import annotations
from typing import Optional
import random

class Tree:
    """
    A tree data structure to represent possible game states in Tic-Tac-Toe.

    Instance Attributes:
        - weight: The probability weight of this branch (Optional).
        - root: The current game state (GameState).
        - children: A list of child Tree nodes.

    Representation Invariants:
        - root.children == [] if root.get_game_result in [0, 1, 2]
    """
    weight: float
    root: GameState
    children: list[Tree]

    def __init__(self, game: Optional[GameState] = None, turn: Optional[int] = None, coords: Optional[tuple] = None) -> None:
        """Initialize a new Tree with all possibile game states."""
        self.weight = 1.0
        self.children = []

        if turn is None:
            turn = 2

        if game is None:
            self.root = GameState()
        else:
            self.root = GameState(game)
            x, y = coords
            self.root.board[x][y] = turn
            self.root.last_move = (x, y)

        if self.root.get_game_result() == -1:
            for i in range(3):
                for j in range(3):
                    if self.root.board[i][j] == 0:
                        self.children.append(Tree(game=self.root, turn=(turn % 2) + 1, coords=(i, j)))

    def choose_move(self, brd: list[list[str]], frst: int) -> tuple[int, int]:
        """Choose a random move from available children depending on their weight."""
        if frst == 0:
            frst = 'X'
        elif frst == 1:
            frst = 'O'
        else:
            raise ValueError

        new_brd = [[], [], []]

        for row in range(3):
            for col in range(3):
                if brd[row][col] == frst:
                    new_brd[row].append(1)
                elif brd[row][col] == '':
                    new_brd[row].append(0)
                else:
                    new_brd[row].append(2)

        t = self.find_subtree(new_brd)

        weights = [child.weight for child in t.children] 

        rand_child_index = random.choices(range(len(t.children)), weights=weights)[0]
        return t.children[rand_child_index].root.last_move

    def choose_random(self) -> int:
        """Choose a random move from available children not depending on their weight."""
        return random.choices(range(len(self.children)))[0]

    def find_subtree(self, target: list[list[str]]) -> Tree:
        if self.root.board == target:
            return self

        for child in self.children:
            result = child.find_subtree(target)
            if result:
                return result


class GameState:
    """
    Represents the state of the Tic-Tac-Toe game.

    Instance Attributes:
        - board: A 3x3 list of lists representing the game board.
        - last_move: the coordinates of the last move
    """
    board: list[list[int]]
    last_move: tuple[int, int]

    def __init__(self, state: Optional[GameState] = None) -> None:
        if state is None:
            self.board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        else:
            self.board = [x.copy() for x in state.board]
        self.last_move = (-1, -1)

    def get_game_result(self) -> int:
        """ Return status of game; 0 if there is a draw, 1 if player 1 wins, and 2 if player 2 wins,
        -1 if the game is still going."""
        # Check rows and columns
        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] != 0:
                return self.board[i][0]  # Row win
            if self.board[0][i] == self.board[1][i] == self.board[2][i] != 0:
                return self.board[0][i]  # Column win

        # Check diagonals
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != 0:
            return self.board[0][0]  # Diagonal win
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != 0:
            return self.board[0][2]  # Diagonal win

        # Check for a tie (if there are no empty spaces left)
        for row in self.board:
            if 0 in row:
                return -1  # The game is not over yet

        return 0  # It's a draw
