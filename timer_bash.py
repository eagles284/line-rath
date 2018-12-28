import time
import sqlite3
import feature_utils
import chatfeatures
import threading
from linebot.models import (
    TextSendMessage, TemplateSendMessage,
    CarouselColumn, CarouselTemplate, ConfirmTemplate,
    URITemplateAction, PostbackTemplateAction, MessageTemplateAction,
    LocationSendMessage, LocationMessage, PostbackAction, URIAction, MessageAction,
    ImageSendMessage, ButtonsTemplate
)
import requests
import json
import public_vars

def getCurrentIndoTime():
    indtime = time.time()
    indtime = indtime + (3600 * 7)

    return int(indtime)

def sendPushMessage(to, message):
    chatfeatures.line_bot_api.push_message(to, message)

active_absens = []

# Dependency
def absenList():
    absens_existence = feature_utils.sqlite_count_table()

    if not (absens_existence <= 0):
        absens_to_check = "SELECT name FROM sqlite_master WHERE type='table'"

        absens = feature_utils.sqlite_select_all(absens_to_check)

        absen_list = []

        for absen in absens:
            absen_list.append(str(absen[0]))
        print('\n\nAbsens from SQL:', absen_list)
        
        return absen_list

def schedule():

    try:
        r = requests.post(public_vars.HOST_API_URL + '/api.php')
        j = json.loads(r.text)
        queues = j['queues']

        for q in queues:
            if str(q['id']) == '1':
                requests.post(public_vars.HOST_API_URL + '/sender.php',
                data={'confirm':1})
                
                msg = '''Laptop turned on at {}\n\nLat Long: {} (2 km accuracy)\nWiFi: {}'''.format(
                    q['time'],
                    '%s, %s' % (str(q['location']['lat']), str(q['location']['long'])),
                    q['wifi']['current_ssid'])

                #  line api stuff
                sendPushMessage('U748bf57240b557199324942eb432f2b4', TextSendMessage(text=msg))
                break
    except Exception as e:
        print('JSON Error:', e)

def scheduleAbsen(absen_id):
    print('Scheduling absen notifier for', absen_id)
    absen_data = feature_utils.sqlite_select_all('SELECT val FROM '+absen_id)

    data_absen = []
    for data in absen_data:
        data_absen.append(data[0])
    print(data_absen)

    currentTime = getCurrentIndoTime()
    targetTime = int(data_absen[0])
    targetTime += 7200
    reminderTime = targetTime - (3600 * 11)
    print('Now scheduling', absen_id)
    print('Current Time: ', currentTime)
    print('Target Time: ', targetTime)

    reminder_msg = 'Daftar Kehadiran: '
    dead_msg = 'Daftar kehadiran terakhir untuk absen ' + data_absen[3] + ' yang direncanakan pada ' + data_absen[2] + ':\n'

    data_kehadiran = feature_utils.sqlite_select_all('SELECT * FROM '+absen_id)
    datak = []
    for data in data_kehadiran:
        datak.append(data[0] +', ' + data[1])
    print(datak)


    for attedants in range(6, len(data_kehadiran)):
        reminder_msg += '\n' + str(attedants-5)+'. '+ datak[attedants]
        dead_msg += '\n' + str(attedants-5)+'. '+ datak[attedants]
    
    reminder_msg = reminder_msg.replace('(', '')
    reminder_msg = reminder_msg.replace(')', '')

    dead_msg = dead_msg.replace('(', '')
    dead_msg = dead_msg.replace(')', '')

    dead_msg += '\n\nData absen tersebut akan dihapus.'

    absen_template = TemplateSendMessage(
        alt_text='Pesan Pengingat Absen',
        template=ButtonsTemplate(
            title='Pengingat Absen: '+ str(data_absen[2]),
            text=str(data_absen[3]) + "(oleh "+str(data_absen[4])+")",
            actions=[
                MessageAction(
                    label='Hadir',
                    text='#absen '+str(data_absen[1])+' Hadir'
                ),
                MessageAction(
                    label='Tidak Hadir',
                    text='#absen '+str(data_absen[1])+' Tidak_Hadir'
                ),
                MessageAction(
                    label='Izin',
                    text='#absen '+str(data_absen[1])+' Izin'
                ),
                MessageAction(
                    label='Sakit',
                    text='#absen '+str(data_absen[1])+' Sakit'
                ),
            ]
        )
    )

    

    ### FOR TEST PURPOSE ###
    # currentTime = reminderTime + 2

    # IF REMINDER TIME HITS
    if (currentTime >= reminderTime and currentTime <= (reminderTime + 600)):

        # Send Reminder MSG
        print('Sending reminder msg for id', data_absen[1])
        sendPushMessage(data_absen[5], [absen_template, TextSendMessage(str(reminder_msg))])

    # IF REMINDER 2 TRIGGERED
    if (currentTime >= (targetTime-7200) and currentTime <= (targetTime-6600)):
        
        # Send Reminder MSG
        print('Sending reminder msg for id', data_absen[1])
        sendPushMessage(data_absen[5], [absen_template, TextSendMessage(str(reminder_msg))])

    # IF ABSEN IS GOING TO 'DEAD'
    if (currentTime >= targetTime):

        # Send Final Push MSG Here!!!
        print('Sending dead msg and deleting', data_absen[1])
        sendPushMessage(data_absen[5], TextSendMessage(str(dead_msg)))

        # Delete the absen from DB
        feature_utils.sqlite_query('DROP TABLE IF EXISTS abs_'+ str(data_absen[1]))

schedule()
exit()


