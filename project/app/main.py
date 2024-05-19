import os
import sys
import random
import pygame
import time

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
        self.width = width
        self.height = height
        self.grid = self.generate_maze()

    def generate_maze(self):
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

    def show_statistics(self, coin_count, elapsed_time):
        self.screen.fill((0, 0, 0))
        stats_text = self.font.render(f"Всего собрано монет: {coin_count}", True, (255, 255, 255))
        time_text = self.font.render(f"Время: {elapsed_time:.2f} секунд", True, (255, 255, 255))
        self.screen.blit(stats_text, (screen_width // 2 - stats_text.get_width() // 2, screen_height // 2 - stats_text.get_height() // 2 - 20))
        self.screen.blit(time_text, (screen_width // 2 - time_text.get_width() // 2, screen_height // 2 - time_text.get_height() // 2 + 20))
        pygame.display.flip()
        pygame.time.wait(3000)

    def show_exit_confirmation(self):
        self.screen.fill((0, 0, 0))
        confirm_text = self.font.render("Вы действительно хотите выйти?", True, (255, 255, 255))
        yes_text = self.font.render("Да", True, (0, 255, 0))
        no_text = self.font.render("Остаться", True, (255, 0, 0))
        self.screen.blit(confirm_text, (screen_width // 2 - confirm_text.get_width() // 2, screen_height // 2 - confirm_text.get_height() // 2 - 40))
        yes_rect = yes_text.get_rect(center=(screen_width // 2 - 60, screen_height // 2 + 20))
        no_rect = no_text.get_rect(center=(screen_width // 2 + 60, screen_height // 2 + 20))
        self.screen.blit(yes_text, yes_rect)
        self.screen.blit(no_text, no_rect)
        pygame.display.flip()

        while True:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    return False
                if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                    return False
                if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                    if yes_rect.collidepoint(e.pos):
                        return True
                    if no_rect.collidepoint(e.pos):
                        return False

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
                    sys.exit()
                if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                    if start_rect.collidepoint(e.pos):
                        return "start"
                    if exit_rect.collidepoint(e.pos):
                        pygame.quit()
                        sys.exit()

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

        global walls, player, coins, end_rect
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

    def run(self):
        while True:
            menu_choice = self.ui.show_main_menu()
            if menu_choice != "start":
                pygame.quit()
                sys.exit()

            self.setup_level()
            
            start_time = time.time()
            max_time = 120
            running = True

            while running:
                self.clock.tick(60)
                
                for e in pygame.event.get():
                    if e.type == pygame.QUIT:
                        running = False
                    if e.type == pygame.KEYDOWN and e.key == pygame.K_BACKQUOTE:
                        if self.ui.show_exit_confirmation():
                            running = False

                key = pygame.key.get_pressed()
                current_time = time.time()
                speed = self.player.speed // 2 if self.player.slowed_until > current_time else self.player.speed

                if key[pygame.K_LEFT]:
                    self.player.move(-speed, 0, self.walls)
                if key[pygame.K_RIGHT]:
                    self.player.move(speed, 0, self.walls)
                if key[pygame.K_UP]:
                    self.player.move(0, -speed, self.walls)
                if key[pygame.K_DOWN]:
                    self.player.move(0, speed, self.walls)

                for coin in self.coins[:]:
                    if self.player.rect.colliderect(coin.rect):
                        self.coins.remove(coin)
                        if coin.slow:
                            self.player.slowed_until = current_time + 5
                        else:
                            self.coin_count += 1

                if self.player.rect.colliderect(self.end_rect):
                    elapsed_time = time.time() - start_time
                    self.ui.show_statistics(self.coin_count, elapsed_time)
                    break

                elapsed_time = time.time() - start_time
                if elapsed_time > max_time:
                    self.ui.show_statistics(self.coin_count, elapsed_time)
                    break

                self.screen.fill((0, 0, 0))
                for wall in self.walls:
                    pygame.draw.rect(self.screen, (255, 255, 255), wall.rect)
                for coin in self.coins:
                    color = (128, 0, 128) if coin.slow else (255, 255, 0)
                    pygame.draw.ellipse(self.screen, color, coin.rect)
                pygame.draw.rect(self.screen, (255, 0, 0), self.end_rect)
                pygame.draw.rect(self.screen, (255, 200, 0), self.player.rect)

                coin_text = self.font.render(f"Монеты: {self.coin_count}", True, (255, 255, 255))
                self.screen.blit(coin_text, (10, 10))

                timer_text = self.font.render(f"Время: {elapsed_time:.2f} с", True, (255, 255, 255))
                self.screen.blit(timer_text, (screen_width - timer_text.get_width() - 10, 10))

                pygame.display.flip()

if __name__ == "__main__":
    game = Game()
    game.run()
