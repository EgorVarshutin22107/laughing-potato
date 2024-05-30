import pytest
import pygame
from unittest.mock import patch, Mock
from main import Game, Player, Coin, Wall, Maze, UI

# -------------------- Фикстуры --------------------

# Фикстура для создания экземпляра игрока для тестирования
@pytest.fixture
def player():
    return Player()

# Фикстура для создания экземпляра монеты для тестирования
@pytest.fixture
def coin():
    return Coin((100, 100))

# Фикстура для создания экземпляра стены для тестирования
@pytest.fixture
def wall():
    return Wall((50, 50))

# Фикстура для создания экземпляра лабиринта для тестирования
@pytest.fixture
def maze():
    return Maze(5, 5)

# Фикстура для создания экземпляра игры для тестирования
@pytest.fixture
def game():
    game_instance = Game()
    game_instance.setup_level()
    return game_instance

@pytest.fixture
def ui():
    pygame.init()
    screen = pygame.display.set_mode((740, 580))
    font = pygame.font.SysFont(None, 36)
    return UI(screen, font)

@pytest.fixture
def game():
    pygame.init()
    game = Game()
    game.setup_level()
    yield game
    pygame.quit()

@pytest.fixture(scope="module")
def setup_pygame():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    font = pygame.font.SysFont(None, 36)
    ui = UI(screen, font)
    yield ui
    pygame.quit()

# -------------------- Тесты для класса Player --------------------

# Тестирование движения игрока без столкновения с препятствиями
def test_player_move_no_collision(player):
    # Перемещаем игрока на 5 пикселей вправо, без стен на пути
    player.move(5, 0, [])
    assert player.rect.x == 37
    assert player.rect.y == 32

# Тестирование движения игрока с столкновением со стеной
def test_player_move_with_collision(player, wall):
    # Устанавливаем начальную позицию игрока рядом со стеной
    wall.rect.topleft = (50, 32)  # Убедитесь, что стена находится на ожидаемой позиции
    player.rect.topleft = (34, 32)  # Начальная позиция игрока
    # Перемещаем игрока вправо на 16 пикселей, что вызывает столкновение со стеной
    player.move(16, 0, [wall])
    assert player.rect.right == wall.rect.left  # Проверяем корректное столкновение

# -------------------- Тесты для класса Coin --------------------

# Тестирование позиции монеты и её свойств
def test_coin_position(coin):
    assert coin.rect.topleft == (100, 100)
    assert not coin.slow

# Тестирование создания монеты с замедляющим эффектом
def test_slow_coin():
    slow_coin = Coin((200, 200), slow=True)
    assert slow_coin.slow

# -------------------- Тесты для класса Wall --------------------

# Тестирование позиции стены
def test_wall_position(wall):
    assert wall.rect.topleft == (50, 50)

# -------------------- Тесты для класса Maze --------------------

# Тестирование проверки размера лабиринта
def test_maze_size():
    with pytest.raises(ValueError):
        Maze(2, 2)  # Создание слишком маленького лабиринта должно вызывать ошибку

# Тестирование генерации лабиринта и убедиться, что проходы прорезаны
def test_generate_maze(maze):
    maze_data = maze.generate_maze()
    assert len(maze_data) == 5
    assert len(maze_data[0]) == 5

    # Убедиться, что есть открытые пространства в лабиринте
    open_spaces = sum(row.count(0) for row in maze_data)
    assert open_spaces > 0

# -------------------- Тесты для класса Game --------------------

# Константы, используемые в игре
MAZE_WIDTH = 40
MAZE_HEIGHT = 30
MAZE_OFFSET_X = 0
MAZE_OFFSET_Y = 50

# Тестирование инициализации игры
def test_game_initialization(game):
    assert isinstance(game, Game)
    assert isinstance(game.player, Player)
    assert isinstance(game.maze, Maze)

# Тестирование настройки уровня
def test_setup_level(game):
    game.setup_level()
    assert len(game.walls) > 0
    assert len(game.coins) > 0
    assert isinstance(game.end_rect, pygame.Rect)
    assert any(isinstance(coin, Coin) for coin in game.coins)
    
    # Убедиться, что игрок размещен правильно
    player_start_position = (1 * 16 + MAZE_OFFSET_X, 1 * 16 + MAZE_OFFSET_Y)
    assert game.player.rect.topleft == player_start_position
    
    # Убедиться, что конечная позиция установлена
    end_position = (MAZE_WIDTH - 2, MAZE_HEIGHT - 2)
    expected_end_rect = pygame.Rect(end_position[0] * 16 + MAZE_OFFSET_X, end_position[1] * 16 + MAZE_OFFSET_Y, 16, 16)
    assert game.end_rect == expected_end_rect

# Тестирование движения игрока
def test_player_movement(game):
    game.setup_level()
    initial_position = game.player.rect.topleft

    # Тест движения вправо
    right_possible = not any(wall.rect.topleft == (initial_position[0] + 16, initial_position[1]) for wall in game.walls)
    game.player.move(16, 0, game.walls)
    new_position = (initial_position[0] + 16, initial_position[1]) if right_possible else initial_position
    assert game.player.rect.topleft == new_position

    # Тест движения влево обратно к начальной позиции
    left_possible = not any(wall.rect.topleft == (new_position[0] - 16, new_position[1]) for wall in game.walls)
    game.player.move(-16, 0, game.walls)
    expected_position = initial_position if left_possible else new_position
    assert game.player.rect.topleft == expected_position

    # Тест движения вниз
    down_possible = not any(wall.rect.topleft == (initial_position[0], initial_position[1] + 16) for wall in game.walls)
    game.player.move(0, 16, game.walls)
    new_position = (initial_position[0], initial_position[1] + 16) if down_possible else initial_position
    assert game.player.rect.topleft == new_position

    # Тест движения вверх обратно к начальной позиции
    up_possible = not any(wall.rect.topleft == (new_position[0], new_position[1] - 16) for wall in game.walls)
    game.player.move(0, -16, game.walls)
    expected_position = initial_position if up_possible else new_position
    assert game.player.rect.topleft == expected_position

# Тестирование столкновения с монетами
def test_coin_collision(game):
    game.setup_level()
    initial_coin_count = len(game.coins)
    for coin in game.coins[:]:
        game.player.rect.topleft = coin.rect.topleft
        game.coins.remove(coin)
    assert len(game.coins) == 0

# Тестирование условия окончания игры
def test_end_game_condition(game):
    game.setup_level()
    game.player.rect.topleft = game.end_rect.topleft
    assert game.player.rect.colliderect(game.end_rect)

# -------------------- Тесты для функции класса UI --------------------------
# def test_show_statistics(setup_pygame):
#     ui = setup_pygame
#     coin_count = 10
#     elapsed_time = 123.45
#     ui.show_statistics(coin_count, elapsed_time)
#     # Проверить отрисовку на экране невозможно, но можно проверить отсутствие ошибок

# def test_show_exit_confirmation(setup_pygame):
#     ui = setup_pygame
#     pygame.event.post(pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'button': 1, 'pos': (ui.screen.get_width() // 2 - 60, ui.screen.get_height() // 2 + 20)}))
#     assert ui.show_exit_confirmation() is True

#     pygame.event.post(pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'button': 1, 'pos': (ui.screen.get_width() // 2 + 60, ui.screen.get_height() // 2 + 20)}))
#     assert ui.show_exit_confirmation() is False
    
# def test_show_main_menu_start(setup_pygame):
#     ui = setup_pygame
#     pygame.event.post(pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'button': 1, 'pos': (ui.screen.get_width() // 2, ui.screen.get_height() // 2 - 20)}))
#     assert ui.show_main_menu() == "start"

# def test_show_main_menu_exit(setup_pygame):
#     ui = setup_pygame
#     with pytest.raises(SystemExit):
#         pygame.event.post(pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'button': 1, 'pos': (ui.screen.get_width() // 2, ui.screen.get_height() // 2 + 40)}))
#         ui.show_main_menu()

# -------------------- Тесты для функции run класса Game --------------------



if __name__ == "__main__":
    pytest.main()
