# main.py

# Pygame
import pygame

# Python Others
from typing import Any

# Gamestates
import game
import menu

# Game Functions
from functional import *
from button import Clickable
from display import Display, Renderable


GAMESTATES = {
    "game" : game,
    "menu" : menu
}


class Gamestate():
    """Subclass for all gamestates."""
    pass


def main() -> None:
    # Initialize display
    display = Display(title="template")

    # Default values
    tracked_values: dict[str, Any] = {'debug_mode': False}
    # gamestate = "game"

    gamestate: Gamestate = GAMESTATES["menu"].scene(display)  # Start with the menu gamestate

    # Main loop
    while True:
        # Get held keys
        keys = pygame.key.get_pressed()

        # Get accurate mouse position
        scaled_mouse_pos = pygame.mouse.get_pos()
        mouse_pos = ([x * y / z for x, y, z in zip(scaled_mouse_pos, display.get_internal_surface().get_size(), display.get_screen().get_size())])

        current_objects = gamestate.get_objects()
        changed_values: dict[str, Any] = event_handling(keys, mouse_pos, [object_ for object_ in current_objects if isinstance(object_, Clickable)])

        tracked_values['mouse_pos'] = mouse_pos # Logic for converting from changed_values format to actual data
        tracked_values['debug_mode'] = not tracked_values['debug_mode'] if 'debug_mode' in changed_values else tracked_values['debug_mode']

        # Interal rendering
        display.fill(gamestate.get_colors().get('BACKGROUND_COLOR', (0, 0, 0)))  # Sub-background

        for object_ in current_objects:
            if isinstance(object_, Renderable):
                object_.render(display)
        if tracked_values['debug_mode']:
            for object_ in current_objects:
                if hasattr(object_, 'debug'):
                    object_.debug(display)

        # Mouse display
        tracked_values["mouse_pos"] = mouse_pos

        # Button hover
        object_hovered = False
        for object_ in (obj for obj in current_objects if isinstance(obj, Clickable)):
            if object_.get_rect().collidepoint(mouse_pos):
                tracked_values["object_hover"] = object_
                object_hovered = True
                break
        if not object_hovered:
            tracked_values.pop("object_hover", None)

        # Update display
        display.update(tracked_values)

if __name__ == "__main__":
    main()