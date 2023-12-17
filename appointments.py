import mysql
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QDateTime
from PyQt5.QtWidgets import QDialog, QHBoxLayout, QLabel, QPushButton, QWidget, QMessageBox

from DATA225utils import make_connection

class Appointment(QDialog):
    def __init__(self, parent=None):
        super(Appointment, self).__init__(parent)
        uic.loadUi("patient_appointments.ui", self)
        #for search button
        self.search_button.clicked.connect(self.update_doctor_list)
        #for book appointment
        self.book_appointment.clicked.connect(self.show_book_appointment)
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

    def show_book_appointment(self):
        selected_item = self.doctors_list.currentItem()
        if selected_item:
            appointment_text = selected_item.text()

            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Question)
            msg_box.setText(f"Do you want to book the appointment:\n{appointment_text}")
            msg_box.setWindowTitle("Appointment Confirmation")

            accept_button = msg_box.addButton("Book", QMessageBox.AcceptRole)
            msg_box.exec_()

            #extracting the info to insert into the tables
            Doctor_ID = self.extract_info(appointment_text, "DoctorID")
            Health_Issue = self.extract_info(appointment_text, "Specialization")
            Consultation_Fee = self.extract_info(appointment_text, "Fee")
            doctor_name = self.extract_info(appointment_text, "Name")
            #print(Doctor_ID,Health_Issue,Consultation_Fee,doctor_name)

            if msg_box.clickedButton() == accept_button:
                #print(f"Booked appointment: {appointment_text}")
                self.show_notification("Appointment Booked", "Wait for the doctor's confirmation")

                #SQL QUERY for creating the Patient Id and inserting into consulting table
                #def register_and_book_appointment(appointment_info):
                    # Connect to the MySQL database
                try:
                        # Create a MySQL cursor
                    connection = make_connection(config_file='hosp.ini')
                    cursor = connection.cursor()

                        # Find the maximum numeric part for all patient IDs
                    cursor.execute("SELECT MAX(CAST(SUBSTRING(Consultation_ID FROM LENGTH('CONS') + 1) AS UNSIGNED)) "
                                       "FROM Consultation WHERE Consultation_ID LIKE 'CONS%'")
                    result = cursor.fetchone()
                    last_numeric_part = result[0] if result[0] is not None else 0

                        # Increment the last numeric part and generate the new patient ID
                    last_numeric_part += 1
                    consultation_id = f'CONS{last_numeric_part}'
                    print(consultation_id)

                        # Insert the new patient into the patient table
                    cursor.execute("INSERT INTO Consultation (Consultation_ID, Doctor_ID, Health_Issue, Consultation_Fee, Appointment_Status) VALUES (%s, %s, %s, %s, %s)",
                                       (consultation_id, Doctor_ID, Health_Issue, Consultation_Fee, 'Pending'))
                    """
                    # Insert the appointment information into the appointments table
                    cursor.execute(
                            "INSERT INTO your_appointments_table (patient_id, appointment_info, other_columns) VALUES (%s, %s, %s)",
                            (new_patient_id, appointment_info, '...'))
                    """
                    # Commit the changes
                    connection.commit()

                        # Optionally, you can return the new patient ID or any other information
                        # return new_patient_id

                except mysql.connector.Error as err:
                    print(f"Error: {err}")

                finally:
                        # Close the cursor and connection
                    cursor.close()
                    connection.close()

            #elif msg_box.clickedButton() == decline_button:
                #print(f"Declined appointment: {appointment_text}")
    def get_filtered_doctors(self, disease, cost, selected_date):
        try:
            connection = make_connection(config_file='hosp.ini')
            cursor = connection.cursor()

            #rating specialization, fee
            query = ("SELECT D.Doctor_ID, D.Doctor_Name, D.Specialization, C.Consultation_Fee FROM Doctor D JOIN Consultation C ON D.Consultation_ID = C.Consultation_ID")
            conditions = []

            if disease != "All":
                conditions.append(f" WHERE Specialization = '{disease}'")

            if cost != "All":
                conditions.append(f" WHERE Consultation_Fee = '{cost}'")

            #conditions.append(f"available_date = '{selected_date.toString('yyyy-MM-dd')}'")

            query += " AND ".join(conditions)
            #print(query)
            cursor.execute(query)
            rows = cursor.fetchall()
            #print(rows)
            #cursor.execute(query)
            #doctors = [doctor for doctor in rows]
            #print("doctors list: ",doctors)
            return rows

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
        #print(selected_disease,selected_cost,selected_date)
        # Clear the current items in the list widget
        self.doctors_list.clear()

        # Update the list widget based on the filters
        doctors_to_display = self.get_filtered_doctors(selected_disease, selected_cost, selected_date)
        #print(doctors_to_display)
        # Add the filtered doctors to the list widget
        for d in doctors_to_display:
            doctor_str = f"Doctor ID: {d[0]}, Name: {d[1]}, Specialization: {d[2]}, Fee: {d[3]}"
            #print(doctor_str)
            self.doctors_list.addItem(f"{doctor_str}")

    def extract_info(self, text, key):
        # Helper function to extract information from the text based on the key
        start_index = text.find(f"{key}: ") + len(f"{key}: ")
        end_index = text.find(",", start_index)
        extracted_info = text[start_index:end_index].strip()

        # Remove the colon if present
        extracted_info = extracted_info.replace(':', '').strip()
        return extracted_info

    def show_notification(self, title, message):
        QMessageBox.information(self, title, message, QMessageBox.Ok)