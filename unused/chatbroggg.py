import sqlite3
from random import randint
import nltk
from nltk.corpus import stopwords
from nltk.stem.lancaster import LancasterStemmer
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
# nltk.download('punkt')

# factory = StemmerFactory()
# stemmer = factory.create_stemmer()
stemmer = LancasterStemmer()
print(1*'\n')

# CONFIG VARIABLES #
learning_chance = 100  # chance % of bot learning new words from input

# SQLITE STUFF #

def sqlite_query(query):
    conn = sqlite3.connect('chatbot.db')
    c = conn.cursor()
    c.execute(query)
    conn.commit()
    conn.close()
    return

def sqlite_select_once(query):
    conn = sqlite3.connect('chatbot.db')
    c = conn.cursor()
    c.execute(query)
    result = c.fetchone()[0]
    conn.close()
    return result
    
def sqlite_select_all(query):
    conn = sqlite3.connect('chatbot.db')
    c = conn.cursor()
    c.execute(query)
    rows = c.fetchall()
    conn.close()
    return rows

# END OF SQLITE STUFF #

# FUNCTION ZONE #
def randomizer():
    global learning_chance
    chance = randint(1, 100)
    if (chance <= learning_chance):
        return True
    return

def learn(text, classif):
    try:
        if randomizer():
            text_class = text.split(' ')
            for t in text_class:
                if (randint(1, 100) <= 25):
                    learn_class = t
                    break
            else:
                learn_class = t

            query = "INSERT INTO chatbot VALUES ('{}', '{}')".format(text, learn_class)
            sqlite_query(query)
            print('Bot telah mempelajari kata baru: {}, class: {}'.format(text, learn_class))
            return
    except:
        print('Error on learning')
        return
    return

def texts():
    texts = sqlite_select_all("SELECT texts FROM chatbot")
    text = []
    for i in texts:
        i = list(i)
        i = i[0]
        text.append(i)
    return text
# END OF FUNCTION ZONE

# print('Responses:', texts())

# LOGIC ZONE #
def get_training_data():
    texts = sqlite_select_all("SELECT * FROM chatbot")
    training_list = []

    for i in texts:
        i = list(i)
        balasan = i[0]
        kelas = i[1]
        training_list.append({"class":kelas, "sentence":balasan})

    return training_list

corpus_words = {}
class_words = {}

def update_training_data():
    # capture unique stemmed words in the training corpus
    training = get_training_data()
    # turn a list into a set (of unique items) and then a list again (this removes duplicates)
    classes = list(set([a['class'] for a in training]))
    for c in classes:
        # prepare a list of words within each class
        class_words[c] = []

    # loop through each sentence in our training data
    for data in training:
        # tokenize each sentence into words
        for word in nltk.word_tokenize(data['sentence']):
            # ignore a some things
            if word not in ["?", "'s"]:
                # stem and lowercase each word
                stemmed_word = stemmer.stem(word.lower())
                # have we not seen this word already?
                if stemmed_word not in corpus_words:
                    corpus_words[stemmed_word] = 1
                else:
                    corpus_words[stemmed_word] += 1

                # add the word to our words in class list
                class_words[data['class']].extend([stemmed_word])

    # print("Corpus words and counts: %s \n" % corpus_words)
    # also we have all words in each class
    # print("Class words: %s" % class_words)

# calculate a score for a given class taking into account word commonality
def calculate_class_score(sentence, class_name, show_details=True):
    score = 0
    # tokenize each word in our new sentence
    for word in nltk.word_tokenize(sentence):
        # check to see if the stem of the word is in any of our classes
        if stemmer.stem(word.lower()) in class_words[class_name]:
            # treat each word with relative weight
            score += (1 / corpus_words[stemmer.stem(word.lower())])

            if show_details:
                print("match: %s (%s)" % (stemmer.stem(word.lower()), 1 / corpus_words[stemmer.stem(word.lower())]))
    return score

# calculate a score for a given class taking into account word commonality
def calculate_class_score_commonality(sentence, class_name, show_details=True):
    score = 0
    # tokenize each word in our new sentence
    for word in nltk.word_tokenize(sentence):
        # check to see if the stem of the word is in any of our classes
        if stemmer.stem(word.lower()) in class_words[class_name]:
            # treat each word with relative weight
            score += (1 / corpus_words[stemmer.stem(word.lower())])

            if show_details:
                print("match: %s (%s)" % (stemmer.stem(word.lower()), 1 / corpus_words[stemmer.stem(word.lower())]))
    return score

# return the class with highest score for sentence
def classify(sentence):
    high_class = None
    high_score = 0
    # loop through our classes
    for c in class_words.keys():
        # calculate score of sentence for each class
        score = calculate_class_score_commonality(sentence, c, show_details=False)
        # keep track of highest score
        if score > high_score:
            high_class = c
            high_score = score

    return high_class, high_score

print(classify('Halo, apa kabar qil?'))



print(2*'\n')
# END Of LOGIC ZONE #

def chat(msg):
    update_training_data()

    print(classify(msg))

    classif = list(classify(msg))
    classif = classif[0]

    learn(msg, classif)

    if classif is None:
        query = "SELECT texts FROM chatbot WHERE class='{}'".format('nanya_nama')
    else:
        query = "SELECT texts FROM chatbot WHERE class='{}'".format(classif)

    reply = sqlite_select_all(query)
    replies = []
    for r in reply:
        z = list(r)
        replies.append(z[0])

    reply_msg = replies[randint(0, len(replies) - 1)]

    lim = 0
    while 'lu' in reply_msg and lim <= 5:
        lim += 1
        reply_msg = replies[randint(0, len(replies) - 1)]

    print(reply_msg)
    return reply_msg

# chat('Halo. Lagi ngapain?')

# while True:
#     update_training_data()
#     input_msg = input('>> ')

#     print(classify(input_msg))

#     classif = list(classify(input_msg))
#     classif = classif[0]

#     learn(input_msg, classif)

#     if classif is None:
#         query = "SELECT texts FROM chatbot WHERE class='{}'".format('nanya_nama')
#     else:
#         query = "SELECT texts FROM chatbot WHERE class='{}'".format(classif)

#     reply = sqlite_select_all(query)
#     replies = []
#     for r in reply:
#         z = list(r)
#         replies.append(z[0])
#     print(replies[randint(0, len(replies) - 1)])

#### USE THIS TO INSERT TRAINING DATA TO DB ####
# training_data = []
# training_data.append({"class":"nanya_nama", "sentence":"nama lu siapa"})
# training_data.append({"class":"nanya_nama", "sentence":"nama kamu siapa"})
# training_data.append({"class":"nanya_nama", "sentence":"ini siapa"})
# training_data.append({"class":"nanya_nama", "sentence":"lu siapa sih"})

# training_data.append({"class":"hai", "sentence":"halo "})
# training_data.append({"class":"hai", "sentence":"apa kabar"})
# training_data.append({"class":"hai", "sentence":"hai"})
# training_data.append({"class":"hai", "sentence":"hi"})

# training_data.append({"class":"pr", "sentence":"lu udah ngerjain pr qil"})
# training_data.append({"class":"pr", "sentence":"kerjain lah pr nya"})
# training_data.append({"class":"pr", "sentence":"gw liat pr dong"})
# training_data.append({"class":"pr", "sentence":"eh gua belum kerjain pr nih"})

# for t in training_data:
#     sqlite_query("INSERT INTO chatbot VALUES ('{}','{}')".format(stemmer.stem(t['sentence']), t['class']))
#################