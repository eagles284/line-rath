from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer

# chats = open('chats.txt', 'r').readlines()
# responds = open('chats.txt', 'r').readlines()
# bot.train(responds)

def chat(input):
    bot = ChatBot('Trombosit')
    bot.set_trainer(ListTrainer)
    response = bot.get_response(input)
    return response