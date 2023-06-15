import pygame 
from settings import *
from snake import Snake

pygame.init()

clock = pygame.time.Clock()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")

#----------------------> Objects <----------------------#
snake = Snake()

run = True
while run:
    dt = clock.tick(FPS) / 1000.0  # Convert milliseconds to seconds
    
    if not snake.alive:
        run = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                snake.move(0)
            if event.key == pygame.K_s:
                snake.move(1)
            if event.key == pygame.K_a:
                snake.move(2)
            if event.key == pygame.K_d:
                snake.move(3)

    snake.update(dt)
    screen.fill((0, 0, 0))    # black background
    snake.draw(screen)

    pygame.display.update() # update display changes
