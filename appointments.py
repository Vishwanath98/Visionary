import mysql
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QDateTime
from PyQt5.QtWidgets import QDialog, QHBoxLayout, QLabel, QPushButton, QWidget

from DATA225utils import make_connection

class Appointment(QDialog):
    def __init__(self, parent=None):
        super(Appointment, self).__init__(parent)
        uic.loadUi("patient_appointments.ui", self)
        #for search button
        self.search_button.clicked.connect(self.update_doctor_list)
        #for date
        self.date_time.setDateTime(QDateTime.currentDateTime())
        #for specialization
        connection = make_connection(config_file='hosp.ini')
        cursor = connection.cursor()
        query = "SELECT DISTINCT Specialization FROM Doctor;"
        cursor.execute(query)

        # Fetch the results
        specializations = [result[0] for result in cursor.fetchall()]

        # Close the cursor and connection
        cursor.close()
        connection.close()
        self.specialisation_cb.addItem("All")
        self.specialisation_cb.addItems(specializations)

        #for cost
        connection = make_connection(config_file='hosp.ini')
        cursor = connection.cursor()
        query = "SELECT DISTINCT Consultation_Fee FROM Billing;"
        cursor.execute(query)

        # Fetch the results
        consultation_fees = [result[0] for result in cursor.fetchall()]

        # Close the cursor and connection
        cursor.close()
        connection.close()

        # Create a combo box and populate it with consultation fees
        self.fee_cb.addItem("All")
        self.fee_cb.addItems(map(str, consultation_fees))
    def add_doctor_buttons(self):
        for doctor in self.get_filtered_doctors("All", "All", QDateTime.currentDateTime()):
            button_layout = QHBoxLayout()

            # Add doctor name to the layout
            doctor_label = QLabel(doctor)
            #rating_label = QLabel(rating)
            button_layout.addWidget(doctor_label)

            # Add "Book Appointment" button
            book_appointment_button = QPushButton("Book Appointment")
            book_appointment_button.clicked.connect(lambda _, doc=doctor: self.book_appointment(doc))
            button_layout.addWidget(book_appointment_button)

            # Add the layout to the list widget
            item_widget = QWidget()
            item_widget.setLayout(button_layout)
            list_item = self.doctor_list.addItem("")
            self.doctors_list.setItemWidget(list_item, item_widget)

    def book_appointment(self, doctor_name):
        # Add your logic here for booking an appointment with the selected doctor
        #create appointment Id function to create appointment id's for every new appointment ID
        #insert into appointments with
        print(f"Booking appointment with {doctor_name}")
    def get_filtered_doctors(self, disease, cost, selected_date):
        try:
            connection = make_connection(config_file='hosp.ini')
            cursor = connection.cursor()

            #rating specialization, fee
            query = ("SELECT Doctor.Doctor_ID, Doctor.Doctor_Name, Doctor.Specialization, Billing.Consultation_Fee FROM Doctor JOIN Billing ON Doctor.Doctor_ID = Billing.Doctor_ID")
            conditions = []

            if disease != "All":
                conditions.append(f"Specialization = '{disease}'")

            if cost != "All":
                conditions.append(f"Consultation_Fee = '{cost}'")

            #conditions.append(f"available_date = '{selected_date.toString('yyyy-MM-dd')}'")

            query += " AND ".join(conditions)

            cursor.execute(query)
            doctors = [doctor[0] for doctor in cursor.fetchall()]

            return doctors

        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return []

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    def update_doctor_list(self):
        selected_disease = self.specialisation_cb.currentText()
        selected_cost = self.fee_cb.currentText()
        selected_date = self.date_time.dateTime()
        print(selected_disease,selected_cost,selected_date)
        # Clear the current items in the list widget
        self.doctors_list.clear()

        # Update the list widget based on the filters
        doctors_to_display = self.get_filtered_doctors(selected_disease, selected_cost, selected_date)

        # Add the filtered doctors to the list widget
        self.doctors_list.addItems(doctors_to_display)