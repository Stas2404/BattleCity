import pygame
from entities.Bullet import Bullet

class Player(pygame.sprite.Sprite):
    def __init__(self, screen_width, screen_height, /, *, walls_group, enemies_group, all_sprites_group, bullets_group, enemy_bullets_group, health = 3):
        super().__init__()

        self.screen_width = screen_width
        self.screen_height = screen_height
        
        self.walls = walls_group
        self.enemies = enemies_group
        self.all_sprites = all_sprites_group
        self.bullets = bullets_group
        self.enemy_bullets = enemy_bullets_group

        self.image = pygame.Surface((40, 40))
        self.image.fill((255, 255, 0))
        self.rect = self.image.get_rect()
        
        self.spawn_pos = (screen_width // 2, screen_height // 2)
        self.rect.center = self.spawn_pos
        
        self.speed = 4.5
        self.direction = 'UP'
        
        self.shoot_delay = 300
        self.last_shot_time = pygame.time.get_ticks()
        
        self._health = health

        self.active_effects = []
    
    @property
    def health(self):
        return self._health

    @health.setter
    def health(self, value):
        if value < 0:
            print("Здоров'я не може бути менше 0! Встановлюємо 0.")
            self._health = 0
        elif value > 10:
            print("Максимальне здоров'я 10!")
            self._health = 10
        else:
            self._health = value
    
    def __str__(self):
        return f"Player Object [HP: {self._health}, Pos: {self.rect.center}]"

    def __len__(self):
        return len(self.active_effects)

    def shoot(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time > self.shoot_delay:
            self.last_shot_time = current_time
            bullet = Bullet(self.rect.centerx, self.rect.centery, self.direction)
            self.all_sprites.add(bullet)
            self.bullets.add(bullet)

    def update(self):
        self.check_hits()

        self.update_effects()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.shoot()

        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
            self.direction = 'LEFT'
        elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
            self.direction = 'RIGHT'
        
        hit_list_x = pygame.sprite.spritecollide(self, self.walls, False)
        for wall in hit_list_x:
            if self.direction == 'RIGHT':
                self.rect.right = wall.rect.left
            elif self.direction == 'LEFT':
                self.rect.left = wall.rect.right

        enemy_hit_list_x = pygame.sprite.spritecollide(self, self.enemies, False)
        for enemy in enemy_hit_list_x:
            if self.direction == 'RIGHT':
                self.rect.right = enemy.rect.left
            elif self.direction == 'LEFT':
                self.rect.left = enemy.rect.right

        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.rect.y -= self.speed
            self.direction = 'UP'
        elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.rect.y += self.speed
            self.direction = 'DOWN'

        hit_list_y = pygame.sprite.spritecollide(self, self.walls, False)
        for wall in hit_list_y:
            if self.direction == 'DOWN':
                self.rect.bottom = wall.rect.top
            elif self.direction == 'UP':
                self.rect.top = wall.rect.bottom

        enemy_hit_list_y = pygame.sprite.spritecollide(self, self.enemies, False)
        for enemy in enemy_hit_list_y:
            if self.direction == 'DOWN':
                self.rect.bottom = enemy.rect.top
            elif self.direction == 'UP':
                self.rect.top = enemy.rect.bottom

        if self.rect.left < 0: 
            self.rect.left = 0
        if self.rect.right > self.screen_width: 
            self.rect.right = self.screen_width
        if self.rect.top < 0: 
            self.rect.top = 0
        if self.rect.bottom > self.screen_height: 
            self.rect.bottom = self.screen_height

    def check_hits(self):
        bullet_hits = pygame.sprite.spritecollide(self, self.enemy_bullets, True)
        if bullet_hits:
            self.health -= 1 
            print(f"Подія: {self}") 

            if self.health <= 0:
                print("Гравець знищений!")
                self.kill()
            else:
                self.rect.center = self.spawn_pos
    

    def heal(self, amount=1):
        self.health += amount
        print(f"ГРАВЕЦЬ ЗЦІЛИВСЯ! Нове здоров'я: {self.health}")

    def add_speed_boost(self, duration_ms):
        original_speed = self.speed
        expire_time = pygame.time.get_ticks() + duration_ms
        is_active = True

        print(f"БОНУС ШВИДКОСТІ! {self.speed} -> {self.speed * 1.5}")

        def speed_effect_updater():
            nonlocal is_active
            
            if pygame.time.get_ticks() > expire_time:
                self.speed = original_speed
                is_active = False
                print("Бонус швидкості закінчився.")
            else:
                self.speed = original_speed * 1.5
            
            return is_active

        self.active_effects.append(speed_effect_updater)

    def update_effects(self):
        self.active_effects = [effect for effect in self.active_effects if effect()]
