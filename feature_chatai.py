from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer

# chats = open('chats.txt', 'r').readlines()
# responds = open('chats.txt', 'r').readlines()
# bot.train(responds)

bot = ChatBot('Trombosit')
bot.set_trainer(ListTrainer)

def chat(input):
    response = bot.get_response(input)
    return response