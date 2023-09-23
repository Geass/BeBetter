import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QCalendarWidget, QListWidget, QListWidgetItem, QAbstractItemView, QListView, QLabel, QPushButton  
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor, QFont
import matplotlib.pyplot as plt
import pickle
import os

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.completed_tasks = self.load_data()
        self.selected_date = None
        self.task_points = {'8 godzin snu': 4, 'siłownia / ćwiczenia': 2, 'brak słodyczy': 1, 'programowanie oraz projekty': 5, '20 minut czytania oraz nauki': 4, '2 litry wody': 1, 'spędzenie czasu w samotności': 1}
        self.initUI()

    def initUI(self):
        self.setWindowTitle('BeBetter')
        self.setGeometry(0, 0, 1920, 1080)

        vbox = QVBoxLayout()
        self.setLayout(vbox)

        # Create a calendar widget
        self.cal = QCalendarWidget(self)
        self.cal.setGridVisible(True)
        self.cal.clicked.connect(self.showTasks)
        self.showMaximized()
        vbox.addWidget(self.cal)

        # Create a list widget
        self.listWidget = QListWidget(self)
        self.listWidget.itemChanged.connect(self.itemChanged)
        vbox.addWidget(self.listWidget)

        self.pointsLabel = QLabel(self)

        self.pointsLabel.setFont(QFont('Arial', 30))
        vbox.addWidget(self.pointsLabel)

        self.dateLabel = QLabel(self)
        self.dateLabel.setFont(QFont('Arial', 18))
        vbox.addWidget(self.dateLabel)

        self.plotButton = QPushButton('Show Plot', self)
        self.plotButton.clicked.connect(self.showPlot)
        vbox.addWidget(self.plotButton)


    def showTasks(self):
        # Clear the list widget
        self.listWidget.clear()

        # Get the selected date
        self.selected_date = self.cal.selectedDate().toString(Qt.ISODate)  

        # List of tasks
        tasks = ['8 godzin snu' , 'siłownia / ćwiczenia', 'brak słodyczy i pustego cukru', 'programowanie oraz projekty','cybersec', '20 minut czytania oraz nauki', '2 litry wody', 'spędzenie czasu w samotności' ]

        self.pointsLabel.setText(f"punkty: {self.completed_tasks.get('points', 0)}")

        for task in tasks:
            item = QListWidgetItem(task)
            item.setFont(QFont('Arial', 25))
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            item.setCheckState(Qt.Unchecked if task not in self.completed_tasks.get(self.selected_date, []) else Qt.Checked) 
            self.listWidget.addItem(item)


        self.dateLabel.setText(f"data: {self.selected_date}")

    


    def itemChanged(self, item):
        if item.checkState() == Qt.Checked:
            self.completed_tasks.setdefault(self.selected_date, set()).add(item.text())
            self.completed_tasks.setdefault('points', 0)
            self.completed_tasks['points'] += self.task_points.get(item.text(), 0)
        else:
            self.completed_tasks.setdefault(self.selected_date, set()).discard(item.text())
            self.completed_tasks.setdefault('points', 0)
            self.completed_tasks['points'] -= self.task_points.get(item.text(), 0)
            self.pointsLabel.setText(f"punkty: {self.completed_tasks.get('points', 0)}")
        self.save_data()

    def load_data(self):
        if os.path.exists('data.pkl'):
            with open('data.pkl', 'rb') as f:
                return pickle.load(f)
        else:
            return {}

    def save_data(self):
        with open('data.pkl', 'wb') as f:
            pickle.dump(self.completed_tasks, f)
    def showPlot(self):
        import matplotlib.pyplot as plt

        # Prepare data for plotting
        dates = list(self.completed_tasks.keys())
        dates.remove('points')  # We don't want to include 'points' in the dates
        points = [len(self.completed_tasks[date]) for date in dates]

        # Create bar chart
        plt.figure(figsize=(10, 5))
        plt.bar(dates, points)
        plt.xlabel('Data')
        plt.ylabel('Liczba punktów')
        plt.title('Zdobyte punkty')
        plt.show()

        
app = QApplication(sys.argv)
app.setStyle("Fusion")

#Palette to switch to dark colors:
palette = QPalette()
palette.setColor(QPalette.Window, QColor(53, 53, 53))
palette.setColor(QPalette.WindowText, Qt.white)
palette.setColor(QPalette.Base, QColor(25, 25, 25))
palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
palette.setColor(QPalette.ToolTipBase, Qt.black)
palette.setColor(QPalette.ToolTipText, Qt.white)
palette.setColor(QPalette.Text, Qt.white)
palette.setColor(QPalette.Button, QColor(53, 53, 53))
palette.setColor(QPalette.ButtonText, Qt.white)
palette.setColor(QPalette.BrightText, Qt.red)
palette.setColor(QPalette.Link, QColor(42, 130, 218))
palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
palette.setColor(QPalette.HighlightedText, Qt.black)
app.setPalette(palette)
    

ex = MyApp()
ex.show()
app.exec_()
