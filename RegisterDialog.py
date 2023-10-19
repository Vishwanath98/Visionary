#!/usr/bin/env python
# coding: utf-8

# In[1]:


import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QApplication, QTableWidgetItem, QHeaderView
from DATA225utils import make_connection


# In[ ]:


class RegisterDialog(QDialog):
    """
        Load the UI and initialize its components.
        """
        super().__init__()
        
        # Load the dialog components.
        self.ui = uic.loadUi('Register_Dialog.ui')
        first = self.lineEdit.text() 
        last = self.lineEdit2.text() 
        email = self.lineEdit3.text() 
        password = self.lineEdit4.text() 
        password_confirm = self.lineEdit5.text()
        
        reg_data=[first,last,email,password,password_confirm]
        self._insert_registration_data()
        
    


# In[ ]:


def show_dialog(self):
      """
      Show this dialog.
      """
      self.ui.show()


# In[ ]:


def _insert_registration_data(self):
        
        
        conn = make_connection(config_file = 'hosp.ini')
        cursor = conn.cursor()
        
        self.cursor.execute(f"INSERT INTO register VALUES ({first}, {last}, {email, password}" 
                            #VALUES (?, ?, ?, ?, ?)", data)
        self.conn.commit()
        
                
        self._adjust_column_widths()
              
        cursor.close()
        conn.close()
        


# In[ ]:


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = RegistertDialog()
    form.show_dialog()
    sys.exit(app.exec_())

