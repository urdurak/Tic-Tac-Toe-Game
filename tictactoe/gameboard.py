import os.path
import random
import pygame
from tictactoe.components import Button
from tictactoe.settings import settings, RESOURCES_PATH

class Gameboard:
    def __init__(self, width, height):
        self.width = int(width)
        self.height = int(height)
        self.cell_size = settings.cell_size
        self.start_X = int((self.width - self.cell_size * 3) // 2)
        self.start_Y = int((self.height - self.cell_size * 3) // 2)
        self.padding = 10
        self.screen = pygame.display.set_mode((width, height))
        self.paused = False
        pygame.display.set_caption("Tic Tac Toe")
        self.fps = pygame.time.Clock()
        self.font = self.set_font()
        self.tic_tac_toe_board = self.create_tic_tac_toe_board()
        self.image_X = self.load_image("X")
        self.image_O = self.load_image("O")
        self.buttons = [
            Button(text="X", border_width=2, border_color=settings.text_color, hover_color="#fdcd56"),
            Button(text="O", border_width=2, border_color=settings.text_color, hover_color="#3aadd9")
        ]
        self.selected_button = None
        self.current_player = None
        self.starter_player = None
        self.start()

    def start(self):
        self.current_player = random.choice(['X', "O"])
        self.starter_player = self.current_player
        self.selected_button = self.buttons[0] if self.current_player == "X" else self.buttons[1]
        self.draw_grids()
        self.tic_tac_toe_board = self.create_tic_tac_toe_board()

    def load_image(self, value: str):
        image_path = os.path.join(RESOURCES_PATH, f"images/1x/image_{value.lower()}.png")
        image = pygame.image.load(image_path)
        image = pygame.transform.smoothscale(image, (100, 100))
        return image

    def create_tic_tac_toe_board(self):
        tic_tac_toe_board = []
        for i in range(3):
            for j in range(3):
                x = self.start_X + j * (self.cell_size + self.padding)
                y = self.start_Y + i * (self.cell_size + self.padding)
                tic_tac_toe_board.append({"value": "", "position": (x, y)})
        return tic_tac_toe_board

    def draw_grids(self):
        grid_width = 5
        for i in range(self.start_X + self.cell_size, self.start_X + self.cell_size * 3, self.cell_size + 10):
            pygame.draw.line(self.screen, settings.text_color, (i, self.start_Y),
                             (i, (self.start_Y + self.cell_size * 3 + self.padding)),
                             grid_width)
        for i in range(self.start_Y + self.cell_size, self.start_Y + self.cell_size * 3, self.cell_size + 10):
            pygame.draw.line(self.screen, settings.text_color, (self.start_X, i),
                             (self.start_X + self.cell_size * 3 + self.padding, i),
                             grid_width)

    def draw_game(self):
        for value in self.tic_tac_toe_board:
            rect = pygame.rect.Rect(value['position'][0], value['position'][1], 100, 100)
            if value['value'] == "":
                pygame.draw.rect(self.screen, settings.grid_color, rect)
            elif value['value'] == "X":
                self.screen.blit(self.image_X, (value['position'][0], value['position'][1]))
            elif value['value'] == "O":
                self.screen.blit(self.image_O, (value['position'][0], value['position'][1]))

    def find_max_font_size(self):
        padding_space = 20
        max_text_width = max(button.text_obj.rect.width for button in self.buttons) + padding_space
        return max_text_width

    def draw_buttons(self):
        max_width = self.find_max_font_size() + self.cell_size
        button_height = self.buttons[0].rect.height
        start_y = self.height - button_height - self.padding

        total_button_width = sum(button.rect.width for button in self.buttons) + len(self.buttons) * self.padding
        start_x = (self.width - total_button_width) // 2 + self.padding

        for i, button in enumerate(self.buttons):
            button_rect = pygame.Rect(start_x + i * (button.rect.width + self.padding),
                                      start_y,
                                      max_width, button.rect.height)

            button.rect = button_rect
            button.text_obj.font = self.set_font(50)
            button.text_obj.render()
            button.is_selected = self.selected_button == button

            button.draw(self.screen)


    def change_player(self):
        self.current_player = "O" if self.current_player == "X" else "X"

    def draw_players(self, gamemode):
        p1_text = f"You : {self.starter_player}" if gamemode == "Single" else f"Player 1 : {self.starter_player}"
        p2_text = f"Pc : {self.get_opposite_player()}" if gamemode == "Single" else f"Player 2 : {self.get_opposite_player()}"

        player_1 = self.set_font(28).render(p1_text, True, settings.text_color)
        player_2 = self.set_font(28).render(p2_text, True, settings.text_color)

        p_rect = player_1.get_rect(topleft=(self.padding, self.padding * 2))
        p2_rect = player_2.get_rect(topleft=(self.padding, p_rect.height + self.padding * 2))

        self.screen.blit(player_1, p_rect)
        self.screen.blit(player_2, p2_rect)

    def draw_your_turn(self, gamemode):
        p1_text = "Your Turn" if gamemode == "Single" else "Player 1 Turn"
        p2_text = "Pc Turn" if gamemode == "Single" else "Player 2 Turn"

        player_1 = self.set_font(28).render(p1_text, True, settings.text_color)
        player_2 = self.set_font(28).render(p2_text, True, settings.text_color)
        p_rect = player_1.get_rect()
        p_rect.center = (self.width//2 - p_rect.width *2, self.height//2)
        p2_rect = player_2.get_rect(center=(self.width//2 + p_rect.width *2, self.height//2))

        player_rect = p_rect if self.current_player == self.starter_player else p2_rect
        self.screen.blit(player_1 if self.current_player == self.starter_player else player_2, player_rect)

    def get_opposite_player(self):
        return "O" if self.starter_player == "X" else "X"

    def update_display(self):
        pygame.display.flip()

    def toggle_pause(self):
        self.paused = not self.paused

    def is_paused(self):
        return self.paused

    def get_screen(self):
        return self.screen


    def set_font(self, font_size=24):
        try:
            font = pygame.font.Font(os.path.join(RESOURCES_PATH, "fonts/Roboto-Black.ttf"), font_size)
        except pygame.error:
            font = pygame.font.Font(None, font_size)
        return font
