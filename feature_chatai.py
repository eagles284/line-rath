from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ChatterBotCorpusTrainer

# chats = open('chats.txt', 'r').readlines()
responds = open('chats.txt', 'r').readlines()

bot = ChatBot(
    'Trombosit', 
    storage_adapter='chatterbot.storage.SQLStorageAdapter', 
    input_adapter="chatterbot.input.VariableInputTypeAdapter", 
    output_adapter="chatterbot.output.OutputAdapter",
    logic_adapters=[
        "chatterbot.logic.BestMatch"
    ])
bot.set_trainer(ListTrainer)
bot.train(responds)

bot.set_trainer(ChatterBotCorpusTrainer)
bot.train('chatterbot.corpus.indonesia')

def chat(input):
    print("received message:", input)
    response = bot.get_response(input)
    print("sending message:", response)
    return response

chatmess = "woi"
print(chat(chatmess))