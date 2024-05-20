import pytest
import pygame

from main import Player, Coin, Wall, Maze

# Тесты для класса Player
def test_player_initialization():
    player = Player()
    assert player.rect == pygame.Rect(32, 32, 16, 16)
    assert player.speed == 2
    assert player.slowed_until == 0

def test_player_move():
    player = Player()
    wall = Wall((50, 32))
    walls = [wall]

    player.move(16, 0, walls)
    assert player.rect.topleft == (32, 32)  # Столкновение со стеной должно остановить игрока

    player.move(0, 16, walls)
    assert player.rect.topleft == (32, 48)  # Движение вниз без столкновения

# Тесты для класса Coin
def test_coin_initialization():
    coin = Coin((100, 100), slow=True)
    assert coin.rect == pygame.Rect(100, 100, 10, 10)
    assert coin.slow is True

# Тесты для класса Wall
def test_wall_initialization():
    wall = Wall((200, 200))
    assert wall.rect == pygame.Rect(200, 200, 16, 16)

# Тесты для класса Maze
def test_maze_initialization():
    with pytest.raises(ValueError):
        Maze(0, 0)

    maze = Maze(10, 10)
    assert maze.width == 10
    assert maze.height == 10
    assert maze.grid is not None

def test_maze_generation():
    maze = Maze(10, 10)
    grid = maze.generate_maze()
    assert len(grid) == 10
    assert all(len(row) == 10 for row in grid)
    assert grid[1][1] == 0  # Начальная точка свободна
