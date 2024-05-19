import pytest
import pygame
from main import Player, Coin, Wall, Maze, Game

@pytest.fixture
def player():
    return Player()

@pytest.fixture
def walls():
    return [Wall((0, 0)), Wall((16, 16)), Wall((32, 32))]

@pytest.fixture
def coins():
    return [Coin((70, 70)), Coin((100, 100), slow=True)]

@pytest.fixture
def maze():
    return Maze(40, 30)

@pytest.fixture
def game():
    return Game()

def test_player_initial_position(player):
    assert player.rect.topleft == (32, 32)
    assert player.speed == 2
    assert player.slowed_until == 0

def test_player_initial_position_negative(player):
    assert player.rect.topleft != (0, 0)
    assert player.speed > 0
    assert player.slowed_until == 0

def test_player_move_no_collision(player, walls):
    player.move(10, 0, walls)
    assert player.rect.x == 42
    player.move(0, 10, walls)
    assert player.rect.y == 42

def test_player_move_negative_values(player, walls):
    player.move(-10, 0, walls)
    assert player.rect.x == 22
    player.move(0, -10, walls)
    assert player.rect.y == 22

def test_coin_collection(player, coins):
    player.rect.topleft = (70, 70)
    coin = coins[0]
    assert player.rect.colliderect(coin.rect)
    coins.remove(coin)
    assert len(coins) == 1

def test_coin_collection_no_coin(player, coins):
    initial_coin_count = len(coins)
    player.rect.topleft = (80, 80)
    for coin in coins[:]:
        if player.rect.colliderect(coin.rect):
            coins.remove(coin)
    assert len(coins) == initial_coin_count

def test_maze_generation(maze):
    grid = maze.generate_maze()
    assert grid[1][1] == 0
    assert grid[maze.height - 2][maze.width - 2] == 0

def test_maze_generation_invalid_size():
    with pytest.raises(ValueError):
        maze = Maze(-1, 10)
        maze.generate_maze()
    with pytest.raises(ValueError):
        maze = Maze(10, -1)
        maze.generate_maze()
    with pytest.raises(ValueError):
        maze = Maze(2, 2)
        maze.generate_maze()

def test_game_setup(game):
    game.setup_level()
    assert game.player.rect.topleft == (16 + 0, 16 + 50)
    assert game.end_rect.topleft == (640 + 0, 480 + 50)

def test_game_setup_invalid():
    game = Game()
    with pytest.raises(ValueError):
        game.maze = Maze(-1, 10)
        game.setup_level()
    with pytest.raises(ValueError):
        game.maze = Maze(10, -1)
        game.setup_level()
