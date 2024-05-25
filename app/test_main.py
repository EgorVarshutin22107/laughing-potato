import pytest
import pygame
from io import *
from main import Game, Player, Coin, Wall, Maze

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
    return Game()

@pytest.fixture
def game():
    game = Game()
    game.setup_level()
    return game

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

# Тестирование позиции монеты и её свойств
def test_coin_position(coin):
    assert coin.rect.topleft == (100, 100)
    assert not coin.slow

# Тестирование создания монеты с замедляющим эффектом
def test_slow_coin():
    slow_coin = Coin((200, 200), slow=True)
    assert slow_coin.slow

# Тестирование позиции стены
def test_wall_position(wall):
    assert wall.rect.topleft == (50, 50)

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

# Constants used in the game
MAZE_WIDTH = 40
MAZE_HEIGHT = 30
MAZE_OFFSET_X = 0
MAZE_OFFSET_Y = 50

@pytest.fixture
def game():
    game_instance = Game()
    game_instance.setup_level()  # Setup the level initially
    return game_instance

def test_game_initialization(game):
    assert isinstance(game, Game)
    assert isinstance(game.player, Player)
    assert isinstance(game.maze, Maze)

def test_setup_level(game):
    game.setup_level()
    assert len(game.walls) > 0
    assert len(game.coins) > 0
    assert isinstance(game.end_rect, pygame.Rect)
    assert any(isinstance(coin, Coin) for coin in game.coins)
    
    # Ensure player is placed correctly
    player_start_position = (1 * 16 + MAZE_OFFSET_X, 1 * 16 + MAZE_OFFSET_Y)
    assert game.player.rect.topleft == player_start_position
    
    # Ensure end position is set
    end_position = (MAZE_WIDTH - 2, MAZE_HEIGHT - 2)
    expected_end_rect = pygame.Rect(end_position[0] * 16 + MAZE_OFFSET_X, end_position[1] * 16 + MAZE_OFFSET_Y, 16, 16)
    assert game.end_rect == expected_end_rect

# def test_internal_wall_count(game, capsys):
#     game.setup_level()
#     captured = capsys.readouterr()
#     internal_walls_count = sum(row.count(1) for row in game.maze.grid)
#     perimeter_walls_count = (MAZE_WIDTH * 2) + (MAZE_HEIGHT * 2)
#     total_walls_count = len(game.walls)
#     expected_internal_walls_count = 600  # The expected count from the output
#     tolerance = 10  # Allowable tolerance
#     assert abs(internal_walls_count - expected_internal_walls_count) <= tolerance, \
#         f"Internal walls count: {internal_walls_count} is not within tolerance of {expected_internal_walls_count}"
#     assert f"Perimeter walls count: {perimeter_walls_count}" in captured.out
#     assert f"Total walls count: {total_walls_count}" in captured.out

def test_player_movement(game):
    game.setup_level()
    initial_position = game.player.rect.topleft
    print(f"Initial position: {initial_position}")

    # Test moving right
    right_possible = not any(wall.rect.topleft == (initial_position[0] + 16, initial_position[1]) for wall in game.walls)
    game.player.move(16, 0, game.walls)
    new_position = (initial_position[0] + 16, initial_position[1]) if right_possible else initial_position
    print(f"Position after moving right: {game.player.rect.topleft}")
    assert game.player.rect.topleft == new_position, \
        f"Expected position: {new_position}, but got: {game.player.rect.topleft}"

    # Test moving left back to initial position
    left_possible = not any(wall.rect.topleft == (new_position[0] - 16, new_position[1]) for wall in game.walls)
    game.player.move(-16, 0, game.walls)
    expected_position = initial_position if left_possible else new_position
    print(f"Position after moving left: {game.player.rect.topleft}")
    assert game.player.rect.topleft == expected_position, \
        f"Expected position: {expected_position}, but got: {game.player.rect.topleft}"

    # Test moving down
    down_possible = not any(wall.rect.topleft == (initial_position[0], initial_position[1] + 16) for wall in game.walls)
    game.player.move(0, 16, game.walls)
    new_position = (initial_position[0], initial_position[1] + 16) if down_possible else initial_position
    print(f"Position after moving down: {game.player.rect.topleft}")
    assert game.player.rect.topleft == new_position, \
        f"Expected position: {new_position}, but got: {game.player.rect.topleft}"

    # Test moving up back to initial position
    up_possible = not any(wall.rect.topleft == (new_position[0], new_position[1] - 16) for wall in game.walls)
    game.player.move(0, -16, game.walls)
    expected_position = initial_position if up_possible else new_position
    print(f"Position after moving up: {game.player.rect.topleft}")
    assert game.player.rect.topleft == expected_position, \
        f"Expected position: {expected_position}, but got: {game.player.rect.topleft}"

def test_coin_collision(game):
    game.setup_level()
    initial_coin_count = len(game.coins)
    for coin in game.coins[:]:
        game.player.rect.topleft = coin.rect.topleft
        game.coins.remove(coin)
    assert len(game.coins) == 0

def test_end_game_condition(game):
    game.setup_level()
    game.player.rect.topleft = game.end_rect.topleft
    assert game.player.rect.colliderect(game.end_rect)

if __name__ == "__main__":
    pytest.main()