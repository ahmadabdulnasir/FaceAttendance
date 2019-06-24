import sys
import cv2
from PyQt5.QtWidgets import (QDialog, QApplication, QFileDialog, QInputDialog)
from PyQt5.uic import loadUi
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSlot
import os
import tempfile
'''constants declaration '''
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Setting database file to use
facestrackUiFile = os.path.join(BASE_DIR, 'face_track.ui')
''' ./constants declaration'''

class FaceTrack(QDialog):
    ''' Qt window object that defines the window of faces tracking    '''
    def __init__(self,  parent):
        super(FaceTrack, self).__init__()
        loadUi(facestrackUiFile, self) # Loading UI
        self.setWindowTitle("FaceAttendance Registering System")
        self.registerFaceButton.clicked.connect(self.registerFace)
        self.loadFaceButton.clicked.connect(self.selectPic)
        self.identifyFaceButton.clicked.connect(self.identifyFace)
        self.quitButton.clicked.connect(self.close)

    @pyqtSlot()
    def selectPic(self):
        fname, filter = QFileDialog.getOpenFileName(self, 'Open file', '', "Image files (*.jpg *.gif *.png)")
        if fname:
            self.loadImg(fname)
        else:
            print("[ERROR]: Invalid Image")
    def loadImg(self, fname):
        self.img = cv2.imread(fname, cv2.IMREAD_COLOR)
        self.img = cv2.resize(self.img, (250,300))
        self.displayImg(self.img)
    def displayImg(self, img, window=1):
        qformat = QImage. qformat = QImage.Format_Indexed8
        if (len(img.shape) ) == 3: # [0] : rows, [1] = cols, [2]: channels
            if img.shape[2] == 4 :
                qformat = QImage.Format_RGBA8888
            else:
                qformat = QImage.Format_RGB888

        frame = QImage(img, img.shape[1], img.shape[0], img.strides[0], qformat)
        # Converting BGR to RGB
        frame = frame.rgbSwapped()
        if window == 1:
            self.facelabel.setPixmap(QPixmap.fromImage(frame))
            self.facelabel.setScaledContents(True)
        else:
            self.responsefacelabel.setPixmap(QPixmap.fromImage(frame))
            self.responsefacelabel.setScaledContents(True)

    def registerFace(self):
        # TODO: fix issue with tmp images
        userid = self.getUId()
        img = self.img
        cv2.imwrite('kumbaya.jpg', img)
        f = cv2.FONT_HERSHEY_SIMPLEX
        #import face_track
        from . import face_track
        msg = face_track.regFace(['kumbaya.jpg'], userid)
        if msg:
            img = cv2.putText(img, userid, (0, 70 ), f, 2, (0, 255 ,0))
            img = cv2.putText(img, msg, (0, 130 ), f, 1, (0, 255, 0))
        else:
            img = cv2.putText(img, 'Error', (0, 70 ), f, 2, (255,0,0))

        self.displayImg(img, window=2)

    def identifyFace(self):
        f = cv2.FONT_HERSHEY_SIMPLEX
        img = self.img
        #small = cv2.resize(img, (250,300) )
        kumbaya = tempfile.mkstemp()[1] + '.jpg'
        # print('[HERE] ', kumbaya)
        cv2.imwrite(kumbaya, img)
        from . import face_track
        binimg = kumbaya
        dta = face_track.preditFace( binimg )
        # {'userid':userid, 'x_min': x_min, 'x_max': x_max, 'y_min': y_min, 'y_max': y_max , 'confidence': msg}
        # print(dta)
        try:
            cv2.rectangle(img, (dta['x_min']-10, dta['y_min']-10), (dta['x_max']-10, dta['y_max']-10), (0, 255, 0), 2)
            # (left, top, right, bottom)
            if dta['userid'] == 'userid':
                person = 'Unknown'
            else:
                person = dta['userid']
            (h, w) = img.shape[:2]

            img = cv2.putText(img, person, (dta['x_min'], dta['y_max'] +15  ), f, 1, (0, 255 ,0))

            small = img
            #small = cv2.resize(img, (100, 50))
            # self.showFullScreen()
        except TypeError as e:
            # print(e)
            cv2.putText(img, "No Face", (10, 150  ), f, 1, (0, 0 ,255))
            small = cv2.putText(img, "Found !!!", (10, 170  ), f, 1, (0, 0 ,255))
        self.displayImg(small, window=2)

    def getUId(self):
        userid, ok = QInputDialog.getText(self, "Enter User ID", "Enter User ID for the Image " )
        if ok and userid is not None:
            userid = userid.strip()
        return userid
def boot():
    app = QApplication([])
    window = FaceTrack(None)
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    boot()
