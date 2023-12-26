import os

import pygame
from tictactoe.settings import settings, RESOURCES_PATH

# Load settings
settings.load_settings()

class Text:
    def __init__(self, text="Hello world", font=None, text_color=settings.text_color):
        # Initialize a Text object with default values
        if font is None:
            # Use the default font if none is provided
            font = pygame.font.Font(os.path.join(RESOURCES_PATH, "fonts/Roboto-Black.ttf"), 24)
        self.text = text
        self.font = font
        self.color = text_color
        self.render()

    def render(self):
        # Render the text using the specified font and color
        self.surface = self.font.render(self.text, True, self.color)
        self.rect = self.surface.get_rect()

    def update_text(self, new_text):
        # Update the text and re-render
        self.text = new_text
        self.render()

    def set_position(self, x, y):
        # Set the top-left corner position of the text
        self.rect.topleft = (x, y)

    def draw(self, screen):
        # Draw the text on the screen
        screen.blit(self.surface, self.rect)

    def get_font(self, font_size=24):
        try:
            # Try loading the specified font
            font = pygame.font.Font(RESOURCES_PATH + "/fonts/Roboto-Black.ttf", font_size)
        except pygame.error:
            # Use a default font if loading fails
            font = pygame.font.Font(None, font_size)
        return font

class Button:
    def __init__(self, x=0, y=0, width=200, height=50, text="Click me", color=settings.button_color,
                 hover_color=settings.button_hover_color,
                 border_color=settings.border_color, border_width=0, corner_radius=0, **kwargs):
        # Initialize a Button object with default values
        self.rect = pygame.Rect(x, y, width, height)
        self.text_obj = Text(text)
        self.color = color
        self.hover_color = hover_color
        self.border_color = border_color
        self.border_width = border_width
        self.corner_radius = corner_radius
        self.is_selected = False

    def draw(self, screen):
        # Draw the button on the screen
        # Border drawing
        if self.border_width > 0:
            pygame.draw.rect(screen, self.border_color, self.rect, self.border_width, border_radius=self.corner_radius)

        # Fill drawing based on selection
        if self.is_selected:
            pygame.draw.rect(screen, self.hover_color,
                             (self.rect.x + self.border_width, self.rect.y + self.border_width,
                              self.rect.width - 2 * self.border_width,
                              self.rect.height - 2 * self.border_width),
                             border_radius=self.corner_radius - self.border_width)
        else:
            pygame.draw.rect(screen, self.color, (self.rect.x + self.border_width, self.rect.y + self.border_width,
                                                  self.rect.width - 2 * self.border_width,
                                                  self.rect.height - 2 * self.border_width),
                             border_radius=self.corner_radius - self.border_width)

        text_rect = self.text_obj.rect
        text_rect.center = self.rect.center
        screen.blit(self.text_obj.surface, text_rect)

# Example usage
# text_obj = {'font_size': 36, 'color': (255, 255, 255), 'font_name': None}
# button = Button(100, 100, 200, 50, "Click me", (50, 50, 50), (100, 100, 100), (255, 0, 0), 0, 0, text_obj)
