#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
__author__ = 'Ahmad Abdulnasir Shu'aib <me@ahmadabdulnasir.com.ng>'
__homepage__ = https://ahmadabdulnasir.com.ng
__copyright__ = 'Copyright (c) 2019, salafi'
__version__ = "0.01t"
"""

import cv2
import os
from datetime import  datetime as dtime
from threading import Thread
from . import face_track
'''constants declaration '''
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Setting database file to use
faceCascade_file = os.path.join(BASE_DIR, "haarcascade_frontalface_default.xml")
''' ./constants declaration'''

# haarcascade_frontalface_default
# haarcascade_profileface
# haarcascade_frontalcatface_extended
# haarcascade_frontalface_default
# haarcascade_upperbody
# Create the haar cascade
faceCascade = cv2.CascadeClassifier(faceCascade_file)
PEOPLE = ['010EEP', 'bata', 'diya', 'hassan', 'nd003', 'nd007', 'nd010', 'nur', 'umar_z', 'abatcha', 'buddy', 'eeeguy', 'HAUWA', 'nd004', 'nd008', 'nd011', 'salafi', 'yeima', 'abbah', 'calculus', 'Friend', 'kalli', 'nd005', 'nd009', 'nd012', 'shelden', 'bakura', 'chairmo', 'geidam', 'nd002', 'nd006', 'nd01', 'nd013', 'shittu']
# x = threading.Thread(target=thread_function, args=(1,), daemon=True)
class PredictionThread(Thread):

    def __init__(self):
        Thread.__init__(self)
        self.daemon = True
        self.images = list()
        self.img = None
        self.working = True
        # self.reg_pipe = face_track.preditFace

    def run(self):
        print('[INFO]: Starting Prediction Thread')
        while True:
            result = face_track.preditFace(self.img)
            #{'userid':userid, 'x_min': x_min, 'x_max': x_max, 'y_min': y_min, 'y_max': y_max , 'confidence': msg}
            if result:
                rows = []
                tstp = str(dtime.now().strftime('%d-%b-%H-%Y-%M-%S%p'))
                username = result['userid']
                present = 'Yes'
                date_ = str(dtime.now().strftime('%d_%b_%Y'))
                row = [tstp, username, present, date_]
                print('adding ', row)
                rows.append(row)
                saveRecord(rows)
            print(result)

    def update(self, img):
        self.img = img
        if not self.working:
            self.run()

def locaPredict(img):
    print('[INFO]: Starting Prediction Thread')
    #import face_track
    # while True:
    result = face_track.preditFace(img)
    #{'userid':userid, 'x_min': x_min, 'x_max': x_max, 'y_min': y_min, 'y_max': y_max , 'confidence': msg}
    if result:
        rows = []
        tstp = str(dtime.now().strftime('%d-%b-%H-%Y-%M-%S%p'))
        username = result['userid']
        present = 'Yes'
        date_ = str(dtime.now().strftime('%d_%b_%Y'))
        row = [tstp, username, present, date_]
        print('adding ', row)
        rows.append(row)
        saveRecord(rows)
    print(result)

def draw_box(frame):
    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    today_dir = 'output/'+'{}/'.format(str(dtime.now().strftime('%d_%b_%Y')))
    #output = os.path.join(BASE_DIR, 'output')
    output = 'output'
    frames_dir = today_dir+ 'frames/'
    if not os.path.isdir(output):
        os.mkdir(output)
    if not os.path.isdir(today_dir):
        os.mkdir(today_dir)
    if not os.path.isdir(frames_dir):
        os.mkdir(frames_dir)
    # Detect faces in the image
    faces = faceCascade.detectMultiScale(
    	gray,
    	scaleFactor=1.1,
    	minNeighbors=5,
    	minSize=(30, 30),
    	#flags = cv2.CV_HAAR_SCALE_IMAGE
        )

    # print("Found {0} faces!".format(len(faces)))

    # Draw a rectangle around the faces
    exT = 30
    for (x, y, w, h) in faces:
        x = x - exT
        # y = y - exT
        # w = w + exT
        h = h + exT
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        imgcrop = frame[y:y+h, x:x+w]
        out_file = today_dir+ str(dtime.now().strftime('%d-%b-%H-%M-%s')) +'.png'
        # cv2.imwrite(out_file, imgcrop)
        frame_file = frames_dir +str(dtime.now().strftime('%d-%b-%H-%M-%s')) +'.jpg'
        cv2.imwrite(frame_file, frame)
        # t = PredictionThread().update(out_file)
        # t.run()
        locaPredict(frame_file)

    return gray

header = ['Time Stamp', 'Username', 'Present', 'Date']
def saveRecord(rows):
    import csv
    if not os.path.isfile('Attendance.csv'):
        exit = False
    else:
        exit = True
    with open('Attendance.csv', 'a+', newline="") as f:
        c = csv.writer(f)
        if exit:
            pass
        else:
            c.writerow(header)
        for r in rows:
            c.writerow(r)
    print('*'*20 + ' Done ' + '*'*20)

def tempFunc():
    rows = []
    for ti in range(100):
        tstp = str(dtime.now().strftime('%d-%b-%H-%Y-%M-%S%p'))
        username= 'userid' + str(ti)
        present = 'Yes'
        date_ = str(dtime.now().strftime('%d_%b_%Y'))
        row = [tstp, username, present, date_]
        print('adding ', row)
        rows.append(row)
    saveRecord(rows)

def boot():
    cap = cv2.VideoCapture(0)
    while(True):
    	# Capture frame-by-frame
    	ret, frame = cap.read()

    	img = draw_box(frame)
    	# Display the resulting frame
    	cv2.imshow('frame', img)
    	if cv2.waitKey(1) & 0xFF == ord('q'):
    		break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    boot()
    # tempFunc()
