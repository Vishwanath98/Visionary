#!/usr/bin/env python
# coding: utf-8
import sys
from PyQt5 import QtWidgets,uic
from PyQt5.QtWidgets import QDialog, QApplication,QTableWidgetItem
from PyQt5.uic import loadUi
from DATA225utils import make_connection

class Login(QDialog):
    def __init__(self):
        super(Login,self).__init__()
        self.ui = uic.loadUi("login.ui",self)
        self.setWindowTitle("Login")
        self.login_button.clicked.connect(self.loginfunction)
        self.register_here_button.clicked.connect(self.create)
        
    def loginfunction(self):
        user_name=self.user_name.text()
        password=self.l_password.text()
        print("Successfully logged in with username: ",user_name, "and password",password) 
        
    def create(self):
        register = Register()
        widget.addWidget(register)
        widget.setCurrentIndex(widget.currentIndex()+1)
        
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
        
        sql="""INSERT INTO register VALUES""" f" ('{first_name}', '{last_name}','{gender}', '{user_name}', '{pwd}')"
        
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
        """
        Initialize the username menu with userid  from the database.
        """
        conn = make_connection(config_file = 'hosp.ini')
        cursor = conn.cursor()
        
        sql = """SELECT distinct(gender) FROM register"""
        
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
        """
        Clear the table and set the column headers.
        """
        self.ui.details_table.clear()

        col = ['  First Name  ', '   Last Name   ','  Gender  ','  username  ']
        self.ui.details_table.setHorizontalHeaderLabels(col)    
        
        
    def _select_details(self):
        
        
        conn = make_connection(config_file = 'hosp.ini')
        cursor = conn.cursor()
               
        name = self.ui.username_menu.currentData()
        sql= (""" SELECT first_name,last_name,gender,username from register """ f" WHERE gender = '{name[0]}' ")
            
            
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
                    
                
                
app = QApplication(sys.argv)
mainwindow = Login()
widget = QtWidgets.QStackedWidget()
widget.addWidget(mainwindow)
widget.setFixedWidth(580)
widget.setFixedHeight(620)
widget.show()
app.exec()






