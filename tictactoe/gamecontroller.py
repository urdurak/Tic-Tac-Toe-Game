import random
import pygame
from tictactoe.components import Button
from tictactoe.settings import settings

class GameController:
    def __init__(self, gameBoard):
        # Initialize the GameController with the provided gameBoard
        self.gameBoard = gameBoard
        self.running = False
        self.is_game_over = False
        self.gameMode = None

    def reset(self):
        # Reset the game state
        self.is_game_over = False
        self.running = False

    def start(self, gamemode):
        # Start the game with the specified game mode
        self.gameBoard.screen.fill(settings.bg_color)
        self.reset()
        self.gameMode = gamemode
        self.gameBoard.start()
        self.running = True

    def update(self):
        # Update the game state
        if self.running:
            if not self.gameBoard.is_paused():
                # Fill the screen with the background color
                self.gameBoard.screen.fill(settings.bg_color)
                # Draw game elements
                self.gameBoard.draw_grids()
                self.gameBoard.draw_players(self.gameMode)
                self.gameBoard.draw_your_turn(self.gameMode)
                self.gameBoard.draw_buttons()
                # Handle events if the game is not over
                if not self.is_game_over:
                    self.handle_events()
                self.gameBoard.draw_game()
                self.check_game_state()
                self.gameBoard.update_display()
                self.gameBoard.fps.tick(60)

    def handle_events(self):
        # Handle user input events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEMOTION:
                self.handle_mouse_motion(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_mouse_button_down(event)

    def handle_mouse_motion(self, event):
        # Handle mouse motion events
        if self.gameMode == "Two_players":
            for button in self.gameBoard.buttons:
                button.is_selected = button.rect.collidepoint(event.pos)

    def handle_mouse_button_down(self, event):
        # Handle mouse button down events
        if self.gameMode == "Two_players":
            for button in self.gameBoard.buttons:
                if button.rect.collidepoint(event.pos):
                    self.gameBoard.selected_button = button

        for pos in self.gameBoard.tic_tac_toe_board:
            if pygame.Rect(pos['position'][0], pos['position'][1], 100, 100).collidepoint(event.pos):
                self.handle_tic_tac_toe_board_click(pos)

    def handle_tic_tac_toe_board_click(self, pos):
        # Handle tic-tac-toe board click events
        if pos['value'] == "" or (
                self.gameBoard.current_player == self.gameBoard.starter_player and self.gameMode == "Single"):
            if pos['value'] == "" or not self.gameMode == "Single":
                pos['value'] = self.gameBoard.selected_button.text_obj.text
                self.gameBoard.change_player()
                self.change_selected_button()

    def change_selected_button(self):
        # Change the selected button and update its appearance
        self.gameBoard.selected_button = self.gameBoard.buttons[1] if self.gameBoard.selected_button == \
                                                                      self.gameBoard.buttons[0] else \
            self.gameBoard.buttons[0]
        self.gameBoard.buttons[0].is_selected, self.gameBoard.buttons[
            1].is_selected = not self.gameBoard.selected_button.is_selected, self.gameBoard.selected_button.is_selected

    def draw_line(self, start_position, end_position, orientation):
        # Draw a line on the screen based on the specified orientation
        if orientation == "row":
            start_position = (start_position[0], start_position[1] + settings.cell_size // 2)
            end_position = (end_position[0] + settings.cell_size, end_position[1] + settings.cell_size // 2)
        elif orientation == "col":
            start_position = (start_position[0] + settings.cell_size // 2, start_position[1])
            end_position = (start_position[0], start_position[1] + 3 * settings.cell_size + self.gameBoard.padding)
        elif orientation == "cross":
            end_position = (end_position[0] + settings.cell_size, end_position[1] + settings.cell_size)
        elif orientation == "reverse_cross":
            start_position = (start_position[0] + settings.cell_size - self.gameBoard.padding, start_position[1])
            end_position = (end_position[0], end_position[1] - self.gameBoard.padding + settings.cell_size)

        pygame.draw.line(self.gameBoard.screen, (255, 0, 0), start_position, end_position, 5)

    def check_game(self):
        # Check for a winner in the game
        for player in ["X", "O"]:
            # Check for rows
            for row in range(3):
                if all(cell["value"] == player for cell in self.gameBoard.tic_tac_toe_board[row * 3: (row + 1) * 3]):
                    start_position = self.gameBoard.tic_tac_toe_board[row * 3]["position"]
                    end_position = self.gameBoard.tic_tac_toe_board[(row + 1) * 3 - 1]["position"]
                    self.draw_line(start_position, end_position, "row")
                    return player

            # Check for columns
            for col in range(3):
                if all(cell["value"] == player for cell in self.gameBoard.tic_tac_toe_board[col::3]):
                    start_position = self.gameBoard.tic_tac_toe_board[col]["position"]
                    end_position = self.gameBoard.tic_tac_toe_board[col + 2]["position"]
                    self.draw_line(start_position, end_position, "col")
                    return player

            # Check for cross
            if all(cell["value"] == player for cell in self.gameBoard.tic_tac_toe_board[::4]):
                start_position = self.gameBoard.tic_tac_toe_board[0]["position"]
                end_position = self.gameBoard.tic_tac_toe_board[8]["position"]
                self.draw_line(start_position, end_position, "cross")
                return player
            # Check for reverse cross
            if all(cell["value"] == player for cell in self.gameBoard.tic_tac_toe_board[2:8:2]):
                start_position = self.gameBoard.tic_tac_toe_board[2]["position"]
                end_position = self.gameBoard.tic_tac_toe_board[6]["position"]
                self.draw_line(start_position, end_position, "reverse_cross")
                return player

        return None

    def check_game_state(self):
        # Check the current state of the game
        winner = self.check_game()
        if winner:
            if winner == self.gameBoard.starter_player:
                self.print_winner(self.gameBoard.starter_player)
            else:
                self.print_winner(self.gameBoard.get_opposite_player())
        else:
            empty_cells = [cell for cell in self.gameBoard.tic_tac_toe_board if cell["value"] == ""]
            if empty_cells:
                if self.gameMode == "Single" and self.gameBoard.current_player != self.gameBoard.starter_player:
                    self.draw_random(empty_cells)
            else:
                self.print_winner("draw")

    def draw_random(self, empty_cells):
        # Draw a random move for the computer player in single-player mode
        selected_cell = random.choice(empty_cells)
        selected_cell["value"] = self.gameBoard.current_player
        self.change_selected_button()
        self.gameBoard.change_player()

    def print_winner(self, winner_name):
        # Display the result of the game
        font = self.gameBoard.set_font(36)
        if winner_name == "draw":
            result_text = "Draw"
        elif winner_name == self.gameBoard.starter_player:
            result_text = "You won" if self.gameMode == "Single" else "Player 1 won"
        else:
            result_text = "PC won" if self.gameMode == "Single" else "Player 2 won"

        text = font.render(result_text, True, (255, 0, 0))

        text_rect = text.get_rect(midtop=(self.gameBoard.width // 2, self.gameBoard.padding * 2))

        self.is_game_over = True
        self.gameBoard.screen.blit(text, text_rect)
        self.show_over_buttons()
        pygame.display.flip()

    def show_over_buttons(self):
        # Display game-over buttons
        buttons = [
            Button(text="Restart", border_width=2, border_color=settings.text_color, hover_color="#fdcd56"),
            Button(text="Main Menu", border_width=2, border_color=settings.text_color, hover_color="#3aadd9")
        ]

        # Calculate total height of the buttons and padding
        total_height = sum(button.rect.height for button in buttons) + (len(buttons) - 1) * self.gameBoard.padding

        # Calculate starting Y position to center the buttons vertically
        start_y = (self.gameBoard.height - total_height - 2 * self.gameBoard.padding)

        # Set the X position for both buttons (fixed width)
        x_position = self.gameBoard.width - buttons[0].rect.width - self.gameBoard.padding

        for button in buttons:
            button.rect.topleft = (x_position, start_y)
            start_y += button.rect.height + self.gameBoard.padding
            button.draw(self.gameBoard.screen)

        self.handle_over_buttons(buttons)

    def handle_over_buttons(self, buttons):
        # Handle input for game-over buttons
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEMOTION:
                for button in buttons:
                    button.is_selected = button.rect.collidepoint(event.pos)
                    button.draw(self.gameBoard.screen)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for button in buttons:
                    if button.rect.collidepoint(event.pos):
                        self.handle_over_button_click(button)

    def handle_over_button_click(self, button):
        # Handle click events for game-over buttons
        if button.text_obj.text == "Restart":
            # Handle Restart button click
            self.start(self.gameMode)
        elif button.text_obj.text == "Main Menu":
            # Handle Main Menu button click
            self.gameBoard.screen.fill(settings.bg_color)
            self.running = False
