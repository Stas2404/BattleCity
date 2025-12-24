import pygame
import sys
import random
import Utils
import UI

from entities.Player import Player
from entities.Wall import Wall
from entities.Bullet import Bullet
from entities.Enemy import Enemy
from entities.Base import Base
from Editor import LevelEditor

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TILE_SIZE = 40
BG_COLOR = (0, 0, 0)

GAME_SCORE = 0

def run_game(screen, level_filename, save_data=None):
    global GAME_SCORE
    
    if save_data:
        GAME_SCORE = save_data['score']
        player_health = save_data['health']
        level_filename = save_data['level']
        print(f"Гру відновлено! Рівень: {level_filename}, Рахунок: {GAME_SCORE}")
    else:
        GAME_SCORE = 0
        player_health = 5
        print(f"Нова гра! Рівень: {level_filename}")

    if level_filename == "RANDOM_GEN":
        level_map = Utils.generate_random_level()
    else:
        level_map = Utils.load_level_from_file(level_filename)
        
    if not level_map:
        return

    clock = pygame.time.Clock()
    
    all_sprites = pygame.sprite.Group()
    walls = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    enemy_bullets = pygame.sprite.Group()
    player_group = pygame.sprite.GroupSingle()
    base_group = pygame.sprite.GroupSingle()

    for row_index, row in enumerate(level_map):
        for col_index, tile_type in enumerate(row):
            x = col_index * TILE_SIZE
            y = row_index * TILE_SIZE
            
            if tile_type == '1' or tile_type == '2':
                wall = Wall(x, y, int(tile_type), TILE_SIZE)
                all_sprites.add(wall)
                walls.add(wall)
            elif tile_type == 'B':
                base = Base(x, y, TILE_SIZE)
                all_sprites.add(base)
                base_group.add(base)

    player = Player(SCREEN_WIDTH, SCREEN_HEIGHT,
                    walls_group=walls,
                    enemies_group=enemies,
                    all_sprites_group=all_sprites,
                    bullets_group=bullets,
                    enemy_bullets_group=enemy_bullets,
                    health=player_health)
    all_sprites.add(player)
    player_group.add(player)

    NUM_ENEMIES = 6
    spawn_gen = Utils.spawn_point_generator(level_map, TILE_SIZE)
    
    print("Спавн ворогів через генератор...")
    
    for _ in range(NUM_ENEMIES):
        try:
            spawn_x, spawn_y = next(spawn_gen)
            
            enemy = Enemy(spawn_x, spawn_y, 
                          walls_group=walls, 
                          player_group=player_group,
                          base_group=base_group, 
                          all_sprites_group=all_sprites,
                          enemy_bullets_group=enemy_bullets)
            all_sprites.add(enemy)
            enemies.add(enemy)
            
        except StopIteration:
            print("УВАГА: На карті закінчилися вільні місця для ворогів!")
            break

    def handle_bullet_collisions(group):
        hits = pygame.sprite.groupcollide(group, walls, True, False)
        for bullet, hit_walls in hits.items():
            for wall in hit_walls:
                if wall.type == 1:
                    wall.kill()

    running = True
    result_message = "ABORTED"

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                
                if event.key == pygame.K_F5:
                    data_to_save = {
                        'level': level_filename,
                        'score': GAME_SCORE,
                        'health': player.health
                    }
                    if Utils.save_game_binary(data_to_save):
                        print("Game Saved!")

        if not player_group:
            print("Game Over - Player Died")
            result_message = "DEFEAT"
            pygame.time.wait(2000)
            running = False

        if not base_group:
            print("Game Over - Base Destroyed")
            result_message = "BASE DESTROYED"
            pygame.time.wait(2000)
            running = False
        
        if not enemies:
            print("Victory - Level Cleared!")
            result_message = "VICTORY"
            pygame.time.wait(2000)
            running = False

        all_sprites.update()
        handle_bullet_collisions(bullets)
        handle_bullet_collisions(enemy_bullets)
        
        all_proyectiles = pygame.sprite.Group()
        all_proyectiles.add(bullets)
        all_proyectiles.add(enemy_bullets)

        if pygame.sprite.groupcollide(all_proyectiles, base_group, True, True):
            pass

        hits = pygame.sprite.groupcollide(bullets, enemies, True, True)
        if hits:
            GAME_SCORE += len(hits) * 100

        screen.fill(BG_COLOR)
        all_sprites.draw(screen)
        
        UI.draw_text(screen, f"Score: {GAME_SCORE}", 30, 70, 20)
        UI.draw_text(screen, f"HP: {player.health}", 30, SCREEN_WIDTH - 70, 20)
        
        pygame.display.flip()
        clock.tick(60)
    
    Utils.log_result_to_text(GAME_SCORE, result_message)

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Battle City")

    while True:
        action_data = UI.main_menu(screen)
        
        if action_data:
            action, data = action_data
        
            if action == "NEW_GAME":
                run_game(screen, level_filename=data)
            
            elif action == "EDITOR":
                editor = LevelEditor(screen)
                editor.run()


            elif action == "CONTINUE":
                save_data = Utils.load_game_binary()
                if save_data:
                    run_game(screen, save_data['level'], save_data)
                else:
                    print("Збереження не знайдено!")
            
            elif action == "REDRAW":
                continue

if __name__ == "__main__":
    main()