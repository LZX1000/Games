# display.py

import pygame

from typing import Any


type color = tuple[int, int, int]
type coords = tuple[int, int]

DEFAULT_INTERNAL_RESOLUTION = (1280, 780)
DEFAULT_EXTERNAL_RESOLUTION = (1920, 1080)
FONT_SCALE_FACTOR = 36


class Display:
    __slots__ = (
        '__internal_resolution',
        '__external_resolution',
        '__title',
        '__font',
        '__debug_font',
        '__internal_surface',
        '__screen'
    )

    def __init__(
        self,
        internal_resolution: tuple[int, int] = DEFAULT_INTERNAL_RESOLUTION,
        external_resolution: tuple[int, int] = DEFAULT_EXTERNAL_RESOLUTION,
        title: str = "unnamed"
    ) -> None:
        from ctypes import windll

        # Make the screen not die
        windll.user32.SetProcessDPIAware()

        # Initialize Pygame
        pygame.init()
        pygame.font.init()
        pygame.display.set_caption(title)

        # Store fields
        self.__internal_resolution = internal_resolution
        self.__external_resolution = external_resolution
        self.__title = title
        
        # Set the font
        self.__font = pygame.font.SysFont("Arial", self.__internal_resolution[0] // FONT_SCALE_FACTOR)
        self.__debug_font = pygame.font.SysFont("Arial", self.__font.get_height() // 2)

        # Create internal surface for rendering
        self.__internal_surface = pygame.Surface(self.__internal_resolution)
        
        # Create the main display surface
        self.__screen = pygame.display.set_mode(self.__external_resolution)  # Fullscreen can be enabled with pygame.FULLSCREEN

    '''FUNCTIONS'''

    def fill(self, new: color) -> None:
        """Fill the internal surface with a color."""
        self.__internal_surface.fill(new)

    def blit(self, source: pygame.Surface, dest: tuple[int, int]) -> None:
        """Blit a source surface onto the internal surface at a given position."""
        self.__internal_surface.blit(source, dest)

    def debug(self, values: dict[str, Any]) -> None:
        """Draw debug information on the internal surface."""
        # Draw a border around the internal surface
        pygame.draw.rect(self.__internal_surface, (255, 0, 0), (0, 0, *self.__internal_resolution), 1)
        
        # Draw the mouse position
        if (mouse_pos := values.get('mouse_pos', False)):
            pygame.draw.circle(self.__internal_surface, (0, 0, 0), mouse_pos, 2)

        # Button hover
        if (button := values.get('button_hover', False)):
            repr_text = repr(button).split('\n')
            for i, line in enumerate(repr_text):
                button_debug_surface = self.__debug_font.render(line, False, (0, 0, 0), (255, 255, 255))
                button_debug_surface = button_debug_surface.convert_alpha()
                button_debug_surface = button_debug_surface.convert_alpha() # Allow per-pixel changes
                button_debug_surface.set_alpha(128)  # Semi-transparent
                self.__internal_surface.blit(button_debug_surface, (mouse_pos[0], mouse_pos[1] + i * self.__debug_font.get_height()))

        # Draw the title
        title_surface = self.__font.render(self.__title, True, (255, 255, 255))
        self.__internal_surface.blit(title_surface, (10, 10))

    def update(self, values: dict[str, Any]) -> None:
        """Update the display with the current internal surface."""
        if values.get('debug_mode', False):
            self.debug(values)

        scaled_surface = pygame.transform.scale(self.__internal_surface, self.__external_resolution)
        self.__screen.blit(scaled_surface, (0, 0))
        pygame.display.flip()

    @property
    def font(self) -> pygame.font.Font: return self.__font
    @property
    def title(self) -> str: return self.__title
    @property
    def internal_surface(self) -> pygame.Surface: return self.__internal_surface
    @property
    def screen(self) -> pygame.Surface: return self.__screen

    @font.setter
    def font(self, font: pygame.font.Font) -> None: self.__font = font
    @font.setter
    def title(self, title: str) -> None:
        self.__title = title
        pygame.display.set_caption(title)