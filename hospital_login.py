from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QDialog

from DATA225utils import make_connection

class Hospital_Login(QDialog):
    def __init__(self, parent=None):
        super(Hospital_Login, self).__init__(parent)
        uic.loadUi("hospital_login_screen.ui", self)