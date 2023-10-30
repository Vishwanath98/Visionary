#!/usr/bin/env python
# coding: utf-8

# In[1]:


import sys
from PyQt5 import QtWidgets,uic
from PyQt5.QtWidgets import QDialog, QApplication,QTableWidgetItem
from PyQt5.uic import loadUi
from DATA225utils import make_connection
from LoginDialog import *
from User_Details import *

# In[ ]:


class Register(QDialog):
    def __init__(self):
        super(Register,self).__init__()
        self.ui = uic.loadUi("register.ui",self)
        self.setWindowTitle("Register")
        self.register_button.clicked.connect(self.registerfunction)
        #self.show_button.clicked.connect(self.open_details)
        #self.back_button.clicked.connect(self.open_login)
        
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
        
    #def open_details(self):
        #user_details = User_Details()
        #widget.addWidget(user_details)
        #widget.setCurrentIndex(widget.currentIndex()+1)
    #def open_login(self):
        #login = Login()
        #widget.addWidget(login)
        #widget.setCurrentIndex(widget.currentIndex()-1)
        
"""
app = QApplication(sys.argv)
mainwindow = Register()
widget = QtWidgets.QStackedWidget()
widget.addWidget(mainwindow)
app.exec()
"""