import sys
import mysql.connector
from PyQt5.QtCore import QDateTime
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QListWidget, QLabel, QComboBox, QDateEdit, QPushButton, \
    QDialog, QDateTimeEdit, QHBoxLayout
from DATA225utils import make_connection

class Appointment(QDialog):
    def __init__(self):
        super(Appointment, self).__init__()

        self.search_button = None
        self.doctor_list = None
        self.date_filter = None
        self.cost_combo = None
        self.disease_combo = None
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Database connection parameters
        connection = make_connection(config_file='hosp.ini')
        cursor = connection.cursor()

        # Filter ComboBoxes
        self.disease_combo = QComboBox()
        self.disease_combo.addItem("All")
        self.disease_combo.addItem("Allergy")
        self.disease_combo.addItem("Cold")
        layout.addWidget(QLabel("Select Disease"))
        layout.addWidget(self.disease_combo)

        self.cost_combo = QComboBox()
        self.cost_combo.addItem("All")
        self.cost_combo.addItem("Low Cost")
        self.cost_combo.addItem("Medium Cost")
        self.cost_combo.addItem("High Cost")
        layout.addWidget(QLabel("Select Cost"))
        layout.addWidget(self.cost_combo)

        self.date_filter = QDateTimeEdit()
        self.date_filter.setDateTime(QDateTime.currentDateTime())
        layout.addWidget(QLabel("Select Date and Time"))
        layout.addWidget(self.date_filter)

        # List Widget
        self.doctor_list = QListWidget()
        layout.addWidget(QLabel("Available Doctors"))
        layout.addWidget(self.doctor_list)

        # Book Appointment Buttons
        self.add_doctor_buttons()

        # Search Button
        self.search_button = QPushButton("Search")
        self.search_button.clicked.connect(self.get_filtered_doctors)
        layout.addWidget(self.search_button)

        back_button = QPushButton("Back to Home Page")
        layout.addWidget(back_button)

        self.setLayout(layout)
        self.setWindowTitle("Appointments Tab")
        self.show()

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
            self.doctor_list.setItemWidget(list_item, item_widget)

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
            query = "SELECT Doctor_Name FROM doctors WHERE "
            conditions = []

            if disease != "All":
                conditions.append(f"disease = '{disease}'")

            if cost != "All":
                conditions.append(f"cost = '{cost}'")

            conditions.append(f"available_date = '{selected_date.toString('yyyy-MM-dd')}'")

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
        selected_disease = self.disease_combo.currentText()
        selected_cost = self.cost_combo.currentText()
        selected_date = self.date_filter.date()

        # Clear the current items in the list widget
        self.doctor_list.clear()

        # Update the list widget based on the filters
        doctors_to_display = self.get_filtered_doctors(selected_disease, selected_cost, selected_date)

        # Add the filtered doctors to the list widget
        self.doctor_list.addItems(doctors_to_display)



