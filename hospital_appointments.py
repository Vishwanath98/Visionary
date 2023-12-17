from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QDateTime
from PyQt5.QtWidgets import QDialog, QHBoxLayout, QLabel, QPushButton, QWidget, QMessageBox

from DATA225utils import make_connection

class Hospital_Appointments(QDialog):
    def __init__(self, parent=None):
        super(Hospital_Appointments, self).__init__(parent)
        uic.loadUi("hospital_appointments_page.ui", self)
        self.load_appointments()
    def load_appointments(self):
        # Fetch appointments from the database and populate the list widget
        #appointments = self.get_appointments_from_db()
        connection = make_connection(config_file='hosp.ini')
        cursor = connection.cursor()
        sql = "SELECT Consultation_ID, Health_Issue, Doctor_ID, Consultation_Fee FROM Consultation WHERE Appointment_Status = 'Pending'"
        cursor.execute(sql)
        sample_appointments = cursor.fetchall()
        #print(sample_appointments)
        for d in sample_appointments:
            doctor_str = f"Consultation ID: {d[0]}, Health issue: {d[1]}, Doctor ID: {d[2]}, Fee: {d[3]}"
            # print(doctor_str)
            self.appointments_list.addItem(f"{doctor_str}")
        self.pushButton.clicked.connect(self.show_accept_decline_message)

    def show_accept_decline_message(self):
        selected_item = self.appointments_list.currentItem()

        if selected_item:
            appointment_text = selected_item.text()
            Consultation_ID = self.extract_info(appointment_text, "Consultation ID")
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Question)
            msg_box.setText(f"Do you want to accept or decline the appointment:\n{appointment_text}")
            msg_box.setWindowTitle("Appointment Confirmation")

            accept_button = msg_box.addButton("Accept", QMessageBox.AcceptRole)
            decline_button = msg_box.addButton("Decline", QMessageBox.RejectRole)

            msg_box.exec_()

            if msg_box.clickedButton() == accept_button:
                if selected_item is not None:
                    connection = make_connection(config_file='hosp.ini')
                    cursor = connection.cursor()
                    sql = f"UPDATE Consultation SET Appointment_Status = 'Active' WHERE Consultation_ID = '{Consultation_ID}'"
                    cursor.execute(sql)
                    # Remove the selected item from the QListWidget
                    self.appointments_list.takeItem(self.appointments_list.row(selected_item))
                print(f"Accepted appointment: {appointment_text}")
            elif msg_box.clickedButton() == decline_button:
                #self.appointment_list.removeItem(selected_item)
                if selected_item is not None:
                    # Remove the selected item from the QListWidget
                    self.appointments_list.takeItem(self.appointments_list.row(selected_item))
                print(f"Declined appointment: {appointment_text}")

    def extract_info(self, text, key):
        # Helper function to extract information from the text based on the key
        start_index = text.find(f"{key}: ") + len(f"{key}: ")
        end_index = text.find(",", start_index)
        extracted_info = text[start_index:end_index].strip()

        # Remove the colon if present
        extracted_info = extracted_info.replace(':', '').strip()
        return extracted_info
