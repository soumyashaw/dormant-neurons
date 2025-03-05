import os, sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox, QWidget
from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QGridLayout, QFormLayout, QFrame
from PyQt6.QtWidgets import QLabel, QLineEdit, QPushButton, QCheckBox, QComboBox
from PyQt6.QtGui import QColor, QPalette
from PyQt6.QtGui import QIcon

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Dormant Neurons")
        self.showFullScreen()

        horizontalLayout = QHBoxLayout()

        # Navbar Area
        innerNavBarLayout = QVBoxLayout()

        self.buttonStyleDescriptionTransparent = """QPushButton {
                                                        font-size: 25px;
                                                        background-color: rgba(255, 255, 255, 0);
                                                        padding: 20px;
                                                        border-radius: 15px;
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
            
        innerNavBarLayout.addWidget(self.papersButton)
        innerNavBarLayout.addWidget(self.teamButton)
        innerNavBarLayout.addWidget(self.latestNewsButton)


        navBar = QWidget()
        navBar.setLayout(innerNavBarLayout)
        navBar.setStyleSheet("background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #B721FF, stop: 1 #21D4FD); padding: 10px; border-radius: 5px;")

        mainContext = QWidget()
        mainContext.setStyleSheet("background-color: #00022D; padding: 10px; border-radius: 5px;")

        horizontalLayout.addWidget(navBar, 5)
        horizontalLayout.addWidget(mainContext, 15)

        widget = QWidget()
        widget.setLayout(horizontalLayout)
        self.setCentralWidget(widget)

    def papersButtonClicked(self, status):
        self.buttonStyleDescriptionClicked = """QPushButton {
                                                font-size: 25px;
                                                background-color: rgba(255, 255, 255, 100);
                                                padding: 20px;
                                                border-radius: 15px;
                                            }
                                        """
        self.papersButton.setStyleSheet(self.buttonStyleDescriptionClicked)
        self.teamButton.setStyleSheet(self.buttonStyleDescriptionTransparent)
        self.latestNewsButton.setStyleSheet(self.buttonStyleDescriptionTransparent)

    def teamButtonClicked(self, status):
        self.teamButton.setStyleSheet(self.buttonStyleDescriptionClicked)
        self.papersButton.setStyleSheet(self.buttonStyleDescriptionTransparent)
        self.latestNewsButton.setStyleSheet(self.buttonStyleDescriptionTransparent)

    def latestNewsButtonClicked(self, status):
        self.latestNewsButton.setStyleSheet(self.buttonStyleDescriptionClicked)
        self.teamButton.setStyleSheet(self.buttonStyleDescriptionTransparent)
        self.papersButton.setStyleSheet(self.buttonStyleDescriptionTransparent)

app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())