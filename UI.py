import pygame
import sys
import os

BG_COLOR = (0, 0, 0)
MENU_COLOR = (50, 50, 50)
TEXT_COLOR = (255, 255, 255)
SCREEN_WIDTH = 800

def draw_text(screen, text, size, x, y, color=TEXT_COLOR):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)
    return text_rect

def show_instructions(screen):
    running = True
    while running:
        screen.fill(BG_COLOR)
        draw_text(screen, "HOW TO PLAY", 50, SCREEN_WIDTH // 2, 50)
        draw_text(screen, "W, A, S, D - Рух", 30, SCREEN_WIDTH // 2, 150)
        draw_text(screen, "SPACE - Постріл", 30, SCREEN_WIDTH // 2, 200)
        draw_text(screen, "F5 - Зберегти гру (Binary save)", 30, SCREEN_WIDTH // 2, 250)
        draw_text(screen, "ESC - Повернутися в меню", 30, SCREEN_WIDTH // 2, 500)
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

def show_level_selection(screen):
    running = True
    level_folder = "levels"
    
    try:
        files = [f for f in os.listdir(level_folder) if f.endswith('.txt')]
        files.sort()
    except FileNotFoundError:
        files = []

    while running:
        screen.fill(BG_COLOR)
        draw_text(screen, "SELECT LEVEL", 50, SCREEN_WIDTH // 2, 50)
        
        level_buttons = {}
        
        rand_rect = draw_text(screen, "[ GENERATE RANDOM ]", 40, SCREEN_WIDTH // 2, 100, (100, 255, 255))

        for i, filename in enumerate(files):
            display_name = filename.replace(".txt", "").upper()
            y_pos = 150 + i * 50
            
            if y_pos < 550:
                rect = draw_text(screen, display_name, 30, SCREEN_WIDTH // 2, y_pos)
                full_path = os.path.join(level_folder, filename)
                level_buttons[full_path] = rect

        back_rect = draw_text(screen, "BACK", 30, SCREEN_WIDTH // 2, 580, (200, 50, 50))
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    
                    if rand_rect.collidepoint(mouse_pos):
                        return "RANDOM_GEN"
                    
                    for lvl_path, rect in level_buttons.items():
                        if rect.collidepoint(mouse_pos):
                            return lvl_path
                    
                    if back_rect.collidepoint(mouse_pos):
                        return None

def main_menu(screen):
    screen.fill(MENU_COLOR)
    draw_text(screen, "BATTLE CITY PYTHON", 60, SCREEN_WIDTH // 2, 80, (255, 215, 0))
    
    btn_play = draw_text(screen, "PLAY", 50, SCREEN_WIDTH // 2, 200)
    btn_editor = draw_text(screen, "LEVEL EDITOR", 50, SCREEN_WIDTH // 2, 270)
    btn_continue = draw_text(screen, "CONTINUE", 50, SCREEN_WIDTH // 2, 340)
    btn_help = draw_text(screen, "HOW TO PLAY", 50, SCREEN_WIDTH // 2, 410)
    btn_exit = draw_text(screen, "EXIT", 50, SCREEN_WIDTH // 2, 480)
    
    pygame.display.flip()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    pos = pygame.mouse.get_pos()
                    
                    if btn_play.collidepoint(pos):
                        level = show_level_selection(screen)
                        if level: return ("NEW_GAME", level)
                        else: return ("REDRAW", None)

                    elif btn_editor.collidepoint(pos):
                        return ("EDITOR", None)
                    elif btn_continue.collidepoint(pos):
                        return ("CONTINUE", None)
                    elif btn_help.collidepoint(pos):
                        show_instructions(screen)
                        return ("REDRAW", None)
                    elif btn_exit.collidepoint(pos):
                        pygame.quit(); sys.exit()