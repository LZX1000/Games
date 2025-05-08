# player.py

import pygame

import random

import config
from display import Display

class Player(pygame.sprite.Sprite, config.Renderable, config.Collidable):
    """Creates a player object, contains a rect object."""
    __slots__ = (
        '__debug_color',
        '__surface',
        '__rect',
        '__velocity'
    )

    __EFFECTS = {
        "WALL" : lambda self: setattr(self, '__velocity', None),
        # Alternative wall collision effect for debugging
        # "WALL" : lambda self: self.__rect.update((random.randint(0, 300), random.randint(0, 300)), (self.__rect.width, self.__rect.height)),
        "GOAL" : lambda: setattr(config, 'CURRENT_GAMESTATE', "menu")
    }

    def __init__(
            self,
            topleft: tuple[int, int],
            size: tuple[int, int] = None,
            debug_color: tuple[int, int, int] | None = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        ) -> None:
        super().__init__()

        try:
            self.__surface = pygame.image.load(config.MAP_ASSET_KEYS["PLAYER"]).convert_alpha()
            if size is not None:
                self.__surface = pygame.transform.scale(self.__surface, size)
        except pygame.error as e:
            raise RuntimeError(f"Failed to load brick image: {e}") from e

        self.__debug_color = debug_color
        self.__rect = pygame.Rect(*topleft, *self.__surface.get_size())

    '''FUNCTIONS'''

    def collide(self, other: config.Collidable) -> None:
        """Called when the player collides with another object."""
        self.__EFFECTS.get(other.type, lambda self: None)(self)

    def render(
            self,
            display: Display,
            pos: tuple[int, int] | None = None
        ) -> None:
        """Renders the given surface by blitting text surfaces at the specified position."""
        if pos is None:
            pos = self.__rect.topleft
        else:
            self.__rect.topleft = pos

        display.blit(self.__surface, self.__rect.topleft)

    def debug(self, display: Display) -> None:
        """Render the debug color of the brick."""
        if self.__debug_color is not None:
            pygame.draw.rect(display.internal_surface, self.__debug_color, self.__rect, 1)

            # Debug information
            font = display.font
            text_surface = font.render(self.__class__.__name__, False, (0, 0, 0))
            text_width, text_height = text_surface.get_size()               # Centered text
            text_offset_x, text_offset_y = (self.__rect.width - text_width) / 2, (self.__rect.height - text_height) / 2
            display.blit(text_surface, (self.__rect.x + text_offset_x, self.__rect.y + text_offset_y))

    @property
    def rect(self) -> pygame.Rect: return self.__rect
    @property
    def position(self) -> tuple[int, int]: return self.__rect.topleft
    @property
    def pos(self) -> tuple[int, int]: return self.__rect.topleft

    @rect.setter
    def pos(self, pos: tuple[int, int]) -> None: self.__rect.topleft = pos