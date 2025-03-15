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
        
####### Main Context: Paper Area ###################################################
        # Tab Widget
        self.tabsPaper = QTabWidget()
        
        labelStyle = "font-size: 20px; color: white; padding-left: 0px;"
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

        submitButton = QPushButton("Submit Paper")
        submitButton.setFixedWidth(300)
        submitButton.clicked.connect(self.submitPaperClicked)
        submitButton.setStyleSheet("font-size: 20px; padding: 10px; border-radius: 15px; background-color: #4972FD; color: white;")
        
        # Adding widgets to Grid Layout
        formLayout.addWidget(dateLabel, 0, 0, 1, 2)
        formLayout.addWidget(dateEdit, 0, 1, 1, 1)
        formLayout.addWidget(linkLabel, 0, 3, alignment=Qt.AlignmentFlag.AlignRight)
        formLayout.addWidget(linkTextBox, 0, 4, 1, 2)
        
        formLayout.addWidget(titleLabel, 1, 0)
        formLayout.addWidget(titleTextBox, 1, 1, 1, 5)
        
        formLayout.addWidget(authorLabel, 2, 0)
        formLayout.addWidget(authorTextBox, 2, 1, 1, 5)
        
        formLayout.addWidget(conferenceLabel, 3, 0)
        formLayout.addWidget(conferenceTextBox, 3, 1, 1, 5)
        
        formLayout.addWidget(bibtexLabel, 4, 0)
        formLayout.addWidget(extractButton, 4, 5, alignment=Qt.AlignmentFlag.AlignRight)
        formLayout.addWidget(bibtexTextBox, 5, 0, 1, 6)

        formLayout.addWidget(submitButton, 6, 0, 1, 6, alignment=Qt.AlignmentFlag.AlignCenter)
        
        layoutAddPaper.addLayout(formLayout)
        layoutAddPaper.setContentsMargins(50, 50, 50, 50)
        tabAddPaper.setLayout(layoutAddPaper)

        # Tab: Modify Paper
        tabModifyPaper = QWidget()
        layoutModifyPaper = QVBoxLayout()
        
        formLayout2 = QGridLayout()

        scroll2 = QScrollArea()
        scroll2.setWidgetResizable(True)
        scroll2.setStyleSheet("background-color: #d9d9d9; margin-bottom: 30px;")
        
        dateLabel2 = QLabel("Date")
        dateLabel2.setStyleSheet(labelStyle)
        
        dateEdit2 = QDateEdit()
        dateEdit2.setCalendarPopup(True)
        dateEdit2.setStyleSheet(textBoxStyle)
        dateEdit2.setDate(QDate.currentDate())
        
        linkLabel2 = QLabel("Link")
        linkLabel2.setStyleSheet(labelStyle)
        linkTextBox2 = QLineEdit()
        linkTextBox2.setStyleSheet(textBoxStyle)
        
        titleLabel2 = QLabel("Name")
        titleLabel2.setStyleSheet(labelStyle)
        titleTextBox2 = QLineEdit()
        titleTextBox2.setStyleSheet(textBoxStyle)
        
        authorLabel2 = QLabel("Author")
        authorLabel2.setStyleSheet(labelStyle)
        authorTextBox2 = QLineEdit()
        authorTextBox2.setStyleSheet(textBoxStyle)
        
        conferenceLabel2 = QLabel("Conference")
        conferenceLabel2.setStyleSheet(labelStyle)
        conferenceTextBox2 = QLineEdit()
        conferenceTextBox2.setStyleSheet(textBoxStyle)
        
        bibtexLabel2 = QLabel("BibTex")
        bibtexLabel2.setStyleSheet(labelStyle)
        
        extractButton2 = QPushButton("Extract")
        extractButton2.setFixedWidth(140)
        extractButton2.clicked.connect(self.extractClicked)
        extractButton2.setStyleSheet("font-size: 20px; padding: 10px; border-radius: 15px; background-color: #4972FD; color: white;")
        
        bibtexTextBox2 = QTextEdit()
        bibtexTextBox2.setStyleSheet(textBoxStyle)
        bibtexTextBox2.setPlaceholderText("Enter BibTex here")

        idLabel2 = QLabel("Paper ID")
        idLabel2.setStyleSheet(labelStyle)
        idTextBox2 = QLineEdit()
        idTextBox2.setStyleSheet(textBoxStyle)

        submitButton2 = QPushButton("Submit Paper")
        submitButton2.setFixedWidth(300)
        submitButton2.clicked.connect(self.submitPaperClicked)
        submitButton2.setStyleSheet("font-size: 20px; padding: 10px; border-radius: 15px; background-color: #4972FD; color: white;")
        
        # Adding widgets to Grid Layout
        formLayout2.addWidget(scroll2, 0, 0, 1, 6)

        formLayout2.addWidget(dateLabel2, 1, 0, 1, 2)
        formLayout2.addWidget(dateEdit2, 1, 1, 1, 1)
        formLayout2.addWidget(linkLabel2, 1, 3, alignment=Qt.AlignmentFlag.AlignRight)
        formLayout2.addWidget(linkTextBox2, 1, 4, 1, 2)
        
        formLayout2.addWidget(titleLabel2, 2, 0)
        formLayout2.addWidget(titleTextBox2, 2, 1, 1, 5)
        
        formLayout2.addWidget(authorLabel2, 3, 0)
        formLayout2.addWidget(authorTextBox2, 3, 1, 1, 5)
        
        formLayout2.addWidget(conferenceLabel2, 4, 0)
        formLayout2.addWidget(conferenceTextBox2, 4, 1, 1, 5)
        
        formLayout2.addWidget(bibtexLabel2, 5, 0)
        formLayout2.addWidget(extractButton2, 5, 5, alignment=Qt.AlignmentFlag.AlignRight)
        formLayout2.addWidget(bibtexTextBox2, 6, 0, 1, 6)

        formLayout2.addWidget(idLabel2, 7, 0)
        formLayout2.addWidget(idTextBox2, 7, 1, 1, 2)
        formLayout2.addWidget(submitButton2, 7, 0, 4, 6, alignment=Qt.AlignmentFlag.AlignRight)
        layoutModifyPaper.addLayout(formLayout2)
        layoutModifyPaper.setContentsMargins(50, 50, 50, 50)
        tabModifyPaper.setLayout(layoutModifyPaper)

        # Tab: Delete Paper
        tabDeletePaper = QWidget()
        layoutDeletePaper = QVBoxLayout()
        
        formLayout3 = QGridLayout()

        scroll3 = QScrollArea()
        scroll3.setWidgetResizable(True)
        scroll3.setStyleSheet("background-color: #d9d9d9; margin-bottom: 30px;")

        idLabel3 = QLabel("Paper ID")
        idLabel3.setStyleSheet(labelStyle+"padding-right: 50px;")
        idTextBox3 = QLineEdit()
        idTextBox3.setStyleSheet(textBoxStyle)
        idTextBox3.setMaximumWidth(145)

        deleteButton3 = QPushButton("Delete Paper")
        deleteButton3.setFixedWidth(300)
        deleteButton3.clicked.connect(self.deletePaperClicked)
        deleteButton3.setStyleSheet("font-size: 20px; padding: 10px; border-radius: 15px; background-color: #4972FD; color: white;")
        
        # Adding widgets to Grid Layout
        formLayout3.addWidget(scroll3, 0, 0, 4, 6)

        formLayout3.addWidget(idLabel3, 4, 0, 1, 3, alignment=Qt.AlignmentFlag.AlignRight)
        formLayout3.addWidget(idTextBox3, 4, 3, 1, 3, alignment=Qt.AlignmentFlag.AlignLeft)
        formLayout3.addWidget(deleteButton3, 5, 0, 1, 6, alignment=Qt.AlignmentFlag.AlignCenter)
        layoutDeletePaper.addLayout(formLayout3)
        layoutDeletePaper.setContentsMargins(50, 50, 50, 50)
        tabDeletePaper.setLayout(layoutDeletePaper)

        
        # Add Tabs to the TabWidget
        self.tabsPaper.addTab(tabAddPaper, "ADD PAPER")
        self.tabsPaper.addTab(tabModifyPaper, "MODIFY PAPER")
        self.tabsPaper.addTab(tabDeletePaper, "DELETE PAPER")

        self.tabsPaper.setStyleSheet("""
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
        
        self.mainContextPaper = QWidget()
        paperLayout = QVBoxLayout(self.mainContextPaper)
        paperLayout.addWidget(self.tabsPaper)
        self.mainContextPaper.setLayout(paperLayout)
        
############################### Main Context: Team Area ###################################################
        # Tab Widget
        self.tabsTeam = QTabWidget()
        
        # Tab: Add Member
        tabAddMember = QWidget()
        layoutAddMember = QVBoxLayout()
        
        formLayout4 = QGridLayout()
        
        dateLabel4 = QLabel("Date")
        dateLabel4.setStyleSheet(labelStyle)
        
        dateEdit4 = QDateEdit()
        dateEdit4.setCalendarPopup(True)
        dateEdit4.setStyleSheet(textBoxStyle)
        dateEdit4.setDate(QDate.currentDate())
        
        linkLabel4 = QLabel("Link")
        linkLabel4.setStyleSheet(labelStyle)
        linkTextBox4 = QLineEdit()
        linkTextBox4.setStyleSheet(textBoxStyle)
        
        titleLabel4 = QLabel("Name")
        titleLabel4.setStyleSheet(labelStyle)
        titleTextBox4 = QLineEdit()
        titleTextBox4.setStyleSheet(textBoxStyle)
        
        authorLabel4 = QLabel("Author")
        authorLabel4.setStyleSheet(labelStyle)
        authorTextBox4 = QLineEdit()
        authorTextBox4.setStyleSheet(textBoxStyle)
        
        conferenceLabel4 = QLabel("Conference")
        conferenceLabel4.setStyleSheet(labelStyle)
        conferenceTextBox4 = QLineEdit()
        conferenceTextBox4.setStyleSheet(textBoxStyle)
        
        bibtexLabel4 = QLabel("BibTex")
        bibtexLabel4.setStyleSheet(labelStyle)
        
        extractButton4 = QPushButton("Extract")
        extractButton4.setFixedWidth(140)
        extractButton4.clicked.connect(self.extractClicked)
        extractButton4.setStyleSheet("font-size: 20px; padding: 10px; border-radius: 15px; background-color: #4972FD; color: white;")
        
        bibtexTextBox4 = QTextEdit()
        bibtexTextBox4.setStyleSheet(textBoxStyle)
        bibtexTextBox4.setPlaceholderText("Enter BibTex here")

        submitButton4 = QPushButton("Submit Paper")
        submitButton4.setFixedWidth(300)
        submitButton4.clicked.connect(self.submitPaperClicked)
        submitButton4.setStyleSheet("font-size: 20px; padding: 10px; border-radius: 15px; background-color: #4972FD; color: white;")
        
        # Adding widgets to Grid Layout
        formLayout4.addWidget(dateLabel4, 0, 0, 1, 2)
        formLayout4.addWidget(dateEdit4, 0, 1, 1, 1)
        formLayout4.addWidget(linkLabel4, 0, 3, alignment=Qt.AlignmentFlag.AlignRight)
        formLayout4.addWidget(linkTextBox4, 0, 4, 1, 2)
        
        formLayout4.addWidget(titleLabel4, 1, 0)
        formLayout4.addWidget(titleTextBox4, 1, 1, 1, 5)
        
        formLayout4.addWidget(authorLabel4, 2, 0)
        formLayout4.addWidget(authorTextBox4, 2, 1, 1, 5)
        
        formLayout4.addWidget(conferenceLabel4, 3, 0)
        formLayout4.addWidget(conferenceTextBox4, 3, 1, 1, 5)
        
        formLayout4.addWidget(bibtexLabel4, 4, 0)
        formLayout4.addWidget(extractButton4, 4, 5, alignment=Qt.AlignmentFlag.AlignRight)
        formLayout4.addWidget(bibtexTextBox4, 5, 0, 1, 6)

        formLayout4.addWidget(submitButton4, 6, 0, 1, 6, alignment=Qt.AlignmentFlag.AlignCenter)
        
        layoutAddMember.addLayout(formLayout4)
        layoutAddMember.setContentsMargins(50, 50, 50, 50)
        tabAddMember.setLayout(layoutAddMember)

        # Tab: Modify Member
        tabModifyMember = QWidget()
        layoutModifyMember = QVBoxLayout()
        
        formLayout5 = QGridLayout()

        scroll5 = QScrollArea()
        scroll5.setWidgetResizable(True)
        scroll5.setStyleSheet("background-color: #d9d9d9; margin-bottom: 30px;")
        
        dateLabel5 = QLabel("Date")
        dateLabel5.setStyleSheet(labelStyle)
        
        dateEdit5 = QDateEdit()
        dateEdit5.setCalendarPopup(True)
        dateEdit5.setStyleSheet(textBoxStyle)
        dateEdit5.setDate(QDate.currentDate())
        
        linkLabel5 = QLabel("Link")
        linkLabel5.setStyleSheet(labelStyle)
        linkTextBox5 = QLineEdit()
        linkTextBox5.setStyleSheet(textBoxStyle)
        
        titleLabel5 = QLabel("Name")
        titleLabel5.setStyleSheet(labelStyle)
        titleTextBox5 = QLineEdit()
        titleTextBox5.setStyleSheet(textBoxStyle)
        
        authorLabel5 = QLabel("Author")
        authorLabel5.setStyleSheet(labelStyle)
        authorTextBox5 = QLineEdit()
        authorTextBox5.setStyleSheet(textBoxStyle)
        
        conferenceLabel5 = QLabel("Conference")
        conferenceLabel5.setStyleSheet(labelStyle)
        conferenceTextBox5 = QLineEdit()
        conferenceTextBox5.setStyleSheet(textBoxStyle)
        
        bibtexLabel5 = QLabel("BibTex")
        bibtexLabel5.setStyleSheet(labelStyle)
        
        extractButton5 = QPushButton("Extract")
        extractButton5.setFixedWidth(140)
        extractButton5.clicked.connect(self.extractClicked)
        extractButton5.setStyleSheet("font-size: 20px; padding: 10px; border-radius: 15px; background-color: #4972FD; color: white;")
        
        bibtexTextBox5 = QTextEdit()
        bibtexTextBox5.setStyleSheet(textBoxStyle)
        bibtexTextBox5.setPlaceholderText("Enter BibTex here")

        idLabel5 = QLabel("Paper ID")
        idLabel5.setStyleSheet(labelStyle)
        idTextBox5 = QLineEdit()
        idTextBox5.setStyleSheet(textBoxStyle)

        submitButton5 = QPushButton("Submit Paper")
        submitButton5.setFixedWidth(300)
        submitButton5.clicked.connect(self.submitPaperClicked)
        submitButton5.setStyleSheet("font-size: 20px; padding: 10px; border-radius: 15px; background-color: #4972FD; color: white;")
        
        # Adding widgets to Grid Layout
        formLayout5.addWidget(scroll5, 0, 0, 1, 6)

        formLayout5.addWidget(dateLabel5, 1, 0, 1, 2)
        formLayout5.addWidget(dateEdit5, 1, 1, 1, 1)
        formLayout5.addWidget(linkLabel5, 1, 3, alignment=Qt.AlignmentFlag.AlignRight)
        formLayout5.addWidget(linkTextBox5, 1, 4, 1, 2)
        
        formLayout5.addWidget(titleLabel5, 2, 0)
        formLayout5.addWidget(titleTextBox5, 2, 1, 1, 5)
        
        formLayout5.addWidget(authorLabel5, 3, 0)
        formLayout5.addWidget(authorTextBox5, 3, 1, 1, 5)
        
        formLayout5.addWidget(conferenceLabel5, 4, 0)
        formLayout5.addWidget(conferenceTextBox5, 4, 1, 1, 5)
        
        formLayout5.addWidget(bibtexLabel5, 5, 0)
        formLayout5.addWidget(extractButton5, 5, 5, alignment=Qt.AlignmentFlag.AlignRight)
        formLayout5.addWidget(bibtexTextBox5, 6, 0, 1, 6)

        formLayout5.addWidget(idLabel5, 7, 0)
        formLayout5.addWidget(idTextBox5, 7, 1, 1, 2)
        formLayout5.addWidget(submitButton5, 7, 0, 4, 6, alignment=Qt.AlignmentFlag.AlignRight)
        layoutModifyMember.addLayout(formLayout5)
        layoutModifyMember.setContentsMargins(50, 50, 50, 50)
        tabModifyMember.setLayout(layoutModifyMember)

        # Tab: Delete Member
        tabDeleteMember = QWidget()
        layoutDeleteMember = QVBoxLayout()
        
        formLayout6 = QGridLayout()

        scroll6 = QScrollArea()
        scroll6.setWidgetResizable(True)
        scroll6.setStyleSheet("background-color: #d9d9d9; margin-bottom: 30px;")

        idLabel6 = QLabel("Paper ID")
        idLabel6.setStyleSheet(labelStyle+"padding-right: 50px;")
        idTextBox6 = QLineEdit()
        idTextBox6.setStyleSheet(textBoxStyle)
        idTextBox6.setMaximumWidth(145)

        deleteButton6 = QPushButton("Delete Paper")
        deleteButton6.setFixedWidth(300)
        deleteButton6.clicked.connect(self.deletePaperClicked)
        deleteButton6.setStyleSheet("font-size: 20px; padding: 10px; border-radius: 15px; background-color: #4972FD; color: white;")
        
        # Adding widgets to Grid Layout
        formLayout6.addWidget(scroll6, 0, 0, 4, 6)

        formLayout6.addWidget(idLabel6, 4, 0, 1, 3, alignment=Qt.AlignmentFlag.AlignRight)
        formLayout6.addWidget(idTextBox6, 4, 3, 1, 3, alignment=Qt.AlignmentFlag.AlignLeft)
        formLayout6.addWidget(deleteButton6, 5, 0, 1, 6, alignment=Qt.AlignmentFlag.AlignCenter)
        layoutDeleteMember.addLayout(formLayout6)
        layoutDeleteMember.setContentsMargins(50, 50, 50, 50)
        tabDeleteMember.setLayout(layoutDeleteMember)

        # Add Tabs to the TabWidget
        self.tabsTeam.addTab(tabAddMember, "ADD MEMBER")
        self.tabsTeam.addTab(tabModifyMember, "MODIFY MEMBER")
        self.tabsTeam.addTab(tabDeleteMember, "DELETE MEMBER")

        self.tabsTeam.setStyleSheet("""
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
        self.mainContextTeam = QWidget()
        teamLayout = QVBoxLayout(self.mainContextTeam)
        teamLayout.addWidget(self.tabsTeam)
        self.mainContextTeam.setLayout(teamLayout)

        ####### Main Context: Latest News ##########
        self.mainContextNews = QWidget()
        newsLayout = QVBoxLayout(self.mainContextNews)
        newsLayout.addWidget(QLabel("Latest News Content Goes Here"))
        self.mainContextNews.setLayout(newsLayout)
        
        self.mainContextLayout = QVBoxLayout()
        self.mainContext = QWidget()
        self.mainContext.setLayout(self.mainContextLayout)
        self.mainContextLayout.addWidget(self.mainContextPaper)
        self.mainContext.setStyleSheet("background-color: #00022D; padding: 10px; border-radius: 5px;")
        
        horizontalLayout.addWidget(navBar, 5)
        horizontalLayout.addWidget(self.mainContext, 15)
        
        widget = QWidget()
        widget.setLayout(horizontalLayout)
        self.setCentralWidget(widget)

    def changeMainContextWidget(self, newWidget):
        # Remove existing widget
        if self.mainContextLayout.count():
            oldWidget = self.mainContextLayout.takeAt(0).widget()
            if oldWidget:
                oldWidget.setParent(None)  # Remove from UI
        
        # Add new widget
        self.mainContextLayout.addWidget(newWidget)

    def papersButtonClicked(self, status):
        self.papersButton.setStyleSheet(self.buttonStyleDescriptionClicked)
        self.teamButton.setStyleSheet(self.buttonStyleDescriptionTransparent)
        self.latestNewsButton.setStyleSheet(self.buttonStyleDescriptionTransparent)

        self.changeMainContextWidget(self.mainContextPaper)

        ## To Do: Change the layout or widget of the main context on Nav bar button click

    def teamButtonClicked(self, status):
        self.teamButton.setStyleSheet(self.buttonStyleDescriptionClicked)
        self.papersButton.setStyleSheet(self.buttonStyleDescriptionTransparent)
        self.latestNewsButton.setStyleSheet(self.buttonStyleDescriptionTransparent)

        self.changeMainContextWidget(self.mainContextTeam)

        ## To Do: Change the layout or widget of the main context on Nav bar button click

    def latestNewsButtonClicked(self, status):
        self.latestNewsButton.setStyleSheet(self.buttonStyleDescriptionClicked)
        self.teamButton.setStyleSheet(self.buttonStyleDescriptionTransparent)
        self.papersButton.setStyleSheet(self.buttonStyleDescriptionTransparent)

        self.changeMainContextWidget(self.mainContextNews)

        ## To Do: Change the layout or widget of the main context on Nav bar button click

    def submitPaperClicked(self):
        print("Submit Paper Clicked")

    def extractClicked(self):
        print("Extract Clicked")

    def deletePaperClicked(self):
        print("Delete Paper Clicked")

    def addPapersFromDatabase(self, layout):
        print("Adding Papers from Database")
        """for i in range(1, 21):
            layout.addWidget(QLabel("This is the function"))
        return layout"""

app = QApplication(sys.argv)
app.setFont(QFont("Montserrat"))
window = MainWindow()
window.show()
sys.exit(app.exec())