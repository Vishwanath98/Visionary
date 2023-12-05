import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QStackedWidget, QPushButton

#from appointments import Appointment
from appointments import Appointment
from graph import AppDemo
from hosp_past_appointments import Hosp_Past_Appointments
from hospital_appointments import Hospital_Appointments
from hospital_home import Hospital_Home
from login import LoginWindow
from manage_appointments import AppointmentManager
from patient_dashboard import Patient_Dashboard
from post_appointment import DoctorFeedback
from register import RegistrationWindow
from patient_home import PatientHomePage
from welcome_page import Welcome_Page
from hospital_login import Hospital_Login

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("Hospital Appointment App")

        # Create a stacked widget to switch between pages
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        # Create instances of the pages
        self.welcome_page = Welcome_Page()
        self.stacked_widget.addWidget(self.welcome_page)
        self.welcome_page.pushButton.clicked.connect(self.show_login)
        self.welcome_page.pushButton_2.clicked.connect(self.show_hosp_login)

        self.login_window = LoginWindow()
        self.login_window.login_successful.connect(self.handle_login_successful)
        self.login_window.pushButton.clicked.connect(self.show_welcome_page)
        self.stacked_widget.addWidget(self.login_window)

        self.hospital_window = Hospital_Login()
        self.stacked_widget.addWidget(self.hospital_window)
        self.hospital_window.login_button.clicked.connect(self.show_hospital_home)
        self.hospital_window.pushButton.clicked.connect(self.show_welcome_page)

        self.hospital_home = Hospital_Home()
        self.stacked_widget.addWidget(self.hospital_home)
        self.hospital_home.new_appointments.clicked.connect(self.show_hospital_appointments)
        self.hospital_home.pushButton_3.clicked.connect(self.show_analytics)
        self.hospital_home.past_appointments.clicked.connect(self.show_past_appointments)

        self.hospital_appointments = Hospital_Appointments()
        self.stacked_widget.addWidget(self.hospital_appointments)
        self.hospital_appointments.back_button.clicked.connect(self.show_hospital_home)

        self.patient_dashboard = Patient_Dashboard()
        self.stacked_widget.addWidget(self.patient_dashboard)
        self.patient_dashboard.pushButton_2.clicked.connect(self.back_function)

        self.graph = AppDemo()
        self.stacked_widget.addWidget(self.graph)


        self.registration_window = RegistrationWindow()
        self.stacked_widget.addWidget(self.registration_window)
        self.login_window.register_here_button.clicked.connect(self.show_registration)
        self.registration_window.back_button.clicked.connect(self.show_login)

        self.patient_home = PatientHomePage()
        self.stacked_widget.addWidget(self.patient_home)
        self.patient_home.logout_button.clicked.connect(self.show_login)
        self.patient_home.my_health_button.clicked.connect(self.show_dashboard)


        ''' the appointment page is missing'''
        self.appointment = Appointment()


        self.stacked_widget.addWidget(self.appointment)
        self.patient_home.appointment_button.clicked.connect(self.make_appointment)
        #self.patient_home.manage_appointments_button.connect(self.manage_appointment)
        self.appointment.pushButton_2.clicked.connect(self.back_function)

        self.past_appointments = Hosp_Past_Appointments()
        self.stacked_widget.addWidget(self.past_appointments)
        self.past_appointments.back_button.clicked.connect(self.show_hospital_home)
        #add post appointments screen when clicked
        self.past_appointments.edit_button.clicked.connect(self.show_doctor_feedback)

        self.doctor_feedback = DoctorFeedback()
        self.stacked_widget.addWidget(self.doctor_feedback)
        self.doctor_feedback.back_button.clicked.connect(self.show_past_appointments)

        self.manage = AppointmentManager()
        self.stacked_widget.addWidget(self.manage)
        self.patient_home.manage_appointments_button.clicked.connect(self.manage_appointment)
        self.manage.back_button.clicked.connect(self.back_function)
        # Set the default page to the login window
        self.stacked_widget.setCurrentWidget(self.welcome_page)

        # Create actions to switch between pages in the menu
        self.login_action = QAction("Login", self)
        self.login_action.triggered.connect(self.show_login)

        self.register_action = QAction("Register", self)
        self.register_action.triggered.connect(self.show_registration)

        self.patient_home_action = QAction("Patient Home", self)
        self.patient_home_action.triggered.connect(self.show_patient_home)
        self.graph.close_button.clicked.connect(self.fixed_issue)
        # Create a menu bar
        #menu_bar = self.menuBar()
        #menu_bar.addAction(self.login_action)
        #menu_bar.addAction(self.register_action)
        #menu_bar.addAction(self.patient_home_action)

        self.show()

    def show_welcome_page(self):
        self.stacked_widget.setCurrentWidget(self.welcome_page)
    def show_login(self):
        self.stacked_widget.setCurrentWidget(self.login_window)
        self.login_window.user_name.clear()
        self.login_window.l_password.clear()
        self.login_window.checkBox.setChecked(False)

    def show_hosp_login(self):
        self.stacked_widget.setCurrentWidget(self.hospital_window)

    def show_hospital_home(self):
        self.stacked_widget.setCurrentWidget(self.hospital_home)

    def show_hospital_appointments(self):
        self.stacked_widget.setCurrentWidget(self.hospital_appointments)

    def show_past_appointments(self):
        self.stacked_widget.setCurrentWidget(self.past_appointments)

    def show_doctor_feedback(self):
        self.stacked_widget.setCurrentWidget(self.doctor_feedback)
    def show_analytics(self):
        self.stacked_widget.setCurrentWidget(self.graph)

    def show_registration(self):
        self.stacked_widget.setCurrentWidget(self.registration_window)
        self.registration_window.first_name.clear()
        self.registration_window.last_name.clear()
        self.registration_window.user_name.clear()
        self.registration_window.email.clear()
        self.registration_window.password.clear()
        self.registration_window.confirm_pass.clear()
        #self.registration_window.radio_button_1.clear()
        #self.registration_window.radio_button_2.clear()

    def show_patient_home(self,user_name):
        self.stacked_widget.setCurrentWidget(self.patient_home)
        self.patient_home.u_name.setText(user_name)
        self.patient_home.profile(user_name)
        

    def make_appointment(self,user_name):
        self.stacked_widget.setCurrentWidget(self.appointment)

    def manage_appointment(self):
        #print("manage")
        self.stacked_widget.setCurrentWidget(self.manage)

    def show_dashboard(self):
        self.stacked_widget.setCurrentWidget(self.patient_dashboard)

    def handle_login_successful(self,user_name):
        self.show_patient_home(user_name)
    
    def back_function(self,user_name):
        self.stacked_widget.setCurrentWidget(self.patient_home)
        
    def fixed_issue(self):
        self.stacked_widget.setCurrentWidget(self.hospital_window)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
