from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QDialog

from DATA225utils import make_connection

class Welcome_Page(QDialog):
    def __init__(self, parent=None):
        super(Welcome_Page, self).__init__(parent)
        uic.loadUi("welcome_page.ui", self)