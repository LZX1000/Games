import pygame
from typing import Any
from config import Scene, Renderable, Clickable
from display import Display

class Game():
    # . . .
    __SPECIAL_COMMANDS = {
        'debug_toggle' : (
            lambda held, pressed: pygame.K_LCTRL in held and pygame.K_SPACE in pressed,
            lambda self, new_values: new_values.update({
                'debug_mode': not self.tracked_values.get('debug_mode', False)
            })
        ),
        'quit' : (
            lambda held, pressed: pygame.K_ESCAPE in held or pygame.K_ESCAPE in pressed,
            lambda self: self.__quit()
        )
    }
    # . . .
    def __event_handling(self, scene: Scene) -> dict[str, Any]:
        """Handles events such as mouse clicks and keyboard inputs."""
        new_values: dict[str, Any] = {}
        objects: list[Renderable | Clickable] = scene.objects
        held: dict = pygame.key.get_pressed()

        new_values['mouse_pos'] = [
            x * y / z for x, y, z in zip(
                pygame.mouse.get_pos(),
                self.display.internal_surface.get_size(),
                self.display.screen.get_size()
            )
        ]
        new_values['unused_keys'] = []

        pressed_keys: set = set()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__quit()

            if event.type == pygame.KEYDOWN:
                pressed_keys.add(event.key)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for button in [obj for obj in objects if isinstance(obj, Clickable)]:
                        if button.rect.collidepoint(new_values['mouse_pos']):
                            button.clicked()

        # Special commands
        for _, (condition, reaction) in self.__SPECIAL_COMMANDS.items():
            if condition(held, pressed_keys):
                reaction(held, pressed_keys)

        # Game command keys
        for key in pressed_keys:
            if not any(condition(held, {key}) for condition, _ in self.__SPECIAL_COMMANDS.values()):
                new_values['unused_keys'].append(key)

        return new_values