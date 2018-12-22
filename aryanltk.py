import sqlite3
from random import randint

# TODO: Idiomatic statement analyzer. Nama gw arya. => reply => Nama lu arya.
# CONFIG VARIABLES #
learning_chance = 100  # chance % of bot learning new words from input


# SQLITE AND BASIC FUNCTIONS #

def sqlite_query(query):
    conn = sqlite3.connect('newchatbot.db')
    c = conn.cursor()    
    c.execute(query)
    conn.commit()
    conn.close()
    return

# sqlite_query('delete from chatbot')
# sqlite_query("INSERT INTO chatbot VALUES ('{}', '{}' ,'{}', '{}')".format('nama lu siapa', 'nama lu siapa', 'nama', ''))



def randomizer():
    global learning_chance
    chance = randint(1, 100)
    if (chance <= learning_chance):
        return True
    return

def sqlite_select_once(query):
    conn = sqlite3.connect('newchatbot.db')
    c = conn.cursor()
    c.execute(query)
    result = c.fetchone()[0]
    conn.close()
    return result
    
def sqlite_select_all(query):
    conn = sqlite3.connect('newchatbot.db')
    c = conn.cursor()
    c.execute(query)
    rows = c.fetchall()
    conn.close()
    return rows

def sqlite_select_old(query):
    conn = sqlite3.connect('chatbot.db')
    c = conn.cursor()
    c.execute(query)
    rows = c.fetchall()
    conn.close()
    return rows

# END OF SQLITE STUFF #

non_context_words = ['lu', 'gw', 'kemana', 'dimana', 'kapan', 'bagaimana', 'lagi', 'belum', 'siapa']

def make_stem(kalimat, kata, kata_dasar):
    # katas = ['memakai', 'mempakai']
    for k in kata:
        if k in kalimat:
            kalimat = kalimat.replace(k, kata_dasar)
            # non_context_words.append(kata_dasar)

    return kalimat

def stem(kalimat):
    kalimat = kalimat.lower()

    if 'nya' in kalimat:
        kalimat = make_stem(kalimat, ['nya'], '')
    if '?' in kalimat:
        kalimat = make_stem(kalimat, ['?'], ' ?')
    
    # kalimat = make_stem(kalimat, ['gue', 'saya'],                                                     'gw')
    
    kalimat = make_stem(kalimat, ['gue', 'saya', 'aku'],                                                'gw')
    kalimat = make_stem(kalimat, ['kamu', ' anda ', 'you'],                                               'lu')
    
    kalimat = make_stem(kalimat, ['bsk', 'bsok'],                                                       'besok')
    kalimat = make_stem(kalimat, ['kmrn', 'kemaren', 'kmaren', 'kmarin'],                               'kemarin')

    kalimat = make_stem(kalimat, ['knp', ' napa ', 'knpe', 'nape', 'knpa', 'kenape'],                   'kenapa')
    kalimat = make_stem(kalimat, ['kmn', 'kmana', 'kemn, ', 'ke mn', 'kemna', 'ke mna', 'ke mana'],     'kemana')
    kalimat = make_stem(kalimat, ['dimn', 'dmn', 'di mn', 'di mana', 'dimna', 'di mna'],                'dimana')
    kalimat = make_stem(kalimat, ['udh', ' uda ', 'udah'],                                                'sudah')
    kalimat = make_stem(kalimat, ['blm', 'belom', 'blom', 'blon', 'blum'],                              'belum')

    kalimat = make_stem(kalimat, ['memakai', 'mempakai'],                                               'pakai')
    kalimat = make_stem(kalimat, ['menggunakan'],                                                       'guna')
    kalimat = make_stem(kalimat, [' msh '],                                                               'masih')
    kalimat = make_stem(kalimat, ['inget'],                                                             'ingat')
    kalimat = make_stem(kalimat, ['ngambil', 'mengambil'],                                              'ambil')
    kalimat = make_stem(kalimat, [' mo ', 'mw', 'maw'],                                                   'mau')
    kalimat = make_stem(kalimat, ['bwt'],                                                               'buat')
    kalimat = make_stem(kalimat, ['mang'],                                                              'emang')
    kalimat = make_stem(kalimat, ['ngapain', 'lg apa'],                                                 'lakukan')
    kalimat = make_stem(kalimat, ['ngerjain', 'kerjain', 'kerjakan'],                                   'kerja')

    return kalimat

def get_type(kalimat):

    # Greetings Add In
    greeting = ['hi', 'hai', 'halo', 'apa', 'sehat', 'kabar', 'pa', 'hei', 'hey', 'hello']
    greeting_score = 0
    for katakata in kalimat.split(' '):
        if katakata in greeting:
            greeting_score += 1
    greeting_score = greeting_score / len(kalimat.split(' '))
    if greeting_score >= 0.5:
        print('Greeting scr: ', greeting_score)
        return 'greeting'

    # 5W 1H Add In
    if 'dimana' in kalimat or 'kemana' in kalimat:
        return 'q_where'

    elif 'kenapa' in kalimat:
        return 'q_why'

    elif 'kapan' in kalimat:
        return 'q_when'

    elif 'bagaimana' in kalimat:
        return 'q_how'

    elif '?' in kalimat:
        return 'q'

    return 'unknown'

def get_context(kalimat):
    kalimat_split = kalimat.split(' ')
    konteks = []

    for katakata in kalimat_split:

        if katakata not in non_context_words:
            konteks.append(katakata)

    return konteks

def classify(kalimat_raw):
    kalimat = stem(kalimat_raw)
    context = get_context(kalimat)
    tipe = get_type(kalimat)

    return {'kalimat_raw':kalimat_raw,
            'kalimat_nlp':kalimat,
            'context':context,
            'tipe':tipe}

def classified_learn(kalimat):
    if randomizer():
        sentence = classify(kalimat)
        raw = sentence['kalimat_raw']
        nlp = sentence['kalimat_nlp']
        context = sentence['context']
        tipe = sentence['tipe']

        # Check if there is no duplicate
        qwery = "SELECT * FROM chatbot WHERE nltk_txt='{}'".format(nlp)
        qwery = sqlite_select_all(qwery)
        if len(qwery) > 0:
            return 'learn_fail_exist'

        if len(context) > 1:
            for c in context:
                query = "INSERT INTO chatbot VALUES ('{}', '{}', '{}', '{}')".format(raw, nlp, c, tipe)
        elif len(context) == 1:
            query = "INSERT INTO chatbot VALUES ('{}', '{}', '{}', '{}')".format(raw, nlp, context[0], tipe)
        else:
            query = "INSERT INTO chatbot VALUES ('{}', '{}', '{}', '{}')".format(raw, nlp, 'unknown', tipe)

        sqlite_query(query)

        return 'learn_success'
    else:
        return 'learn_fail'



#
# Mengambil balasan dari kalimat-kalimat di berbagai macam / 1 konteks  kalimat
# Jika kemiripan setiap kata sangat besar, maka kalimat itu yang akan menjadi balasan
# Biasanya balasan ini digunakan jika input adalah pertayaan
#
def contextual_word_reply(kalimat):
    dunno_reply = ['Kgk tau dah', 'Entahlah', 'Au dah', 'Gatau deh', 'Gk tau gw', 'Gw kaga tau']

    sentence = classify(kalimat)
    raw = sentence['kalimat_raw']
    nlp = sentence['kalimat_nlp']
    context = sentence['context']
    tipe = sentence['tipe']

    sentences = []
    sentences_raw = []

    if len(context) > 0:
        for c in context:
            sens = [r[0] for r in sqlite_select_all("SELECT raw_txt FROM chatbot WHERE cont='{}'".format(c))]
            sens_n = [r[0] for r in sqlite_select_all("SELECT nltk_txt FROM chatbot WHERE cont='{}'".format(c))]
            for s, n in zip(sens, sens_n):
                if 'q' in classify(s)['tipe'] or 'lu' in s.lower():
                    continue
                sentences_raw.append(s)
                sentences.append(n)
            pass
    else:
        dunno_reply = dunno_reply[randint(0, len(dunno_reply)-1)]
        return dunno_reply
    
    selector = {'score': 0, 'index': -1}
    sentences = tuple(sentences)

    tempindex = -1
    for perkalimat in sentences:
        
        tempscore = 0

        for katabanding in nlp.split(' '):
            if katabanding in perkalimat:
                tempscore += 1

        tempindex += 1

        if tempscore > selector['score']:
            selector['score'] = tempscore
            selector['index'] = tempindex
    
    print(sentences)

    if selector['index'] < 0 or len(sentences_raw) < 1:
        dunno_reply = dunno_reply[randint(0, len(dunno_reply)-1)]
        return dunno_reply

    return sentences_raw[selector['index']]

#
# Mengambil balasan dari perbandingan antara konteks-konteks di kalimat
# Konteks yang paling banyak kemunculan katanya (non duplicate) akan dipilih sebagai asal kalimat
# Untuk saat ini, pengambilan kalimat dari konteks diambil acak
# Biasanya balasan ini digunakan jika input bukan pertanyaan
# UNTUK SEMENTARA PAKE NAIVE BAIYES CLASsIFIER
#
def contextual_reply(kalimat):
    dunno_reply = ['Kgk tau dah', 'Entahlah', 'Au dah', 'Gatau deh', 'Gk tau gw', 'Gw kaga tau']

    sentence = classify(kalimat)
    raw = sentence['kalimat_raw']
    nlp = sentence['kalimat_nlp']
    context = sentence['context']
    tipe = sentence['tipe']

    struktur = {}

    if len(context) < 1:
        dunno_reply = dunno_reply[randint(0, len(dunno_reply)-1)]
        return dunno_reply

    for c in context:
        sens = [r[0] for r in sqlite_select_all("SELECT nltk_txt FROM chatbot WHERE cont='{}'".format(c))]
        struktur[c] = list(set(sens))

    print(struktur)
    pass

# print(10 * '\n')

# contextual_reply('Lu udah ngerjain pr')
# print([r[0] for r in sqlite_select_all("SELECT raw_txt FROM chatbot WHERE cont='pr'")])

# while True:
#     msg = input('> ')
#     print(classified_learn(msg))
#     print(contextual_word_reply(msg))
#     # print(classify(msg))

def chat(msg):
    print(classified_learn(msg))
    return contextual_word_reply(msg)























# oldtexts = sqlite_select_old("SELECT texts FROM chatbot")

# for o in oldtexts:
#     txt = list(o)
#     txt = classify(txt[0])

#     raw = str(txt['kalimat_raw'])
#     nlp = str(txt['kalimat_nlp'])
#     cont = txt['context']
#     tipe = str(txt['tipe'])
#     le = '|'

#     if (len(cont) > 1):
#         for c in cont:
#             # print(raw, le, nlp, le, c, le, tipe)
#             sqlite_query("INSERT INTO chatbot VALUES ('{}', '{}' ,'{}', '{}')".format(raw, nlp, c, tipe))
#     else:
#         if len(cont) == 0:
#             sqlite_query("INSERT INTO chatbot VALUES ('{}', '{}' ,'{}', '{}')".format(raw, nlp, 'unknown', tipe))
#             pass
#         else:
#             sqlite_query("INSERT INTO chatbot VALUES ('{}', '{}' ,'{}', '{}')".format(raw, nlp, cont[0], tipe))
#             pass

#     # print(raw, nlp, cont, tipe)

