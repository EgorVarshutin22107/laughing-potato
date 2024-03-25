# Варшутин Егор группа 22107
--------------------------------------------------


## Первая лабораторная работа

Название игры: Подземелье Приключений.

Описание игры: Подземелье Приключений - это простая Roguelike игра, где игрок управляет персонажем, исследующим случайно сгенерированные подземелья и собиарет монетки.

Цель игры: Собрать 20 монеток.

Функциональные возможности:

1. Пользователь может создать нового персонажа:
   - Пользователь запускает игру и выбирает опцию "Запустить игру", "Выйти из игры" (пользователь должен ввести 1 - если он хочет запустить игру или 2 - если хочет выйти из игры и нажать клавишу ENTER).
   - Пользователь вводит имя персонажа (если игрок выбрал 1 вариант) и для продолжения нажимает клавишу ENTER.

2. Пользователь может перемещаться по подземелью:
   - Пользователь использует клавиши управления (стрелки).

3. Пользователь может собирать монетки:
   - Пользователь подходит к монетке и по нажатию клавишы "R" подбирает ее.
   - Приложение отображает сообщение о том, что его количество монеток увеличилось.

4. Пользователь может обнаруживать секретные комнаты:
   - При исследовании подземелья персонаж может обнаружить скрытую дверь.
   - Приложение отображает сообщение о обнаружении секретной комнаты и позволяет персонажу войти в неё.

5. Пользователь может завершить игру:
   - После достижения финального количества монеток или при поражении пользователь может завершить игру.
   - Так же в игре есть ограничение сеанса. Если игрок не успевает за 10 минут собрать 10 монеток - LOSE.
   - Пользователь может сам выйти из игры в любой момент, нажав кнопку "ё" на клавитауре.
   - В консоль выводится статистика игры. (время нахождения в игре и кол-во монеток).

Ключевые алгоритмы:

1. Смена карты
   - У нас будет 3 варианта карт. При запуске игры генерируется рандомно одна из них.

2. Передвижение по карте
   - При нажатии на стрелочки пользователь может перемещаться по лабиринту.
   - Двигаться он может вверх, вниз, влево и вправо.

2. Нахождение скрытой комнаты и вывод информации об этом.
   - Как пользователь пройдет в "дверную рамку" скрытой комнаты, у пользователя появится надпись о том, что он ее нашел.

3. Подбор монетки
   - Пользователь обнаруживает монетку и если он находится в радиусе действия подбора монетки, то при нажатии клавиши 'R' он ее подберет и счетчик монет увеличится. Если в радиусе действия подбора монеток не обнаружено, пользователю высветится сообщение "Монеток нет..."

4. Таймер завершения игры 
   - Работает таймер, который стоит на ограничении в 10 минут. При окончании сеанса по времени у пользователя выводится надпись "YOU LOSE" и игра завершается с выводом статистики в консоль.

5. Вывод статистики игры пользователя
   - Во время сеанса будет работать счетчик монеток и таймер. После завершения сеанса результаты этих параметров выведутся в консоль.
--------------------------------------------------


## Третья лабораторная работа

* [Описание функциональных моделей](docs/functions.md)
