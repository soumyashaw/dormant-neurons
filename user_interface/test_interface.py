import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QLineEdit, QTextEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QGridLayout, QTabWidget, QDateEdit
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
        
        # Tab Widget
        self.tabs = QTabWidget()
        
        labelStyle = "font-size: 20px; color: white;"
        textBoxStyle = "font-size: 18px; padding: 5px; border-radius: 10px; background-color: #d9d9d9; color: black;"
        
        # Tab: Add Paper
        tabAddPaper = QWidget()
        layoutAddPaper = QVBoxLayout()
        
        formLayout = QGridLayout()
        
        dateLabel = QLabel("Date")
        dateLabel.setStyleSheet(labelStyle)
        
        dateEdit = QDateEdit()
        dateEdit.setCalendarPopup(True)
        dateEdit.setStyleSheet(textBoxStyle)
        dateEdit.setDate(QDate.currentDate())
        
        calendarIcon = QLabel("\U0001F4C5")  # Calendar icon
        calendarIcon.setStyleSheet("font-size: 20px;")
        
        linkLabel = QLabel("Link")
        linkLabel.setStyleSheet(labelStyle)
        linkTextBox = QLineEdit()
        linkTextBox.setStyleSheet(textBoxStyle)
        
        titleLabel = QLabel("Name")
        titleLabel.setStyleSheet(labelStyle)
        titleTextBox = QLineEdit()
        titleTextBox.setStyleSheet(textBoxStyle)
        
        authorLabel = QLabel("Author")
        authorLabel.setStyleSheet(labelStyle)
        authorTextBox = QLineEdit()
        authorTextBox.setStyleSheet(textBoxStyle)
        
        conferenceLabel = QLabel("Conference")
        conferenceLabel.setStyleSheet(labelStyle)
        conferenceTextBox = QLineEdit()
        conferenceTextBox.setStyleSheet(textBoxStyle)
        
        bibtexLabel = QLabel("BibTex")
        bibtexLabel.setStyleSheet(labelStyle)
        
        extractButton = QPushButton("Extract")
        extractButton.setFixedWidth(140)
        extractButton.clicked.connect(self.extractClicked)
        extractButton.setStyleSheet("font-size: 20px; padding: 10px; border-radius: 15px; background-color: #4972FD; color: white;")
        
        bibtexTextBox = QTextEdit()
        bibtexTextBox.setStyleSheet(textBoxStyle)
        bibtexTextBox.setPlaceholderText("Enter BibTex here")
        bibtexTextBox.setFixedHeight(250)
        
        # Adding widgets to Grid Layout
        formLayout.addWidget(dateLabel, 0, 0)
        formLayout.addWidget(dateEdit, 0, 1)
        formLayout.addWidget(calendarIcon, 0, 2)
        formLayout.addWidget(linkLabel, 0, 3)
        formLayout.addWidget(linkTextBox, 0, 4)
        
        formLayout.addWidget(titleLabel, 1, 0)
        formLayout.addWidget(titleTextBox, 1, 1, 1, 4)
        
        formLayout.addWidget(authorLabel, 2, 0)
        formLayout.addWidget(authorTextBox, 2, 1, 1, 4)
        
        formLayout.addWidget(conferenceLabel, 3, 0)
        formLayout.addWidget(conferenceTextBox, 3, 1, 1, 4)
        
        formLayout.addWidget(bibtexLabel, 4, 0)
        formLayout.addWidget(extractButton, 4, 4)
        formLayout.addWidget(bibtexTextBox, 5, 0, 1, 5)
        
        submitButton = QPushButton("Submit Paper")
        submitButton.setFixedWidth(300)
        submitButton.clicked.connect(self.submitPaperClicked)
        submitButton.setStyleSheet("font-size: 20px; padding: 10px; border-radius: 15px; background-color: #4972FD; color: white;")
        
        layoutAddPaper.addLayout(formLayout)
        layoutAddPaper.addWidget(submitButton, alignment=Qt.AlignmentFlag.AlignCenter)
        tabAddPaper.setLayout(layoutAddPaper)

        # Create Tab for 'Modify Paper'
        tabModifyPaper = QWidget()
        layoutModifyPaper = QVBoxLayout()
        layoutModifyPaper.addWidget(QLabel("This is the ModifyPaper tab"))
        tabModifyPaper.setLayout(layoutModifyPaper)

        # Create Tab for 'Delete Paper'
        tabDeletePaper = QWidget()
        layoutDeletePaper = QVBoxLayout()
        layoutDeletePaper.addWidget(QLabel("This is the Latest News tab"))
        tabDeletePaper.setLayout(layoutDeletePaper)
        
        # Add Tabs to the TabWidget
        self.tabs.addTab(tabAddPaper, "ADD PAPER")
        self.tabs.addTab(tabModifyPaper, "MODIFY PAPER")
        self.tabs.addTab(tabDeletePaper, "DELETE PAPER")

        self.tabs.setStyleSheet("""
                                    QTabBar::tab {
                                        width: 200px;
                                        height: 50px;
                                        font-size: 20px;
                                        padding: 10px;
                                        margin: 15px;
                                        border-radius: 10px;
                                    }
                                    QTabBar::tab:selected {
                                        background-color: rgba(255, 255, 255, 100);
                                        font-weight: bold;
                                    }
                                    QTabBar::tab:!selected {
                                        font-weight: normal;
                                    }
                                """)

        
        mainContext = QWidget()
        mainContextLayout = QVBoxLayout()
        mainContextLayout.addWidget(self.tabs)
        mainContext.setLayout(mainContextLayout)
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
                                                border-radius: 10px;
                                                font-weight: bold;
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

    def submitPaperClicked(self):
        print("Submit Paper Clicked")

    def extractClicked(self):
        print("Extract Clicked")

app = QApplication(sys.argv)
app.setFont(QFont("Montserrat"))
window = MainWindow()
window.show()
sys.exit(app.exec())
