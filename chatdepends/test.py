from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
import nltk

bot = ChatBot('Trombosit')

responds = open('chats.txt', 'r').readlines()

bot.set_trainer(ListTrainer)

# bot.train(responds)

def chat(input):
    response = bot.get_response(input)
    return response

while True:
    inp = input('You: ')
    print(chat(inp))
