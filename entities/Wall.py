import pygame

BRICK_COLOR = (180, 80, 30)
STEEL_COLOR = (190, 190, 190)

class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, wall_type, tile_size):
        super().__init__()
        
        self.type = wall_type

        self.image = pygame.Surface((tile_size, tile_size))
        
        if self.type == 1:
            self.image.fill(BRICK_COLOR)
        elif self.type == 2:
            self.image.fill(STEEL_COLOR)
            
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y