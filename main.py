import pygame

import random

from typing import Any

import game
from button import Button
from display import Display

type color = tuple[int, int, int]

BACKGROUND_COLOR: color = (180, 180, 180)
RUNNING: bool = True


def main() -> None:
    display = Display(title="template")

    running = True
    debug_mode = False
    gamestate = "game"
    max_fps = 60

    buttons: list[Button] = []

    new_button = Button(
        surface=(button_surface := display.get_font().render("Change Background Color", False, (0, 0, 0), (200, 200, 200))),
        topleft=(display.get_internal_surface().get_width() // 2 - button_surface.get_width() // 2, display.get_internal_surface().get_height() // 2 - button_surface.get_height() // 2),
        effect=lambda: globals().__setitem__('BACKGROUND_COLOR', random.choice([(0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255), (255, 128, 0)])),
        debug_color=(0, 255, 0)
    )
    buttons.append(new_button)

    while running:
        keys = pygame.key.get_pressed()

        # Get accurate mouse position
        scaled_mouse_pos = pygame.mouse.get_pos()
        mouse_pos = ([x * y / z for x, y, z in zip(scaled_mouse_pos, display.get_internal_surface().get_size(), display.get_screen().get_size())])

        changed_values: dict[str, Any] = game.event_handling(keys, mouse_pos, buttons)

        if 'debug_mode' in changed_values:
            debug_mode = not debug_mode

        if keys[pygame.K_ESCAPE]:
            game.quit()

        display_values: dict[str, Any] = {
            'mouse_pos': mouse_pos,
            'debug_mode': debug_mode
        }

        # Render in 640x360
        if gamestate == "game":
            # Interal rendering
            display.fill(BACKGROUND_COLOR) # Sub-background

            for button in buttons:
                button.update(display)
                if debug_mode:
                    button.debug(display)

        # Global debugs
        if debug_mode:
            # Mouse display
            display_values["mouse_pos"] = mouse_pos

            # Button hover
            for button in buttons:
                if button.get_rect().collidepoint(mouse_pos):
                    display_values["button_hover"] = button

        display.update(display_values)

if __name__ == "__main__":
    main()