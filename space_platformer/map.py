# map.py

import pygame

from os import PathLike

from settings import Settings
from config import Renderable
from display import Display
import map_objects
from player import Player


class Map(Renderable):
    __slots__ = (
        '__settings',
        "__simple_game_map",
        "__map_objects",
        "__collidable_objects",
        "__player_spawn_pos",
        "__player",
        "__display"
    )

    def __init__(
        self,
        settings: Settings,
        filepath: PathLike,
        display: Display
    ) -> None:
        self.__settings: Settings = settings

        self.__load(filepath)

        self.__display: Display = display
        self.__map_objects: list[map_objects.Brick] = []
        self.__build_map()

    def __load(self, filepath: PathLike) -> None:
        """Load the map from the file."""
        try:
            image: pygame.Surface = pygame.image.load(filepath).convert_alpha()
        except pygame.error as e:
            raise RuntimeError(f"Failed to load map image: {e}") from e
        
        width, height = image.get_size()
        
        self.__simple_game_map: list[list[str | None]] = []
        self.__player_pos: tuple[int, int] | None = None

        # Create a simple game map based on the image colors
        for y in range(height):
            row: list[str] = []
            for x in range(width):
                color = tuple(round(x) for x in image.get_at((x, y)).normalize())
                if (type_ := self.__settings.map_color_keys.get(color, None)) != "PLAYER":
                    row.append(type_)
                else:
                    row.append(None)
                    self.__player_spawn_pos = (x, y)

            self.__simple_game_map.append(row)

        # Place the player in the first empty space if not already placed
        if self.__player_pos is None:
            for y in range(height):
                for x in range(width):
                    if self.__simple_game_map[y][x] is None:
                        self.__player_pos = (x, y)
                        break

                if self.__player_pos is not None:
                    break

    def __build_map(self) -> None:
        """Build the map from the simple game map."""
        surface_width, surface_height = self.__display.internal_surface.get_size()

        # Calculate square tile size that fits in screen
        tile_size = min(
            surface_width / (map_columns := len(self.__simple_game_map[0])),
            surface_height / (map_rows := len(self.__simple_game_map))
        )

        # Calculate offsets to center the map
        offset_x = (surface_width - tile_size * map_columns) / 2
        offset_y = (surface_height - tile_size * map_rows) / 2

        for y, row in enumerate(self.__simple_game_map):
            for x, cell in enumerate(row):
                if cell is not None:
                    self.__map_objects.append(map_objects.Brick(
                        settings=self.__settings,
                        type_=cell,
                        topleft=(offset_x + x * tile_size, offset_y + y * tile_size),
                        size=(round(tile_size), round(tile_size))
                    ))

        self.__collidable_objects = pygame.sprite.Group(self.__map_objects)
        self.__player = Player(
            settings=self.__settings,
            topleft=(offset_x + self.__player_spawn_pos[0] * tile_size, offset_y + self.__player_spawn_pos[1] * tile_size),
            size=(round(tile_size), round(tile_size))
        )

    '''FUNCTIONS'''

    def render(self, display: Display) -> None:
        """Render the map."""
        for brick in self.__map_objects:
            brick.render(display)
        self.__player.render(display)

    def debug(self, display: Display) -> None:
        """Render the debug information of the map."""
        for brick in self.__map_objects:
            brick.debug(display)
        self.__player.debug(display)

    '''GETTERS'''
    @property
    def player_spawn_location(self) -> tuple[int, int] | None: return self.__player_spawn_pos
    @property
    def player(self) -> Player: return self.__player
    @property
    def map_objects(self) -> list[map_objects.Brick]: return self.__map_objects
    @property
    def collidable_objects(self) -> pygame.sprite.Group: return self.__collidable_objects