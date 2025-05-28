# settings.py
import pygame

from typing import Any
from os import PathLike

from config import Clickable, Renderable, Scene, Collidable, Movable


class Settings():
    """Configuration class for the game."""

    __slots__ = (
        '__delta_time',
        '__gamestate',
        '__gamestates',
        '__display',
        '__tracked_values',
        '__command_category_enabled',
    )


    __DEFAULT_INTERNAL_RESOLUTION: tuple[int, int] = (1280, 780)
    __DEFAULT_EXTERNAL_RESOLUTION: tuple[int, int] = (1920, 1080)
    # __DEFAULT_INTERNAL_RESOLUTION = (2293, 960)
    # __DEFAULT_EXTERNAL_RESOLUTION = (3440, 1440)

    __FONT_SCALE_FACTOR: int = 36

    __FRAME_RATE: int = 60

    __BUTTON_EDGE_SPACING: float = 1/3
    __JUMPABLE_DISTANCE_THRESHOLD: float = 0.05
    __JUMP_SPEED: float = 0.5

    __MAPS: dict[str, PathLike] = {
        "Test_Map_1": "space_platformer/assets/Test_Map_1.png",
        "Test_Map_2": "space_platformer/assets/Test_Map_2.png",
    }

    # Define colors (R, G, B, A) with RGBA
    __MAP_COLOR_KEYS = {
        (0, 0, 0, 1) : "WALL",        # Black
        (0, 1, 0, 1) : "GOAL",      # Green
        (1, 1, 0, 1) : "PLAYER"   # Yellow
    }

    __MAP_ASSET_KEYS = {
        "WALL": "space_platformer/assets/wall.png",
        "GOAL": "space_platformer/assets/goal.png",
        "PLAYER": "space_platformer/assets/player.png",
    }

    __SPECIAL_COMMANDS = {
        'system' : {
        # 'system' : (("new_values"), {
            'debug_toggle' : (
                lambda held, pressed: held[pygame.K_LCTRL] and pygame.K_SPACE in pressed,
                lambda self, new_values: new_values.update({
                    'debug_mode': not self.tracked_values.get('debug_mode', False)
                })
            ),
            'quit' : (
                lambda held, pressed: held[pygame.K_ESCAPE] or pygame.K_ESCAPE in pressed,
                lambda self, _: self.__quit()
            )
        },
        # }),
        'player_controls' : {
            'jump' : (
                lambda held, pressed: held[pygame.K_SPACE] or pygame.K_SPACE in pressed,
                lambda self, _: self.tracked_values['map'].player.jump(self.tracked_values['mouse_pos'])
            ),
        }
    }


    def __init__(self) -> None:
        from map import Map
        from display import Display

        import scene_1
        import scene_2
        import menu

        self.__gamestate = "menu"

        self.__gamestates = {
            "scene_1": scene_1,
            "scene_2": scene_2,
            "menu": menu
        }

        self.__command_category_enabled = {
            'debug': False,
            'player_controls': False,
            'system': True,
        }

        # Initialize display
        self.__display = Display(
            self,
            internal_resolution=self.internal_resolution,
            external_resolution=self.external_resolution,
            title="Space Platformer"
        )

        # Default values
        self.__tracked_values: dict[str, Any] = {}

        clock = pygame.time.Clock()

        scene: Scene = self.gamestates[self.gamestate].Scene(self, self.display)
        self.__tracked_values['has_map'] = False

        while True:
            if self.gamestate != str(scene):
                if self.gamestate == "quit":
                    quit()
                scene: Scene = self.gamestates[self.gamestate].Scene(self, self.display)
                for object_ in scene.objects:
                    if object_ in self.maps.values():
                        self.__tracked_values['has_map'] = True
                        self.__command_category_enabled['player_controls'] = True
                        self.__tracked_values['map'] = Map(self, filepath=object_, display=self.display)
                        scene.objects = [object_ for object_ in scene.objects if object_ not in self.maps.values()] + [self.__tracked_values['map']]
                        # # Debugging to check that collision works
                        # object_.player.pos = (object_.player.pos[0] - 5, object_.player.pos[1] - 5)
                        break
                else:
                    self.__tracked_values['has_map'] = False
                    self.__command_category_enabled['player_controls'] = False

            changed_values: dict[str, Any] = self.__event_handling(scene)
            self.__tracked_values.update(changed_values)

            self.__delta_time = clock.tick(self.__FRAME_RATE) / 1000

            self.__update(scene)

            if self.tracked_values.get("has_map", False):
                self.__check_player_collision(self.tracked_values["map"])

            self.__render(scene)

            # Update display
            self.__display.update(self.tracked_values)


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

        for category, commands in self.__SPECIAL_COMMANDS.items():
            if not self.command_category_enabled.get(category, False):
                continue

            for _, (condition, reaction) in commands.items():
                if condition(held, pressed_keys):
                    reaction(self, new_values)

        return new_values


    def __check_player_collision(self, map_: pygame.sprite.Sprite) -> None:
        from player import Player

        wall_collided: Collidable = pygame.sprite.spritecollideany(
            (player := map_.player), [brick for brick in map_.collidable_objects if brick.type == "WALL"],
            # collided=__check_player_grounded
            collided=lambda s1, s2: s1.rect.colliderect(s2.grounded_rect) if isinstance(s2, Player) else s1.grounded_rect.colliderect(s2.rect)
        )
        if wall_collided and not player.grounded:
            player.grounded = bool(wall_collided)

        collided_objects: list[Collidable] = pygame.sprite.spritecollide(
            player, map_.collidable_objects,
            dokill=False
        )
        did_wall: bool = False
        for collided in collided_objects:
            if collided.type == "WALL":
                if did_wall:
                    continue
                else:
                    did_wall = True
            player.collide(collided)
            

    def __render(self, scene) -> None:
        """Renders the given objects."""
        self.__display.fill(scene.colors.get('BACKGROUND_COLOR', (0, 0, 0)))

        for object in [obj for obj in scene.objects if isinstance(obj, Renderable)]:
            object.render(self.display)

        if self.tracked_values.get('debug_mode', False):
            for object in [obj for obj in scene.objects if hasattr(obj, 'debug')]:
                object.debug(self.display)


    def __update(self, scene) -> None:
        """Updates the given objects."""
        for object in [obj for obj in scene.objects if isinstance(obj, Movable)]:
            object.update()


    def __quit() -> None:
        """Quits the Pygame instance."""
        pygame.quit()
        exit()

    
    @property
    def command_category_enabled(self) -> dict[str, bool]: return self.__command_category_enabled
    @property
    def delta_time(self) -> float: return self.__delta_time
    @property
    def internal_resolution(self) -> tuple[int, int]: return self.__DEFAULT_INTERNAL_RESOLUTION
    @property
    def external_resolution(self) -> tuple[int, int]: return self.__DEFAULT_EXTERNAL_RESOLUTION
    @property
    def font_scale_factor(self) -> int: return self.__FONT_SCALE_FACTOR
    @property
    def button_edge_spacing(self) -> float: return self.__BUTTON_EDGE_SPACING
    @property
    def jumpable_distance_threshold(self) -> int: return self.__JUMPABLE_DISTANCE_THRESHOLD
    @property
    def gamestate(self) -> str: return self.__gamestate
    @property
    def gamestates(self) -> dict[str, Any]: return self.__gamestates
    @property
    def map_color_keys(self) -> dict[tuple[int, int, int], str]: return self.__MAP_COLOR_KEYS
    @property
    def map_asset_keys(self) -> dict[str, str]: return self.__MAP_ASSET_KEYS
    @property
    def display(self) -> Any: return self.__display
    @property
    def tracked_values(self) -> dict[str, Any]: return self.__tracked_values
    @property
    def maps(self) -> dict[str, PathLike]: return self.__MAPS
    
    @gamestate.setter
    def gamestate(self, value: str) -> None:
        self.__gamestate = value
        # self.__GAMESTATES[value].Scene(self).run()