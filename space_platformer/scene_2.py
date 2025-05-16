# menu.py
from typing import Any

from settings import Settings

from button import *
from map import *


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
            'BACKGROUND_COLOR': (180, 200, 180)
        }

        self.__settings = settings

        # Create buttons
        self.__objects: list[Any] = []
        self.__objects.append(Button(
            surface=(button_surface := display.font.render(" < ", False, (0, 0, 0), (200, 200, 200))),
            topleft=(
                button_surface.get_width() * self.__settings.button_edge_spacing,
                display.internal_surface.get_height() - button_surface.get_height() * self.__settings.button_edge_spacing - button_surface.get_height()
                ),
            effect=lambda: setattr(self.__settings, 'gamestate', 'scene_1'),
        ))

        # Create map
        self.__objects.append(settings.maps.get("Test_Map_2", None))

    @property
    def objects(self) -> list[Any]: return self.__objects
    @property
    def colors(self) -> dict[str, tuple[int, int, int]]: return self.__colors
    @property
    def name(self) -> str: return f"{self.__class__.__module__}"

    @objects.setter
    def objects(self, value: list[Any]) -> None:
        if isinstance(value, list):
            self.__objects = value
        else:
            raise TypeError("Expected a list")
    @colors.setter
    def colors(self, key_value: tuple[str, tuple[int, int, int]]) -> None:
        key, value = key_value
        self.__colors[key] = value

    def __str__(self) -> str:
        return self.name