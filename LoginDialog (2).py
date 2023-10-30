#!/usr/bin/env python
# coding: utf-8
import sys
from PyQt5 import QtWidgets,uic
from PyQt5.QtWidgets import QDialog, QApplication,QTableWidgetItem
from PyQt5.uic import loadUi
from DATA225utils import make_connection
from RegisterDialog import *
from User_Details import *

class Login(QDialog):
    def __init__(self):
        super(Login,self).__init__()
        self.ui = uic.loadUi("login.ui",self)
        self.setWindowTitle("Login")
        self.login_button.clicked.connect(self.loginfunction)
        #self.register_here_button.clicked.connect(self.create)
        
    def loginfunction(self):
        user_name=self.user_name.text()
        self.l_password.setEchoMode(QtWidgets.QLineEdit.Password)
        password=self.l_password.text()
        if len(user_name) == 0 or len(password) == 0:
            print("Please input all fields")
        else:
            conn = make_connection(config_file = 'hosp.ini')
            cursor = conn.cursor()
            sql = 'SELECT pwd from register WHERE user_name = \''+user_name+"\'"
            cursor.execute(sql)
            result_pass = cursor.fetchone()[0]
            if result_pass == password:
                print("Login Successful")
            else:
                print("Invalid user name or password")
        #print("Successfully logged in with username: ",user_name, "and password",password) 
        
    #def create(self):
        #register = Register()
        #widget.addWidget(register)
        #widget.setCurrentIndex(widget.currentIndex()+1)
"""        
class Register(QDialog):
    def __init__(self):
        super(Register,self).__init__()
        self.ui = uic.loadUi("register.ui",self)
        self.setWindowTitle("Register")
        self.register_button.clicked.connect(self.registerfunction)
        self.show_button.clicked.connect(self.open_details)
        
    def registerfunction(self):
        
        first_name = self.first_name.text()
        last_name = self.last_name.text()
        user_name = self.user_name.text()
        pwd=self.password.text()
        if pwd != self.confirm_pass.text():
            print("passwords do not match")
            
        if self.radioButton.isChecked() == True:
            gender = self.radioButton.text()
        else:
            gender = self.radioButton_2.text()
        
        conn = make_connection(config_file = 'hosp.ini')
        cursor = conn.cursor()
      
        
        cursor.execute(sql)
        conn.commit()
              
        cursor.close()
        conn.close()
        
    def open_details(self):
        
        user_details = User_Details()
        widget.addWidget(user_details)
        widget.setCurrentIndex(widget.currentIndex()+1)
    
     
        
class User_Details(QDialog):
    
    def __init__(self):
        
        super(User_Details,self).__init__()
        self.ui = uic.loadUi("details.ui",self) 
        self._initialize_table()
        self._initialize_username_menu()
        self.display_button.clicked.connect(self._select_details)
    
    def _initialize_username_menu(self):
   
        conn = make_connection(config_file = 'hosp.ini')
        cursor = conn.cursor()
        
      
        
        cursor.execute(sql)
        rows = cursor.fetchall()
            
        cursor.close()
        conn.close()
        
        #print(rows)
        # Set the username items to the usernames.
        for row in rows:
            name = row[0] #+ ' ' + row[1]
            self.ui.username_menu.addItem(name, row) 
    
    
    def _initialize_table(self):
    
        self.ui.details_table.clear()

        col = ['  First Name  ', '   Last Name   ','  Gender  ','  username  ']
        self.ui.details_table.setHorizontalHeaderLabels(col)    
        
        
    def _select_details(self):
        
        
        conn = make_connection(config_file = 'hosp.ini')
        cursor = conn.cursor()
               
        name = self.ui.username_menu.currentData()
        
            
            
        cursor.execute(sql)
        rows = cursor.fetchall()
              
        cursor.close()
        conn.close()
        
        row_index = 0
        for row in rows:
            column_index = 0
            
            for data in row:
                item = QTableWidgetItem(str(data))
                self.ui.details_table.setItem(row_index, column_index, item)
                column_index += 1

            row_index += 1
                    
 """               

class MainWindow(QtWidgets.QStackedWidget):
    def __init__(self):
        super().__init__()
        self.login_screen = Login()
        self.register_screen = Register()
        self.user_details_screen = User_Details()

        self.addWidget(self.login_screen)
        self.addWidget(self.register_screen)
        self.addWidget(self.user_details_screen)

        self.setFixedWidth(580)
        self.setFixedHeight(620)

        self.login_screen.register_here_button.clicked.connect(self.goto_register)
        self.register_screen.back_button.clicked.connect(self.goto_login)
        self.register_screen.show_button.clicked.connect(self.goto_details)

    def goto_register(self):
        self.setCurrentIndex(self.indexOf(self.register_screen))

    def goto_login(self):
        self.setCurrentIndex(self.indexOf(self.login_screen))
        
    def goto_details(self):
        self.setCurrentIndex(self.indexOf(self.user_details_screen))
"""        
def main():
    app = QApplication(sys.argv)
    widget = MainWindow()
    widget.show()
    try:
        app.exec_()
        #sys.exit(app_exec())
    except:
        print("Exiting gracefully")
if __name__=='__main__':
    app = QApplication(sys.argv)
    main()
"""
app = QApplication(sys.argv)
widget = MainWindow()
#mainwindow = Login()
#widget = QtWidgets.QStackedWidget()
#widget.addWidget(mainwindow)
#widget.setFixedWidth(580)
#widget.setFixedHeight(620)
widget.show()
app.exec()







