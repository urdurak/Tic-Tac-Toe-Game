import json
import os
import pygame
from tictactoe.colors import Color


class Settings:
    def __init__(self):
        self.cell_size = 110
        self.padding = 10
        self.width, self.height = self.get_screen_resolution()
        self.bg_color = None
        self.grid_color = None
        self.border_color = None
        self.text_color = None
        self.button_color = None
        self.button_hover_color = None
        self.overlay_color = None
        self.Game_theme = "light"
        self.DEV_MODE = True
        self.set_theme(self.Game_theme)

    def get_screen_resolution(self):
        pygame.init()
        w, h = pygame.display.get_desktop_sizes()[0]
        pygame.quit()
        width = w * 0.8
        height = h * 0.8
        adjusted_width = ((width // self.cell_size) * self.cell_size) + 2 * self.padding
        adjusted_height = ((height // self.cell_size) * self.cell_size) + (2 * self.padding)
        return adjusted_width, adjusted_height

    def set_light_theme(self):
        self.bg_color = Color("seasalt")
        self.grid_color = Color("light_gray")
        self.border_color = Color("dodger_blue")  # "#2196F3"
        self.text_color = Color("black")
        self.button_color = Color("seasalt")
        self.button_hover_color = Color("timberwolf")  # Color("light_gray")
        self.overlay_color = Color("giants_orange")

    def set_dark_theme(self):
        self.bg_color = Color("eerie_black")
        self.grid_color = Color("jet")
        self.border_color = Color("dodger_blue")
        self.text_color = Color("white")
        self.button_color = Color("black")
        self.button_hover_color = Color("eerie_black")
        self.overlay_color = Color("giants_orange")

    def set_theme(self, theme):
        if theme == "light":
            self.set_light_theme()
        elif theme == "dark":
            self.set_dark_theme()
        else:
            print("This theme is not correct")

    def save_settings(self):
        settings_data = {
            "cell_size": self.cell_size,
            "width": self.width,
            "height": self.height,
            "bg_color": self.bg_color,
            "grid_color": self.grid_color,
            "border_color": self.border_color,
            "text_color": self.text_color,
            "button_color": self.button_color,
            "button_hover_color": self.button_hover_color,
            "overlay_color": self.overlay_color,
            "Game_theme": self.Game_theme,
            "DEV_MODE": self.DEV_MODE,
        }

        with open("settings.json", "w") as file:
            json.dump(settings_data, file)

    def load_settings(self):
        try:
            with open("settings.json", "r") as file:
                settings_data = json.load(file)
                self.cell_size = settings_data.get("cell_size", self.cell_size)
                self.width = settings_data.get("width", self.width)
                self.height = settings_data.get("height", self.height)
                self.bg_color = settings_data.get("bg_color", self.bg_color)
                self.grid_color = settings_data.get("grid_color", self.grid_color)
                self.border_color = settings_data.get("border_color", self.border_color)
                self.button_color = settings_data.get("button_color", self.button_color)
                self.button_hover_color = settings_data.get("button_hover_color", self.button_hover_color)
                self.overlay_color = settings_data.get("overlay_color", self.overlay_color)
                self.Game_theme = settings_data.get("Game_theme", self.Game_theme)
                self.DEV_MODE = settings_data.get("DEV_MODE", self.DEV_MODE)


        except FileNotFoundError:
            self.save_settings()  # Save Default values


settings: Settings = Settings()
settings.load_settings()

# Get the current working directory
current_directory = os.getcwd()

# Define the relative path to the resources directory
resources_directory = "resources/"

# Create the full path by joining the current directory and the resources directory
RESOURCES_PATH = os.path.join(current_directory, resources_directory)
