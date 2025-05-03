import pygame

import random

from typing import Any

import game
from button import Button
from display import Display


def main() -> None:
    # Initialize display
    display = Display(title="template")

    # Default values
    tracked_values: dict[str, Any] = {'debug_mode': False}
    gamestate = "game"

    # Create buttons
    buttons: list[Button] = []
    buttons.append(Button(
        surface=(button_surface := display.get_font().render("Change Background Color", False, (0, 0, 0), (200, 200, 200))),
        topleft=(display.get_internal_surface().get_width() // 2 - button_surface.get_width() // 2, display.get_internal_surface().get_height() // 2 - button_surface.get_height() // 2),
        effect=lambda: setattr(game, 'BACKGROUND_COLOR', random.choice([(0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255), (255, 128, 0)])),
        debug_color=(0, 255, 0)
    ))

    # Main loop
    while True:
        # Get held keys
        keys = pygame.key.get_pressed()

        # Get accurate mouse position
        scaled_mouse_pos = pygame.mouse.get_pos()
        mouse_pos = ([x * y / z for x, y, z in zip(scaled_mouse_pos, display.get_internal_surface().get_size(), display.get_screen().get_size())])

        changed_values: dict[str, Any] = game.event_handling(keys, mouse_pos, buttons)

        tracked_values['mouse_pos'] = mouse_pos # Logic for converting from changed_values format to actual data
        tracked_values['debug_mode'] = not tracked_values['debug_mode'] if 'debug_mode' in changed_values else tracked_values['debug_mode']

        # Render in 640x360
        if gamestate == "game":
            # Interal rendering
            display.fill(game.BACKGROUND_COLOR) # Sub-background

            for button in buttons:
                button.update(display)
                if tracked_values['debug_mode']:
                    button.debug(display)

        # Global debugs
        if tracked_values['debug_mode']:
            # Mouse display
            tracked_values["mouse_pos"] = mouse_pos

            # Button hover
            for button in buttons:
                if button.get_rect().collidepoint(mouse_pos):
                    tracked_values["button_hover"] = button

        # Update display
        display.update(tracked_values)

if __name__ == "__main__":
    main()