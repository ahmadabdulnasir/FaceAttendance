#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
__author__ = 'Ahmad Abdulnasir Shu'aib <me@ahmadabdulnasir.com.ng>'
__homepage__ = https://ahmadabdulnasir.com.ng
__copyright__ = 'Copyright (c) 2019, salafi'
__version__ = "0.01t"
"""
import sys
import cv2
from PyQt5.QtWidgets import (QMainWindow, QApplication,)
from PyQt5.uic import loadUi
from PyQt5.QtGui import QImage, QPixmap, QIcon
from PyQt5.QtCore import QTimer, pyqtSlot
import os
'''constants declaration '''
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
iconImg = os.path.join(BASE_DIR, 'icon.png')
errorImg = iconImg
mainUiFile = os.path.join(BASE_DIR, 'mainWindow.ui')
VIDEO_SOURCE = 0
TRACKING_ACTIVE = 'Tracking activated ....'
APP_READY = 'Ready'
''' ./constants declaration'''

class MainWindow(QMainWindow):
    ''' Qt window object that defines the window of faces tracking '''
    def __init__(self,  parent):
        super(MainWindow, self).__init__()
        loadUi(mainUiFile, self) # Loading UI
        self.setWindowTitle("Face Tracking and Attendance System")
        self.startButton.clicked.connect(self.startSystem)
        self.settingsButton.clicked.connect(self.settings)
        self.trainButton.clicked.connect(self.train)
        self.helpButton.clicked.connect(self.help)
        self.quitButton.clicked.connect(self.exitApp)

        self.statusBox.setText(APP_READY)

        self.working = False

        self.dialogs = list()

    def startSystem(self):
        if not self.working:
            self.statusBox.setText(TRACKING_ACTIVE)
            self.feed = cv2.VideoCapture(VIDEO_SOURCE)
            self.feed.set(cv2.CAP_PROP_FRAME_HEIGHT, 361)
            self.feed.set(cv2.CAP_PROP_FRAME_WIDTH, 631)
            cv2.flip
            # fps = self.feed.get(cv2.CAP_PROP_FPS)
            self.timer = QTimer(self)
            self.timer.timeout.connect(self.loadFeed)
            self.timer.start(1)
            self.working = True
            self.startButton.setText('Stop')
        else:
            self.timer.stop()
            self.feed.release()
            self.working = False
            self.startButton.setText('Start')
            self.statusBox.setText(APP_READY)

    def loadFeed(self):
        """ Load feed with opencv from source (webcam) """
        ret, self.img = self.feed.read() #  reading feed frame by frame'
        self.img = cv2.flip(self.img, 1)
        self.displayFeed(self.img, 1)
        self.displayFeed(self.img, 2)

    def displayFeed(self, fram, window=1):
        """  Method to display feed on viewfield """
        qformat = QImage.Format_Indexed8
        f = cv2.FONT_HERSHEY_TRIPLEX #FONT_HERSHEY_SIMPLEX
        try:
            ''' recent version of opencv return '''
            if (len(fram.shape)) == 3:  # [0] : rows, [1] = cols, [2]: channels
                if fram.shape[2] == 4:
                    qformat = QImage.Format_RGBA8888
                else:
                    qformat = QImage.Format_RGB888
        except:
            text1 = "Error!!!"
            text2 = "{}".format(self.camId)
            img = cv2.imread(errorImg, 1)
            img = cv2.putText(img, text1, (0, 70), f, 2, (255, 255, 255))
            fram = cv2.putText(img, text2, (0, 130), f, 2, (255, 255, 255))
        try:
            frameI = QImage(fram, fram.shape[1], fram.shape[0], fram.strides[0], qformat)
            # Converting BGR (openCv) to RGB (Qt)
            frameI = frameI.rgbSwapped()
            if window == 1:
                self.mainFrame.setPixmap(QPixmap.fromImage(frameI))
                self.mainFrame.setScaledContents(True)
            else:
                # on second window
                self.responseFrame.setPixmap(QPixmap.fromImage(frameI))
                self.responseFrame.setScaledContents(True)
        except AttributeError:
            print('No more frames')

    def settings(self):
        pass

    def train(self):
        pass

    def help(self):
        pass

    def exitApp(self):
        try:
            self.timer.stop()
            self.feed.release()
            self.close()
        except Exception as e:
            try:
                self.feed.stop()
                self.close()
            except Exception as e:
                print(e)
        self.close()




def boot():
    app = QApplication([])
    main = MainWindow(None)
    #window.setWindowTitle("Face Tracking and Attendance System")
    main.setWindowIcon(QIcon(iconImg))
    main.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    boot()
