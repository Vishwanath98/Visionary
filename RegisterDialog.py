#!/usr/bin/env python
# coding: utf-8

# In[1]:


import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QApplication, QTableWidgetItem, QHeaderView,QLineEdit, QLabel, QLineEdit
from DATA225utils import make_connection


# In[ ]:


class RegisterDialog(QDialog):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(1102, 837)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(80, 80, 151, 16))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(220, 120, 71, 20))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.lineEdit = QtWidgets.QLineEdit(Dialog)
        self.lineEdit.setGeometry(QtCore.QRect(300, 120, 221, 22))
        self.lineEdit.setObjectName("lineEdit")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(220, 170, 71, 20))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.lineEdit_2 = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_2.setGeometry(QtCore.QRect(300, 170, 221, 22))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.lineEdit_3 = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_3.setGeometry(QtCore.QRect(300, 220, 221, 22))
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setGeometry(QtCore.QRect(220, 220, 71, 20))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.lineEdit_4 = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_4.setGeometry(QtCore.QRect(300, 270, 221, 22))
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.label_5 = QtWidgets.QLabel(Dialog)
        self.label_5.setGeometry(QtCore.QRect(220, 270, 71, 20))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.lineEdit_5 = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_5.setGeometry(QtCore.QRect(300, 320, 221, 22))
        self.lineEdit_5.setObjectName("lineEdit_5")
        self.label_6 = QtWidgets.QLabel(Dialog)
        self.label_6.setGeometry(QtCore.QRect(170, 320, 121, 20))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(Dialog)
        self.label_7.setGeometry(QtCore.QRect(220, 360, 71, 20))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.radioButton = QtWidgets.QRadioButton(Dialog)
        self.radioButton.setGeometry(QtCore.QRect(300, 360, 95, 20))
        self.radioButton.setObjectName("radioButton")
        self.radioButton_2 = QtWidgets.QRadioButton(Dialog)
        self.radioButton_2.setGeometry(QtCore.QRect(300, 390, 95, 20))
        self.radioButton_2.setObjectName("radioButton_2")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "Create Your Account:"))
        self.label_2.setText(_translate("Dialog", "First Name"))
        self.lineEdit.setText(_translate("Dialog", "sandeep"))
        self.label_3.setText(_translate("Dialog", "Last Name"))
        self.lineEdit_2.setText(_translate("Dialog", "Reddy"))
        self.lineEdit_3.setText(_translate("Dialog", "Reddy"))
        self.label_4.setText(_translate("Dialog", "User Name"))
        self.lineEdit_4.setText(_translate("Dialog", "Password"))
        self.label_5.setText(_translate("Dialog", "Password"))
        self.lineEdit_5.setText(_translate("Dialog", "Confirm password"))
        self.label_6.setText(_translate("Dialog", "Confirm Password"))
        self.label_7.setText(_translate("Dialog", "Gender"))
        self.radioButton.setText(_translate("Dialog", "Male"))
        self.radioButton_2.setText(_translate("Dialog", "Female"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi('Register_Dialog.ui')
        self.first = self.lineEdit.text() 
        self.last = self.lineEdit_2.text() 
        self.email = self.lineEdit_3.text() 
        self.password = self.lineEdit_4.text() 
        self.password_confirm = self.lineEdit_5.text()
        
        reg_data=[first,last,email,password,password_confirm]
        self._insert_registration_data()
        
    


# In[ ]:

    def show_dialog(self):
        self.ui.show()


# In[ ]:


    def _insert_registration_data(self):
          
        conn = make_connection(config_file = 'hosp.ini')
        cursor = conn.cursor()
        
        self.cursor.execute(f"INSERT INTO register VALUES ({first}, {last}, {email, password}")
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

