# player.py

import pygame

import random

from settings import Settings
from config import Renderable, Collidable
from display import Display

class Player(pygame.sprite.Sprite, Renderable, Collidable):
    """Creates a player object, contains a rect object."""
    __slots__ = (
        '__settings',
        '__debug_color',
        '__surface',
        '__main_rect',
        '__grounded_rect',
        '__grounded',
        '__velocity'
    )

    __EFFECTS = {
        "WALL" : lambda self: setattr(self, '__velocity', None),
        # Alternative wall collision effect for debugging
        # "WALL" : lambda self: self.__main_rect.update((random.randint(0, 300), random.randint(0, 300)), (self.__main_rect.width, self.__main_rect.height)),
        "GOAL" : lambda self: setattr(self.__settings, 'gamestate', "menu")
    }

    def __init__(
            self,
            settings: Settings,
            topleft: tuple[int, int],
            size: tuple[int, int] = None,
            debug_color: tuple[int, int, int] | None = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        ) -> None:
        super().__init__()

        self.__settings: Settings = settings

        try:
            self.__surface = pygame.image.load(self.__settings.map_asset_keys["PLAYER"]).convert_alpha()
            if size is not None:
                self.__surface = pygame.transform.scale(self.__surface, size)
        except pygame.error as e:
            raise RuntimeError(f"Failed to load brick image: {e}") from e

        self.__grounded = False
        self.__debug_color = debug_color
        self.__main_rect = pygame.Rect(*topleft, *self.__surface.get_size())
        # self.__grounded_rect = pygame.Rect(
        #     *(x - self.__settings.jumpable_distance_threshold for x in topleft),
        #     *(x + 2 * self.__settings.jumpable_distance_threshold for x in (self.__surface.get_size()))
        # )
        player_width, player_height = self.__surface.get_size()
        self.__grounded_rect = pygame.Rect(
            topleft[0] - self.__settings.jumpable_distance_threshold * player_width,
            topleft[1] - self.__settings.jumpable_distance_threshold * player_height,
            player_width + 2 * self.__settings.jumpable_distance_threshold * player_width,
            player_height + 2 * self.__settings.jumpable_distance_threshold * player_height
        )

    '''FUNCTIONS'''

    def collide(self, other: Collidable) -> None:
        """Called when the player collides with another object."""
        self.__EFFECTS.get(other.type, lambda self: None)(self)

    def render(
            self,
            display: Display,
            pos: tuple[int, int] | None = None
        ) -> None:
        """Renders the given surface by blitting text surfaces at the specified position."""
        if pos is None:
            pos = self.__main_rect.topleft
        else:
            self.__main_rect.topleft = pos

        display.blit(self.__surface, self.__main_rect.topleft)

    def debug(self, display: Display) -> None:
        """Render the debug color of the brick."""
        if self.__debug_color is not None:
            pygame.draw.rect(display.internal_surface, self.__debug_color, self.__main_rect, 1)
            pygame.draw.rect(display.internal_surface, self.__debug_color, self.__grounded_rect, 1)

            # Debug information
            font = display.debug_font
            texts: list[pygame.Surface] = [
                font.render(self.__class__.__name__, False, (0, 0, 0)),
                font.render(str(self.__grounded), False, (0, 0, 0))
            ]
            for i, text in enumerate(texts):
                width, height = text.get_size()
                text_offset_x, text_offset_y = (self.__main_rect.width - width) / 2, height * i
                display.blit(text, (self.__main_rect.x + text_offset_x, self.__main_rect.y + text_offset_y))

    @property
    def rect(self) -> pygame.Rect: return self.__main_rect
    @property
    def grounded_rect(self) -> pygame.Rect: return self.__grounded_rect
    @property
    def grounded(self) -> bool: return self.__grounded
    @property
    def position(self) -> tuple[int, int]: return self.__main_rect.topleft
    @property
    def pos(self) -> tuple[int, int]: return self.__main_rect.topleft

    @rect.setter
    def pos(self, pos: tuple[int, int]) -> None:
        self.__main_rect.topleft = pos
        self.__grounded_rect.topleft = tuple(x * self.__settings.jumpable_distance_threshold for x in pos)
    @grounded.setter
    def grounded(self, grounded: bool) -> None:
        self.__grounded = grounded
        if grounded:
            self.__velocity = (0, 0)