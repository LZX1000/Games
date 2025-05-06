# menu.py

from typing import Any

import config

from button import *


class Scene():
    __slots__ = (
        '__objects',
        '__colors'
    )

    def __init__(self, display) -> None:
        super().__init__()

        self.__colors: dict[str, tuple[int, int, int]] = {
            'BACKGROUND_COLOR': (180, 180, 180)
        }

        # Create buttons
        self.__objects: list[Any] = []
        self.__objects.append(Button(
            surface=(button_surface := display.get_font().render("Go To Game", False, (0, 0, 0), (200, 200, 200))),
            topleft=(
                display.get_internal_surface().get_width() // 2 - button_surface.get_width() // 2,
                display.get_internal_surface().get_height() // 2 - button_surface.get_height() // 2 + 50
                ),
            effect=lambda: setattr(config, 'CURRENT_GAMESTATE', 'game'),
        ))
        self.__objects.append(Button(
            surface=(button_surface := display.get_font().render("Exit Game", False, (0, 0, 0), (200, 200, 200))),
            topleft=(
                display.get_internal_surface().get_width() // 2 - button_surface.get_width() // 2,
                display.get_internal_surface().get_height() // 2 - button_surface.get_height() // 2
                ),
            effect=lambda: setattr(config, 'CURRENT_GAMESTATE', 'quit'),
            debug_color=(0, 255, 0)
        ))

    '''GETTERS'''

    def get_objects(self) -> list[Any]:
        return self.__objects
    
    def get_colors(self) -> dict[str, tuple[int, int, int]]:
        return self.__colors
    
    def get_name(self) -> str:
        return f"{self.__class__.__module__}"