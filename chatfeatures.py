from random import randint
from linebot.models import (
    TextSendMessage, TemplateSendMessage,
    CarouselColumn, CarouselTemplate, ConfirmTemplate,
    URITemplateAction, PostbackTemplateAction, MessageTemplateAction,
    LocationSendMessage, LocationMessage, PostbackAction, URIAction, MessageAction,
    ImageSendMessage, ButtonsTemplate
)
from utility import line_bot_api
import feature_chatai
import feature_utils
from bs4 import BeautifulSoup
import re
import requests
import datetime
import time
import contextlib
import public_vars
import linebot.exceptions
import aryanltk
import time
import datetime
import feature_cv

aimode = False
helptext = """=== SKAKMAT-AI ===
||  /help
||  /help absen
||  /tentang
||  /iq (nama orang)
||  /jadwal
||  /chatmode (on/off)
||  /love (orang1, orang2)
||  /wikipedia (search...)
||  /grafik (ax + by = c)
||  /checkuserid (line_api_id) atau /id
||  /screenshot (www.alamat.web)
||  /instagram (username)
||  /catur atau /catur online link
||  
||  BARU! 
||  /analisisfoto (on/off)
||
||  Tip: masukkan perintah diawali
||  garis miring (/) dan huruf kecil
=================="""

absenhelptext = """ Help: Absen

Untuk menggunakan fitur absen, pastikan Anda sudah menambahkan skakmat.ai sebagai teman anda.

/help absen - Memunculkan pesan bantuan absen

/absen (01/12/2000) (keterangan) - Merencanakan absen baru (maksimal 4 absen yang bisa dijalankan)
Contoh: /absen 12/04/2019 Ultah arya ke-17

/daftarabsen - Memunculkan menu daftar absen yang sedang berjalan

/daftarkehadiran - Memunculkan menu daftar absen yang sedang berjalan beserta data kehadiran dari absen yang dipilih

(/daftarabsen dan /daftarkehadiran berguna jika Anda berubah pikiran mengenai absen)


/hapusabsen - Memunculkan menu untuk memilih daftar absen yang akan dihapus

/absengrup - Memunculkan menu untuk mendaftarkan seluruh anggota grup untuk berpartisipasi terhadap absen yang dipilih

(Saat ini perintah /absengrup dan #absengrup sedang dalam perbaikan)

Anda bisa memanggil perintah-perintah tersebut di grup atau multichat.
"""


def textreply(event, message):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=message))

def imgreply(event, imgurl):
    line_bot_api.reply_message(
        event.reply_token,
        ImageSendMessage(
            original_content_url=imgurl,
            preview_image_url=imgurl
        ), timeout=None)

def imgpush(target, imgurl):
    line_bot_api.push_message(
        target,
        ImageSendMessage(
            original_content_url=imgurl,
            preview_image_url=imgurl
        ), timeout=None)

def getUserId(event):
    profile = line_bot_api.get_profile(event.source.user_id)
    return profile
    
# Get Push ID
def getPushId(event):
    absen_group = ''
    try:
        profile = line_bot_api.get_group_member_profile(event.source.group_id, event.source.user_id)
        absen_group = str(event.source.group_id)
    except AttributeError:
        try:
            profile = line_bot_api.get_room_member_profile(event.source.room_id, event.source.user_id)
            absen_group = str(event.source.room_id)
        except AttributeError:
            profile = line_bot_api.get_profile(event.source.user_id)
            absen_group = str(event.source.user_id)
            # texterror = TextSendMessage(text='Untuk dapat menggunakan absen, Anda harus menambahkan skakmat.ai sebagai teman terlebih dahulu.')
        except linebot.exceptions.LineBotApiError:
            profile = line_bot_api.get_profile(event.source.user_id)
            absen_group = str(event.source.user_id)
    except linebot.exceptions.LineBotApiError:
        try:
            profile = line_bot_api.get_room_member_profile(event.source.room_id, event.source.user_id)
            absen_group = str(event.source.room_id)
        except AttributeError:
            profile = line_bot_api.get_profile(event.source.user_id)
            absen_group = str(event.source.user_id)
        except linebot.exceptions.LineBotApiError:
            profile = line_bot_api.get_profile(event.source.user_id)
            absen_group = str(event.source.user_id)

    try:
        profile = line_bot_api.get_group_member_profile(event.source.group_id, event.source.user_id)
        absen_group = str(event.source.group_id)
    except AttributeError:
        try:
            profile = line_bot_api.get_room_member_profile(event.source.room_id, event.source.user_id)
            absen_group = str(event.source.room_id)
        except AttributeError:
            profile = line_bot_api.get_profile(event.source.user_id)
            absen_group = str(event.source.user_id)

    return absen_group

def log(event):
    curtime = time.time() + (3600 * 7)
    curtime = datetime.datetime.utcfromtimestamp(curtime).strftime("%d/%m/%Y %H:%M")

    user_msg = event.message.text
    user_id = line_bot_api.get_profile(event.source.user_id)
    user_group = getPushId(event)
    user_name = user_id.display_name

    log_msg = '\n[{}] ({}){}:{}: {}'.format(curtime, user_group, user_id.user_id, user_name, user_msg)
    log_file = open('static/log.txt', 'a')
    log_file.write(log_msg)

def phrases(event):
    msg = str(event.message.text)

    if msg.startswith('/') or msg.startswith('#'):
        return

    p_file = open('static/phrases.txt', 'a')
    p_file.write('\n' + msg)

# /help /trombosit
def help(event):
    msg = event.message.text
    if msg == "/help":
        textreply(event, helptext)
    elif msg == "/skakmat":
        textreply(event, 'Skakmat AI (Artificial Intelligence) adalah Kecerdasan Buatan berbasis LINE yang dibuat oleh seseorang dari kelas IPS. \n \n' + helptext)
    elif msg == "/help absen":
        textreply(event, absenhelptext)
    return



imgmode = False
# image related
def img(event):
    global imgmode

    print('\n\n Event MSG \n\n', event.message)

    if(event.message.type == 'image' and imgmode is True):
        print('\nEvent Dict: \n', event.__dict__)
        print('\nEvent source: \n', event.source.__dict__)
        print('\nEvent: \n', event)

        message_content = line_bot_api.get_message_content(event.message.id)

        with open('static/res/temp_cv_img.png', 'wb') as fd:
            for chunk in message_content.iter_content():
                fd.write(chunk)

        currentDate = str(datetime.datetime.now().time())
        datenow = currentDate.replace(":","")

        file_name = 'cv_' + datenow +'.png'
        file_url = public_vars.HOST_PUBLIC_URL + '/rout/' + file_name

        feature_cv.detect_object(file_name)

        imgreply(event, file_url)

# /chatmode on/off     
def aimodeon(event):
    global aimode
    global imgmode

    msg = event.message.text

    if msg == "/analisisfoto on":
        imgmode = True
        textreply(event, 'Mode analisis foto aktif. Silahkan kirim pesan foto untuk dianalisis.')
    elif msg == "/analisisfoto off":
        imgmode = False
        textreply(event, 'Mode analisis foto telah dinonaktifkan.')

    if msg == "/chatmode on":
        aimode = True
        textreply(event, "Chatting mode on. Bot akan membalas pesan melalui algoritma Machine Learning.")
    elif msg == "/chatmode off":
        aimode = False
        textreply(event, "Chatting mode off.")

# /push (msg)
def push(event):
    msg = str(event.message.text)
    if msg.startswith('/push '):
        msg = msg.replace('/push ', '')
        to = msg.split(' ')
        msg = ' '.join(to[1:])

        if to[0] == 'kage':
            to[0] = 'Cff038353c82adb84ee137cc8775f7e2f'
        elif to[0] == 'checkmate':
            to[0] = 'C842bd66f34c7fb8352325fe2ed23dfa5'

        line_bot_api.push_message(to[0], TextSendMessage(msg))

# /checkuserid
def checkuserid(event):
    msg = str(event.message.text)
    if (msg.startswith('/checkuserid ')):
        msg = msg.replace("/checkuserid ", "")
        
        # groupid = event.source.group_id
        userid = msg
        print(userid)

        profile = line_bot_api.get_profile(userid)
        message = "LINE_API_ID: \n" + profile.user_id + "\n\nName: \n" + profile.display_name + "\n\nProfile Picture URL: \n" + profile.picture_url + "\n\nStatus Message: \n" + profile.status_message
        textreply(event, message)

    if (msg == '/id'):
        profile = line_bot_api.get_profile(event.source.user_id)
        message = "LINE_API_ID: \n" + profile.user_id + "\n\nName: \n" + profile.display_name + "\n\nProfile Picture URL: \n" + profile.picture_url + "\n\nStatus Message: \n" + profile.status_message
        textreply(event, message)

# /chess atau /catur
def chess(event):
    msg = str(event.message.text)

    if msg == "/catur" or msg == "/chess":
        print('Chess command triggered')
        url = public_vars.HOST_FRONTEND_URL + '/chessai'
        chess_template = TemplateSendMessage(
            alt_text='Pesan Catur',
            template=ButtonsTemplate(
                title='Bermain Catur',
                text='Silahkan pilih mode permainan dibawah.',
                actions=[
                    URIAction(
                        label='VS Bot (Offline)',
                        uri=url
                    ),
                    MessageAction(
                        label='Online Multiplayer',
                        text='/catur online'
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, chess_template)
        return
    
    if msg.startswith("/catur online"):
        id_gen = '123456789'
        id = ''
        for i in range(5):
            id += id_gen[randint(0,8)]
        url_id = 'Klik LINK (biru) dibawah untuk mulai bermain: \n' + public_vars.HOST_FRONTEND_URL + ':3000/room/' + id
        url = public_vars.HOST_FRONTEND_URL + ':3000/room/' + id
        chess_template = TemplateSendMessage(
            alt_text='Pesan Catur',
            template=ButtonsTemplate(
                title='Ruang Catur: ' + id,
                text='Telah dibuat ruang pertandingan catur. Silahkan bergabung.',
                actions=[
                    URIAction(
                        label='Gabung',
                        text='Saya ingin bergabung catur: ' + id,
                        uri=url
                    )
                ]
            )
        )
        if 'url' in msg or 'link' in msg:
            textreply(event, url_id)
            return
        line_bot_api.reply_message(event.reply_token, chess_template)

# /tentang
def creator(event):
    msg = event.message.text

    if msg == "/tentang":
        # line_bot_api.reply_message(event.reply_token, buttons_template_message)
        textreply(event, "Skakmat AI (Artificial Intelligence) adalah Kecerdasan Buatan berbasis LINE yang dibuat oleh seseorang dari kelas IPS.")
    elif msg == "/jadwal":
        imgreply(event, public_vars.HOST_PUBLIC_URL + '/static/jadwal.jpg')
    return


def reply(msgserv):
    return msgserv

def aireply(event):
    msg = event.message.text
    global aimode
    if aimode:
        airesponse = aryanltk.chat(msg)
        textreply(event, str(airesponse))
    
# /love
def love(event):
    msg = str(event.message.text)
    if msg.startswith("/love "):
        
        proceedmsg = msg.replace("/love ", "").split(",")
        int_love = randint(0,100)
        replystring = "Hasil percintaan: \n" + proceedmsg[0] + " &" + proceedmsg[1] + " adalah " + str(int_love) + "%"
        textreply(event, replystring)
        # print(replystring)

    if msg.startswith("/iq "):
        msgnolow = msg.replace('/iq ', '')
        msg = msgnolow.lower()

        iq = randint(85, 126)

        if('faisal' in msg):
            iq = 129
        if('arya' in msg):
            iq = 83
        if('einstein' in msg):
            iq = 200

        if('rare' in msg):
            iq += randint(2, 11)
            msgnolow = msgnolow.replace('rare', '')
        elif('epic' in msg):
            iq += randint(5, 26)
            msgnolow = msgnolow.replace('epic', '')
        elif('legendary' in msg):
            iq += randint(11, 36)
            msgnolow = msgnolow.replace('legendary', '')
        elif('gifted' in msg):
            iq += randint(11, 36)
            msgnolow = msgnolow.replace('gifted', '')
        elif('genius' in msg):
            iq += randint(15, 45)
            msgnolow = msgnolow.replace('genius', '')
        elif('prodigy' in msg):
            iq += randint(21, 51)
            msgnolow = msgnolow.replace('prodigy', '')

        textreply(event, 'IQ dari '+msgnolow+': '+str(iq))

# /wikipedia
def wiki(event):
    msg = str(event.message.text)
    if msg.startswith("/wikipedia"):

        cleanmsg = msg.replace("/wikipedia","")
        replystring = str(feature_utils.wikipedia_search(cleanmsg))
        textreply(event, replystring)

# /screenshot
# /instagram
def webss(event):
    msg = str(event.message.text)

    if msg.startswith("/screenshot") or msg.startswith("/instagram"):
        currentDate = str(datetime.datetime.now().time())
        datenow = currentDate.replace(":","")

        # temp_f = open('static/rout/'+datenow+'.png', 'w+')
        # temp_f.write('#')

        file_name = 'ss_' + datenow +'.png'
        file_url = public_vars.HOST_PUBLIC_URL + '/rout/' + file_name

        if feature_utils.ssweb(msg, file_name) is None:
            textreply(event, 'Error saat melakukan screenshot. Silahkan coba lagi.')
            return

        imgreply(event, file_url)
        print(file_name, file_url)

# /grafik 
bukanUjian = True
def grafik(event):
    global bukanUjian
    msg = str(event.message.text)
    if msg == "/ujian true":
        bukanUjian = False
        textreply(event, "Lagi ujian : ON")
    elif msg == "/ujian false":
        bukanUjian = True
        textreply(event, "Lagi ujian : OFF")
    if bukanUjian:
        if msg.startswith("/grafik"):
            msg.replace("/grafik", "")

            print("Command is", msg)
            fileurl = feature_utils.plot(msg)
            time.sleep(2)
            print("File url is", fileurl)

            if fileurl is not None:
                imgreply(event, fileurl)
            else:
                textreply(event, "Tolong masukkan dengan format: \n /grafik ax + by = c \n Contoh: \n /grafik 1x + 2y = 6")
    else:
        if msg.startswith("/grafik"):
            textreply(event, "Lagi ujian cuk, anda tercyduk!!")

# /berita
# def berita(event):
#     msg = str(event.message.text)
#     if msg == "/berita":
        # columns = [_news_carousel(entry) for entry in feature_utils.google_news()]

        # # Carousel template is accepted until 5 columns.
        # # See https://devdocs.line.me/ja/#template-message
        # columns = [c for c in columns if c is not None][:5]

        # carousel_template_message = TemplateSendMessage(
        #     alt_text="Berita hari ini \n Pesan tidak dapat dilihat",
        #     template=CarouselTemplate(columns=columns)
        # )
        # line_bot_api.reply_message(event.reply_token, carousel_template_message)


absen_name = ""
absen_group = None
def absen(event):

    msg = str(event.message.text)
    global absen_name

    if (msg.startswith('/absen ')):

        global absen_group
        absen_group = None

        try:
            profile = line_bot_api.get_group_member_profile(event.source.group_id, event.source.user_id)
            absen_group = str(event.source.group_id)
        except AttributeError:
            try:
                profile = line_bot_api.get_room_member_profile(event.source.room_id, event.source.user_id)
                absen_group = str(event.source.room_id)
            except AttributeError:
                profile = line_bot_api.get_profile(event.source.user_id)
                absen_group = str(event.source.user_id)
                # texterror = TextSendMessage(text='Untuk dapat menggunakan absen, Anda harus menambahkan skakmat.ai sebagai teman terlebih dahulu.')
            except linebot.exceptions.LineBotApiError:
                profile = line_bot_api.get_profile(event.source.user_id)
                absen_group = str(event.source.user_id)
        except linebot.exceptions.LineBotApiError:
            try:
                profile = line_bot_api.get_room_member_profile(event.source.room_id, event.source.user_id)
                absen_group = str(event.source.room_id)
            except AttributeError:
                profile = line_bot_api.get_profile(event.source.user_id)
                absen_group = str(event.source.user_id)
            except linebot.exceptions.LineBotApiError:
                profile = line_bot_api.get_profile(event.source.user_id)
                absen_group = str(event.source.user_id)

        try:
            profile = line_bot_api.get_group_member_profile(event.source.group_id, event.source.user_id)
            absen_group = str(event.source.group_id)
        except AttributeError:
            try:
                profile = line_bot_api.get_room_member_profile(event.source.room_id, event.source.user_id)
                absen_group = str(event.source.room_id)
            except AttributeError:
                profile = line_bot_api.get_profile(event.source.user_id)
                # absen_group = str(event.source.user_id)

        if event.source.user_id is None:
            textreply(event, 'Mohon tambah \'skakmat.ai\' sebagai teman terlebih dahulu. \nAbsen tidak dapat bekerja di LINE Lite. ')
            return
        absen_name = str(profile.display_name)

        absen_msg = feature_utils.check_string(msg)
        
        if (absen_msg == str('date_below')):
            textreply(event, 'Kesalahan: Penanggalan tidak boleh menuju masa lampau.')
        elif (absen_msg == str('format_error')):
            textreply(event, 'Kesalahan pada format penanggalan. Silahkan lakukan penanggalan sesuai contoh.\n\nContoh: /absen 17/08/2019 Upacara')
        elif (absen_msg == str('kejauhan')):
            textreply(event, 'Kesalahan: Penanggalan yang diberikan terlalu jauh.')
        elif (absen_msg == str('kepanjangan')):
            textreply(event, 'Kesalahan: Keterangan terlalu panjang.')
        elif (absen_msg == str('more_than_4')):
            textreply(event, 'Kesalahan: Daftar absen sudah mencapai batas maksimum (4).')
        elif (absen_msg == str('table_existed')):
            textreply(event, 'Kesalahan: Sudah ada jadwal di tanggal yang sama.')
        elif (absen_msg == 'pass'):
            absen_reply = feature_utils.absen(msg)
            line_bot_api.reply_message(event.reply_token, absen_reply)
            absen_group = None
        else:
            textreply(event, 'Telah terjadi kesalahan. Silahkan coba lagi dengan format yang disesuaikan. \n\nContoh: /absen 17/08/2019 Upacara')
    

    if (msg.startswith('/hapusabsen')):

        jumlah_absen = feature_utils.sqlite_count_table()

        if (jumlah_absen <= 0):
            textreply(event, 'Kesalahan: Jadwal absensi kosong. Tidak ada yang bisa dihapus.')
        else:
            hapus_absen_reply = feature_utils.delete_absen()
            line_bot_api.reply_message(event.reply_token, hapus_absen_reply)


    if (msg.startswith('/daftarkehadiran')):

        jumlah_absen = feature_utils.sqlite_count_table()

        if (jumlah_absen <= 0):
            textreply(event, 'Kesalahan: Jadwal absensi kosong. Tidak ada yang bisa dilihat.')
        else:
            daftar_absen_reply = feature_utils.daftar_absen()
            line_bot_api.reply_message(event.reply_token, daftar_absen_reply)

    if (msg.startswith('/daftarabsen')):

        jumlah_absen = feature_utils.sqlite_count_table()

        if (jumlah_absen <= 0):
            textreply(event, 'Kesalahan: Jadwal absensi kosong. Tidak ada yang bisa dilihat.')
        else:
            daftar_absen_reply = feature_utils.daftar_absen_carousel()
            line_bot_api.reply_message(event.reply_token, daftar_absen_reply)

    if (msg.startswith('/absengrup')):
        jumlah_absen = feature_utils.sqlite_count_table()

        return

        if (jumlah_absen <= 0):
            textreply(event, 'Kesalahan: Jadwal absensi kosong. Tidak ada yang bisa dilihat.')
        else:
            daftar_absen_grup_reply = feature_utils.absengrup()
            line_bot_api.reply_message(event.reply_token, daftar_absen_grup_reply)
            

    if (msg.startswith('#hapusabsen ')):

        absen_data_id = feature_utils.hapus_absen(msg)

        if absen_data_id == 'table_not_found':
            textreply(event, 'Tidak dapat menemukan data tersebut. Gunakan /hapusabsen')
        else:
            textreply(event, 'Berhasil menghapus data absen dengan id ' + absen_data_id)

    if (msg.startswith('#absen ')):

        try:
            profile = line_bot_api.get_group_member_profile(event.source.group_id, event.source.user_id)
        except AttributeError:
            try:
                profile = line_bot_api.get_room_member_profile(event.source.room_id, event.source.user_id)
            except AttributeError:
                profile = line_bot_api.get_profile(event.source.user_id)
                # texterror = TextSendMessage(text='Untuk dapat menggunakan absen, Anda harus menambahkan skakmat.ai sebagai teman terlebih dahulu.')
            except linebot.exceptions.LineBotApiError:
                profile = line_bot_api.get_profile(event.source.user_id)
        except linebot.exceptions.LineBotApiError:
            try:
                profile = line_bot_api.get_room_member_profile(event.source.room_id, event.source.user_id)
            except AttributeError:
                profile = line_bot_api.get_profile(event.source.user_id)
            except linebot.exceptions.LineBotApiError:
                profile = line_bot_api.get_profile(event.source.user_id)

        if event.source.user_id is None:
            textreply(event, 'Mohon tambah \'skakmat.ai\' sebagai teman terlebih dahulu. \nAbsen tidak dapat bekerja di LINE Lite. ')
            return
        absen_name = str(profile.display_name)

        checkmsg = msg.replace('#absen ', '')
        checkmsg = checkmsg.split(' ')
        checkmsg = 'abs_'+checkmsg[0]

        if not(feature_utils.sqlite_check_table(checkmsg)):
            textreply(event, 'Kesalahan: Tidak ada daftar absen dengan id tersebut. \nGunakan /daftarabsen atau /daftarkehadiran')
        else:
            text_reply = feature_utils.kehadiran(msg)
            textreply(event, text_reply)

    if msg.startswith('#daftarkehadiran '):
        checkmsg = msg.replace('#daftarkehadiran ', '')
        checkmsg = 'abs_'+checkmsg

        if not(feature_utils.sqlite_check_table(checkmsg)):
            textreply(event, 'Kesalahan: Tidak ada daftar absen dengan id tersebut. \nGunakan /daftarabsen atau /daftarkehadiran')
        else:
            daftar_absen_reply = feature_utils.daftarabsen(msg)
            daftar_kehadiran_reply = feature_utils.daftarkehadiran(msg)
            line_bot_api.reply_message(event.reply_token, [daftar_absen_reply, daftar_kehadiran_reply])

    if msg.startswith('#absengrup '):
        checkmsg = msg.replace('#absengrup ', '')
        checkmsg = 'abs_'+checkmsg

        return

        if not(feature_utils.sqlite_check_table(checkmsg)):
            textreply(event, 'Kesalahan: Tidak ada daftar absen dengan id tersebut.')
        else:

            try:
                member_ids_res = line_bot_api.get_group_member_ids(event.source.group_id)
            except AttributeError:
                try:
                    member_ids_res = line_bot_api.get_room_member_ids(event.source.room_id)
                except AttributeError:
                    textreply(event, 'Tidak bisa dilakukan di personal chat')
                    return

            member_ids_res = line_bot_api.get_group_member_ids(event.source.group_id)

            print(member_ids_res.member_ids)
            print(member_ids_res.next)

            absen_msg = feature_utils.kehadirangrup(msg)
            absen_grup_kehadiran = feature_utils.isikehadirangrup(msg)
            line_bot_api.reply_message(event.reply_token, [absen_msg, absen_grup_kehadiran])
        

        
    # line_bot_api.push_message("U748bf57240b557199324942eb432f2b4", TextSendMessage(text='Hello World!'))
    # Ud7804103c2edcf6fae6e0e9b138d0db9

