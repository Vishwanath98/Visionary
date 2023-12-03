from PyQt5 import QtWidgets, uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QDialog
from PyQt5.uic.properties import QtCore

from DATA225utils import make_connection
from login import LoginWindow

class PatientHomePage(QDialog):
    def __init__(self, parent=None):
        super(PatientHomePage, self).__init__(parent)
        uic.loadUi("patient_home_page.ui", self)

    def profile(self,user_name):
        print("entered")
        conn = make_connection(config_file='hosp.ini')
        cursor = conn.cursor()
        #user_name = self.u_name.text()
        print(user_name)
        sql = 'SELECT gender FROM register WHERE user_name = \'' + user_name + "\'"
        cursor.execute(sql)
        result = cursor.fetchone()
        print(result)
        if result[0] == 'Male':
            label = self.profile_pic
            pixmap = QPixmap('profile_pic_male.png')
            label.setPixmap(pixmap)
            #self.setCentralWidget(label)
            self.resize(pixmap.width(),pixmap.height())
        else:
            label = self.profile_pic
            pixmap = QPixmap('profile_pic_female.png')
            label.setPixmap(pixmap)
            #self.setCentralWidget(label)
            self.resize(pixmap.width(), pixmap.height())
