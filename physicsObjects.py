import pygame

class Ball(pygame.sprite.Sprite):
    def __init__(self, screen, image_path, radius, initial_velocity, initial_position):
        self.screen = screen

        self.texture = pygame.image.load(image_path)
        self.texture = pygame.transform.scale(self.texture, (radius * 2, radius * 2))
        self.rect = self.texture.get_rect()

        self.rect.center = initial_position
        self.velocity = pygame.Vector2(initial_velocity)
        self.gravity = pygame.Vector2(0, 0.5)

    def draw(self):
        self.screen.blit(self.texture, self.rect)

    def move(self):
        self.velocity += self.gravity
        self.rect.move_ip(self.velocity)

    def check_collision(self):
        width, height = self.screen.get_size()

        if self.rect.left <= 0 or self.rect.right >= width:
            self.velocity = self.velocity.reflect(pygame.Vector2(1, 0))

        if self.rect.top <= 0 or self.rect.bottom >= height:
            self.velocity = self.velocity.reflect(pygame.Vector2(0, 1))

class Peg(pygame.sprite.Sprite):
    def __init__(self):
        pass
