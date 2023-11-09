from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi
from DATA225utils import make_connection
from LoginDialog import *
class Patient_Home(QDialog):
    def __init__(self):
        super(Patient_Home,self).__init__()
        self.ui = uic.loadUi("Patient_home_page.ui",self)
        self.setWindowTitle("Patient Home Page")
        self.u_name.setText("sandeep")
