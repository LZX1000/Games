import pygame

from typing import Any


type color = tuple[int, int, int]

BACKGROUND_COLOR: color = (180, 180, 180)

def event_handling(
    keys: dict[int, bool],
    mouse_pos: tuple[int, int],
    buttons: list[pygame.sprite.Sprite] = []
) -> dict[str, Any]:
    """Handles events such as mouse clicks and keyboard inputs."""
    changed_values: dict[str, Any] = {}

    for event in pygame.event.get():
        if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
            quit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and keys[pygame.K_LCTRL]:
                changed_values['debug_mode'] = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for button in buttons:
                    if button.get_rect().collidepoint(mouse_pos):
                        button.clicked()

    return changed_values

def quit() -> None:
    """Quits the Pygame instance."""
    pygame.quit()
    exit()