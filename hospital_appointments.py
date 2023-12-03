from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QDateTime
from PyQt5.QtWidgets import QDialog, QHBoxLayout, QLabel, QPushButton, QWidget, QMessageBox

from DATA225utils import make_connection

class Hospital_Appointments(QDialog):
    def __init__(self, parent=None):
        super(Hospital_Appointments, self).__init__(parent)
        uic.loadUi("hospital_appointments_page.ui", self)
        #self.load_appointments()
    #def load_appointments(self):
        # Fetch appointments from the database and populate the list widget
        #appointments = self.get_appointments_from_db()
        sample_appointments = [
            "John Doe - Cardiology - 2023-06-15 10:30 AM",
            "Jane Smith - Orthopedics - 2023-06-20 02:00 PM",
            "Bob Johnson - Pediatrics - 2023-06-25 11:45 AM",
        ]
        self.appointments_list.addItems(sample_appointments)
        self.pushButton.clicked.connect(self.show_accept_decline_message)

    def show_accept_decline_message(self):
        selected_item = self.appointments_list.currentItem()

        if selected_item:
            appointment_text = selected_item.text()

            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Question)
            msg_box.setText(f"Do you want to accept or decline the appointment:\n{appointment_text}")
            msg_box.setWindowTitle("Appointment Confirmation")

            accept_button = msg_box.addButton("Accept", QMessageBox.AcceptRole)
            decline_button = msg_box.addButton("Decline", QMessageBox.RejectRole)

            msg_box.exec_()

            if msg_box.clickedButton() == accept_button:
                print(f"Accepted appointment: {appointment_text}")
            elif msg_box.clickedButton() == decline_button:
                print(f"Declined appointment: {appointment_text}")
