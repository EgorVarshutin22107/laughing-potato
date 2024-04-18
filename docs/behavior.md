# Поведенческие модели ПО
-------
## Алгоритм "Смена карты"

**Диаграмма состояний**:

```mermaid
stateDiagram
    [*] --> Generating
    Generating --> Generated: Карта сгенерирована
    Generated --> [*]
```
**Диаграмма последовательности**:

```mermaid
sequenceDiagram
    participant User
    participant Game
    User ->> Game: Запуск игры
    Game ->> Game: Генерация карты
    Note over Game: Случайный выбор карты
```
-------
## Алгоритм "Смена карты"

**Диаграмма состояний**

```mermaid
stateDiagram
    [*] --> Standing
    Standing --> Moving: Нажатие на стрелочку
    Moving --> Standing: Достижение новой клетки
    Moving --> Moving: Продолжение движения
```
-------
## Алгоритм "Нахождение скрытой комнаты":

**Диаграмма состояний**

```mermaid
stateDiagram
    [*] --> Searching
    Searching --> Found: Вхождение в дверную рамку
    Found --> [*]: Отображение сообщения

```