import pygame
import random
import toml

# Load config file
config_file_path = "./config.toml"
with open(config_file_path, "r") as f:
    config = toml.load(f)
    
# Set config values
initial_speed = config["physics"]["initial_speed"]
gravity = pygame.Vector2(0, config["physics"]["gravity"])
ball_size = config["objects"]["ball_size"]
peg_size = config["objects"]["peg_size"]
base_points_awarded = config["objects"]["points"]

class Ball(pygame.sprite.Sprite):
    def __init__(self, screen):
        super().__init__() # Initialize Ball instance as child of Sprite class

        # Initialize rectangle and texture
        self.screen = screen
        self.size = (ball_size, ball_size)
        self.texture = pygame.image.load("assets/ball.png")
        self.texture = pygame.transform.scale(self.texture, self.size)
        self.rect = self.texture.get_rect()
        self.has_collided = False

        # Set starting position
        self.start_position = pygame.Vector2((self.screen.get_size()[0] / 2, 50))
        self.reset_pos()

    def reset_pos(self):
        # Reset ball to starting position
        self.rect.center = self.start_position
        self.is_moving = False

    def get_initial_velocity_vector(self):
        # Calculate initial velocity vector using mouse position and set speed
        mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
        direction = mouse_pos - self.start_position
        initial_velocity_vector = direction.normalize() * initial_speed

        # Return initial velocity vector
        return pygame.Vector2(initial_velocity_vector)
    
    def start_physics(self):
        # Set velocity
        self.velocity = self.get_initial_velocity_vector()

        # Start movement
        self.is_moving = True

    def draw(self):
        self.screen.blit(self.texture, self.rect)

    def move(self):
        self.velocity += gravity
        self.rect.move_ip(self.velocity)

        # Move ball down if velocity is close to 0 to prevent ball stuck bug
        if self.velocity.x < 1 and self.velocity.x > -1 and self.velocity.y < 1 and self.velocity.y > -1:
            self.rect.move_ip(pygame.Vector2(0,1))

    def check_collision(self):
        width, height= self.screen.get_size()

        if self.rect.left <= 0 or self.rect.right >= width :
            if not self.has_collided:
                self.velocity = self.velocity.reflect(pygame.Vector2(1, 0)) * 0.9
                self.has_collided = True
        
        if self.rect.top <= 0:
            if not self.has_collided:
                self.velocity = self.velocity.reflect(pygame.Vector2(0, 1)) * 0.9
                self.has_collided = True

        if self.rect.bottom >= height + 40:
            self.reset_pos()


class BallTrajectory(Ball):
    def __init__(self, screen):
        super().__init__(screen)
        self.trajectory = None # Init trajectory as none
        self.prev_mouse_pos = pygame.mouse.get_pos()

    def check_trace_collision(self, trace_pos, all_pegs):
        # Return false if colliding walls (or other object), otherwise return false
        width, height = self.screen.get_size()
        if trace_pos.x <= 0 or trace_pos.x >= width or trace_pos.y >= height or trace_pos.y <= 0:
            return False
        
        for peg in all_pegs:
            if peg.rect.collidepoint(trace_pos):
                return False

        return True

    def calc_trajectory(self, all_pegs):
        mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
        direction = mouse_pos - self.start_position
        trace_velocity = direction.normalize() * initial_speed

        trace_pos = pygame.Vector2(self.start_position)
        trajectory_points = []

        while self.check_trace_collision(trace_pos, all_pegs):
            trace_velocity += gravity
            trace_pos += trace_velocity
            trajectory_points.append(trace_pos.copy())

        return trajectory_points
    
    def update_trajectory(self, all_pegs):
        current_mouse_pos = pygame.mouse.get_pos()
        if current_mouse_pos != self.prev_mouse_pos:
            self.trajectory = self.calc_trajectory(all_pegs)
            self.prev_mouse_pos = current_mouse_pos

    def draw_trajectory(self, screen):
        if self.trajectory:
            for point in self.trajectory:
                pygame.draw.circle(screen, (79, 240, 255), (int(point.x), int(point.y)), 2)   
            

class Peg(pygame.sprite.Sprite):
    def __init__(self,screen, position, type): 
        super().__init__()
        # Attributes for all pegs
        self.screen = screen
        self.position = position
        self.has_collided = False
        self.is_hit = False
        self.radius = peg_size
        self.border = 1

        self.points = base_points_awarded
        self.type = type

        # Set peg-type-specific attributes
        if self.type == "blue":
            self.color = (21, 18, 179)
            self.border_color = (138, 156, 235)
        elif self.type == "red":
            self.color = (186, 64, 11)
            self.border_color = (230, 173, 76)
        elif self.type == "purple":
            self.color = (117, 10, 163)
            self.border_color = (213, 169, 222)
        else:
            raise ValueError("Invalid peg type")
        
        self.image = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        self.update()
        self.rect = self.image.get_rect(center=self.position)

    def draw(self):
        # Draw the peg on the screen
        self.screen.blit(self.image, self.rect.topleft)

    def update(self):
        # Update peg visuals
        pygame.draw.circle(self.image, self.color, (self.radius, self.radius), self.radius)
        pygame.draw.circle(self.image, self.border_color, (self.radius, self.radius), self.radius, 2) 
        pygame.draw.circle(self.image, (0, 0, 0), (self.radius, self.radius), self.radius + 2, 1)

    def check_collision(self, ball, all_pegs):

        # Get list of all collisions
        collisions = pygame.sprite.spritecollide(ball, all_pegs, False)

        for peg in collisions:
            if peg == self:
                print("Peg collision detected!")
                self.has_collided = True
                normal = (pygame.Vector2(ball.rect.center) - peg.position).normalize()
                ball.velocity = ball.velocity.reflect(normal) * 0.7
                self.on_collision()

                # To prevent vector normalizing 0 crash (and ball infinitely bouncing on one peg),
                # send ball in random direction if 0.3 > ball x velocity > -0.3
                if ball.velocity.x < 0.3 and ball.velocity.x > -0.3:
                    if random.random() > 0.5:
                        ball.velocity.x = 2
                    else:
                        ball.velocity.x = -2

    def on_collision(self):
        # 
        if self.is_hit:
            return
        
        self.is_hit = True

        if self.type == "purple":
            self.color = (149, 76, 245)
        elif self.type == "red":
            self.color = (247, 163, 17)
        else:
            self.color = (82, 112, 247)

        self.update()


class Trough(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
