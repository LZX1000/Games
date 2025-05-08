# menu.py
from typing import Any

import config

from button import *
from map import *


class Scene():
    __slots__ = (
        '__objects',
        '__colors'
    )

    def __init__(self, display) -> None:
        super().__init__()

        self.__colors: dict[str, tuple[int, int, int]] = {
            'BACKGROUND_COLOR': (180, 200, 180)
        }

        # Create buttons
        self.__objects: list[Any] = []
        self.__objects.append(Button(
            surface=(button_surface := display.font.render(" < ", False, (0, 0, 0), (200, 200, 200))),
            topleft=(
                button_surface.get_width() * config.BUTTON_EDGE_SPACING,
                display.internal_surface.get_height() - button_surface.get_height() * config.BUTTON_EDGE_SPACING - button_surface.get_height()
                ),
            effect=lambda: setattr(config, 'CURRENT_GAMESTATE', 'menu'),
        ))

        # Create map
        self.__objects.append(Map(
            filepath="space_platformer/assets/Test_Map_1.png",
            display=display
        ))

    '''GETTERS'''

    @property
    def objects(self) -> list[Any]: return self.__objects
    @ property
    def colors(self) -> dict[str, tuple[int, int, int]]: return self.__colors
    @property
    def name(self) -> str: return f"{self.__class__.__module__}"