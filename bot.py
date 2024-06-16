import telebot
from main import *
import pandas as pd
import ast


bot = telebot.TeleBot('ваш токен')

RT = Node()


if __name__ == "__main__":
    # Загружаем данные из CSV-файла
    results = pd.read_csv('recipes - recipes.csv')
    keys = []
    recipes = []

    results = results.dropna(subset=['ingredients'])  # удаляем строки с пустыми значениями в столбце 'ingredients'

    for i in range(len(results)):
        try:
            ingredients_str = results['ingredients'][i]
        except KeyError:
            print(f"Error: Index {i} does not exist in the DataFrame")
            continue
        ingredients = ast.literal_eval(ingredients_str)
        ingredients_lower = {k.lower(): v for k, v in ingredients.items()}  # преобразуем название ингридиентов в нижний регистр
        keys.append(list(ingredients_lower.keys()))
        recipes.append((results['url'][i], results['name'][i]))

    sz = len(keys)

    for i in range(sz):
        tmp = Node(keys[i], recipes[i])
        add(RT, tmp)


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет! Я помощник в нахождении рецептов. Какие продукты у вас есть?')


@bot.message_handler(content_types=['text'])
def handle_text(message):
    ingredients = sorted([x.strip().lower() for x in message.text.lower().split(', ')])
    match = get_similar_recipies(RT, ingredients)
    if not match:
        bot.send_message(message.chat.id, 'Рецепт не найден(')
    else:
        match2 = []
        for i in range(len(match)):
            if len(match2) < 4:
                match2.append(match[i])
        for ingredient, recipe in match2:
            bot.send_message(message.chat.id, f"Название блюда: {recipe[1]},\nИнгридиенты: {ingredient},\nСсылка, по "
                                              f"которой вы можете ознакомиться с порядком приготовления: {recipe[0]}\n")


bot.polling()
