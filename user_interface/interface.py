import os, sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox, QWidget
from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QGridLayout, QFormLayout, QFrame
from PyQt6.QtWidgets import QLabel, QLineEdit, QTextEdit, QPushButton, QCheckBox, QComboBox, QTabWidget
from PyQt6.QtGui import QColor, QPalette, QFont
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
                                                        border-radius: 10px;
                                                        font-size: 30px;
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
            
        innerNavBarLayout.addWidget(self.papersButton)
        innerNavBarLayout.addWidget(self.teamButton)
        innerNavBarLayout.addWidget(self.latestNewsButton)


        navBar = QWidget()
        navBar.setLayout(innerNavBarLayout)
        navBar.setStyleSheet("background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #B721FF, stop: 1 #21D4FD); padding: 10px; border-radius: 5px;")


        # Tab Widget Area
        self.tabs = QTabWidget()

        labelStyle = "font-size: 20px; color: white;"
        textBoxStyle = "font-size: 18px; padding: 5px; border-radius: 10px; background-color: #d9d9d9; color: black;"

        # Create Tab for 'Add Paper'
        tabAddPaper = QWidget()
        layoutAddPaper = QVBoxLayout()
        
        # Row 1
        layoutRow1 = QHBoxLayout()
        dateLabel = QLabel("Date")
        dateLabel.setStyleSheet(labelStyle)
        dateTextBox = QLineEdit()
        dateTextBox.setStyleSheet(textBoxStyle)
        
        linkLabel = QLabel("Link")
        linkLabel.setStyleSheet(labelStyle)
        linkTextBox = QLineEdit()
        linkTextBox.setStyleSheet(textBoxStyle)
        
        layoutRow1.addWidget(dateLabel)
        layoutRow1.addWidget(dateTextBox)
        layoutRow1.addWidget(linkLabel)
        layoutRow1.addWidget(linkTextBox)

        # Row 2
        layoutRow2 = QHBoxLayout()
        titleLabel = QLabel("Title")
        titleLabel.setStyleSheet(labelStyle)
        titleTextBox = QLineEdit()
        titleTextBox.setStyleSheet(textBoxStyle)
        
        layoutRow2.addWidget(titleLabel)
        layoutRow2.addWidget(titleTextBox)

        # Row 3
        layoutRow3 = QHBoxLayout()
        authorLabel = QLabel("Author")
        authorLabel.setStyleSheet(labelStyle)
        authorTextBox = QLineEdit()
        authorTextBox.setStyleSheet(textBoxStyle)
        
        layoutRow3.addWidget(authorLabel)
        layoutRow3.addWidget(authorTextBox)

        # Row 4
        layoutRow4 = QHBoxLayout()
        conferenceLabel = QLabel("Conference")
        conferenceLabel.setStyleSheet(labelStyle)
        conferenceTextBox = QLineEdit()
        conferenceTextBox.setStyleSheet(textBoxStyle)

        layoutRow4.addWidget(conferenceLabel)
        layoutRow4.addWidget(conferenceTextBox)

        # Row 5
        layoutRow5 = QVBoxLayout()
        bibtexLayout = QHBoxLayout()
        bibtexLabel = QLabel("BibTex")
        bibtexLabel.setStyleSheet(labelStyle)
        extractButton = QPushButton("Extract")
        extractButton.setStyleSheet("font-size: 20px; padding: 10px; border-radius: 15px; background-color: #4972FD; color: white;")
        bibtexLayout.addWidget(bibtexLabel)
        bibtexLayout.addWidget(extractButton)
        bibtexTextBox = QTextEdit()
        bibtexTextBox.setStyleSheet("font-size: 18px; padding: 5px; border-radius: 10px; background-color: #d9d9d9; color: black;")
        bibtexTextBox.setPlaceholderText("Enter BibTex here")
        bibtexTextBox.setFixedHeight(200)
        bibtexTextBox.setStyleSheet(textBoxStyle)
        
        layoutRow5.addLayout(bibtexLayout)
        layoutRow5.addWidget(bibtexTextBox)

        # Row 6
        layoutRow6 = QHBoxLayout()
        submitButton = QPushButton("Submit Paper")
        submitButton.setFixedWidth(300)
        submitButton.setStyleSheet("font-size: 20px; padding: 10px; border-radius: 15px; background-color: #4972FD; color: white;")
        submitButton.clicked.connect(self.submitPaperClicked)
        layoutRow6.addWidget(submitButton)

        layoutAddPaper.addLayout(layoutRow1)
        layoutAddPaper.addLayout(layoutRow2)
        layoutAddPaper.addLayout(layoutRow3)
        layoutAddPaper.addLayout(layoutRow4)
        layoutAddPaper.addLayout(layoutRow5)
        layoutAddPaper.addLayout(layoutRow6)
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
                                                font-size: 30px;
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

app = QApplication(sys.argv)
font = QFont("Montserrat")
app.setFont(font)
window = MainWindow()
window.show()
sys.exit(app.exec())