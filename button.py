import pygame

from typing import Callable

from display import Display

class Button(pygame.sprite.Sprite):
    '''
    Creates a button object, contains a text surface and a rect object.
    '''
    __slots__ = ('__debug_color', '__surface', '__rect', '__effect')

    def __init__(
        self,
        surface: pygame.Surface,
        topleft: tuple[int, int] = (0, 0),
        effect: Callable | None = None,
        debug_color: tuple[int, int, int] | None = (255, 0, 0)
    ) -> None:
        super().__init__()

        self.__debug_color = debug_color
        self.__surface = surface
        self.__effect = effect

        self.__rect = pygame.Rect(*topleft, *surface.get_size())
    
    def get_rect(self) -> pygame.Rect:
        '''
        Returns the rect object of the button.
        '''
        return self.__rect

    def update(
        self,
        display: Display,
        pos: tuple[int, int] | None = None
    ) -> None:
        '''
        Updates the given surface by blitting text surfaces at the specified position.
        '''
        if pos is None:
            pos = self.__rect.topleft
        else:
            self.__rect.topleft = pos

        display.blit(self.__surface, self.__rect.topleft)

    def clicked(self) -> None:
        '''
        Called when the button is clicked.
        '''
        if self.__effect is not None:
            self.__effect()

    def debug(self, display: Display) -> None:
        '''
        Draws a debug rectangle on the given surface.
        '''
        pygame.draw.rect(display.get_internal_surface(), self.__debug_color, self.__rect, 1)