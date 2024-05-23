import os
import random
import pygame

# Класс для игрока
class Player:
    def __init__(self):
        self.rect = pygame.Rect(32, 32, 16, 16)
        self.speed = 2
        self.slowed_until = 0

    def move(self, dx, dy, walls):
        if dx != 0:
            self.move_single_axis(dx, 0, walls)
        if dy != 0:
            self.move_single_axis(0, dy, walls)

    def move_single_axis(self, dx, dy, walls):
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
class Coin:
    def __init__(self, pos, slow=False):
        self.rect = pygame.Rect(pos[0], pos[1], 10, 10)
        self.slow = slow

# Класс для стены
class Wall:
    def __init__(self, pos):
        self.rect = pygame.Rect(pos[0], pos[1], 16, 16)

# Класс для генерации лабиринта
class Maze:
    def __init__(self, width, height):
        if width <= 0 or height <= 0:
            raise ValueError("Invalid maze size")
        self.width = width
        self.height = height
        self.grid = self.generate_maze()

    def generate_maze(self):
        if self.width < 3 or self.height < 3:
            raise ValueError("Maze size too small")
        maze = [[1] * self.width for _ in range(self.height)]
        
        def carve_passages_from(cx, cy):
            directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
            random.shuffle(directions)
            for direction in directions:
                nx, ny = cx + direction[0] * 2, cy + direction[1] * 2
                if 0 <= nx < self.width and 0 <= ny < self.height and maze[ny][nx] == 1:
                    maze[cy + direction[1]][cx + direction[0]] = 0
                    maze[ny][nx] = 0
                    carve_passages_from(nx, ny)
                    
        maze[1][1] = 0
        carve_passages_from(1, 1)
        return maze

# Класс для отображения интерфейса
class UI:
    def __init__(self, screen, font):
        self.screen = screen
        self.font = font

    def show_main_menu(self):
        self.screen.fill((0, 0, 0))
        title_text = self.font.render("Главное Меню", True, (255, 255, 255))
        start_text = self.font.render("Начать Игру", True, (0, 255, 0))
        exit_text = self.font.render("Выйти", True, (255, 0, 0))
        self.screen.blit(title_text, (screen_width // 2 - title_text.get_width() // 2, screen_height // 2 - title_text.get_height() // 2 - 80))
        start_rect = start_text.get_rect(center=(screen_width // 2, screen_height // 2 - 20))
        exit_rect = exit_text.get_rect(center=(screen_width // 2, screen_height // 2 + 40))
        self.screen.blit(start_text, start_rect)
        self.screen.blit(exit_text, exit_rect)
        pygame.display.flip()

        while True:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                    return "exit"
                if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                    if start_rect.collidepoint(e.pos):
                        return "start"
                    if exit_rect.collidepoint(e.pos):
                        pygame.quit()
                        return "exit"

# Класс для игры
class Game:
    def __init__(self):
        os.environ["SDL_VIDEO_CENTERED"] = "1"
        pygame.init()

        global screen_width, screen_height, maze_offset_x, maze_offset_y
        screen_width, screen_height = 740, 580
        maze_offset_x, maze_offset_y = 0, 50
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("Достигните конца лабиринта!")

        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 36)
        self.ui = UI(self.screen, self.font)

        self.walls = []
        self.coins = []
        self.player = Player()

        global maze_width, maze_height
        maze_width, maze_height = 40, 30
        self.maze = Maze(maze_width, maze_height)
        self.end_rect = None
        self.coin_count = 0

    def setup_level(self):
        self.walls.clear()
        self.coins.clear()
        self.player = Player()
        
        maze = self.maze.generate_maze()
        
        player_start = (1, 1)
        maze[1][1] = 0
        end_position = (maze_width - 2, maze_height - 2)
        maze[maze_height - 2][maze_width - 2] = 0

        positive_coin_count = 0
        slow_coin_count = 0
        max_positive_coins = (maze_width * maze_height) // 20

        for y in range(maze_height):
            for x in range(maze_width):
                if maze[y][x] == 1:
                    self.walls.append(Wall((x * 16 + maze_offset_x, y * 16 + maze_offset_y)))
                elif (x, y) == player_start:
                    self.player.rect.topleft = (x * 16 + maze_offset_x, y * 16 + maze_offset_y)
                elif (x, y) == end_position:
                    self.end_rect = pygame.Rect(x * 16 + maze_offset_x, y * 16 + maze_offset_y, 16, 16)
                elif random.random() < 0.1 and positive_coin_count < max_positive_coins * 2:
                    if slow_coin_count < positive_coin_count // 3:
                        is_slow = random.random() < 0.25
                    else:
                        is_slow = False

                    if is_slow:
                        slow_coin_count += 1
                    else:
                        positive_coin_count += 1

                    self.coins.append(Coin((x * 16 + maze_offset_x, y * 16 + maze_offset_y), slow=is_slow))

        for x in range(maze_width):
            self.walls.append(Wall((x * 16 + maze_offset_x, maze_height * 16 + maze_offset_y)))
        for y in range(maze_height):
            self.walls.append(Wall((maze_width * 16 + maze_offset_x, y * 16 + maze_offset_y)))

        # Отладочный вывод
        internal_walls_count = sum(row.count(1) for row in maze)
        perimeter_walls_count = (maze_width * 2) + (maze_height * 2)
        total_walls_count = len(self.walls)
        print(f"Internal walls count: {internal_walls_count}")
        print(f"Perimeter walls count: {perimeter_walls_count}")
        print(f"Total walls count: {total_walls_count}")

if __name__ == "__main__":
    game = Game()
    game.run()
