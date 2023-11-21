import pygame
from physicsObjects import Ball

pygame.init()

screen = pygame.display.set_mode((960,720))

pygame.display.set_caption("Goofy ass peggle clone")

app_running = True
deltatime = 0.0
clock = pygame.time.Clock()

bouncy_ball = Ball(screen, "assets/ball.png", 15, [5,5], [20,20])

while app_running:
    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            app_running = False

    screen.fill((50,50,50))

    bouncy_ball.move()
    bouncy_ball.check_collision()
    bouncy_ball.draw()

    # delta_time = 0.001 * clock.tick(144)

    clock.tick(60)

    pygame.display.flip()
    
pygame.quit()