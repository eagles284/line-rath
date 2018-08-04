from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer

bot = ChatBot('Trombosit')

responds = open('chats.txt', 'r').readlines()

bot.set_trainer(ListTrainer)

bot.train(responds)

while True:
    received = input('you: ')
    response = bot.get_response(received)

    print(response)