# �������� ������
----------------------------------------

## ���ᠭ�� ����७��� �������� �ਫ������

```mermaid
---
title: ��������� �ਪ��祭��
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

    note for Character "���ᮭ��, ����� �ࠢ��� ���짮��⥫�"
    note for LevelGenerator "������� ��砩�� �஢�� ���������� ��� ��᫥�������"
    note for GameEngine "�⢥砥� �� ���樠������ � �ࠢ����� ��஢� ����ᮬ"
    note for Timer "��᫥������ �६� ���� � �����頥� �� ����砭�� �६���"
    note for Rendering "�⢥砥� �� �⮡ࠦ���� ��஢��� ��� � ����䥩� ���짮��⥫�"
    note for InputManager "��ࠡ��뢠�� ���� ���짮��⥫� � ����������"
    note for GameStats "����ࠥ� � �⮡ࠦ��� ��������� ���ଠ�� � ⥪�饩 ���"
    note for MainApplicationClass "���樠������� �� ���������� �ਫ������ � �ࠢ��� �� ����������⢨��"
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
