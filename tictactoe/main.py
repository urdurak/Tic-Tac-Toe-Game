import pygame
from tictactoe.gameboard import Gameboard
from tictactoe.gamecontroller import GameController
from tictactoe.settings import settings, RESOURCES_PATH
from tictactoe.menu import MainMenu

# Initialize pygame
pygame.init()

# Create an instance of the Gameboard, GameController, and MainMenu
gameBoard = Gameboard(settings.width, settings.height)
game_controller = GameController(gameBoard)
main_menu = MainMenu(gameBoard, game_controller)

# Load settings
settings.load_settings()


def play_game(gameMode):
    # Start the game with the specified game mode
    game_controller.start(gameMode)
    while game_controller.running:
        # Update the game state
        game_controller.update()


def main():
    while True:
        # Uncomment the following line if you have a background image
        # main_menu.draw_background()

        # Draw the main menu and handle user input
        main_menu.draw_menu()
        action = main_menu.check_events()

        # Perform actions based on user input
        if action == "Play Single Player (Vs PC)":
            play_game("Single")
        elif action == "Play Two Players":
            play_game("Two_players")
        elif action == "Exit":
            pygame.quit()
            quit()


if __name__ == "__main__":
    main()
