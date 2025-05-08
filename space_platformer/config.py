# config.py

from typing import TYPE_CHECKING
from abc import ABC, abstractmethod

if TYPE_CHECKING:
    from display import Display


type color = tuple[int, int, int]
type coords = tuple[int, int]


class Collidable:
    """Subclass for collidable objects."""
    pass

class Clickable:
    """Subclass for clickable objects."""
    pass

class Renderable(ABC):
    @abstractmethod
    def render(self, display: 'Display', pos: tuple[int, int] | None = None) -> None:
        """Render the object on the display."""
        pass

class Gamestate():
    """Subclass for all gamestates."""
    pass


DEFAULT_INTERNAL_RESOLUTION = (1280, 780)
DEFAULT_EXTERNAL_RESOLUTION = (1920, 1080)
# DEFAULT_INTERNAL_RESOLUTION = (2293, 960)
# DEFAULT_EXTERNAL_RESOLUTION = (3440, 1440)
FONT_SCALE_FACTOR = 36

CURRENT_GAMESTATE = "menu"
BUTTON_EDGE_SPACING = 1/3
JUMPABLE_DISTANCE_THRESHOLD = 2

# Define colors (R, G, B, A) with RGBA
MAP_COLOR_KEYS = {
    (0, 0, 0, 1) : "WALL",        # Black
    (0, 1, 0, 1) : "GOAL",      # Green
    (1, 1, 0, 1) : "PLAYER"   # Yellow
}

MAP_ASSET_KEYS = {
    "WALL": "space_platformer/assets/wall.png",
    "GOAL": "space_platformer/assets/goal.png",
    "PLAYER": "space_platformer/assets/player.png",
}