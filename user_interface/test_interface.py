import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QLineEdit, QTextEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QGridLayout, QTabWidget, QDateEdit, QScrollArea
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import QDate, Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dormant Neurons")
        self.showFullScreen()

        horizontalLayout = QHBoxLayout()
        
        # Sidebar Navigation
        navBarLayout = QVBoxLayout()

        self.buttonStyleDescriptionClicked = """QPushButton {
                                                font-size: 25px;
                                                background-color: rgba(255, 255, 255, 100);
                                                padding: 20px;
                                                border-radius: 10px;
                                                font-weight: bold;
                                            }
                                        """
        
        self.buttonStyleDescriptionTransparent = """
            QPushButton {
                font-size: 25px;
                background-color: rgba(255, 255, 255, 0);
                padding: 20px;
                border-radius: 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 100);
            }
        """
        
        self.papersButton = QPushButton("\U0001F4D1 Papers")
        self.papersButton.setStyleSheet(self.buttonStyleDescriptionTransparent)
        self.papersButton.setCheckable(True)
        self.papersButton.clicked.connect(self.papersButtonClicked)
        
        self.teamButton = QPushButton("\U0001F464 Team")
        self.teamButton.setStyleSheet(self.buttonStyleDescriptionTransparent)
        self.teamButton.setCheckable(True)
        self.teamButton.clicked.connect(self.teamButtonClicked)
        
        self.latestNewsButton = QPushButton("\U0001F4E2 Latest News")
        self.latestNewsButton.setStyleSheet(self.buttonStyleDescriptionTransparent)
        self.latestNewsButton.setCheckable(True)
        self.latestNewsButton.clicked.connect(self.latestNewsButtonClicked)
        
        navBarLayout.addWidget(self.papersButton)
        navBarLayout.addWidget(self.teamButton)
        navBarLayout.addWidget(self.latestNewsButton)
        
        navBar = QWidget()
        navBar.setLayout(navBarLayout)
        navBar.setStyleSheet("background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #B721FF, stop: 1 #21D4FD);")

        ####### Main Context: Paper Area ##########
        self.tabsPaper = QTabWidget()
        tabAddPaper = QWidget()
        layoutAddPaper = QVBoxLayout()
        layoutAddPaper.addWidget(QLabel("Add Paper Form Goes Here"))
        tabAddPaper.setLayout(layoutAddPaper)
        self.tabsPaper.addTab(tabAddPaper, "ADD PAPER")
        self.tabsPaper.setStyleSheet("QTabBar::tab { width: 200px; height: 50px; font-size: 20px; }")
        
        self.mainContextPaper = QWidget()
        paperLayout = QVBoxLayout(self.mainContextPaper)
        paperLayout.addWidget(self.tabsPaper)
        self.mainContextPaper.setLayout(paperLayout)

        ####### Main Context: Team Area ##########
        self.tabsTeam = QTabWidget()
        tabAddTeam = QWidget()
        layoutAddTeam = QVBoxLayout()
        layoutAddTeam.addWidget(QLabel("Add Team Member Form Goes Here"))
        tabAddTeam.setLayout(layoutAddTeam)
        self.tabsTeam.addTab(tabAddTeam, "ADD MEMBER")
        self.tabsTeam.setStyleSheet("QTabBar::tab { width: 200px; height: 50px; font-size: 20px; }")
        
        self.mainContextTeam = QWidget()
        teamLayout = QVBoxLayout(self.mainContextTeam)
        teamLayout.addWidget(self.tabsTeam)
        self.mainContextTeam.setLayout(teamLayout)

        ####### Main Context: Latest News ##########
        self.mainContextNews = QWidget()
        newsLayout = QVBoxLayout(self.mainContextNews)
        newsLayout.addWidget(QLabel("Latest News Content Goes Here"))
        self.mainContextNews.setLayout(newsLayout)

        ####### Main Context Setup ##########
        self.mainContext = QWidget()
        self.mainContextLayout = QVBoxLayout()
        self.mainContext.setLayout(self.mainContextLayout)
        self.mainContextLayout.addWidget(self.mainContextPaper)  # Default context

        horizontalLayout.addWidget(navBar, 5)
        horizontalLayout.addWidget(self.mainContext, 15)
        
        widget = QWidget()
        widget.setLayout(horizontalLayout)
        self.setCentralWidget(widget)

    def changeMainContextWidget(self, newWidget):
        """Removes the current main context widget and sets a new one."""
        # Remove existing widget
        if self.mainContextLayout.count():
            oldWidget = self.mainContextLayout.takeAt(0).widget()
            if oldWidget:
                oldWidget.setParent(None)  # Remove from UI
        
        # Add new widget
        self.mainContextLayout.addWidget(newWidget)

    def papersButtonClicked(self, status):
        """Handles clicking on the Papers button."""
        self.papersButton.setStyleSheet(self.buttonStyleDescriptionClicked)
        self.teamButton.setStyleSheet(self.buttonStyleDescriptionTransparent)
        self.latestNewsButton.setStyleSheet(self.buttonStyleDescriptionTransparent)
        self.changeMainContextWidget(self.mainContextPaper)

    def teamButtonClicked(self, status):
        """Handles clicking on the Team button."""
        self.teamButton.setStyleSheet(self.buttonStyleDescriptionClicked)
        self.papersButton.setStyleSheet(self.buttonStyleDescriptionTransparent)
        self.latestNewsButton.setStyleSheet(self.buttonStyleDescriptionTransparent)
        self.changeMainContextWidget(self.mainContextTeam)

    def latestNewsButtonClicked(self, status):
        """Handles clicking on the Latest News button."""
        self.latestNewsButton.setStyleSheet(self.buttonStyleDescriptionClicked)
        self.teamButton.setStyleSheet(self.buttonStyleDescriptionTransparent)
        self.papersButton.setStyleSheet(self.buttonStyleDescriptionTransparent)
        self.changeMainContextWidget(self.mainContextNews)

    def submitPaperClicked(self):
        print("Submit Paper Clicked")

    def extractClicked(self):
        print("Extract Clicked")

    def deletePaperClicked(self):
        print("Delete Paper Clicked")

app = QApplication(sys.argv)
app.setFont(QFont("Montserrat"))
window = MainWindow()
window.show()
sys.exit(app.exec())