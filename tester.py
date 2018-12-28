import requests
import json

HOST_PUBLIC_URL = 'https://skakmat.ip-dynamic.com:5000'
HOST_API_URL = 'http://skakmat.ip-dynamic.com/rath-api'
HOST_FRONTEND_URL = HOST_PUBLIC_URL


try:
    r = requests.post(HOST_API_URL + '/sender.php')
    j = json.loads(r.text)
    queues = j['queues']

    for q in queues:
        if str(q['id']) == '1':
            requests.post(HOST_API_URL + '/sender.php',
            data={'confirm':0})
            
            msg = '''
            Laptop turned on at {}
            Lat Long: {}
            WiFi: {}
            '''.format(q['time'],
                '%s, %s' % (str(q['location']['lat']), str(q['location']['long'])),
                q['wifi']['current_ssid'])

            print(msg)
            break
except Exception as e:
    print('Error:', e)