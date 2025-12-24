import pygame
import sys
import os

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TILE_SIZE = 40
BG_COLOR = (0, 0, 0)
GRID_COLOR = (50, 50, 50)

COLORS = {
    '0': BG_COLOR,
    '1': (180, 80, 30),
    '2': (190, 190, 190),
    'B': (0, 255, 0)
}

class LevelEditor:
    def __init__(self, screen):
        self.screen = screen
        self.rows = SCREEN_HEIGHT // TILE_SIZE
        self.cols = SCREEN_WIDTH // TILE_SIZE
        self.grid = [['0' for _ in range(self.cols)] for _ in range(self.rows)]
        self.current_tile = '1'
        self.font = pygame.font.Font(None, 30)

    def run(self):
        running = True
        print("EDITOR STARTED: 1-Brick, 2-Steel, 3-Base, 0-Erase, S-Save, ESC-Exit")
        
        while running:
            self.screen.fill(BG_COLOR)
            self.draw_grid()
            self.draw_tiles()
            self.draw_ui()
            
            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    
                    elif event.key == pygame.K_1: self.current_tile = '1'
                    elif event.key == pygame.K_2: self.current_tile = '2'
                    elif event.key == pygame.K_3: self.current_tile = 'B'
                    elif event.key == pygame.K_0: self.current_tile = '0'
                    
                    elif event.key == pygame.K_s:
                        self.save_level("levels/custom.txt")

                if pygame.mouse.get_pressed()[0]:
                    self.handle_mouse()

    def handle_mouse(self):
        mx, my = pygame.mouse.get_pos()
        col = mx // TILE_SIZE
        row = my // TILE_SIZE
        
        if 0 <= row < self.rows and 0 <= col < self.cols:
            self.grid[row][col] = self.current_tile

    def draw_grid(self):
        for x in range(0, SCREEN_WIDTH, TILE_SIZE):
            pygame.draw.line(self.screen, GRID_COLOR, (x, 0), (x, SCREEN_HEIGHT))
        for y in range(0, SCREEN_HEIGHT, TILE_SIZE):
            pygame.draw.line(self.screen, GRID_COLOR, (0, y), (SCREEN_WIDTH, y))

    def draw_tiles(self):
        for r in range(self.rows):
            for c in range(self.cols):
                tile = self.grid[r][c]
                if tile != '0':
                    color = COLORS.get(tile, (255, 255, 255))
                    rect = pygame.Rect(c * TILE_SIZE, r * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                    pygame.draw.rect(self.screen, color, rect)
                    pygame.draw.rect(self.screen, (0,0,0), rect, 1)

    def draw_ui(self):
        text = f"Tool: {self.get_tool_name()} (Press 1,2,3,0). [S]ave, [ESC]xit"
        surf = self.font.render(text, True, (255, 255, 255))
        self.screen.blit(surf, (10, 10))

    def get_tool_name(self):
        if self.current_tile == '1': return "Brick"
        if self.current_tile == '2': return "Steel"
        if self.current_tile == 'B': return "Base"
        return "Eraser"

    def save_level(self, filename):
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        try:
            with open(filename, 'w') as f:
                for row in self.grid:
                    line = "".join(row)
                    f.write(line + "\n")
            print(f"Рівень збережено у {filename}!")
        except Exception as e:
            print(f"Помилка збереження: {e}")