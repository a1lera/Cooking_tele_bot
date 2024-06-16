# Телеграмм-бот для поиска рецептов

Телеграмм-бот для поиска рецепта по названиям ингридиента на python. 


## Используемые библиотеки
- telebot
- pandas
- ast

## Используемый датасет
[147к кулинарных рецептов](https://www.kaggle.com/datasets/rogozinushka/povarenok-recipes) - содержит более 147 тыс рецептов, где указаны название блюда, его ингридиенты и ссылка для поэтапного приготовления.
  
## Что входит в основу?
Основой послужило BK-дерево. Вообще BK-Tree — это структура данных, используемая для эффективного определения слов, близких к целевому слову с точки зрения расстояния Левенштейна. Расстояние Левенштейна - минимальное количество односимвольных операций (а именно вставки, удаления, замены), необходимых для превращения одной последовательности символов в другую. В данном случае модифицированное BK-дерево - это структура данных, которая позволяет осуществлять эффективный поиск ближайших соседей путем организации узлов таким образом, чтобы свести к минимуму количество узлов, подлежащих поиску.

## Как это всё работает

Используется 2 класса: 
- main
- bot

### Рассмотрим класс main

Константы и глобальные переменные:

- MAXN: максимальное количество узлов в дереве (в данном случае 144742)
- TOL: допустимый порог для рассмотрения двух списков ингредиентов как похожих (в данном случае 1)
- ptr: глобальный указатель для отслеживания следующего доступного индекса узла в дереве
  
Класс узла

- Узел: класс, представляющий узел в BK-дереве с атрибутами:
  - keys: список ключей ингредиентов (например, ["яблоко", "банан"])
  - recipe: соответствующая информация о рецепте
  - next: массив индексов дочерних узлов (изначально заданный равным 0)
 
Инициализация дерева

  - tree: массив объектов Node, инициализированный элементами MAXN

Далее идут функции добавления ингридиентов в дерево, рассчёта расстояния на основании схожести ингридиентов и нахождения рецепта по введенным данным.

Функция "add": 
- add(root, curr): добавляет новый узел curr в дерево, начиная с корневого узла
  - Если корневой узел пуст, установите для его ключей и атрибутов рецепта значения, соответствующие атрибутам curr
  - Вычислите расстояние редактирования между ключами корневого узла и ключами curr, используя функцию edit_distance
  - Если расстояние редактирования находится в пределах допустимого порога, добавьте curr в качестве дочернего узла root
  - В противном случае рекурсивно вызовите add для дочернего узла с вычисленным индексом расстояния редактирования

Функция "get_similar_recipies":
- get_similar_recipies(root, s, threshold=TOL): выполняет поиск рецептов, аналогичных входным данным (список ингредиентов), начиная с корневого узла
Если корневой узел пуст, возвращает пустой список
  - Рассчитайте расстояние редактирования между ключами корневого узла и s с помощью функции edit_distance
  - Если расстояние редактирования находится в пределах допустимого порога, добавьте рецепт корневого узла в список результатов
  - Рекурсивно вызывайте get_similar_recipies для дочерних узлов в пределах диапазона изменения расстояния и добавляйте их результаты в список

Функция "edit_distance":
- edit_distance(a, b): вычисляет расстояние редактирования между двумя списками ингредиентов a и b с помощью динамического программирования
  - Инициализирует двумерный массив dp для хранения расстояний редактирования между префиксами a и b
  - Заполняет массив dp, используя рекуррентное соотношение:
dp[i][j] = min(dp[i-1][j] + 1, dp[i][j-1] + 1, dp[i-1][j-1] + 1), если a[i-1]!= b[j-1]
dp[i][j] = dp[i-1][j-1] в противном случае
  - Возвращает расстояние редактирования между целыми списками a и b

### Рассмотрим класс bot

- Инициализируется Telegram-бота:

- Создаётся новый экземпляр TeleBot с помощью вашего токена бота

- Инициализируется BK-дерево:
  - Создаётся новый экземпляр узла (RT) для корня BK-дерева

- Загружаются данные из CSV-файла:
  - Преобразуется файл "recipes-recipes.csv" в базу данных pandas
  - Удаляются строки с пропущенными значениями в столбце "ингредиенты"
  - Выполняется итерация по базе данных и создайте список ингредиентов и рецептов
  - Предварительно обработываются ингредиенты, преобразовав их названия в нижний регистр и добавив их в BK-дерево с помощью функции добавления
 
- Обрабатываюся пользовательские команды:
  - Определяется обработчик команды "/start", который отправляет приветственное сообщение пользователю

- Обрабатываюся вводимые пользователем данные:
  - Определяется обработчик текстовых сообщений, который обрабатывает вводимые пользователем данные в виде списка ингредиентов
  - Предварительно обрабатываются ингредиенты, преобразовав их в нижний регистр, отсортировав и разделив запятыми
  - Находятся похожие рецепты с помощью функции get_similar_recipies
  - Отправляется пользователю 4 наиболее подходящих рецепта в виде списка сообщений
 
- Запуск цикла опроса бота:
  - Запускается цикл опроса бота для прослушивания входящих сообщений

