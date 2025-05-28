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

class Controllable:
    """Subclass for controllable objects."""
    pass

class Clickable:
    """Subclass for clickable objects."""
    pass

class Renderable(ABC):
    @abstractmethod
    def render(self, display: 'Display', pos: tuple[int, int] | None = None) -> None:
        """Render the object on the display."""
        pass

class Movable(ABC):
    @abstractmethod
    def update(self) -> None:
        """Update the object based on the delta time."""
        pass

class Scene():
    """Subclass for all scenes."""
    pass