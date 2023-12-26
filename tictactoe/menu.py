import pygame
from tictactoe.components import ui_button
from tictactoe.settings import settings, RESOURCES_PATH

class BaseMenu:
    def __init__(self, title, gameboard, game_controller, buttons):
        # Initialize the BaseMenu with the provided parameters
        self.title = title
        self.gameboard = gameboard
        self.game_controller = game_controller
        self.font = self.gameboard.set_font(24)
        self.buttons = buttons
        self.selected_button = self.buttons[0]
        self.gameboard.screen.fill(settings.bg_color)

    def draw_menu(self):
        # Draw the menu on the screen
        between_space = 10
        button_height = self.buttons[0].rect.height
        total_height = len(self.buttons) * (button_height + between_space)  # Leave a space of 10 units between each button
        start_y = (self.gameboard.height - total_height) // 2
        for i, button in enumerate(self.buttons):
            self.draw_button(button, i, button_height, start_y, between_space)
        pygame.display.flip()

    def draw_button(self, button, index, button_height, start_y, between_space):
        # Draw a button on the screen
        button.text_obj.font = self.font
        button.text_obj.render()
        max_width = self.find_max_font_size(self.buttons)
        button_rect = pygame.Rect(self.gameboard.width // len(self.buttons),
                                  start_y + index * (button_height + between_space),
                                  max_width, button_height)
        button_rect.x = self.gameboard.width // 2 - button_rect.width // 2
        button.rect = button_rect

        if button == self.selected_button:
            button.is_selected = True
        else:
            button.is_selected = False
        button.draw(self.gameboard.screen)

    def find_max_font_size(self, buttons):
        # Find the maximum font size among the buttons
        padding_space = 20
        max_text_width = max(button.text_obj.rect.width for button in buttons) + padding_space
        return max_text_width

    def check_events(self):
        # Check user input events
        mouse_pos = pygame.mouse.get_pos()
        for i, button in enumerate(self.buttons):
            if button.rect.collidepoint(mouse_pos):
                self.selected_button = button
                button.is_selected = True
            else:
                button.is_selected = False
        self.draw_menu()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for button in self.buttons:
                    if button.rect.collidepoint(pygame.mouse.get_pos()):
                        return button.text_obj.text
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    self.selected_button = self.get_adjacent_button(-1)
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    self.selected_button = self.get_adjacent_button(1)
                elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    return self.selected_button.text_obj.text
            elif event.type == pygame.MOUSEBUTTONUP:
                break

    def get_adjacent_button(self, direction):
        # Get the button adjacent to the currently selected button
        current_index = self.buttons.index(self.selected_button)
        new_index = (current_index + direction) % len(self.buttons)
        return self.buttons[new_index]

class MainMenu(BaseMenu):
    def __init__(self, gameboard, game_controller):
        # Initialize the MainMenu with specific parameters
        title = "mainMenu"
        buttons = [ui_button.Button(text="Play Single Player (Vs PC)", border_width=2, corner_radius=10),
                   ui_button.Button(text="Play Two Players", border_width=2, corner_radius=10),
                   ui_button.Button(text="Exit", border_width=2, corner_radius=10)
                   ]
        super().__init__(title, gameboard, game_controller, buttons)
        # Uncomment the following lines if you have the background image
        # self.main_back = pygame.image.load(os.path.join(RESOURCES_PATH, "images/back.png"))
        # self.main_back = pygame.transform.scale(self.main_back, (self.gameboard.width, self.gameboard.height))
        # self.draw_background()

    # Uncomment the following method if you have the background image
    # def draw_background(self):
    #     self.gameboard.screen.blit(self.main_back, (0, 0))
