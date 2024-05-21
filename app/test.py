import pytest
import pygame
import time
from main import Player, Coin, Wall, Maze, Game

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

# Тестирование движения игрока без столкновения
def test_player_move_no_collision(player):
    player.move(5, 0, [])
    assert player.rect.x == 37
    assert player.rect.y == 32

# Тестирование движения игрока с столкновением со стеной
def test_player_move_with_collision(player, wall):
    player.move(18, 0, [wall])
    assert player.rect.right == wall.rect.left

# Тестирование позиции монеты и эффекта замедления
def test_coin_position(coin):
    assert coin.rect.topleft == (100, 100)
    assert not coin.slow

# Тестирование создания монеты с замедлением
def test_slow_coin():
    slow_coin = Coin((200, 200), slow=True)
    assert slow_coin.slow

# Тестирование позиции стены
def test_wall_position(wall):
    assert wall.rect.topleft == (50, 50)

# Тестирование проверки размера лабиринта
def test_maze_size():
    with pytest.raises(ValueError):
        Maze(2, 2)

# Тестирование генерации лабиринта и убедиться, что проходы прорезаны
def test_generate_maze(maze):
    maze_data = maze.generate_maze()
    assert len(maze_data) == 5
    assert len(maze_data[0]) == 5

    # Убедиться, что есть открытые пространства в лабиринте
    open_spaces = sum(row.count(0) for row in maze_data)
    assert open_spaces > 0

# Тестирование инициализации игры
def test_game_initialization(game):
    assert game.coin_count == 0
    assert isinstance(game.maze, Maze)
    assert isinstance(game.player, Player)

# Тестирование настройки уровня
def test_setup_level(game):
    game.setup_level()
    assert len(game.walls) == game.maze.width + game.maze.height + 4
    assert isinstance(game.end_rect, pygame.Rect)

# Тестирование сбора монет игроком
def test_coin_collection(game):
    game.setup_level()
    initial_coin_count = len(game.coins)
    game.player.rect.topleft = game.coins[0].rect.topleft
    game.run()
    assert len(game.coins) < initial_coin_count
    assert game.coin_count >= 1

# Тестирование временного ограничения игры
def test_time_limit(game):
    game.setup_level()
    game.run()
    assert time.time() - game.start_time <= game.max_time
