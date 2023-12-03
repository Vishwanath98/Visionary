from PyQt5 import uic
from PyQt5.QtCore import QDateTime
from PyQt5.QtWidgets import QDialog, QHBoxLayout, QLabel, QPushButton, QWidget, QMessageBox

from DATA225utils import make_connection

class Hosp_Past_Appointments(QDialog):
    def __init__(self, parent=None):
        super(Hosp_Past_Appointments, self).__init__(parent)
        uic.loadUi("past_appointments.ui", self)
        #self.load_appointments()
    #def load_appointments(self):
        # Fetch appointments from the database and populate the list widget
        #appointments = self.get_appointments_from_db()
        sample_appointments = [
            "John Doe - Cardiology - 2023-06-15 10:30 AM",
            "Jane Smith - Orthopedics - 2023-06-20 02:00 PM",
            "Bob Johnson - Pediatrics - 2023-06-25 11:45 AM",
        ]
        self.listWidget.addItems(sample_appointments)