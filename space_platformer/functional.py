# functional.py

import pygame

from typing import Any

import config
from player import Player
from map_objects import Brick


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
                    if button.rect.collidepoint(mouse_pos):
                        button.clicked()

    return changed_values


def check_player_collision(map_: pygame.sprite.Sprite) -> None:
    wall_collided: config.Collidable = pygame.sprite.spritecollideany(
        (player := map_.player), [brick for brick in map_.collidable_objects if brick.type == "WALL"],
        # collided=__check_player_grounded
        collided=lambda s1, s2: s1.rect.colliderect(s2.grounded_rect) if isinstance(s2, Player) else s1.grounded_rect.colliderect(s2.rect)
    )
    if wall_collided and not player.grounded:
        player.grounded = True

    collided_objects: list[config.Collidable] = pygame.sprite.spritecollide(
        player, map_.collidable_objects,
        dokill=False
    )
    did_wall: bool = False
    for collided in collided_objects:
        if collided.type == "WALL" and not did_wall:
            did_wall = True
        player.collide(collided)


def quit() -> None:
    """Quits the Pygame instance."""
    pygame.quit()
    exit()