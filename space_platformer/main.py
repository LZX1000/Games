# main.py

# Python
import pygame
from typing import Any

# Gamestates
import config
import game
import menu

# Game Functions
from functional import *
from map import Map
from display import Display


GAMESTATES = {
    "game" : game,
    "menu" : menu
}

CURRENT_GAMESTATE = "menu"  # Starting gamestate


def main() -> None:
    # Initialize display
    display = Display(title="Space Platformer")

    # Default values
    tracked_values: dict[str, Any] = {'debug_mode': False}
    # gamestate = "game"

    gamestate: config.Gamestate = GAMESTATES[config.CURRENT_GAMESTATE].Scene(display)  # Start with the menu gamestate
    tracked_values['has_map'] = False

    # Main loop
    while True:
        if config.CURRENT_GAMESTATE != gamestate.get_name():
            if config.CURRENT_GAMESTATE == "quit":
                quit()
            gamestate = GAMESTATES[config.CURRENT_GAMESTATE].Scene(display)
            for object_ in gamestate.get_objects():
                if isinstance(object_, Map):
                    tracked_values['has_map'] = True
                    tracked_values['map'] = object_
                    break
            else:
                tracked_values['has_map'] = False

        # Get held keys
        keys = pygame.key.get_pressed()

        # Get accurate mouse position
        scaled_mouse_pos = pygame.mouse.get_pos()
        mouse_pos = ([x * y / z for x, y, z in zip(scaled_mouse_pos, display.get_internal_surface().get_size(), display.get_screen().get_size())])

        current_objects = gamestate.get_objects()
        changed_values: dict[str, Any] = event_handling(keys, mouse_pos, [object_ for object_ in current_objects if isinstance(object_, config.Clickable)])

        tracked_values['mouse_pos'] = mouse_pos # Logic for converting from changed_values format to actual data
        tracked_values['debug_mode'] = not tracked_values['debug_mode'] if 'debug_mode' in changed_values else tracked_values['debug_mode']

        # Interal rendering
        display.fill(gamestate.get_colors().get('BACKGROUND_COLOR', (0, 0, 0)))  # Sub-background

        for object_ in current_objects:
            if isinstance(object_, config.Renderable):
                object_.render(display)
        if tracked_values['debug_mode']:
            for object_ in current_objects:
                if hasattr(object_, 'debug'):
                    object_.debug(display)

        # Mouse display
        tracked_values["mouse_pos"] = mouse_pos

        # Button hover
        object_hovered = False
        for object_ in (obj for obj in current_objects if isinstance(obj, config.Clickable)):
            if object_.get_rect().collidepoint(mouse_pos):
                tracked_values["object_hover"] = object_
                object_hovered = True
                break
        
        # if tracked_values.get("has_map", False):
        #     check_player_collision(tracked_values["map"])

        if not object_hovered:
            tracked_values.pop("object_hover", None)

        # Update display
        display.update(tracked_values)

if __name__ == "__main__":
    main()