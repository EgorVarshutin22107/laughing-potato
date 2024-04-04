# Структурные модели
----------------------------------------

## Описание внутренней структуры приложения

```mermaid
---
title: Подземелье Приключений
---
classDiagram 
    class GameEngine {
        + initializeGame()
        + startGame()
        + update()
        + render()
    }
    class LevelGenerator {
        + generateLevel()
        + placeCoins()
        + placeSecretRooms()
    }
    class Character {
        + move()
        + collectCoin()
        + detectSecretRoom()
    }
    class Timer {
        + startTimer()
        + stopTimer()
        + checkTimeLimit()
    }
    class Rendering {
        + drawLevel()
        + drawCharacter()
        + drawUI()
    }
    class InputManager {
        + handleKeyPress()
    }
    class GameStats {
        + updateCoinCount()
        + displayStats()
    }
    class MainApplicationClass {
        + initialize()
        + run()
    }

    GameEngine --|> LevelGenerator
    GameEngine --|> Character
    GameEngine --|> Rendering
    GameEngine --|> Timer
    LevelGenerator --|> Rendering
    Character --|> InputManager
    Character --|> GameStats
    MainApplicationClass --|> GameEngine
    MainApplicationClass --|> InputManager

```
