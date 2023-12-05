import sys
from datetime import datetime
import numpy as np
import datetime
#from scipy.stats import norm
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QDateEdit,QDialog,QGridLayout ,QApplication,QLabel,QVBoxLayout,QPushButton, QComboBox,QHBoxLayout
from PyQt5.QtCore import QDate
from DATA225utils import make_connection, dataframe_query,read_config
class Canvas(FigureCanvas):
    def __init__(self,parent):
        fig, self.ax= plt.subplots(figsize=(50,50),gridspec_kw=({'bottom': 0.35,'left': 0.25}))
        super().__init__(fig)
        self.setParent(parent)


    def plot_logs(self): #optional (date1,date2,specialization)
        """self.clear_axes()"""
        conn = make_connection(config_file='hosp.ini')
        cursor = conn.cursor()

        sql = """SELECT username,count(log_id) as no_of_logins FROM login_log group by username"""

        cursor.execute(sql)
        rows = cursor.fetchall()
        # print(rows)
        cursor.close()
        conn.close()

        user, login = zip(*rows)
        self.ax.clear()
        self.ax.bar(user, login, color='blue')
        self.ax.set(xlabel='Names', ylabel='Logins', title='Bar Chart of User Logins')
        # self.ax.grid()
        self.draw()

    def patient_by_location(self): #4 DONE

        conn_warehouse = make_connection(config_file='hosp-wh.ini')
        cursor = conn_warehouse.cursor()

        sql = """SELECT Patient_Location, count(Patient_ID) as p_count From Patient Group by Patient_Location order by p_count desc limit 8"""
        cursor.execute(sql)
        rows = cursor.fetchall()
        cursor.close()
        conn_warehouse.close()

        locations, counts = zip(*rows)

        self.ax.clear()
        self.ax.barh(locations, counts, color='green')
        self.ax.set(xlabel='Number of Patients', ylabel='Location', title=f'Patients by Location')
        # self.ax.grid()
        self.draw()

    def consult_duration_boxplot(self, ail): #3 boxplot with health_issue

        #
        conn_warehouse = make_connection(config_file='hosp-wh.ini')
        cursor = conn_warehouse.cursor()
        if ail=='All':
            sql="""Select Consultation_Duration from Consultation """
        else:
            sql=f"""Select Consultation_Duration from Consultation where Health_Issue = '{ail}'"""

        #sql = f"""Select Consultation_Duration from Consultation where Health_Issue ='{ail}'"""
        cursor.execute(sql)
        rows = cursor.fetchall()
        #print(ail)
        #print(rows)
        cursor.close()
        conn_warehouse.close()

        #locations, counts = zip(*rows)
        numbers = [item[0] for item in rows]
        #print(numbers)
        self.ax.clear()
        self.ax.boxplot(numbers,showfliers=True, showmeans=True, showbox=True, patch_artist=True)
        stat_values = {
            'Mean': np.mean(numbers),
            'Q1': np.percentile(numbers, 25),
            'Q3': np.percentile(numbers, 75),
        }

        for stat, value in stat_values.items():
            self.ax.text(1.1, value, f'{stat}: {value:.2f}', color='black', ha='left', va='center')
        self.ax.set(xlabel='Health Issue', ylabel='Consultation Duration',title=f'Consultation Durations: {ail}')#{ail}
        self.draw()

    def pie_gender_on_issue(self,ail):#2

        if ail=='All':
            sql=""" SELECT d.Specialization,
                    COUNT(CASE WHEN p.Gender = 'Male' THEN 1 END) AS male_count,
                    COUNT(CASE WHEN p.Gender = 'Female' THEN 1 END) AS female_count
                    FROM Doctor d
                    JOIN Consultation c ON d.Doctor_id = c.Doctor_id
                    JOIN Patient p ON c.Patient_ID = p.Patient_ID GROUP BY d.Specialization;"""
            conn = make_connection(config_file='hosp-wh.ini')
            cursor = conn.cursor()

            cursor.execute(sql)
            rows = cursor.fetchall()
            # print(rows)
            cursor.close()
            conn.close()
            # Extracting labels and sizes from the data
            labels = ['Male', 'Female']
            sizes = [rows[0][1], rows[0][2]]
            colors = ['lightblue', 'lightcoral']

            self.ax.clear()
            self.ax.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors, startangle=90)
            self.ax.set_title(f'Gender Distribution for Specialization: {ail}')

            # self.ax.grid()
            self.draw()

        else:
            sql = f"""SELECT d.Specialization,COUNT(CASE WHEN p.Gender = 'Male' THEN 1 END) AS male_count,COUNT(CASE WHEN p.Gender = 'Female' THEN 1 END) AS female_count FROM Doctor d JOIN Consultation c ON d.Doctor_id = c.Doctor_id JOIN Patient p ON c.Patient_ID = p.Patient_ID WHERE d.Specialization = '{ail}' GROUP BY d.Specialization"""
            conn = make_connection(config_file='hosp-wh.ini')
            cursor = conn.cursor()

            cursor.execute(sql)
            rows = cursor.fetchall()
            # print(rows)
            cursor.close()
            conn.close()
            # Extracting labels and sizes from the data
            labels = ['Male', 'Female']
            sizes = [rows[0][1], rows[0][2]]
            colors = ['lightblue', 'lightcoral']

            self.ax.clear()
            self.ax.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors, startangle=90)
            self.ax.set_title(f'Gender Distribution for Specialization: {ail}')

            # self.ax.grid()
            self.draw()

    def age_distribution(self,ail): #1
        """self.clear_axes()"""
        if ail=='All':
            sql="""select Date_of_Birth from Patient p """
        else:
            sql=f"""select Date_of_Birth from Patient p join Consultation c on c.Patient_ID=p.Patient_ID where c.Health_Issue ='{ail}'"""

        conn = make_connection(config_file='hosp-wh.ini')
        cursor = conn.cursor()

        cursor.execute(sql)
        rows = cursor.fetchall()

        cursor.close()
        conn.close()

        dates = [item[0] for item in rows]
        today = datetime.date.today()
        ages = [(today - date).days // 365 for date in dates]

        # Clear the existing plot and create a box plot
        self.ax.clear()
        self.ax.hist(ages, bins=20, color='skyblue', edgecolor='black')
        self.ax.set(xlabel='Age', ylabel='Number of Patients', title=f'Age Distribution of Patients for {ail}')
        #self.ax.plot(sorted(ages), norm.pdf(sorted(ages), np.mean(ages), np.std(ages)), color='red',label='Distribution Line')

        self.draw()

    """def clear_axes(self,ax):
        self.ax.clear()"""
    def patient_visits(self,date1,date2): # other 1 bar graph

        # count of patients for each health issue

        conn = make_connection(config_file='hosp-wh.ini')
        cursor = conn.cursor()

        sql = """SELECT username,count(log_id) as no_of_logins FROM login_log where group by username"""

        cursor.execute(sql)
        rows = cursor.fetchall()
        # print(rows)
        cursor.close()
        conn.close()

        user, login = zip(*rows)
        self.ax.clear()
        self.ax.bar(user, login, color='green')
        self.ax.set(xlabel='Names', ylabel='Logins', title=f'Patients visited between {date1} & {date2}')
        self.ax.tick_params(axis='x', rotation=60)
        #self.ax.grid(axis='x', linestyle='--', pha=0.6)
        self.draw()

    def patient_count_health_issue(self,p_s): #2 bar graph backpain

        conn = make_connection(config_file='hosp-wh.ini')
        cursor = conn.cursor()
        sql = """SELECT Health_Issue, count(Prescription_ID) as coun FROM Prescription group by Health_Issue order by coun desc"""

        cursor.execute(sql)
        rows = cursor.fetchall()
        # print(rows)
        cursor.close()
        conn.close()

        health_issues, num_patients = zip(*rows)
        self.ax.clear()
        self.ax.bar(health_issues, num_patients, color='skyblue')
        self.ax.set(xlabel='Health Issues', ylabel='Number of Patients', title=f'Number of Patients for Each Health Issue')
        self.ax.tick_params(axis='x', rotation=75)
        #self.ax.grid(axis='x', linestyle='--', alpha=0.6)
        self.draw()


    def doctor_count_by_specialization(self,spez):
        """self.clear_axes()"""
        conn = make_connection(config_file='hosp.ini')
        cursor = conn.cursor()

        sql = """SELECT username,count(log_id) as no_of_logins FROM login_log group by username"""

        cursor.execute(sql)
        rows = cursor.fetchall()
        # print(rows)
        cursor.close()
        conn.close()

        user, login = zip(*rows)
        self.ax.clear()
        self.ax.bar(user, login, color='red')
        self.ax.set(xlabel='Names', ylabel='Logins', title='Top 10 Billings')
        # self.ax.grid()
        self.draw()

    def billing_date_range(self,date1,date2):
        """self.clear_axes()"""
        conn = make_connection(config_file='hosp.ini')
        cursor = conn.cursor()

        sql = f"""select Amount_Billed from Billing b join Prescription p on p.Prescription_ID=b.Prescription_ID where Prescription_date between'{start_date}' and '{end_date}'"""

        cursor.execute(sql)
        rows = cursor.fetchall()
        # print(rows)
        cursor.close()
        conn.close()

        user, login = zip(*rows)
        self.ax.clear()
        self.ax.bar(user, login, color='red')
        self.ax.set(xlabel='Names', ylabel='Logins', title=f'Appointments from {date1} to {date2}')
        # self.ax.grid()
        self.draw()

    def highest_consulting_fees_specialization(self,spez):
        """self.clear_axes()"""
        conn = make_connection(config_file='hosp.ini')
        cursor = conn.cursor()

        sql =f"""select distinct(Consultation_Fee) from Consultation c join Doctor d on d.Doctor_ID = c.Doctor_ID where d.Specialization ='{spez}' order by Consultation_Fee desc limit 10"""

        cursor.execute(sql)
        rows = cursor.fetchall()
        # print(rows)
        cursor.close()
        conn.close()

        user, login = zip(*rows)
        self.ax.clear()
        self.ax.bar(user, login, color='red')
        self.ax.set(xlabel='Names', ylabel='Logins', title='Top 10 Billings')
        # self.ax.grid()
        self.draw()

    def doc_earnings_scatter(self):
        """self.clear_axes()"""
        conn = make_connection(config_file='hosp.ini')
        cursor = conn.cursor()

        sql = """SELECT username,count(log_id) as no_of_logins FROM login_log group by username"""

        cursor.execute(sql)
        rows = cursor.fetchall()
        # print(rows)
        cursor.close()
        conn.close()

        user, login = zip(*rows)
        self.ax.clear()
        self.ax.bar(user, login, color='red')
        self.ax.set(xlabel='Names', ylabel='Logins', title='Top 10 Billings')
        # self.ax.grid()
        self.draw()
    def prescription_timeline(self,start_date,end_date):#,start_date,end_date
        conn = make_connection(config_file='hosp-wh.ini')
        cursor = conn.cursor()
        # prescriptions by day
        sql3 = f""" Select Prescription_date, count(Prescription_ID) as prescription_count from Prescription where Prescription_date BETWEEN '{start_date}' AND '{end_date}' group by Prescription_date"""

        cursor.execute(sql3)
        rows = cursor.fetchall()
        # print(rows)
        cursor.close()
        conn.close()

        rows.sort(key=lambda x: x[0])
        dates = [item[0] for item in rows]
        counts = [item[1] for item in rows]


        # Plotting the timeline graph using line
        self.ax.clear()
        self.ax.plot(dates, counts, marker='o', linestyle='-', color='red')
        self.ax.set(xlabel='Date', ylabel='Prescription Count', title='Prescription Counts Over Time')
        # Rotate x-axis tick labels
        self.ax.tick_params(axis='x', rotation=45)
        self.draw()
    def consultation_scatter(self,sp):
        conn = make_connection(config_file='hosp-wh.ini')
        cursor = conn.cursor()
        if sp=='All':
            sql = f"""  select C.Consultation_Fee, count(Patient_ID) from Consultation C join Doctor D on D.Doctor_ID=C.Doctor_ID WHERE D.Specialization ='{sp}'GROUP BY C.Consultation_Fee order by count(Patient_ID) desc limit 5
"""

        cursor.execute(sql)
        rows = cursor.fetchall()
        # print(rows)
        cursor.close()
        conn.close()

        consulting_fee,specialization,num_patients = zip(*rows)

        # Assuming self.ax is an AxesSubplot
        self.ax.clear()

        # Create a scatter plot
        self.ax.scatter(num_patients, consulting_fee, color='red')

        # Set labels and title
        self.ax.set(xlabel='Number of Patients', ylabel='Consulting Fee',title='Scatter Plot of Consulting Fee vs Number of Patients')

        # Adding text labels for each point
        for i in range(len(rows)):
            self.ax.text(num_patients[i], consulting_fee[i], specialization[i])

        # Show the plot
        self.draw()
        """self.ax.clear()
        self.ax.bar(user, login, color='red')
        self.ax.set(xlabel='Names', ylabel='Logins', title='Top 10 Billings')
        # self.ax.grid()
        self.draw()"""
class AppDemo(QDialog): #QWidget for Widget based

    def __init__(self):
        super().__init__()

        self.resize(1000,1000)
        self.setWindowTitle("Login Analytics")  # Set the window title

        layout = QVBoxLayout(self)

        # Create a combo box for selecting user type
        user_type_label = QLabel("Analyze info of:")
        self.user_type_combo = QComboBox(self)
        self.user_type_combo.addItems(["Patient", "Doctor","Other"])
        self.user_type_combo.currentIndexChanged.connect(self.update_graph)

        # Create a horizontal layout for the user type combo box
        user_type_layout = QHBoxLayout()
        user_type_layout.addWidget(user_type_label)
        user_type_layout.addWidget(self.user_type_combo)
        layout.addLayout(user_type_layout)

        # Common combo box for locations and specializations
        self.common_combo = QComboBox(self)
        layout.addWidget(self.common_combo)

        # This layout will arrange its child widgets horizontally.
        self.combo_layout = QHBoxLayout()
        # Date ComboBox
        self.start_date_combo = QDateEdit(self)
        self.start_date_combo.setDate(QDate.currentDate())
        self.start_date_combo.setCalendarPopup(True)
        self.combo_layout.addWidget(self.start_date_combo)

        self.end_date_combo = QDateEdit(self)
        self.end_date_combo.setDate(QDate.currentDate())
        self.end_date_combo.setCalendarPopup(True)
        self.combo_layout.addWidget(self.end_date_combo)

        # Add the horizontal layout to the main layout
        layout.addLayout(self.combo_layout)

        # Vertical Layout for Buttons
        button_layout = QVBoxLayout()

        # Add a button to trigger graph update
        self.update_button = QPushButton("Update Graph", self)
        self.update_button.clicked.connect(self.update_graph)
        button_layout.addWidget(self.update_button)

        self.close_button = QPushButton("Close Window", self)
        self.close_button.clicked.connect(self.close_window)
        button_layout.addWidget(self.close_button)

        # Add the vertical layout to the main layout
        layout.addLayout(button_layout)

        # Create a grid layout for the graphs
        graph_layout = QGridLayout()

        self.chart1 = Canvas(self)
        self.chart2 = Canvas(self)
        self.chart3 = Canvas(self)
        self.chart4 = Canvas(self)

        # Add the Canvas widgets to the grid layout
        graph_layout.addWidget(self.chart1, 0, 0)
        graph_layout.addWidget(self.chart2, 0, 1)
        graph_layout.addWidget(self.chart3, 1, 0)
        graph_layout.addWidget(self.chart4, 1, 1)

        # Add the grid layout to the main layout
        layout.addLayout(graph_layout)

        # Set the initial visibility of the graphs to False
        self.chart1.setVisible(False)
        self.chart2.setVisible(False)
        self.chart3.setVisible(False)
        self.chart4.setVisible(False)

    def update_graph(self):

        # Get selected user type
        user_type = self.user_type_combo.currentText()
        present_loc_spez = self.common_combo.currentText()
        start_date = self.start_date_combo.date().toString("yyyy-MM-dd")
        end_date = self.end_date_combo.date().toString("yyyy-MM-dd")

        # Determine the title based on the user type
        if user_type == "Patient":
             if self.common_combo.currentText() not in ['All','Anxiety','Hypertension','Infection','Asthma','Flu','Cold','Depression','Thyroid','Appendix','Gynecology','Nasal problem','Liver problems','Brain','Cardiac','Kidney','Stomach problems']:
                 self.common_combo.clear()
                 present_loc='All'
             self.common_combo.addItems(['All','Anxiety','Hypertension','Infection','Asthma','Flu','Cold','Depression','Thyroid','Appendix','Gynecology','Nasal problem','Liver problems','Brain','Cardiac','Kidney','Stomach problems'])
             present_loc = self.common_combo.currentText()
             self.show_patient_graphs(present_loc,start_date,end_date)
             self.chart1.setVisible(True)
             self.chart2.setVisible(False)
             self.chart3.setVisible(True)
             self.chart4.setVisible(True)


        elif user_type == "Doctor":
            if self.common_combo.currentText() not in ['All','Allergist','Endocrinologist','Psychiatrist','Infectious Disease Specialist','General Practitioner','Pulmonologist','Orthopedist','Cardiologist','General Surgeon','Gynecologist','Otolaryngologist','Hepatologist','Neurologist','Nephrologist','Gastroenterologist']:
                self.common_combo.clear()
                present_loc = 'All'
            self.common_combo.addItems(['All','Allergist','Endocrinologist','Psychiatrist','Infectious Disease Specialist','General Practitioner','Pulmonologist','Orthopedist','Cardiologist','General Surgeon','Gynecologist','Otolaryngologist','Hepatologist','Neurologist','Nephrologist','Gastroenterologist'])
            present_loc = self.common_combo.currentText()
            self.show_doctor_graphs(present_loc,start_date,end_date)
            self.chart1.setVisible(True)
            self.chart2.setVisible(False)
            self.chart3.setVisible(False)
            self.chart4.setVisible(False)
        else:
            self.common_combo.clear()
            self.common_combo.addItems(["Prescription", "Surgical"])
            self.create_default_combos(present_loc_spez,start_date,end_date)
            self.chart1.setVisible(True)
            self.chart2.setVisible(True)
            self.chart3.setVisible(False)
            self.chart4.setVisible(False)


        """self.chart1.setVisible(True)
        self.chart2.setVisible(False)
        self.chart3.setVisible(False)
        self.chart4.setVisible(False)"""
    def show_patient_graphs(self,present_loc_spez,start_date,end_date):

        self.chart1.age_distribution(present_loc_spez)
        #self.chart2.pie_gender_on_issue(present_loc_spez)
        self.chart3.consult_duration_boxplot(present_loc_spez)
        self.chart4.patient_by_location()

    def show_doctor_graphs(self,present_loc_spez,start_date,end_date):
        pass
        self.chart1.pie_gender_on_issue(present_loc_spez)
        #self.chart2.consultation_scatter()
        #self.chart3.doctor_earning_by_specialization()
        #self.chart4.consults_range(start_date,end_date)


    def create_default_combos(self,present_loc_spez,start_date,end_date):
        # Remove existing combo boxes
        """self.chart3.setVisible(False)
        self.chart4.setVisible(False)"""

        self.chart1.patient_count_health_issue(present_loc_spez)
        self.chart2.prescription_timeline(start_date, end_date)

        #self.chart3.patient_by_alignment()
        #self.chart4.prescription_pattern(start_date, end_date)

    def close_window(self):
        self.close()

    """def clear_combos(self):
        # Clear existing combo boxes
        for i in reversed(range(self.combo_layout.count())):
            print(range(self.combo_layout.count()))
            widget = self.combo_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)"""

    """def close_analytics(self):
        # Switch back to the main page
        self.stacked_widget.setCurrentIndex(0)"""

    """" 
        use this in the hospital portal __init__ functino to open this analytics page
        from appdemo import AppDemo
    
     # Create a button to open the AppDemo window
        open_analytics_button = QPushButton("Open Analytics", self)
        open_analytics_button.clicked.connect(self.open_analytics)
        self.setCentralWidget(open_analytics_button)
        
    def open_analytics(self):
        # Create an instance of AppDemo and show it
        app_demo = AppDemo()
        app_demo.show()
        """
""""
app=QApplication(sys.argv)
demo=AppDemo()
demo.show()
sys.exit(app.exec_())
"""