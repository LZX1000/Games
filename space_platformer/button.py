# button.py

import pygame

import inspect
import random
from typing import Callable

from display import Display, Renderable


class Clickable:
    """Subclass for clickable objects."""
    pass


class Button(pygame.sprite.Sprite, Renderable, Clickable):
    """Creates a button object, contains a text surface and a rect object."""
    __slots__ = (
        '__debug_color',
        '__surface',
        '__effect',
        '__rect'
    )

    def __init__(
        self,
        surface: pygame.Surface,
        topleft: tuple[int, int] = (0, 0),
        effect: Callable | None = None,
        debug_color: tuple[int, int, int] | None = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    ) -> None:
        super().__init__()

        self.__debug_color = debug_color
        self.__surface = surface
        self.__effect = effect

        self.__rect = pygame.Rect(*topleft, *surface.get_size())

    '''FUNCTIONS'''

    def clicked(self) -> None:
        """Called when the button is clicked."""
        if self.__effect is not None:
            self.__effect()

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
        """Draws a debug rectangle on the given surface."""
        pygame.draw.rect(display.get_internal_surface(), self.__debug_color, self.__rect, 1)

    '''GETTERS'''

    def get_rect(self) -> pygame.Rect:
        return self.__rect

    '''DUNDERS'''

    def __repr__(self) -> str:
        return f"Button\n  rect={str(self.__rect.topleft)}, ({str(self.__rect.left)}, {str(self.__rect.height)}),\n  effect={inspect.getsource(self.__effect)[15:]}"