# settings.py
import pygame

from typing import Any
from os import PathLike

from config import Clickable, Renderable, Scene, Collidable


class Settings():
    """Configuration class for the game."""

    __slots__ = (
        '__gamestate',
        '__gamestates',
        '__display',
        '__tracked_values'
    )


    __DEFAULT_INTERNAL_RESOLUTION = (1280, 780)
    __DEFAULT_EXTERNAL_RESOLUTION = (1920, 1080)
    # __DEFAULT_INTERNAL_RESOLUTION = (2293, 960)
    # __DEFAULT_EXTERNAL_RESOLUTION = (3440, 1440)

    __FONT_SCALE_FACTOR = 36

    __BUTTON_EDGE_SPACING = 1/3
    __JUMPABLE_DISTANCE_THRESHOLD = 2

    __MAPS: dict[str, PathLike] = {
        "Test_Map_1": "space_platformer/assets/Test_Map_1.png",
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

    def __init__(self) -> None:
        from map import Map
        from display import Display

        import game
        import menu

        self.__gamestate = "menu"

        self.__gamestates = {
            "game": game,
            "menu": menu
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
                        self.__tracked_values['map'] = Map(self, filepath=object_, display=self.display)
                        scene.objects = [object_ for object_ in scene.objects if object_ not in self.maps.values()] + [self.__tracked_values['map']]
                        # # Debugging to check that collision works
                        # object_.player.pos = (object_.player.pos[0] - 5, object_.player.pos[1] - 5)
                        break
                else:
                    self.__tracked_values['has_map'] = False

            changed_values: dict[str, Any] = self.__event_handling(scene)
            self.__tracked_values.update(changed_values)

            self.__render(scene)
            
            if self.tracked_values.get("has_map", False):
                self.__check_player_collision(self.tracked_values["map"])

            # Update display
            self.__display.update(self.tracked_values)


    def __event_handling(self, scene: Scene) -> dict[str, Any]:
        """Handles events such as mouse clicks and keyboard inputs."""
        new_values: dict[str, Any] = {}

        # Get held keys
        keys = pygame.key.get_pressed()
        # Get accurate mouse position
        new_values['mouse_pos'] = ([x * y / z for x, y, z in zip(pygame.mouse.get_pos(), self.display.internal_surface.get_size(), self.display.screen.get_size())])

        objects: list[Renderable | Clickable] = scene.objects

        for event in pygame.event.get():
            if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
                self.__quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and keys[pygame.K_LCTRL]:
                    new_values['debug_mode'] = not self.tracked_values['debug_mode'] if 'debug_mode' in self.tracked_values else True
                elif event.key == pygame.K_SPACE:
                    new_values['jumped'] = True
                    new_values['jumped_pos'] = new_values['mouse_pos']
                else:
                    new_values['jumped_pos'] = None
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for button in [obj for obj in objects if isinstance(obj, Clickable)]:
                        if button.rect.collidepoint(new_values['mouse_pos']):
                            button.clicked()

        return new_values


    def __check_player_collision(self, map_: pygame.sprite.Sprite) -> None:
        from player import Player

        wall_collided: Collidable = pygame.sprite.spritecollideany(
            (player := map_.player), [brick for brick in map_.collidable_objects if brick.type == "WALL"],
            # collided=__check_player_grounded
            collided=lambda s1, s2: s1.rect.colliderect(s2.grounded_rect) if isinstance(s2, Player) else s1.grounded_rect.colliderect(s2.rect)
        )
        if wall_collided and not player.grounded:
            player.grounded = True

        collided_objects: list[Collidable] = pygame.sprite.spritecollide(
            player, map_.collidable_objects,
            dokill=False
        )
        did_wall: bool = False
        for collided in collided_objects:
            if collided.type == "WALL" and not did_wall:
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


    def __quit() -> None:
        """Quits the Pygame instance."""
        pygame.quit()
        exit()


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