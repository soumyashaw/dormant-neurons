import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QTabWidget, QLabel

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PyQt6 Tabs Example")
        self.setGeometry(100, 100, 600, 400)

        # Create the Tab Widget
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)  # Set as main widget

        # Create Tab 1
        tab1 = QWidget()
        layout1 = QVBoxLayout()
        layout1.addWidget(QLabel("This is the Papers tab"))
        tab1.setLayout(layout1)

        # Create Tab 2
        tab2 = QWidget()
        layout2 = QVBoxLayout()
        layout2.addWidget(QLabel("This is the Team tab"))
        tab2.setLayout(layout2)

        # Create Tab 3
        tab3 = QWidget()
        layout3 = QVBoxLayout()
        layout3.addWidget(QLabel("This is the Latest News tab"))
        tab3.setLayout(layout3)

        # Add Tabs to the TabWidget
        self.tabs.addTab(tab1, "📄 Papers")  # Unicode emoji for Papers
        self.tabs.addTab(tab2, "👥 Team")  # Unicode emoji for Team
        self.tabs.addTab(tab3, "📰 Latest News")  # Unicode emoji for News

app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())