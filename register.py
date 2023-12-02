from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QDialog, QMessageBox

from DATA225utils import make_connection


class RegistrationWindow(QDialog):
    def __init__(self, parent=None):
        super(RegistrationWindow, self).__init__(parent)
        uic.loadUi("register.ui", self)
        self.register_button.clicked.connect(self.registerfunction)
    def registerfunction(self):
            first_name = self.first_name.text()
            last_name = self.last_name.text()
            email = self.email.text()
            user_name = self.user_name.text()
            pwd = self.password.text()
            if pwd != self.confirm_pass.text():
                print("passwords do not match")

            if self.radioButton.isChecked() == True:
                gender = self.radioButton.text()
            else:
                gender = self.radioButton_2.text()

            conn = make_connection(config_file='hosp.ini')
            cursor = conn.cursor()

            sql_1 = """SELECT user_name FROM register WHERE user_name =""" f"('{user_name}')"
            cursor.execute(sql_1)
            result = cursor.fetchone()
            # cursor.close()
            # conn.close()
            print(result)

            if result == user_name:
                print("User name already exists")
            else:
                print("register")
                conn = make_connection(config_file='hosp.ini')
                cursor = conn.cursor()
                sql_2 = """INSERT INTO register VALUES""" f" ('{first_name}', '{last_name}','{email}','{gender}', '{user_name}', '{pwd}')"
                cursor.execute(sql_2)
                conn.commit()
                cursor.close()
                conn.close()
                print("end")
                self.show_notification("Registration Successful", "Successfully registered! Now you can log in.")

    def show_notification(self, title, message):
        QMessageBox.information(self, title, message, QMessageBox.Ok)
