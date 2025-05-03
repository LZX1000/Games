import pygame

def event_handling(
    keys: dict[int, bool],
    debug_mode: bool
) -> bool:
    '''
    Handles events such as mouse clicks and keyboard inputs.
    '''
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and keys[pygame.K_LCTRL]:
                debug_mode = not debug_mode

    return debug_mode