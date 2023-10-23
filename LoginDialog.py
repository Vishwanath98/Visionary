#!/usr/bin/env python
# coding: utf-8
import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.uic import loadUi

class Login(QDialog):
    def __init__(self):
        super(Login,self).__init__()
        loadUi("login.ui",self)
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
        loadUi("register.ui",self)
        self.register_button.clicked.connect(self.registerfunction)
    def registerfunction(self):
        first_name = self.first_name.text()
        last_name = self.last_name.text()
        user_name = self.user_name.text()
        if self.password.text() == self.confirm_pass.text():
            print("password is correct")
                    
app = QApplication(sys.argv)
mainwindow = Login()
widget = QtWidgets.QStackedWidget()
widget.addWidget(mainwindow)
widget.setFixedWidth(480)
widget.setFixedHeight(620)
widget.show()
app.exec()






