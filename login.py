from PyQt5 import QtWidgets, uic, QtCore
import mysql.connector
from PyQt5.QtWidgets import QDialog, QMessageBox
from DATA225utils import make_connection

class LoginWindow(QDialog):
    login_successful = QtCore.pyqtSignal(str)

    def __init__(self, parent=None):
        super(LoginWindow, self).__init__(parent)
        uic.loadUi("login.ui", self)

        self.login_button.clicked.connect(self.login)

    def login(self):
        if self.checkBox.isChecked():
            user_name = self.user_name.text()
            # self.l_password.setEchoMode(QtWidgets.QLineEdit.Password)
            password = self.l_password.text()
            if len(user_name) == 0 or len(password) == 0:
                self.show_notification("Missing Credentials", "Input all credentials to Login")
            else:
                conn = make_connection(config_file='hosp.ini')
                cursor = conn.cursor()
                sql = 'SELECT pwd from register WHERE user_name = \'' + user_name + "\'"
                cursor.execute(sql)
                result_pass = cursor.fetchone()
                print(result_pass)
                if result_pass[0] == password:
                    print("Login Successful")
                    self.login_successful.emit(user_name)
                    self.login_log(user_name)
                    self.show_notification("Login Successful", "Welcome back, " + user_name + "!")
                else:
                    print("wrong")
                    self.show_notification("Incorrect Credentials", "Enter valid username or password")
        else:
            self.show_notification("Agree to the Terms & Conditions", "Please check I agree to Login")
    def login_log(self,user_name):
        from datetime import datetime

        conn = make_connection(config_file='hosp.ini')
        cursor = conn.cursor()

        currtime = datetime.now()

        sql_2 = """INSERT INTO login_log (username, login_time) VALUES""" f"('{user_name}', '{currtime}')"

        cursor.execute(sql_2)
        conn.commit()
        cursor.close()
        conn.close()

    def show_notification(self, title, message):
        QMessageBox.information(self, title, message, QMessageBox.Ok)
