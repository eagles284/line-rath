from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer

# chats = open('chats.txt', 'r').readlines()
# responds = open('chats.txt', 'r').readlines()
# bot.train(responds)

bot = ChatBot('Trombosit', storage_adapter='chatterbot.storage.SQLStorageAdapter', input_adapter="chatterbot.input.VariableInputTypeAdapter", output_adapter="chatterbot.output.OutputAdapter")
bot.set_trainer(ListTrainer)

def chat(input):
    print("received message:", input)
    response = bot.get_response(input)
    print("sending message:", response)
    return response

chatmess = "woi"
print(chat(chatmess))