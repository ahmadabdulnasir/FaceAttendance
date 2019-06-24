#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
__author__ = 'Ahmad Abdulnasir Shu'aib <me@ahmadabdulnasir.com.ng>'
__homepage__ = https://ahmadabdulnasir.com.ng
__copyright__ = 'Copyright (c) 2019, salafi'
__version__ = "0.01t"
"""
import sys, os
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.uic import loadUi
import csv

'''constants declaration '''
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Setting database file to use
helpUiFile = os.path.join(BASE_DIR, 'help.ui')
''' ./constants declaration'''

class HelpDialog(QDialog):
    def __init__(self,  parent):
        super(HelpDialog, self).__init__()
        loadUi(helpUiFile, self) # Loading UI
        self.setWindowTitle(" Help | FaceAttendance System")
        self.okButton.clicked.connect(self.quitDialog)
        # self.quitButton.clicked.connect(self.close)


    def quitDialog(self):
        self.close()


def boot():
    app = QApplication([])
    window = HelpDialog(None)
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    boot()
