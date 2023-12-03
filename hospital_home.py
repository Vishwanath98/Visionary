from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QDialog

from DATA225utils import make_connection

class Hospital_Home(QDialog):
    def __init__(self, parent=None):
        super(Hospital_Home, self).__init__(parent)
        uic.loadUi("hospital_home_page.ui", self)