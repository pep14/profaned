import pygame
from entity import Entity


PIXEL_SIZE = 4
SCREEN_DIMENSIONS = (1280, 720)

# entity setup
player = Entity(
    (SCREEN_DIMENSIONS[0] / 2, 0), 
    (PIXEL_SIZE * 32, PIXEL_SIZE * 48)
)

# pygame setup
pygame.init()

window = pygame.display.set_mode(SCREEN_DIMENSIONS)
pygame.display.set_caption("Profaned")

run = True
while run:
    pygame.time.delay(60)

    pygame.draw.rect(
        window, 
        (255, 0, 0), 
        (
            player.x - player.hitbox[0] / 2, 
            SCREEN_DIMENSIONS[1] - player.y - player.hitbox[1], 
            player.hitbox[0], 
            player.hitbox[1]
        )
    )

    pygame.display.update()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

pygame.quit()