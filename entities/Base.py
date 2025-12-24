import pygame

class Base(pygame.sprite.Sprite):
    def __init__(self, x, y, tile_size):
        super().__init__()
        
        self.image = pygame.Surface((tile_size, tile_size))
        self.image.fill((0, 255, 0))
        
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        self.health = 1