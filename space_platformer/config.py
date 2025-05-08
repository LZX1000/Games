# config.py

from typing import TYPE_CHECKING
from abc import ABC, abstractmethod

if TYPE_CHECKING:
    from display import Display


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


CURRENT_GAMESTATE = "menu"
BUTTON_EDGE_SPACING = 1/3

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