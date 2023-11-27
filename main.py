from modules.physicsObjects import Ball, BallTrajectory
from modules.pegLoader import all_pegs
import pygame
import toml


# Load config
config_file_path = "./config.toml"
with open(config_file_path, "r") as f:
    config = toml.load(f)["game"]

# Set config values
title = config["title"]
resolution = config["resolution"]
fps = config["fps"]

# Initialize pygame
pygame.init()
pygame.display.set_caption(title)
screen = pygame.display.set_mode(resolution)

# Initialize physics objects
ball = Ball(screen)
trajectory = BallTrajectory(screen)

# Initialize clock and collision cooldown 
clock = pygame.time.Clock()
ball_collision_cooldown = 0
peg_collision_cooldown = 0
collision_cooldown_limit = 10

# Start game
app_running = True

# Main event loop
while app_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            app_running = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not ball.is_moving:
            ball.start_physics()
            
    screen.fill((50,50,50))
    # Use collision cooldown
    '''
    if ball.is_moving:     
        ball.move()
        
        # Collision cooldown logic
        if ball.has_collided and ball_collision_cooldown == 0:
            ball.has_collided = False
            ball_collision_cooldown = collision_cooldown_limit

        if ball_collision_cooldown > 0:
            ball_collision_cooldown -= 1
            
        
        for peg in all_pegs:
            if peg.has_collided and peg_collision_cooldown == 0:
                peg.has_collided = False
                peg_collision_cooldown = collision_cooldown_limit

            if peg_collision_cooldown > 0:
                peg_collision_cooldown -= 1

            if not peg.has_collided:
                peg.check_collision(ball, all_pegs)

        ball.check_collision()

    else:
        trajectory.update_trajectory(all_pegs)
        trajectory.draw_trajectory(screen)

        for peg in all_pegs:
            if peg.is_hit:
                peg.kill()
    '''
    # No use of collision cooldown
    if ball.is_moving:
        ball.move()
        ball.check_collision()

        for peg in all_pegs:
            peg.check_collision(ball, all_pegs)
    else:
        trajectory.update_trajectory(all_pegs)
        trajectory.draw_trajectory(screen)

        for peg in all_pegs:
            if peg.is_hit:
                peg.kill()
                
    ball.draw()
    all_pegs.draw(screen)
        
    #clock.tick(10)
    clock.tick(fps)
    pygame.display.flip()

pygame.quit()