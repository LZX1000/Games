# menu.py

from typing import Any

from settings import Settings

from button import *


class Scene():
    __slots__ = (
        '__settings',
        '__objects',
        '__colors'
    )

    def __init__(
        self,
        settings: Settings,
        display: Display
    ) -> None:
        super().__init__()

        self.__colors: dict[str, tuple[int, int, int]] = {
            'BACKGROUND_COLOR': (180, 180, 180)
        }

        self.__settings = settings

        # Create buttons
        self.__objects: list[Any] = []
        self.__objects.append(Button(
            surface=(button_surface := display.font.render(" > ", False, (0, 0, 0), (200, 200, 200))),
            topleft=(
                display.internal_surface.get_width() - button_surface.get_width() * self.__settings.button_edge_spacing - button_surface.get_width(),
                display.internal_surface.get_height() - button_surface.get_height() * self.__settings.button_edge_spacing - button_surface.get_height()
                ),
            effect=lambda: setattr(self.__settings, 'gamestate', 'game'),
        ))
        self.__objects.append(Button(
            surface=(button_surface := display.font.render("Exit Game", False, (0, 0, 0), (200, 200, 200))),
            topleft=(
                display.internal_surface.get_width() // 2 - button_surface.get_width() // 2,
                display.internal_surface.get_height() // 2 - button_surface.get_height() // 2
                ),
            effect=lambda: setattr(self.__settings, 'gamestate', 'quit'),
            debug_color=(0, 255, 0)
        ))

    '''GETTERS'''
    
    @property
    def objects(self) -> list[Any]: return self.__objects
    @property
    def colors(self) -> dict[str, tuple[int, int, int]]: return self.__colors
    @property
    def name(self) -> str: return f"{self.__class__.__module__}"

    def __str__(self) -> str:
        return self.name