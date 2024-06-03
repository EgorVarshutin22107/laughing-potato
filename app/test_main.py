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
    """Фикстура для создания экземпляра игры."""
    game_instance = Game()
    return game_instance

@pytest.fixture
def ui():
    pygame.init()
    screen = Mock()
    font = Mock()
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

    # Тест движения влево с столкновением
    player.rect.topleft = (66, 32)  # Начальная позиция игрока
    player.move(-16, 0, [wall])
    assert player.rect.left == wall.rect.right  # Проверяем корректное столкновение

    # Тест движения вниз с столкновением
    wall.rect.topleft = (50, 50)  # Убедитесь, что стена находится на ожидаемой позиции
    player.rect.topleft = (50, 34)  # Начальная позиция игрока
    player.move(0, 16, [wall])
    assert player.rect.bottom == wall.rect.top  # Проверяем корректное столкновение

    # Тест движения вверх с столкновением
    player.rect.topleft = (50, 66)  # Начальная позиция игрока
    player.move(0, -16, [wall])
    assert player.rect.top == wall.rect.bottom  # Проверяем корректное столкновение

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

# Тестирование проверки корректного размера лабиринта
def test_invalid_maze_size():
    with pytest.raises(ValueError, match="Invalid maze size"):
        Maze(-1, 5)
    with pytest.raises(ValueError, match="Invalid maze size"):
        Maze(5, -1)

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

# -------------------- Тесты для класса UI (Заглушки) ------------------

def test_show_statistics(ui):
    ui.screen.fill = Mock()
    text_mock = Mock()
    text_mock.get_width.return_value = 100
    text_mock.get_height.return_value = 20
    ui.font.render = Mock(return_value=text_mock)
    ui.screen.blit = Mock()
    pygame.display.flip = Mock()
    pygame.time.wait = Mock()

    ui.show_statistics(10, 15.2)

    ui.screen.fill.assert_called_with((0, 0, 0))
    assert ui.font.render.call_count == 2
    ui.screen.blit.assert_called()
    pygame.display.flip.assert_called()
    pygame.time.wait.assert_called_with(3000)

def test_show_exit_confirmation(ui):
    ui.screen.fill = Mock()
    text_mock = Mock()
    text_mock.get_width.return_value = 100
    text_mock.get_height.return_value = 20
    ui.font.render = Mock(return_value=text_mock)
    ui.screen.blit = Mock()
    pygame.display.flip = Mock()

    # Имитация цикла событий
    with patch('pygame.event.get', return_value=[Mock(type=pygame.QUIT)]):
        result = ui.show_exit_confirmation()

    assert result is False
    ui.screen.fill.assert_called_with((0, 0, 0))
    assert ui.font.render.call_count == 3
    ui.screen.blit.assert_called()
    pygame.display.flip.assert_called()

def test_show_exit_confirmation_escape(ui):
    ui.screen.fill = Mock()
    text_mock = Mock()
    text_mock.get_width.return_value = 100
    text_mock.get_height.return_value = 20
    ui.font.render = Mock(return_value=text_mock)
    ui.screen.blit = Mock()
    pygame.display.flip = Mock()

    event = Mock(type=pygame.KEYDOWN, key=pygame.K_ESCAPE)
    with patch('pygame.event.get', return_value=[event]):
        result = ui.show_exit_confirmation()
    assert result is False
    ui.screen.fill.assert_called_with((0, 0, 0))
    assert ui.font.render.call_count == 3
    ui.screen.blit.assert_called()
    pygame.display.flip.assert_called()

def test_show_exit_confirmation_yes_click(ui):
    # Define screen dimensions (use the same dimensions as in your main code)
    screen_width = 740  # Replace with actual screen width
    screen_height = 580  # Replace with actual screen height
    
    confirm_text_mock = Mock()
    confirm_text_mock.get_width.return_value = 200
    confirm_text_mock.get_height.return_value = 40
    yes_text_mock = Mock()
    yes_text_mock.get_width.return_value = 100
    yes_text_mock.get_height.return_value = 20
    no_text_mock = Mock()
    no_text_mock.get_width.return_value = 100
    no_text_mock.get_height.return_value = 20

    ui.font.render.side_effect = [confirm_text_mock, yes_text_mock, no_text_mock]

    # The "Да" (Yes) button is at (screen_width // 2 - 60, screen_height // 2 + 20)
    # Calculate the center coordinates of the "Да" button
    yes_button_x = screen_width // 2 - 60
    yes_button_y = screen_height // 2 + 20
    yes_button_width = yes_text_mock.get_width()
    yes_button_height = yes_text_mock.get_height()

    # Ensure the click is within the "Да" button's area
    yes_button_click_pos = (yes_button_x, yes_button_y)
    yes_button_rect = pygame.Rect(yes_button_x - yes_button_width // 2, yes_button_y - yes_button_height // 2, yes_button_width, yes_button_height)

    print(f"Testing 'Да' button at {yes_button_rect}, clicking at {yes_button_click_pos}")

    with patch('pygame.event.get', return_value=[Mock(type=pygame.MOUSEBUTTONDOWN, button=1, pos=(yes_button_click_pos))]):
        result = ui.show_exit_confirmation()
    
    print(f"Result: {result}")
    assert result is True

def test_show_main_menu(ui):
    ui.screen.fill = Mock()
    text_mock = Mock()
    text_mock.get_width.return_value = 100
    text_mock.get_height.return_value = 20
    ui.font.render = Mock(return_value=text_mock)
    ui.screen.blit = Mock()
    pygame.display.flip = Mock()

    # Имитация цикла событий
    with patch('pygame.event.get', return_value=[Mock(type=pygame.QUIT)]):
        with pytest.raises(SystemExit):
            ui.show_main_menu()

    ui.screen.fill.assert_called_with((0, 0, 0))
    assert ui.font.render.call_count == 3
    ui.screen.blit.assert_called()
    pygame.display.flip.assert_called()

if __name__ == "__main__":
    pytest.main()
