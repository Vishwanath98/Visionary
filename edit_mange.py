import sys
from unittest import signals

import mysql.connector
from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QListWidget, QPushButton, QDialog, QFormLayout, QLineEdit
from DATA225utils import make_connection

class Edit_Manage(QDialog):
    accepted = pyqtSignal()  # Custom signal to notify the acceptance of the dialog

    def __init__(self, parent=None):
        super(Edit_Manage, self).__init__(parent)

        self.init_ui()

    def init_ui(self):
        layout = QFormLayout()

        # Create a QLineEdit for editing the appointment info
        self.edit_line_edit = QLineEdit()

        layout.addRow(QLabel("Edit Appointment:"), self.edit_line_edit)

        # Add an "OK" button to accept the changes
        ok_button = QPushButton("OK")
        ok_button.clicked.connect(self.handle_accept)

        layout.addRow(ok_button)

        self.setLayout(layout)

    def setAppointmentInfo(self, info):
        # Set the initial appointment info in the QLineEdit
        self.edit_line_edit.setText(info)

    def getEditedInfo(self):
        # Retrieve the edited information from the QLineEdit
        return self.edit_line_edit.text()

    def handle_accept(self):
        # Emit the custom signal when the dialog is accepted
        self.accepted.emit()
        self.accept()