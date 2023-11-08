import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QCoreApplication

import LoginDialog
from LoginDialog import *
from PyQt5 import QtWidgets

from LoginDialog import *
from RegisterDialog import *
from User_Details import *
from Patient_home_page import *

class MainWindow(QtWidgets.QStackedWidget):
    def __init__(self):
        super().__init__()
        self.login_screen = Login()
        self.register_screen = Register()
        self.user_details_screen = User_Details()
        self.patient_home_screen = Patient_Home()

        self.addWidget(self.login_screen)
        self.addWidget(self.register_screen)
        self.addWidget(self.user_details_screen)
        self.addWidget(self.patient_home_screen)

        self.setFixedWidth(580)
        self.setFixedHeight(620)

        self.login_screen.register_here_button.clicked.connect(self.goto_register)
        self.register_screen.back_button.clicked.connect(self.goto_login)
        self.register_screen.show_button.clicked.connect(self.goto_details)
        self.login_screen.login_button.clicked.connect(self.goto_patient_home)

    def goto_register(self):
        self.setCurrentIndex(self.indexOf(self.register_screen))

    def goto_login(self):
        self.setCurrentIndex(self.indexOf(self.login_screen))

    def goto_details(self):
        self.setCurrentIndex(self.indexOf(self.user_details_screen))

    def goto_patient_home(self):
        self.setCurrentIndex(self.indexOf(self.patient_home_screen))
app = QApplication(sys.argv)
widget = MainWindow()
#mainwindow = Login()
#widget = QtWidgets.QStackedWidget()
#widget.addWidget(mainwindow)
#widget.setFixedWidth(580)
#widget.setFixedHeight(620)
widget.show()
app.exec()