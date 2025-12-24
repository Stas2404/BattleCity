import pygame

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        super().__init__()
        
        self.image = pygame.Surface((10, 10))
        self.image.fill((255, 255, 255))
        
        self.rect = self.image.get_rect()
        
        self.rect.centerx = x
        self.rect.centery = y
        self.direction = direction
        self.speed = 10 

    def update(self):
        if self.direction == 'UP':
            self.rect.y -= self.speed
        elif self.direction == 'DOWN':
            self.rect.y += self.speed
        elif self.direction == 'LEFT':
            self.rect.x -= self.speed
        elif self.direction == 'RIGHT':
            self.rect.x += self.speed
            
        if self.rect.bottom < 0 or self.rect.top > 600 or \
           self.rect.right < 0 or self.rect.left > 800:
            self.kill()