import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QDateEdit,QDialog,QMainWindow,QApplication, QWidget,QVBoxLayout,QPushButton, QComboBox,QHBoxLayout
from PyQt5.QtCore import QDate
from DATA225utils import make_connection
class Canvas(FigureCanvas):
    def __init__(self,parent):
        fig, self.ax= plt.subplots(figsize=(5,4),dpi=100)
        super().__init__(fig)
        self.setParent(parent)



    def plot_logs(self):

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


class AppDemo(QDialog): #QWidget for Widget based
    def __init__(self):
        super().__init__()
        self.resize(500,500)
        self.setWindowTitle("Login Analytics")  # Set the window title

        #central_widget = QWidget(self)
        #self.setCentralWidget(central_widget) #remove for QWidget doesnt work
        # organize the widgets within the central widget.
        # This layout will arrange its child widgets vertically.
        layout = QVBoxLayout(self)
        combo_layout=QHBoxLayout()

        # Add a dropdown filter for selecting chart type
        self.chart_type_combo = QComboBox(self)
        self.chart_type_combo.addItems(["Bar Chart", "Line Chart","Scatter Plot"])
        combo_layout.addWidget(self.chart_type_combo)

        # Specialization ComboBox
        self.specialization_combo = QComboBox(self)
        self.specialization_combo.addItems(["Specialization 1", "Specialization 2", "Specialization 3"])
        combo_layout.addWidget(self.specialization_combo)

        # Date ComboBox
        self.start_date_combo = QDateEdit(self)
        self.start_date_combo.setDate(QDate.currentDate())
        self.start_date_combo.setCalendarPopup(True)
        combo_layout.addWidget(self.start_date_combo)

        self.end_date_combo = QDateEdit(self)
        self.end_date_combo.setDate(QDate.currentDate())
        self.end_date_combo.setCalendarPopup(True)
        combo_layout.addWidget(self.end_date_combo)

        # Add the horizontal layout to the main layout
        layout.addLayout(combo_layout)

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

        self.chart = Canvas(self)
        layout.addWidget(self.chart)

        #self.chart.plot_logs()

    def update_graph(self):
        selected_chart = self.chart_type_combo.currentText()

        if selected_chart == "Bar Chart":
            self.chart.plot_logs()
        #elif selected_chart == "Line Chart":
            #self.chart.plot_line_chart(self.data)

    def close_window(self):
        self.close()

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

app=QApplication(sys.argv)
demo=AppDemo()
demo.show()
sys.exit(app.exec_())