import pickle
import os
import datetime
import random

SAVE_FILE = "savegame.dat"
LOG_FILE = "game_log.txt"

def generate_random_level(rows=15, cols=20):
    grid = [['0' for _ in range(cols)] for _ in range(rows)]
    
    for r in range(2, rows - 2):
        for c in range(2, cols // 2):
            
            roll = random.random()
            
            if roll < 0.20:
                grid[r][c] = '1'
            elif roll < 0.23:
                grid[r][c] = '2'

    for r in range(rows):
        for c in range(cols // 2):
            mirror_col = cols - 1 - c
            grid[r][mirror_col] = grid[r][c]

    base_x = cols // 2
    base_y = rows - 1
    
    real_base_x = 10 
    
    if real_base_x < cols:
        grid[base_y][real_base_x] = 'B'
        
        if real_base_x - 1 >= 0:
            grid[base_y][real_base_x - 1] = '1'
            grid[base_y - 1][real_base_x - 1] = '1'
        grid[base_y - 1][real_base_x] = '1'
        if real_base_x + 1 < cols:
            grid[base_y][real_base_x + 1] = '1'
            grid[base_y - 1][real_base_x + 1] = '1'

    final_level = ["".join(row) for row in grid]
    
    print("[Utils] Згенеровано рандомний рівень.")
    return final_level

def debug_logger(func):
    def wrapper(*args, **kwargs):
        print(f"[DEBUG] Виклик функції: {func.__name__}")
        result = func(*args, **kwargs)
        print(f"[DEBUG] Функція {func.__name__} завершила роботу")
        return result
    return wrapper

@debug_logger
def load_level_from_file(filename):
    try:
        with open(filename, 'r') as f:
            lines = [line.strip() for line in f.readlines()][:]
        
        unique_blocks = set()
        for line in lines:
            for char in line:
                unique_blocks.add(char)
        
        print(f"[Utils] Рівень {filename} завантажено. Типи блоків: {unique_blocks}")
        return lines

    except FileNotFoundError:
        print(f"[Utils] Помилка: Файл {filename} не знайдено!")
        return None
    
def save_game_binary(data: dict) -> bool:
    try:
        with open(SAVE_FILE, 'wb') as f:
            pickle.dump(data, f)
        print("[Utils] Гру збережено успішно (binary).")
        return True
    except Exception as e:
        print(f"[Utils] Помилка збереження: {e}")
        return False

def load_game_binary():
    if not os.path.exists(SAVE_FILE):
        return None
    try:
        with open(SAVE_FILE, 'rb') as f:
            return pickle.load(f)
    except Exception as e:
        print(f"[Utils] Помилка завантаження сейву: {e}")
        return None

def log_result_to_text(score, result_type="GAME OVER"):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {result_type} | Score: {score}\n"
    
    with open(LOG_FILE, 'a') as f:
        f.write(log_entry)
    print(f"[Utils] Результат записано у {LOG_FILE}")

def spawn_point_generator(level_map, tile_size):
    rows = len(level_map)
    cols = len(level_map[0])
    
    possible_positions = []
    for r in range(rows):
        for c in range(cols):
            if level_map[r][c] == '0':
                possible_positions.append((r, c))
    
    random.shuffle(possible_positions)
    
    for row, col in possible_positions:
        x = col * tile_size
        y = row * tile_size
        yield (x, y)