import sys
import numpy as np
from PyQt5.QtWidgets import QSpinBox, QDialog, QTextEdit, QApplication, QLabel, QVBoxLayout, QPushButton, QComboBox, \
    QHBoxLayout
from PyQt5.QtCore import QDate
from DATA225utils import make_connection


class DoctorFeedback(QDialog):  # QWidget for Widget based

    def __init__(self):
        super().__init__()

        self.resize(400, 200)
        self.setWindowTitle("Doctor Feedback")  # Set the window title

        layout = QVBoxLayout(self)

        # Create a combo box for selecting user type
        user_type_label = QLabel("Provide feedback on:")
        self.feedback_type = QComboBox(self)
        self.feedback_type.addItems(["Prescription", "Treatment", ])
        self.feedback_type.currentIndexChanged.connect(self.update_feedback_ui)

        # Create a horizontal layout for the feedback type combo box
        feedback_type_layout = QHBoxLayout()
        feedback_type_layout.addWidget(user_type_label)
        feedback_type_layout.addWidget(self.feedback_type)
        layout.addLayout(feedback_type_layout)

        # horizontal layer 2
        type_data_layout = QHBoxLayout()

        # Common combo box for locations and specializations
        self.common_list_space = QComboBox(self)
        type_data_layout.addWidget(self.common_list_space)

        # if feed_type=='Prescription'

        self.quantity_Sestimate = QSpinBox(self)
        type_data_layout.addWidget(self.quantity_Sestimate)

        layout.addLayout(type_data_layout)

        # Horizontal Layer 3
        text_data_layout = QHBoxLayout()
        feed_text = QTextEdit(self)
        text_data_layout.addWidget(feed_text)
        layout.addLayout(text_data_layout)

        # Horizontal Layer 4
        button_layout = QHBoxLayout()

        # Back button
        self.back_button = QPushButton("Back", self)
        #back_button.clicked.connect(self.close_window)
        button_layout.addWidget(self.back_button)

        self.confirm_button = QPushButton("Confirm", self)
        self.confirm_button.clicked.connect(self.confirm_feedback)
        button_layout.addWidget(self.confirm_button)

        layout.addLayout(button_layout)

    def update_feedback_ui(self):

        # Get selected user type
        feed_type = self.feedback_type.currentText()

        # Determine the title based on the user type
        if feed_type == "Prescription":
            self.common_list_space.clear()
            self.common_list_space.addItems(["Medicine 1", "Medicine 2"])
            # self.text_data_layout.addWidget(self.feed_text)

        elif feed_type == "Treatment":
            self.common_list_space.clear()
            self.common_list_space.addItems(["Surgery 1", "Surgery 2"])
            # self.text_data_layout.removeWidget(self.feed_text)
            # self.text_data_layout.setParent(None)

    def confirm_feedback(self):
        feed_type = self.feedback_type.currentText()
        selected_item = self.common_list_space.currentText()
        quantity_estimate = self.quantity_Sestimate.value()
        feedback_text = self.findChild(QTextEdit).toPlainText()

        # if feed_type=='Prescription':
        # conn = make_connection(config_file='hosp.ini')
        # cursor = conn.cursor()

        # sql = f"""INSERT into Prescription values ({patient_name},{})"""

        # cursor.execute(sql)
        # rows = cursor.fetchall()
        # print(rows)
        # cursor.close()
        # conn.close()
        # elif feed_type=='Treatment':

        print(f"Feedback Type: {feed_type}")
        print(f"Selected Item: {selected_item}")
        print(f"Quantity/Surgery Cost Estimate: {quantity_estimate}")
        print(f"Feedback Text: {feedback_text}")

    def close_window(self):
        self.close()


""""        
app=QApplication(sys.argv)
DF=DoctorFeedback()
DF.show()
sys.exit(app.exec_())
"""
