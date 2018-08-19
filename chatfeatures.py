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


aimode = False
helptext = """===== SKAKMAT-AI V1.01 ========
||  /help
||  /help absen
||  /tentang
||  /iq (nama orang)
||  /jadwal *Mapel XI IPS 2
||  /chatmode (on/off)
||  /love (orang1, orang2)
||  /wikipedia (search...)
||  /grafik (ax + by = c)
||  /screenshot (web url)
||  /instagram (username)
||
||  Tip: masukkan perintah diawali
||  garis miring (/) dan huruf kecil
=============================="""

absenhelptext = """ Help: Absen

Untuk menggunakan fitur absen, pastikan Anda sudah menambahkan skakmat.ai sebagai teman anda.

/help absen - Memunculkan pesan bantuan absen

/absen (01/12/2000) (keterangan) - Merencanakan absen baru (maksimal 4 absen yang bisa dijalankan)
Contoh: /absen 12/04/2019 Ultah arya ke-17

/daftarabsen - Memunculkan menu daftar absen yang sedang berjalan

/daftarkehadiran - Memunculkan menu daftar absen yang sedang berjalan beserta data kehadiran dari absen yang dipilih

/hapusabsen - Memunculkan menu untuk memilih daftar absen yang akan dihapus

/absengrup - Memunculkan menu untuk mendaftarkan seluruh anggota grup untuk berpartisipasi terhadap absen yang dipilih
(Saat ini perintah /absengrup dan #absengrup sedang dalam perbaikan)

Anda bisa memanggil perintah-perintah tersebut di grup, multichat atau personal chat.
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
        ))

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


# /tentang
def creator(event):
    msg = event.message.text

    if msg == "/tentang":
        # line_bot_api.reply_message(event.reply_token, buttons_template_message)
        textreply(event, "Skakmat AI (Artificial Intelligence) adalah Kecerdasan Buatan berbasis LINE yang dibuat oleh seseorang dari kelas IPS.")
    elif msg == "/jadwal":
        imgreply(event, public_vars.HOST_PUBLIC_URL + '/static/jadwal.jpg')
    return

# /chatmode on/off     
def aimodeon(event):
    global aimode
    msg = event.message.text
    if msg == "/chatmode on":
        
        aimode = True
        textreply(event, "Chatting mode on")
    elif msg == "/chatmode off":
        
        aimode = False
        textreply(event, "Chatting mode off")

def reply(msgserv):
    return msgserv

def aireply(event):
    msg = event.message.text
    global aimode
    if aimode:
        airesponse = feature_chatai.chat(msg)
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

        iq = randint(81, 121)

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
        wFile = feature_utils.ssweb(msg)
        if wFile is not None:
         
            print("IMG File is:", wFile)

            time.sleep(2)
            
            imgreply(event, wFile)
            
        else:
            textreply(event, "Screenshot gagal, cobalah untuk screenshot ulang.")

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

# /checkuserid
def checkuserid(event):
    msg = str(event.message.text)
    if (msg.startswith('/checkuserid')):
        msg_clear = msg.replace("/checkuserid", "")
        msg_final = msg_clear.replace(" ", "")
        
        # groupid = event.source.group_id
        userid = msg_final
        print(userid)

        profile = line_bot_api.get_profile(userid)
        message = "UserID: " + profile.user_id + "\nName: " + profile.display_name + "\nPic URL: " + profile.picture_url + "\n Status: " + profile.status_message
        textreply(event, message)


absen_name = ""
def absen(event):

    msg = str(event.message.text)


    if (msg.startswith('/absen ')):

        try:
            profile = line_bot_api.get_group_member_profile(event.source.group_id, event.source.user_id)
        except AttributeError:
            try:
                profile = line_bot_api.get_room_member_profile(event.source.room_id, event.source.user_id)
            except AttributeError:
                profile = line_bot_api.get_profile(event.source.user_id)

        global absen_name
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
        else:
            textreply(event, 'Telah terjadi kesalahan. Silahkan coba lagi dengan format yang disesuaikan. \n\nContoh: /absen 17/08/2019 Upacara')
    

    if (msg.startswith('/hapusabsen')):

        jumlah_absen = feature_utils.sqlite_count_table()

        if (jumlah_absen == 0):
            textreply(event, 'Kesalahan: Jadwal absensi kosong. Tidak ada yang bisa dihapus.')
        else:
            hapus_absen_reply = feature_utils.delete_absen()
            line_bot_api.reply_message(event.reply_token, hapus_absen_reply)


    if (msg.startswith('/daftarkehadiran')):

        jumlah_absen = feature_utils.sqlite_count_table()

        if (jumlah_absen == 0):
            textreply(event, 'Kesalahan: Jadwal absensi kosong. Tidak ada yang bisa dilihat.')
        else:
            daftar_absen_reply = feature_utils.daftar_absen()
            line_bot_api.reply_message(event.reply_token, daftar_absen_reply)

    if (msg.startswith('/daftarabsen')):

        jumlah_absen = feature_utils.sqlite_count_table()

        if (jumlah_absen == 0):
            textreply(event, 'Kesalahan: Jadwal absensi kosong. Tidak ada yang bisa dilihat.')
        else:
            daftar_absen_reply = feature_utils.daftar_absen_carousel()
            line_bot_api.reply_message(event.reply_token, daftar_absen_reply)

    if (msg.startswith('/absengrup')):
        jumlah_absen = feature_utils.sqlite_count_table()

        if (jumlah_absen == 0):
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

        global absen_name
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

