import pygame
import random
from entities.Bullet import Bullet

class LoggableMixin:
    def log_creation(self):
        print(f"[LogMixin] Створено ворога! ID об'єкта: {id(self)}")

class Enemy(pygame.sprite.Sprite, LoggableMixin):
    def __init__(self, x, y, /, *, walls_group, player_group, base_group, all_sprites_group, enemy_bullets_group):
        super().__init__()

        self.log_creation()
        
        self.walls = walls_group
        self.player_group = player_group
        self.base = base_group
        self.all_sprites = all_sprites_group
        self.enemy_bullets = enemy_bullets_group

        self.image = pygame.Surface((40, 40))
        self.image.fill((200, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        self.speed = 3
        self.direction = random.choice(['UP', 'DOWN', 'LEFT', 'RIGHT'])
        
        self.move_delay = 2000
        self.last_move_time = pygame.time.get_ticks()

        self.shoot_delay = 1500
        self.last_shot_time = pygame.time.get_ticks()

    def update(self): 
        self.move()
        self.shoot()

    def move(self):
        current_time = pygame.time.get_ticks()
        
        if current_time - self.last_move_time > self.move_delay:
            self.direction = random.choice(['UP', 'DOWN', 'LEFT', 'RIGHT'])
            self.last_move_time = current_time
            self.move_delay = random.randint(1500, 3000) 

        if self.direction == 'UP':
            self.rect.y -= self.speed
        elif self.direction == 'DOWN':
            self.rect.y += self.speed
        elif self.direction == 'LEFT':
            self.rect.x -= self.speed
        elif self.direction == 'RIGHT':
            self.rect.x += self.speed
            
        obstacle_list = self.walls.sprites() + self.player_group.sprites() + self.base.sprites()
        
        hit_list = pygame.sprite.spritecollide(self, obstacle_list, False)

        if hit_list:
            if self.direction == 'UP':
                self.rect.top = hit_list[0].rect.bottom
            elif self.direction == 'DOWN':
                self.rect.bottom = hit_list[0].rect.top
            elif self.direction == 'LEFT':
                self.rect.left = hit_list[0].rect.right
            elif self.direction == 'RIGHT':
                self.rect.right = hit_list[0].rect.left
            
            self.direction = random.choice(['UP', 'DOWN', 'LEFT', 'RIGHT'])
            self.last_move_time = current_time

        if not (0 <= self.rect.x <= 760): 
            if self.rect.x < 0:
                self.rect.x = 0
                self.direction = 'RIGHT'
            else:
                self.rect.x = 760
                self.direction = 'LEFT'
                
        if not (0 <= self.rect.y <= 560):
            if self.rect.y < 0:
                self.rect.y = 0
                self.direction = 'DOWN'
            else:
                self.rect.y = 560
                self.direction = 'UP'

    def shoot(self):
        current_time = pygame.time.get_ticks()
        
        if current_time - self.last_shot_time > self.shoot_delay:
            self.last_shot_time = current_time
            self.shoot_delay = random.randint(1000, 2500) 
            
            bullet = Bullet(self.rect.centerx, self.rect.centery, self.direction)
            
            self.all_sprites.add(bullet)
            self.enemy_bullets.add(bullet)