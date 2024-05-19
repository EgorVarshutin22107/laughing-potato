import os
import sys
import random
import pygame
import time

# Класс для игрока (оранжевого персонажа)
class Player(object):
    def __init__(self):
        self.rect = pygame.Rect(32, 32, 16, 16)

    def move(self, dx, dy):
        if dx != 0:
            self.move_single_axis(dx, 0)
        if dy != 0:
            self.move_single_axis(0, dy)

    def move_single_axis(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

        for wall in walls:
            if self.rect.colliderect(wall.rect):
                if dx > 0:
                    self.rect.right = wall.rect.left
                if dx < 0:
                    self.rect.left = wall.rect.right
                if dy > 0:
                    self.rect.bottom = wall.rect.top
                if dy < 0:
                    self.rect.top = wall.rect.bottom

# Класс для монеты
class Coin(object):
    def __init__(self, pos, negative=False):
        self.rect = pygame.Rect(pos[0], pos[1], 10, 10)
        self.negative = negative

# Класс для стены
class Wall(object):
    def __init__(self, pos):
        walls.append(self)
        self.rect = pygame.Rect(pos[0], pos[1], 16, 16)

# Генерация лабиринта с использованием алгоритма DFS
def generate_maze(width, height):
    maze = [[1] * width for _ in range(height)]
    
    def carve_passages_from(cx, cy):
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        random.shuffle(directions)
        for direction in directions:
            nx, ny = cx + direction[0] * 2, cy + direction[1] * 2
            if 0 <= nx < width and 0 <= ny < height and maze[ny][nx] == 1:
                maze[cy + direction[1]][cx + direction[0]] = 0
                maze[ny][nx] = 0
                carve_passages_from(nx, ny)
                
    maze[1][1] = 0
    carve_passages_from(1, 1)
    return maze

# Инициализация pygame
os.environ["SDL_VIDEO_CENTERED"] = "1"
pygame.init()

# Настройка экрана
screen_width, screen_height = 740, 580
maze_offset_x, maze_offset_y = 0, 50  # Смещение лабиринта для создания пространства для счетчика
pygame.display.set_caption("Достигните красного квадрата!")
screen = pygame.display.set_mode((screen_width, screen_height))  # Увеличенный размер экрана

clock = pygame.time.Clock()
walls = []  # Список для хранения стен
player = Player()  # Создание игрока
coins = []  # Список для хранения монет

# Генерация случайного лабиринта
maze_width, maze_height = 40, 30
maze = generate_maze(maze_width, maze_height)

# Обеспечение проходимости стартовых и конечных позиций
player_start = (1, 1)
maze[1][1] = 0
end_position = (maze_width - 2, maze_height - 2)
maze[maze_height - 2][maze_width - 2] = 0

# Парсинг сетки лабиринта и создание стен и монет
positive_coin_count = 0
negative_coin_count = 0
for y in range(maze_height):
    for x in range(maze_width):
        if maze[y][x] == 1:
            Wall((x * 16 + maze_offset_x, y * 16 + maze_offset_y))
        elif (x, y) == player_start:
            player.rect.topleft = (x * 16 + maze_offset_x, y * 16 + maze_offset_y)
        elif (x, y) == end_position:
            end_rect = pygame.Rect(x * 16 + maze_offset_x, y * 16 + maze_offset_y, 16, 16)
        elif random.random() < 0.1:  # Случайное размещение монет
            if negative_coin_count < positive_coin_count / 2:  # Обеспечение меньшего количества отрицательных монет
                is_negative = random.random() < 0.33  # Регулировка вероятности для отрицательных монет
            else:
                is_negative = False
            
            if is_negative:
                negative_coin_count += 1
            else:
                positive_coin_count += 1
            
            coins.append(Coin((x * 16 + maze_offset_x, y * 16 + maze_offset_y), negative=is_negative))

# Создание границ справа и снизу
for x in range(maze_width):
    Wall((x * 16 + maze_offset_x, maze_height * 16 + maze_offset_y))
for y in range(maze_height):
    Wall((maze_width * 16 + maze_offset_x, y * 16 + maze_offset_y))

# Инициализация счетчика монет и таймера
coin_count = 0
font = pygame.font.SysFont(None, 36)
start_time = time.time()
max_time = 60  # Максимальное время в секундах

def show_statistics(elapsed_time):
    screen.fill((0, 0, 0))
    stats_text = font.render(f"Всего собрано монет: {coin_count}", True, (255, 255, 255))
    time_text = font.render(f"Время: {elapsed_time:.2f} секунд", True, (255, 255, 255))
    screen.blit(stats_text, (screen_width // 2 - stats_text.get_width() // 2, screen_height // 2 - stats_text.get_height() // 2 - 20))
    screen.blit(time_text, (screen_width // 2 - time_text.get_width() // 2, screen_height // 2 - time_text.get_height() // 2 + 20))
    pygame.display.flip()
    pygame.time.wait(3000)  # Отображение статистики в течение 3 секунд

running = True
while running:

    clock.tick(60)

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
            running = False

    # Перемещение игрока при нажатии клавиши со стрелкой
    key = pygame.key.get_pressed()
    if key[pygame.K_LEFT]:
        player.move(-2, 0)
    if key[pygame.K_RIGHT]:
        player.move(2, 0)
    if key[pygame.K_UP]:
        player.move(0, -2)
    if key[pygame.K_DOWN]:
        player.move(0, 2)

    # Проверка, собирает ли игрок монету
    for coin in coins[:]:
        if player.rect.colliderect(coin.rect):
            coins.remove(coin)  # Удаление монеты, если игрок ее собирает
            if coin.negative:
                if coin_count > 0:  # Уменьшение счетчика монет только если он больше нуля
                    coin_count -= 1
            else:
                coin_count += 1  # Увеличение счетчика монет, если это положительная монета

    # Проверка, достигает ли игрок конца
    if player.rect.colliderect(end_rect):
        elapsed_time = time.time() - start_time
        show_statistics(elapsed_time)
        pygame.quit()
        sys.exit()

    # Проверка, истекло ли время
    elapsed_time = time.time() - start_time
    if elapsed_time > max_time:
        show_statistics(elapsed_time)
        pygame.quit()
        sys.exit()

    # Отрисовка сцены
    screen.fill((0, 0, 0))
    for wall in walls:
        pygame.draw.rect(screen, (255, 255, 255), wall.rect)
    for coin in coins:
        color = (255, 0, 0) if coin.negative else (255, 255, 0)  # Красные для отрицательных монет, желтые для положительных
        pygame.draw.ellipse(screen, color, coin.rect)  # Отрисовка монет
    pygame.draw.rect(screen, (255, 0, 0), end_rect)
    pygame.draw.rect(screen, (255, 200, 0), player.rect)

    # Отображение счетчика монет и таймера вне области лабиринта
    coin_text = font.render(f"Монеты: {coin_count}", True, (255, 255, 255))
    screen.blit(coin_text, (10, 10))
    
    timer_text = font.render(f"Время: {elapsed_time:.2f} с", True, (255, 255, 255))
    screen.blit(timer_text, (screen_width - timer_text.get_width() - 10, 10))

    pygame.display.flip()
    clock.tick(360)

pygame.quit()
