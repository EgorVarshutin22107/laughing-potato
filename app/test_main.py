import pytest
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

# Тестирование инициализации игры
def test_game_initialization(game):
    assert game.coin_count == 0
    assert isinstance(game.maze, Maze)
    assert isinstance(game.player, Player)

@pytest.fixture
def game():
    game = Game()
    game.setup_level()
    return game

# def test_maze_setup(game):
#     # Test that walls are created correctly
#     assert len(game.walls) > 0, "Walls should be created"
    
#     # Ensure that the maze grid is generated
#     maze = game.maze.grid
#     assert len(maze) == game.maze.height, "Maze height should be correct"
#     assert len(maze[0]) == game.maze.width, "Maze width should be correct"

#     # Check that player starts at the correct position
#     assert game.player.rect.topleft == (1 * 16 + game.maze_offset_x, 1 * 16 + game.maze_offset_y), "Player start position should be correct"

#     # Check that end position is set correctly
#     end_x = (game.maze.width - 2) * 16 + game.maze_offset_x
#     end_y = (game.maze.height - 2) * 16 + game.maze_offset_y
#     assert game.end_rect.topleft == (end_x, end_y), "End position should be correct"

#     # Ensure coins are placed
#     assert len(game.coins) > 0, "Coins should be placed in the maze"

#     # Count the number of slow and normal coins
#     positive_coins = sum(1 for coin in game.coins if not coin.slow)
#     slow_coins = sum(1 for coin in game.coins if coin.slow)
    
#     assert positive_coins > 0, "There should be some positive coins"
#     assert slow_coins > 0, "There should be some slow coins"

#     # Ensure walls do not overlap with coins or player
#     for wall in game.walls:
#         assert not wall.rect.colliderect(game.player.rect), "Player should not overlap with walls"
#         assert not wall.rect.colliderect(game.end_rect), "End position should not overlap with walls"
#         for coin in game.coins:
#             assert not wall.rect.colliderect(coin.rect), "Coins should not overlap with walls"

#     # Ensure coins do not overlap with the player start position or end position
#     for coin in game.coins:
#         assert not coin.rect.colliderect(game.player.rect), "Coins should not overlap with player start position"
#         assert not coin.rect.colliderect(game.end_rect), "Coins should not overlap with end position"

def test_game_initialization():
    game = Game()
    assert game.screen.get_width() == 740
    assert game.screen.get_height() == 580
    assert game.font is not None
    assert game.player is not None
    assert game.maze is not None

if __name__ == "__main__":
    pytest.main()
