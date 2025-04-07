import copy
import random
import pygame
from learningModel import MlModel
from settings import *
from sprites import *
import learningModel
import treeStruct

class Game:
    def __init__(self):

        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(title)
        self.clock = pygame.time.Clock()
        self.player_score = 0
        self.computer_score = 0

        # Easy Model
        self.esy_ai = learningModel.MlModel(100000, treeStruct.Tree())
        self.esyAI = self.esy_ai.load_model("easy_game_model.pkl")

        # Medium Model
        self.med_ai = learningModel.MlModel(5000000, treeStruct.Tree())
        self.mdmAI = self.med_ai.load_model("medium_game_model.pkl")

        # Hard Model
        self.hard_ai = learningModel.MlModel(15000000, treeStruct.Tree())
        self.hrdAI = self.hard_ai.load_model("hard_game_model.pkl")


    def new(self):
        self.board = Board()
        self.player_turn = random.randint(0, 1)

    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
        else:
            self.end_screen()

    def update(self):
        if not self.player_turn and not self.board.is_board_full() and not self.is_winner(self.board.board_list, "X"):
            row, col = self.use_ai()
            self.move(row, col)

    def is_winner(self, board, icon):
        # check horizontal
        for row in range(3):
            if board[row][0] == icon and board[row][1] == icon and board[row][2] == icon:
                self.draw_horizontal_line(row)
                return True

        # check vertical
        for col in range(3):
            if board[0][col] == icon and board[1][col] == icon and board[2][col] == icon:
                self.draw_vertical_line(col)
                return True

        # check ascending diagonal
        if board[2][0] == icon and board[1][1] == icon and board[0][2] == icon:
            self.draw_ascending_diagonal()
            return True

        # check descending diagonal
        if board[0][0] == icon and board[1][1] == icon and board[2][2] == icon:
            self.draw_descending_diagonal()
            return True

        return False

    def draw_horizontal_line(self, row):
        pos_y = row * TILESIZE + (MARGIN_Y + TILESIZE / 2)
        pygame.draw.line(self.screen, LIGHTGREY, (MARGIN_X + TILESIZE / 2, pos_y), (MARGIN_X + 5 * TILESIZE / 2, pos_y),
                         4)

    def draw_vertical_line(self, col):
        pos_x = col * TILESIZE + (MARGIN_X + TILESIZE / 2)
        pygame.draw.line(self.screen, LIGHTGREY, (pos_x, MARGIN_Y + TILESIZE / 2), (pos_x, MARGIN_Y + 5 * TILESIZE / 2),
                         4)

    def draw_descending_diagonal(self):
        pygame.draw.line(self.screen, LIGHTGREY, (MARGIN_X + TILESIZE / 2, MARGIN_Y + TILESIZE / 2),
                         (MARGIN_X + 5 * TILESIZE / 2, MARGIN_Y + 5 * TILESIZE / 2), 4)

    def draw_ascending_diagonal(self):
        pygame.draw.line(self.screen, LIGHTGREY, (MARGIN_X + TILESIZE / 2, MARGIN_Y + 5 * TILESIZE / 2),
                         (MARGIN_X + 5 * TILESIZE / 2, MARGIN_Y + TILESIZE / 2), 4)

    def move(self, row, col):
        if self.player_turn:
            self.board.board_list[row][col] = "X"
        else:
            self.board.board_list[row][col] = "O"
        self.player_turn = not self.player_turn

    def use_ai(self):

        return self.hrdAI.decisionTree.choose_move(self.board.board_list, self.player_turn)

    def draw_icons(self):
        for i, row in enumerate(self.board.board_list):
            for j, icon in enumerate(row):
                x, y = board_to_pixel(j, i)
                Icon(x, y, icon).draw(self.screen)

    def draw(self):
        self.screen.fill(BGCOLOUR)
        self.board.draw_board(self.screen)
        self.draw_icons()
        if self.is_winner(self.board.board_list, "X"):
            # player won
            self.player_score += 1
            UIElement(160, 500, "Human Wins!").draw(self.screen, 40)
            UIElement(100, 550, "Click anywhere to play again").draw(self.screen, 20)
            self.playing = False
        elif self.is_winner(self.board.board_list, "O"):
            # computer won
            self.computer_score += 1
            UIElement(140, 500, "AI Wins!").draw(self.screen, 40)
            UIElement(100, 550, "Click anywhere to play again").draw(self.screen, 20)
            self.playing = False
        elif self.board.is_board_full():
            # Tie game
            UIElement(140, 500, "It's a Tie!").draw(self.screen, 40)
            UIElement(100, 550, "Click anywhere to play again").draw(self.screen, 20)
            self.playing = False

        UIElement(50, 40, f"Human: {self.player_score}").draw(self.screen, 30)
        UIElement(350, 40, f"AI: {self.computer_score}").draw(self.screen, 30)
        pygame.display.flip()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit(0)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.player_turn:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    row, col = self.board.is_clicked(mouse_x, mouse_y)
                    if row is not None:
                        # add the icon to the board
                        self.move(row, col)

    def end_screen(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit(0)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    return


game = Game()
while True:
    game.new()
    game.run()
