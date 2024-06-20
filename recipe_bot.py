import telebot
from bk_tree import *
from dataset_loader import DatasetLoader


class RecipeBot:
    def __init__(self, token, dataset_loader):
        self.bot = telebot.TeleBot(token)
        self.dataset_loader = dataset_loader
        self.RT = Node()

    def start(self):
        self.dataset_loader.load_data()
        recipes = self.dataset_loader.get_recipes()
        for recipe in recipes:
            tmp = Node(recipe[2], (recipe[0], recipe[1]))
            add(self.RT, tmp)

    def handle_message(self, message):
        ingredients = sorted([x.strip().lower() for x in message.text.lower().split(', ')])
        match = get_similar_recipies(self.RT, ingredients)
        if not match:
            self.bot.send_message(message.chat.id, 'Рецепт не найден(')
        else:
            match2 = []
            for i in range(len(match)):
                if len(match2) < 4:
                    match2.append(match[i])
            for ingredient, recipe in match2:
                self.bot.send_message(message.chat.id, f"Название блюда: {recipe[1]},\nИнгридиенты: {ingredient},\nСсылка, по "
                                                      f"которой вы можете ознакомиться с порядком приготовления: {recipe[0]}\n")

    def run(self):
        @self.bot.message_handler(commands=['start'])
        def start_message(message):
            self.bot.send_message(message.chat.id, 'Привет! Я помощник в нахождении рецептов. Какие продукты у вас '
                                                   'есть?')

        @self.bot.message_handler(content_types=['text'])
        def handle_text(message):
            self.handle_message(message)

        self.bot.polling()


if __name__ == "__main__":
    dataset_loader = DatasetLoader('recipes - recipes.csv')
    bot = RecipeBot('Ваш токен', dataset_loader)
    bot.start()
    bot.run()