import sys
import mysql.connector
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QListWidget, QPushButton, QDialog, QFormLayout, QLineEdit
from DATA225utils import make_connection
from edit_mange import Edit_Manage


class AppointmentManager(QDialog):
    def __init__(self, parent=None):
        super(AppointmentManager, self).__init__(parent)
        uic.loadUi("manage_appointments.ui", self)
        self.edit_button.clicked.connect(self.edit_appointment)
        sample_appointments = [
            "John Doe - Cardiology - 2023-06-15 10:30 AM",
            "Jane Smith - Orthopedics - 2023-06-20 02:00 PM",
            "Bob Johnson - Pediatrics - 2023-06-25 11:45 AM",
        ]
        self.booked_list.addItems(sample_appointments)
    def edit_appointment(self):
            selected_item = self.booked_list.currentItem()
            if selected_item:
                appointment_info = selected_item.text()
                edit_dialog = Edit_Manage(self)
                edit_dialog.setAppointmentInfo(appointment_info)
                edit_dialog.accepted.connect(self.handle_edit_accept)

                if edit_dialog.exec_() == QDialog.Accepted:
                    # The edited information will be handled in the handle_edit_accept method
                    pass

    def handle_edit_accept(self):
        # Retrieve the edited information from the EditDialog
        edited_info = self.sender().getEditedInfo()

        # Update the QListWidget item text
        selected_item = self.booked_list.currentItem()
        if selected_item:
            selected_item.setText(edited_info)


"""
class AppointmentManager(QDialog):
    def __init__(self):
        super(AppointmentManager, self).__init__()

        self.back_button = None
        self.init_ui()
        self.load_appointments()  # Load appointments when the window is initialized

    def init_ui(self):
        layout = QVBoxLayout()

        # List Widget to display booked appointments
        self.appointment_list = QListWidget()
        layout.addWidget(QLabel("Booked Appointments"))
        layout.addWidget(self.appointment_list)

        # Buttons to manage appointments
        #view_button = QPushButton("View Appointment")
        #view_button.clicked.connect(self.view_appointment)
        #layout.addWidget(view_button)

        edit_button = QPushButton("Edit Appointment")
        edit_button.clicked.connect(self.edit_appointment)
        layout.addWidget(edit_button)

        past_appointments_button = QPushButton("View Past Appointments")
        past_appointments_button.clicked.connect(self.view_past_appointments)
        layout.addWidget(past_appointments_button)

        #view_bills_button = QPushButton("View Bills")
        #view_bills_button.clicked.connect(self.view_bills)
        #layout.addWidget(view_bills_button)

        self.back_button = QPushButton("Back to Home Page")
        layout.addWidget(self.back_button)

        self.setLayout(layout)
        self.setWindowTitle("Appointment Manager")

    def load_appointments(self):
        # Fetch appointments from the database and populate the list widget
        appointments = self.get_appointments_from_db()
        self.appointment_list.addItems(appointments)

    def get_appointments_from_db(self):
        try:
            connection = make_connection(config_file='hosp.ini')
            cursor = connection.cursor()

            query = "SELECT appointment_info FROM appointments"  # Replace with your actual query
            cursor.execute(query)
            appointments = [appointment[0] for appointment in cursor.fetchall()]

            return appointments

        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return []

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def view_appointment(self):
        # Add logic to view the selected appointment
        selected_item = self.appointment_list.currentItem()
        if selected_item:
            appointment_info = selected_item.text()
            self.show_message_dialog("View Appointment", f"Viewing Appointment:\n{appointment_info}")

    def edit_appointment(self):
        # Add logic to edit the selected appointment
        selected_item = self.appointment_list.currentItem()
        if selected_item:
            appointment_info = selected_item.text()
            edit_dialog = QDialog(self)
            edit_dialog.setWindowTitle("Edit Appointment")

            # Create a simple edit form, #QDateEdit, confirm, cancel appointment
            form_layout = QFormLayout()
            form_layout.addRow(QLabel("Edit Appointment:"), QLineEdit(appointment_info))
            edit_dialog.setLayout(form_layout)

            # Add an "OK" button to close the dialog
            ok_button = QPushButton("OK")
            ok_button.clicked.connect(edit_dialog.accept)
            form_layout.addRow(ok_button)

            if edit_dialog.exec_() == QDialog.Accepted:
                # Save the changes to the appointment
                edited_info = form_layout.itemAt(1, QFormLayout.FieldRole).widget().text()
                self.show_message_dialog("Edit Appointment", f"Appointment Edited:\n{edited_info}")

    def view_past_appointments(self):
        # Add logic to view past appointments
        self.show_message_dialog("View Past Appointments", "Viewing Past Appointments")

    def view_bills(self):
        # Add logic to view bills
        self.show_message_dialog("View Bills", "Viewing Bills")

    def show_message_dialog(self, title, message):
        msg_dialog = QDialog(self)
        msg_dialog.setWindowTitle(title)
        msg_layout = QVBoxLayout()
        msg_layout.addWidget(QLabel(message))
        msg_dialog.setLayout(msg_layout)
        msg_dialog.exec_()
"""

