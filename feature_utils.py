import feedparser
import requests
from unicodedata import east_asian_width
import wikipedia
import re
from bs4 import BeautifulSoup
import time
import datetime
import contextlib
import selenium.webdriver as webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import os
import public_vars
import sqlite3
import chatfeatures
from linebot.models import (
    TextSendMessage, TemplateSendMessage,
    CarouselColumn, CarouselTemplate, ConfirmTemplate,
    URITemplateAction, PostbackTemplateAction, MessageTemplateAction,
    LocationSendMessage, LocationMessage, PostbackAction, URIAction, MessageAction,
    ImageSendMessage, ButtonsTemplate
)
import matplotlib
matplotlib.use('agg')
from matplotlib import pyplot as plt

# message_content = line_bot_api.get_message_content(message_id)

# with open(file_path, 'wb') as fd:
#     for chunk in message_content.iter_content():
#         fd.write(chunk)

# ====================================
# Wikipedia Search
# ====================================
def wikipedia_search(word):
    """Search a word meaning on wikipedia."""
    wikipedia.set_lang('id')
    results = wikipedia.search(word)

    # get first result
    if results:
        page = wikipedia.page(results[0])
        msg = page.title + "\n" + page.url
    else:
        msg = '`{}` Tidak bisa menemukan kata yang dicari'.format(word)
    return msg

# ====================================
# Google News
# ====================================
def google_news():
    # RSS Feed of yahoo news doesn't contain thumbnail image.
    url = 'https://news.google.com/news?hl=id&ned=us&ie=UTF-8&oe=UTF-8&topic=po&output=rss'
    parsed = feedparser.parse(url)
    return parsed.entries

currentDate = ""
realCurrentDate = ""

# ==================
# Screenshot Website
# ==================

tempUrl = ""

def ssweb(url):

    global currentDate, realCurrentDate, tempUrl
    tempUrl = url
    currentDate = str(datetime.datetime.now().time())
    datenow = currentDate.replace(":","")
    realCurrentDate = datenow

    rawinputstring = ""

    if url.startswith("/instagram"):
        rawinputstring = "www.instagram.com/"
        rawinputstring += url.replace("/instagram", "")
    if url.startswith("/screenshot"):
        rawinputstring = url.replace("/screenshot", "")

    inputstring = rawinputstring.replace(" ", "")


    print(inputstring)
    # print("http://instagram.com/"+inputstring)
    # return
    try:
        options = Options()
        options.add_argument('-headless')
        # options.add_argument('--ignore-certificate-errors')
        # options.add_argument("--test-type")
        # options.add_argument('--disable-gpu')
        # options.add_argument('disable-infobars')
        # options.add_argument('--no-sandbox')
        # options.add_argument('--start-maximized')
        # options.add_argument('--disable-dev-shm-usage')
        
        # options.add_argument('--screenshot --window-size=412,732 https://www.google.com/')
        # options.binary_location = "/app/.apt/usr/bin/google-chrome"

        # binary = FirefoxBinary('path/to/installed firefox binary')
        driver = webdriver.Firefox(executable_path='/usr/local/bin/geckodriver', firefox_options=options)
        ##
        webFile = public_vars.HOST_PUBLIC_URL + "/static/" + realCurrentDate + ".png"

        # driver.set_window_position(0, 0)
        # driver.set_window_size(1024, 768)
        # if url.startswith("/instagram"):
        #     driver.set_window_size(480, 768)

        if not url.startswith("/instagram"):
            print("Screenshot input:", inputstring)
            if inputstring.startswith("https://"):
                print("HTTPS Input:", inputstring)
                driver.get(inputstring)
            elif inputstring.startswith("http://"):
                print("HTTP Input:", inputstring)
                driver.get(inputstring)
            else:
                print("Not Specified Input: http://" + inputstring)
                driver.get("http://" + inputstring)

        elif url.startswith("/instagram"):
            print("Instagram Input: https://" + inputstring)
            driver.get('https://' + inputstring)

        # if url.startswith("/instagram"):
            # driver.find_element_by_class_name('.Szr5J').click()
            # driver.find_element_by_css_selector('.Szr5J').click()
            
        print("Getting screenshot")
        driver.get_screenshot_as_file("static/" + realCurrentDate + ".png")
        driver.save_screenshot("static/ss.png")
        driver.quit()
        print("Closing screenshot")
        return str(webFile)

    except Exception as e:
        print("Error :", e, "Retrying screenshot...")
        # ssweb(tempUrl)
        return None

# ssweb("/screenshot https://www.google.com")

# ================
# Grafik Persamaan
# ================
def plot(persamaan):

    global currentDate, realCurrentDate
    currentDate = str(datetime.datetime.now().time())
    datenow = currentDate.replace(":","")
    realCurrentDate = datenow

    rawinputstring = persamaan.replace(" ", "")
    inputstring = rawinputstring.replace("/grafik", "")
    print(inputstring)

    if "x" in inputstring and "y" in inputstring and "=" in inputstring and "/" not in inputstring and "*" not in inputstring:
        
        try:
            plt.clf()
            removex = inputstring.replace(" ", "").split("x")
            removey = removex[1].split("y")
            removee = removey[1].split("=")

            if removex[0] == '' or removex[0] == '-':
                xraw = int(1)
                if removex[0] == '-':
                    xraw = int(-1)
            else:
                xraw = int(removex[0])
            
            if removey[0] == '+' or removey[0] == '-' or removey[0] == '':
                yraw = int(1)
                if removey[0] == '-':
                    yraw = int(-1)
            else:
                yraw = int(removey[0])

            e = int(removee[1])

            x = e/xraw
            y = e/yraw

            stringx = str(x)
            stringy = str(y)

            if '.0' in stringx:
                stringx = stringx.replace(".0","")
            if '.0' in stringy:
                stringy = stringy.replace(".0","")

            print("x:",xraw,"y:",yraw,"e:",e)
            print("x:",x,"y:",y,"e:",e)
            print("label X:",stringx,"label Y:",stringy)

            # Create a dataframe with an x column containing values from -10 to 10
            # df = pd.DataFrame({'x': range(-10, 11)})

            # Define slope and y-intercept
            # m = 1.5
            # yInt = -2

            # Add a y column by applying the slope-intercept equation to x
            # df['y'] = m*df['x'] + yInt
            # print(df)

            # Plot the line
            print("Going to plot")
            xi = [0, x]
            yi = [y, 0]

            plt.plot(xi, yi, color="red")
            # plt.xlabel('x')
            # plt.ylabel('y')
            plt.axhline()
            plt.axvline()    
            plt.grid()
            print("Going to plot...2")
            # strx = str(x)
            # stry = str(y)

            # label the y and x - intercept
            plt.axvspan(x, y, facecolor='g', alpha=0)
            plt.annotate(stringx[0:15],(x,0), color='green')
            plt.annotate(stringy[0:15],(0,y), color='green')
            print("PLOT SUCCESS")
            # plot the slope from the y-intercept for 1x
            # mx = [0, 1]
            # my = [yInt, yInt + m]
            # plt.plot(mx,my, color='red', lw=5)
            print("Creating file....")

            plt.savefig('static/' + realCurrentDate + ".png")

            print("Create file success")
            print("Generating URL")

            fileurl = public_vars.HOST_PUBLIC_URL + "/static/" + realCurrentDate + ".png"

            print("fileurl:", fileurl)

            return str(fileurl)

            # plt.show()  # REMOVE THIS ON EXECUTE!!!
            
        except IndexError:
            return
    else:
            print("Format error")
            return

# plot("-3x+3y=10")
# plot("5x+4y=20")

def hari(date):
    english_day = datetime.datetime.strptime(date, '%d/%m/%Y').strftime('%A')
    hari = ""

    if(english_day == "Monday"):
        hari = "Senin"
    elif(english_day == "Tuesday"):
        hari = "Selasa"
    elif(english_day == "Wednesday"):
        hari = "Rabu"
    elif(english_day == "Thursday"):
        hari = "Kamis"
    elif(english_day == "Friday"):
        hari = "Jumat"
    elif(english_day == "Saturday"):
        hari = "Sabtu"
    elif(english_day == "Sunday"):
        hari = "Minggu"
    else:
        hari = english_day
    
    print(hari)
    return(hari)

#sqlite create table
def sqlite_query(query):
    sqlite_db_name = 'absen.sqlite3'

    conn = sqlite3.connect(sqlite_db_name)
    c = conn.cursor()
    
    c.execute(query)

    conn.commit()
    conn.close()

def sqlite_check_table(tablename):
    sqlite_db_name = 'absen.sqlite3'
    conn = sqlite3.connect(sqlite_db_name)

    try:
        dbcur = conn.cursor()
        dbcur.execute("""
            SELECT name
            FROM sqlite_master
            WHERE type = 'table' AND
            name = """ +"'"+tablename+"'")
        try:
            result = dbcur.fetchone()[0]
        except TypeError:
            # Table is NOT existed
            dbcur.close()
            return False
    except sqlite3.OperationalError as e:
        dbcur.close()
        # Table is NOT existed
        print("Table is not existed. Continuing....")
        print(e)
        return False

    if(len(str(result)) > 0):
        # Table is existed
        dbcur.close()
        return True

    dbcur.close()
    # Table IS NOT existed
    return False

def sqlite_count_table():

    sqlite_db_name = 'absen.sqlite3'
    conn = sqlite3.connect(sqlite_db_name)

    dbcur = conn.cursor()
    dbcur.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type = 'table'""")
    try:
        tables = dbcur.fetchall()
    except TypeError:
        # Tables is empty
        dbcur.close()
        return 0

    return len(tables)

def sqlite_select_once(query):
    sqlite_db_name = 'absen.sqlite3'

    conn = sqlite3.connect(sqlite_db_name)
    c = conn.cursor()
    
    c.execute(query)
    result = c.fetchone()[0]

    conn.close()
    return result

def sqlite_select_all(query):

    sqlite_db_name = 'absen.sqlite3'
    connect = sqlite3.connect(sqlite_db_name)

    cursor = connect.cursor()
    cursor.execute(query)

    rows = cursor.fetchall()

    connect.close()
    return rows

# =====================
# ABSEN SCRIPT START
# =====================
def check_string(msg):

    try:
        # String Manipulation
        remove_absenmsg = msg.replace("/absen ", "")
        grouped_msg = remove_absenmsg.split(" ")

        date_raw = grouped_msg[0]
        print("DateRaw:", date_raw)

        target_date = time.mktime(datetime.datetime.strptime(date_raw, "%d/%m/%Y").timetuple())
        target_date = str(target_date)
        target_date = target_date.replace(".0", "")
        target_date = int(target_date)
        target_date = target_date + (3600 * 13)

        target_date_rdb = datetime.datetime.utcfromtimestamp(target_date).strftime('%d/%m/%Y')
        target_date_rdb = target_date_rdb.replace("/", "")

        reminder_date = target_date - (3600 * 9)

        print("Target date in unix:", target_date)
        print("Target date:", datetime.datetime.utcfromtimestamp(target_date).strftime('%d/%m/%Y %H:%M:%S'))
        print("Reminder date:", datetime.datetime.utcfromtimestamp(reminder_date).strftime('%d/%m/%Y %H:%M:%S'))

        keterangan = ""
        for i in range(1, len(grouped_msg)):
            keterangan += grouped_msg[i] + " "

        print("Keterangan:", keterangan)

        target_date_str = str(target_date_rdb)
        keterangan = "'" + keterangan + "'"
        initiator = "'" + chatfeatures.absen_name + "'"

        current_date = int(time.time()) + (3600 * 7)
        template_text = 'Absensi ' + keterangan + "(oleh " + str(chatfeatures.absen_name) + ")"

        # Check if target date is not below current date
        if (target_date < current_date):
            return 'date_below'

        # Check if reply body length is not longer than 60 letters
        if (len(template_text) >= 60):
            return 'kepanjangan'

        # Check if absens is not more than 4
        if (sqlite_count_table() >= 4):
            return 'more_than_4'

        # Check if table is not exist
        if (sqlite_check_table('abs_'+target_date_str)):
            print('Table has been existed. Stopped')
            return 'table_existed'
    except ValueError:
        # Check if format is valid
        return 'format_error'
    except OverflowError:
        # Check if time is not overflow
        return 'kejauhan'

    return 'pass'

def absen(msg):

    # Current = 1534496457 + (3600 * 7)
    # print("\n\nReal Time: 17/08/2018 16.00\n")
    # print("Current TS:", Current, "\nCurrent Time:", datetime.datetime.utcfromtimestamp(Current).strftime('%d/%m/%Y %H:%M:%S'), "\n\n")

    # REPEAT The Same String Manipulation
    remove_absenmsg = msg.replace("/absen ", "")
    grouped_msg = remove_absenmsg.split(" ")

    date_raw = grouped_msg[0]

    target_date = time.mktime(datetime.datetime.strptime(date_raw, "%d/%m/%Y").timetuple())
    target_date = str(target_date)
    target_date = target_date.replace(".0", "")
    target_date = int(target_date)
    target_date = target_date + (3600 * 13)

    target_date_rdb = datetime.datetime.utcfromtimestamp(target_date).strftime('%d/%m/%Y')
    target_date_rdb = target_date_rdb.replace("/", "")

    reminder_date = target_date - (3600 * 9)

    keterangan = ""
    for i in range(1, len(grouped_msg)):
        keterangan += grouped_msg[i] + " "

    target_date_str = str(target_date_rdb)
    # keterangan = "'" + keterangan + "'"
    initiator = "'" + chatfeatures.absen_name + "'"

    current_date = int(time.time()) + (3600 * 7)
    template_text = 'Keterangan: ' + keterangan + "(oleh " + str(chatfeatures.absen_name) + ")"

    eventdatesql = str(datetime.datetime.utcfromtimestamp(target_date).strftime('%d/%m/%Y'))
    daysql = str(hari(eventdatesql))
    sqlrdate = "'"+daysql + ", " + eventdatesql+"'"

    # =================
    # PROCEDURAL SQLITE
    # =================

    # Create table
    create_abs_table = '''CREATE TABLE IF NOT EXISTS abs_''' + target_date_str + '''
             (type text, val text)'''

    sqlite_query(create_abs_table)
    
    # Insert the initial data
    sql_insert_date_unix = "INSERT INTO abs_" + target_date_str + " VALUES ('target-date-unix', " + str(target_date) + ")"
    sql_insert_table = "INSERT INTO abs_" + target_date_str + " VALUES ('target-date', " + "'"+target_date_str+"'" + ")"
    sql_insert_rdate = "INSERT INTO abs_" + target_date_str + " VALUES ('readable-date', " + sqlrdate + ")"
    sql_insert_ket = "INSERT INTO abs_" + target_date_str + " VALUES ('keterangan', " + "'"+keterangan+"'" + ")"
    sql_insert_initiator = "INSERT INTO abs_" + target_date_str + " VALUES ('initiator', " + initiator + ")"
    
    sqlite_query(sql_insert_date_unix)
    sqlite_query(sql_insert_table)
    sqlite_query(sql_insert_rdate)
    sqlite_query(sql_insert_ket)
    sqlite_query(sql_insert_initiator)

    # Get keterangan
    event_date = str(datetime.datetime.utcfromtimestamp(target_date).strftime('%d/%m/%Y'))
    day = str(hari(event_date))

    # ket = sqlite_select_once("SELECT val FROM abs_" + target_date_str + " WHERE type='keterangan'")

    absen_template = TemplateSendMessage(
        alt_text='Pesan Absen',
        template=ButtonsTemplate(
            title=day + ", " + event_date,
            text=template_text,
            actions=[
                MessageAction(
                    label='Hadir',
                    text='#absen '+target_date_str+' Hadir'
                ),
                MessageAction(
                    label='Izin',
                    text='#absen '+target_date_str+' Izin'
                ),
                MessageAction(
                    label='Sakit',
                    text='#absen '+target_date_str+' Sakit'
                ),
            ]
        )
    )
    return absen_template

# Hapus Absen
def delete_absen():

    absens_query = """
        SELECT name
        FROM sqlite_master
        WHERE type = 'table'"""

    absens = sqlite_select_all(absens_query)

    print(absens)

    actions_template = []

    for absen in absens:
        absen = list(absen)
        absen = str(absen[0])
        absen = absen.replace("abs_", "")
        print(absen)

        absendate = datetime.datetime.strptime(absen, '%d%m%Y').strftime('%d/%m/%Y')
        absenhari = str(hari(absendate))

        actions_template.append(
            MessageAction(
                label=absenhari + ", " + absendate,
                text='#hapusabsen ' + absen
            ),
        )

    delete_absen_template = TemplateSendMessage(
        alt_text='Pesan Absen',
        template=ButtonsTemplate(
            title="Hapus Absen",
            text="Tekan salah satu absen di bawah untuk menghapusnya.",
            actions=actions_template
        )
    )

    return delete_absen_template
    # return None

# Daftar Absen
def daftar_absen():

    absens_query = """
        SELECT name
        FROM sqlite_master
        WHERE type = 'table'"""

    absens = sqlite_select_all(absens_query)

    print(absens)

    actions_template = []

    for absen in absens:
        absen = list(absen)
        absen = str(absen[0])
        absen = absen.replace("abs_", "")
        print(absen)

        absendate = datetime.datetime.strptime(absen, '%d%m%Y').strftime('%d/%m/%Y')
        absenhari = str(hari(absendate))

        actions_template.append(
            MessageAction(
                label=absenhari + ", " + absendate,
                text='#daftarkehadiran ' + absen
            ),
        )

    daftar_absen_template = TemplateSendMessage(
        alt_text='Pesan Absen',
        template=ButtonsTemplate(
            title="Daftar Absen & Kehadiran",
            text="Tekan absen di bawah untuk memunculkan opsi kehadiran.",
            actions=actions_template
        )
    )

    return daftar_absen_template

def daftarabsen(msg):
    msg = msg.replace("#daftarkehadiran ", "")
    table_id = "abs_"+msg

    date = sqlite_select_once("SELECT val FROM "+table_id+" WHERE type='readable-date'")
    initiator = sqlite_select_once("SELECT val FROM "+table_id+" WHERE type='initiator'")
    keterangan = sqlite_select_once("SELECT val FROM "+table_id+" WHERE type='keterangan'")

    absen_template = TemplateSendMessage(
        alt_text='Pesan Absen',
        template=ButtonsTemplate(
            title=date,
            text=keterangan + "(oleh "+initiator+")",
            actions=[
                MessageAction(
                    label='Hadir',
                    text='#absen '+msg+' Hadir'
                ),
                MessageAction(
                    label='Izin',
                    text='#absen '+msg+' Izin'
                ),
                MessageAction(
                    label='Sakit',
                    text='#absen '+msg+' Sakit'
                ),
            ]
        )
    )
    return absen_template



# Daftar Absen
def daftar_absen_carousel():

    absens_query = """
        SELECT name
        FROM sqlite_master
        WHERE type = 'table'"""

    absens = sqlite_select_all(absens_query)

    print(absens)

    carousel_columns = []

    for absen_id in absens:
        absen_id = list(absen_id)
        absen_id = str(absen_id[0])
        print(absen_id)
        
        select_all_in_absen_query = "SELECT val FROM " +absen_id
        select_all_in_absen = sqlite_select_all(select_all_in_absen_query)
        
        data_list = []
        for data_in_absen in select_all_in_absen:
            data_in_absen = list(data_in_absen)
            data_in_absen = str(data_in_absen[0])
            data_list.append(data_in_absen)
            print(data_in_absen)

        carousel_columns.append(
            CarouselColumn(
                title=data_list[2],
                text=data_list[3] + "(oleh " + data_list[4] + ")",
                actions=[
                    MessageAction(
                        label='Hadir',
                        text='#absen '+ data_list[1] +' Hadir'
                    ),
                    MessageAction(
                        label='Izin',
                        text='#absen '+ data_list[1] +' Izin'
                    ),
                    MessageAction(
                        label='Sakit',
                        text='#absen '+ data_list[1] +' Sakit'
                    ),
                ]
            ),
        )

        print(data_list)



    # daftar_absen_template = TemplateSendMessage(
    #     alt_text='Pesan Absen',
    #     template=ButtonsTemplate(
    #         title="Daftar Absen",
    #         text="Tekan absen di bawah untuk memunculkan opsi kehadiran.",
    #         actions=actions_template
    #     )
    # )

    daftar_absen_template = TemplateSendMessage(
        alt_text='Pesan Daftar Absen',
        template=CarouselTemplate(
            columns=carousel_columns
        )
    )

    return daftar_absen_template

def hapus_absen(msg):
    msg = msg.replace('#hapusabsen ', '')
    table_id = "abs_" + msg

    if not(sqlite_check_table(table_id)):
        return 'table_not_found'

    sqlite_query('DROP TABLE IF EXISTS '+table_id)

    return msg

def kehadiran(msg):
    msg = msg.replace('#absen ', '')
    msg_split = msg.split(' ')
    table_id = 'abs_' + msg_split[0]

    print("Table_id: ", table_id)
    # Check if table exist
    if not (sqlite_check_table(table_id)):
        return 'Tidak dapat menemukan data absen. Ketik "/help absen" untuk melihat perintah pada absen.'

    nama = "'"+chatfeatures.absen_name+"'"
    alasan = "'"+msg_split[1]+"'"
    values = nama + ", " + alasan
    print(values)

    # Get keterangan and tanggal absen from db:
    keterangan_query = "SELECT val FROM "+table_id+" WHERE type='keterangan'"
    tanggal_query = "SELECT val FROM "+table_id+" WHERE type='readable-date'"

    keterangan = sqlite_select_once(keterangan_query)
    tanggal = sqlite_select_once(tanggal_query)

    reply_msg = nama + " " + alasan + " dalam absensi " + keterangan + " yang direncanakan pada: " + tanggal
    
    # Check if commander's name isn't duplicate
    try:
        sqlite_select_once('SELECT * FROM '+table_id+' WHERE type='+nama)
    except TypeError:
        # If Commander's name is not exist, Insert the commander's name and alasan into db
        query = 'INSERT INTO '+table_id+' VALUES ('+ values +')'
        sqlite_query(query)

        if (alasan == "'Hadir'"):
            reply_msg = nama + ' akan hadir dalam absensi ' + keterangan + ' yang direncanakan pada: ' + tanggal
        if (alasan == "'Izin'"):
            reply_msg = nama + ' izin dalam absensi ' + keterangan + ' yang direncanakan pada: ' + tanggal
        if (alasan == "'Sakit'"):
            reply_msg = nama + ' sedang sakit dalam absensi ' + keterangan + ' yang direncanakan pada: ' + tanggal
            
        # return reply_msg
    else:
        # If Commander's name is existed, update values
        query = 'UPDATE '+table_id+' SET val = '+alasan+' WHERE type ='+nama
        sqlite_query(query)

        if (alasan == "'Hadir'"):
            reply_msg = nama + ' lebih memilih untuk hadir dalam absensi ' + keterangan + ' yang direncanakan pada: ' + tanggal
        if (alasan == "'Izin'"):
            reply_msg = nama + ' meminta izin dalam absensi ' + keterangan + ' yang direncanakan pada: ' + tanggal
        if (alasan == "'Sakit'"):
            reply_msg = nama + ' saat ini sedang sakit dalam absensi ' + keterangan + ' yang direncanakan pada: ' + tanggal
        # return reply_msg

    # Get the attedants of the absent
    attedants_list = list(sqlite_select_all('SELECT * FROM '+table_id))

    reply_msg += '\n\nDaftar kehadiran sementara:'
    attedants_reply_msg = ""
    
    for i in range(5, len(attedants_list)):
        indexx = i-3
        attedants_reply_msg += "\n" + str(attedants_list[i])
        print(str(indexx) + ". ", attedants_list[i])

    reply_msg += attedants_reply_msg

    return reply_msg

def daftarkehadiran(msg):
    table_id = 'abs_' + msg.replace('#daftarkehadiran ', '')

    # Get the attedants of the absent
    attedants_list = list(sqlite_select_all('SELECT * FROM '+table_id))

    reply_text = 'Daftar kehadiran sementara:\n'
    attedants_reply_msg = ""
    
    for i in range(5, len(attedants_list)):
        indexx = i-3
        attedants_reply_msg += "\n" + str(attedants_list[i])
        print(str(indexx) + ". ", attedants_list[i])

    reply_text += attedants_reply_msg

    reply_msg = TextSendMessage(text=reply_text)
    return reply_msg

def absengrup():
    absens_query = """
        SELECT name
        FROM sqlite_master
        WHERE type = 'table'"""

    absens = sqlite_select_all(absens_query)

    print(absens)

    actions_template = []

    for absen in absens:
        absen = list(absen)
        absen = str(absen[0])
        absen = absen.replace("abs_", "")
        print(absen)

        absendate = datetime.datetime.strptime(absen, '%d%m%Y').strftime('%d/%m/%Y')
        absenhari = str(hari(absendate))

        actions_template.append(
            MessageAction(
                label=absenhari + ", " + absendate,
                text='#absengrup ' + absen
            ),
        )

    daftar_absen_template = TemplateSendMessage(
        alt_text='Pesan Absen',
        template=ButtonsTemplate(
            title="Daftar Absen & Kehadiran",
            text="Tekan absen di bawah untuk memunculkan opsi kehadiran.",
            actions=actions_template
        )
    )

    return daftar_absen_template

def kehadirangrup(msg):
    msg = msg.replace('#absengrup ', '')
    table_id = "abs_"+msg

    date = sqlite_select_once("SELECT val FROM "+table_id+" WHERE type='readable-date'")
    initiator = sqlite_select_once("SELECT val FROM "+table_id+" WHERE type='initiator'")
    keterangan = sqlite_select_once("SELECT val FROM "+table_id+" WHERE type='keterangan'")

    # Do the 'add all members' logic here


    absen_template = TemplateSendMessage(
        alt_text='Pesan Absen',
        template=ButtonsTemplate(
            title=date,
            text=keterangan + "(oleh "+initiator+")",
            actions=[
                MessageAction(
                    label='Hadir',
                    text='#absen '+msg+' Hadir'
                ),
                MessageAction(
                    label='Izin',
                    text='#absen '+msg+' Izin'
                ),
                MessageAction(
                    label='Sakit',
                    text='#absen '+msg+' Sakit'
                ),
            ]
        )
    )
    return absen_template

def isikehadirangrup(msg):
    table_id = 'abs_' + msg.replace('#absengrup ', '')

    # Get the attedants of the absent
    attedants_list = list(sqlite_select_all('SELECT * FROM '+table_id))

    reply_text = 'Daftar kehadiran sementara:\n'
    attedants_reply_msg = ""
    
    for i in range(5, len(attedants_list)):
        indexx = i-3
        attedants_reply_msg += "\n" + str(attedants_list[i])
        print(str(indexx) + ". ", attedants_list[i])

    reply_text += attedants_reply_msg

    reply_msg = TextSendMessage(text=reply_text)
    return reply_msg



