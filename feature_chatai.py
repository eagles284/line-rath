from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer

bot = ChatBot('Trombosit')

# responds = open('chats.txt', 'r').readlines()
# bot.train(responds)

bot.set_trainer(ListTrainer)


def chat(input):
    response = bot.get_response(input)
    return response