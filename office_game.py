import pygame
import ctypes

import game


class Button(pygame.sprite.Sprite):
    '''
    Creates a button object, contains a text surface and a rect object.
    '''
    __slots__ = ('debug_color', '__surface', '__rect')

    def __init__(
        self,
        surface: pygame.Surface,
        topleft: tuple[int, int] = (0, 0),
        debug_color: tuple[int, int, int] | None = (255, 0, 0)
    ) -> None:
        super().__init__()

        self.debug_color = debug_color
        self.__surface = surface

        self.__rect = pygame.Rect(*topleft, *surface.get_size())
    
    def update(
        self,
        surface: pygame.Surface,
        pos: tuple[int, int] | None = None
    ) -> None:
        '''
        Updates the given surface by blitting text surfaces at the specified position.
        '''
        if pos is None:
            pos = self.__rect.topleft
        else:
            self.__rect.topleft = pos

        surface.blit(self.__surface, self.__rect.topleft)

    def debug(self, surface: pygame.Surface) -> None:
        '''
        Draws a debug rectangle on the given surface.
        '''
        pygame.draw.rect(surface, self.debug_color, self.__rect, 1)


def event_handling() -> None:
    '''
    Handles events such as mouse clicks and keyboard inputs.
    '''
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()


def main():
    # Initialize
    pygame.init()
    pygame.font.init()
    font = pygame.font.SysFont("Arial", 20)
    pygame.display.set_caption("Office Game")
    clock = pygame.time.Clock()

    # Screen Settings
    internal_width = 640
    internal_height = 360
    ctypes.windll.user32.SetProcessDPIAware()
    screen_size = (1920, 1080)

    internal_surface = pygame.Surface((internal_width, internal_height))
    screen = pygame.display.set_mode(screen_size) # pygame.FULLSCREEN

    running = True
    debug_mode = False
    gamestate = "game"
    max_fps = 60

    changing = {}

    buttons: list[Button] = []

    space_pressed = False

    new_button = Button(
        surface=(button_surface := font.render("Change", False, (0, 0, 0), (200, 200, 200))),
        topleft=(internal_width // 2 - button_surface.get_width() // 2, internal_height // 2 - button_surface.get_height() // 2),
        debug_color=(255, 0, 0)
    )
    buttons.append(new_button)

    while running:
        keys = pygame.key.get_pressed()

        # Get accurate mouse position
        scaled_mouse_pos = pygame.mouse.get_pos()
        mouse_pos = (
            scaled_mouse_pos[0] * internal_width / screen_size[0],
            scaled_mouse_pos[1] * internal_height / screen_size[1]
            )

        debug_mode = game.event_handling(keys, debug_mode)

        if keys[pygame.K_ESCAPE]:
            running = False
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Render in 640x360
        if gamestate == "game":
            # Interal rendering
            internal_surface.fill((180, 180, 180)) # Sub-background

            for button in buttons:
                button.update(internal_surface)
                if debug_mode:
                    button.debug(internal_surface)

        # Global debugs
        if debug_mode:
            # Mouse
            pygame.draw.circle(internal_surface, (0, 0, 0), mouse_pos, 2)

        # Upscale to 1920x1080
        scaled_surface = pygame.transform.scale(internal_surface, screen_size)
        screen.blit(scaled_surface, (0, 0))

        pygame.display.flip()
        # Tick Speed
        dt = clock.tick(max_fps) / 1000

if __name__ == "__main__":
    main()