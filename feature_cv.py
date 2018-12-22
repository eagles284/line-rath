from os import walk
import numpy as np
import cv2
import face_recognition
from random import randint

img_dir = 'static/res/temp_cv_img.png'

# TODO: What will you do for PEOPLE FACE recognition?

# What haars you want to use for object detection?
haars = ['haar/haarcascade_upperbody.xml',
         'haar/haarcascade_fullbody.xml']

labels = ['Orang',
          'Orang']


def bgrRandom():
    bgr = [
        [255,0,0], [0,255,0], [0,0,255],
        [0,128,255], [0,255,128], [128,255,0],
        [255,255,0],[255,0,255], [127,0,255], 
        [255,0,127],[102,178,255], [255,178,102]]

    return bgr[randint(0, len(bgr)-1)]

def increase_brightness(img, value=30):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)

    lim = 255 - value
    v[v > lim] = 255
    v[v <= lim] += value

    final_hsv = cv2.merge((h, s, v))
    img = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
    return img


ANALYZE_IMG = None

def face_cascade(bgr=bgrRandom(), scale=1.3, imgdir=img_dir):
    global ANALYZE_IMG

    print('Processing face')

    image = face_recognition.load_image_file(img_dir)

    faces = face_recognition.face_locations(image)

    if ANALYZE_IMG is None:
        img = cv2.imread(imgdir)
    else:
        img = ANALYZE_IMG
    
    for (h, w, y, x) in faces:
        font = cv2.FONT_HERSHEY_PLAIN

        # Init_x, Init, y, Font scaling
        # text_attr = [int(x+(1/20*x)), int(y+(1/15*y)), 1/1000*(w+h)]

        # cv2.putText(img, 'WAJAH',(text_attr[0],text_attr[1]), font, text_attr[2], (bgr[0],bgr[1],bgr[2]), 1, cv2.LINE_AA)
        cv2.rectangle(img,(x,y),(w,h),(bgr[0],bgr[1],bgr[2]),int(1/300*(w+h)))

    ANALYZE_IMG = img
    print('Processing face Finished')

def haar_cascade(xml, label, bgr=[255,0,0], scale=1.3, imgdir=img_dir):
    global ANALYZE_IMG

    if ANALYZE_IMG is None:
        img = cv2.imread(imgdir)
    else:
        img = ANALYZE_IMG

    cascade = cv2.CascadeClassifier(xml)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    detections = cascade.detectMultiScale(gray, scale, 5)

    for (x,y,w,h) in detections:
        font = cv2.FONT_HERSHEY_PLAIN

        # Init_x, Init, y, Font scaling
        text_attr = [int(x+(4/100*w)), int(y+(9/100*h)), 1/1000*(2*w+2*h)]

        cv2.putText(img, label,(text_attr[0],text_attr[1]), font, text_attr[2], (bgr[0],bgr[1],bgr[2]), 1, cv2.LINE_AA)
        cv2.rectangle(img,(x,y),(x+w,y+h),(bgr[0],bgr[1],bgr[2]),int(1/100*(2*w+2*h)))

    ANALYZE_IMG = img

def detect_object(filename):
    global ANALYZE_IMG

    face_cascade()

    for haar, label in zip(haars, labels):
        haar_cascade(haar, label, bgrRandom(), 1.3)

    cv2.imwrite('static/rout/' + filename, ANALYZE_IMG)

    ANALYZE_IMG = None