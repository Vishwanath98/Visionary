from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QDialog

from DATA225utils import make_connection

class Patient_Dashboard(QDialog):
    def __init__(self, parent=None):
        super(Patient_Dashboard, self).__init__(parent)
        uic.loadUi("patient_dashboard.ui", self)