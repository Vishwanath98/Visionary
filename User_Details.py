import sys
from PyQt5 import QtWidgets,uic
from PyQt5.QtWidgets import QDialog, QApplication,QTableWidgetItem
from PyQt5.uic import loadUi
from DATA225utils import make_connection
from RegisterDialog import *

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
        sql= (""" SELECT first_name,last_name,gender,user_name from register """ f" WHERE gender = '{name[0]}' ")
            
            
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
            
