import time
import sched
import sqlite3
import asyncio
import feature_utils
import chatfeatures
import threading

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

def checkAbsens():
    global active_absens

    """ Check:
    if Absen is already existed in [active_absens], do NOT add to while loop
    if Absen is NOT existed in [active_absens], add into while loop """

    for absen in absenList():
        if absen in active_absens:
            print(absen, 'is already existed. Not inserting this into active absens')
        else:
            active_absens.append(absen)
    pass
    print('Current Active Absens:', active_absens)

    return

def checkPerAbsen(absen_id):
    if (absen_id in active_absens):
        return True
    return False

def checkIfAbsenDeleted(absen_id):
    tempAbsens = absenList()

    if absen_id not in tempAbsens:
        active_absens.remove(absen_id)
        print(absen_id, 'is deleted by user. Deleting from active list')
        return True
    else:
        return False

exitFlag = 0
class myThread (threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        
    def run(self):
        scheduleAbsen(self.name)

def schedule():

    i = 0
    thread = []
    for absen in absenList():
        # if absen not in active_absens:
        # print('Absen', absen, 'isnt exist, adding to thread')
        # active_absens.append(absen)
        # thread.append(myThread(i, absen))
        # thread[i].start()
        # print('thread', i)
        scheduleAbsen(absen)
        i = i + 1
        

def scheduleAbsen(absen_id):
    print('Scheduling absen notifier for', absen_id)
    absen_data = feature_utils.sqlite_select_all('SELECT val FROM '+absen_id)

    data_absen = []
    for data in absen_data:
        # print(data[0])
        data_absen.append(data[0])

    targetTime = int(data_absen[0])
    # print('Data:', data_absen)
    # print('Target Time:', targetTime)

    
    # while True:

    # if(checkIfAbsenDeleted(absen_id)):
    #     print('Absen not exist. Stopping')
    #     break
    # else:
    #     print('Absen is still exist.')

    # print(absenList())
    
    currentTime = getCurrentIndoTime()
    
    print(absen_id)
    print('Current Time: ', currentTime)
    print('Target Time: ', targetTime)

    if (currentTime >= targetTime):

        # Send Push MSG Here!!!
        print('booh!!!')

        # Delete the absen from DB
    
    # time.sleep(5)

# time.sleep(10)
schedule()



# sendPushMessage('U748bf57240b557199324942eb432f2b4', chatfeatures.TextSendMessage(text='Woi, dikirim darii 2nd file!!'))



