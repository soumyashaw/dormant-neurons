import os
import re
import sys
import json
from datetime import datetime
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QLineEdit, QTextEdit, QPushButton, QFileDialog,
    QVBoxLayout, QHBoxLayout, QGridLayout, QTabWidget, QDateEdit, QScrollArea, QComboBox, QMessageBox
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import QDate, Qt
from pyqt6_multiselect_combobox import MultiSelectComboBox

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
        
        self.dateEdit = QDateEdit()
        self.dateEdit.setCalendarPopup(True)
        self.dateEdit.setStyleSheet(textBoxStyle)
        self.dateEdit.setDate(QDate.currentDate())
        
        linkLabel = QLabel("Link")
        linkLabel.setStyleSheet(labelStyle)
        self.linkTextBox = QLineEdit()
        self.linkTextBox.setStyleSheet(textBoxStyle)
        
        titleLabel = QLabel("Title")
        titleLabel.setStyleSheet(labelStyle)
        self.titleTextBox = QLineEdit()
        self.titleTextBox.setStyleSheet(textBoxStyle)
        
        authorLabel = QLabel("Author")
        authorLabel.setStyleSheet(labelStyle)
        self.authorTextBox = QLineEdit()
        self.authorTextBox.setStyleSheet(textBoxStyle)
        
        conferenceLabel = QLabel("Conference")
        conferenceLabel.setStyleSheet(labelStyle)
        self.conferenceTextBox = QLineEdit()
        self.conferenceTextBox.setStyleSheet(textBoxStyle)
        
        bibtexLabel = QLabel("BibTex")
        bibtexLabel.setStyleSheet(labelStyle)
        
        extractButton = QPushButton("Extract")
        extractButton.setFixedWidth(140)
        extractButton.clicked.connect(lambda: self.extractClicked(1))
        extractButton.setStyleSheet("font-size: 20px; padding: 10px; border-radius: 15px; background-color: #4972FD; color: white;")
        
        self.bibtexTextBox = QTextEdit()
        self.bibtexTextBox.setAcceptRichText(False)
        self.bibtexTextBox.setStyleSheet(textBoxStyle)
        self.bibtexTextBox.setPlaceholderText("Enter BibTex here")

        submitButton = QPushButton("Submit Paper")
        submitButton.setFixedWidth(300)
        submitButton.clicked.connect(self.submitPaperClicked)
        submitButton.setStyleSheet("font-size: 20px; padding: 10px; border-radius: 15px; background-color: #4972FD; color: white;")
        
        # Adding widgets to Grid Layout
        formLayout.addWidget(dateLabel, 0, 0, 1, 2)
        formLayout.addWidget(self.dateEdit, 0, 1, 1, 2)
        formLayout.addWidget(linkLabel, 0, 3, alignment=Qt.AlignmentFlag.AlignRight)
        formLayout.addWidget(self.linkTextBox, 0, 4, 1, 2)
        
        formLayout.addWidget(titleLabel, 1, 0)
        formLayout.addWidget(self.titleTextBox, 1, 1, 1, 5)
        
        formLayout.addWidget(authorLabel, 2, 0)
        formLayout.addWidget(self.authorTextBox, 2, 1, 1, 5)
        
        formLayout.addWidget(conferenceLabel, 3, 0)
        formLayout.addWidget(self.conferenceTextBox, 3, 1, 1, 5)
        
        formLayout.addWidget(bibtexLabel, 4, 0)
        formLayout.addWidget(extractButton, 4, 5, alignment=Qt.AlignmentFlag.AlignRight)
        formLayout.addWidget(self.bibtexTextBox, 5, 0, 1, 6)

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
        
        self.dateEdit2 = QDateEdit()
        self.dateEdit2.setCalendarPopup(True)
        self.dateEdit2.setStyleSheet(textBoxStyle)
        self.dateEdit2.setDate(QDate.currentDate())
        
        linkLabel2 = QLabel("Link")
        linkLabel2.setStyleSheet(labelStyle)
        self.linkTextBox2 = QLineEdit()
        self.linkTextBox2.setStyleSheet(textBoxStyle)
        
        titleLabel2 = QLabel("Title")
        titleLabel2.setStyleSheet(labelStyle)
        self.titleTextBox2 = QLineEdit()
        self.titleTextBox2.setStyleSheet(textBoxStyle)
        
        authorLabel2 = QLabel("Author")
        authorLabel2.setStyleSheet(labelStyle)
        self.authorTextBox2 = QLineEdit()
        self.authorTextBox2.setStyleSheet(textBoxStyle)
        
        conferenceLabel2 = QLabel("Conference")
        conferenceLabel2.setStyleSheet(labelStyle)
        self.conferenceTextBox2 = QLineEdit()
        self.conferenceTextBox2.setStyleSheet(textBoxStyle)
        
        bibtexLabel2 = QLabel("BibTex")
        bibtexLabel2.setStyleSheet(labelStyle)
        
        extractButton2 = QPushButton("Extract")
        extractButton2.setFixedWidth(140)
        extractButton2.clicked.connect(lambda: self.extractClicked(2))
        extractButton2.setStyleSheet("font-size: 20px; padding: 10px; border-radius: 15px; background-color: #4972FD; color: white;")
        
        self.bibtexTextBox2 = QTextEdit()
        self.bibtexTextBox2.setAcceptRichText(False)
        self.bibtexTextBox2.setStyleSheet(textBoxStyle)
        self.bibtexTextBox2.setPlaceholderText("Enter BibTex here")

        idLabel2 = QLabel("Paper ID")
        idLabel2.setStyleSheet(labelStyle)
        self.idTextBox2 = QLineEdit()
        self.idTextBox2.setStyleSheet(textBoxStyle)

        submitButton2 = QPushButton("Modify Paper")
        submitButton2.setFixedWidth(300)
        submitButton2.clicked.connect(self.modifyPaperClicked)
        submitButton2.setStyleSheet("font-size: 20px; padding: 10px; border-radius: 15px; background-color: #4972FD; color: white;")
        
        # Adding widgets to Grid Layout
        formLayout2.addWidget(scroll2, 0, 0, 1, 6)

        formLayout2.addWidget(dateLabel2, 1, 0, 1, 2)
        formLayout2.addWidget(self.dateEdit2, 1, 1, 1, 1)
        formLayout2.addWidget(linkLabel2, 1, 3, alignment=Qt.AlignmentFlag.AlignRight)
        formLayout2.addWidget(self.linkTextBox2, 1, 4, 1, 2)
        
        formLayout2.addWidget(titleLabel2, 2, 0)
        formLayout2.addWidget(self.titleTextBox2, 2, 1, 1, 5)
        
        formLayout2.addWidget(authorLabel2, 3, 0)
        formLayout2.addWidget(self.authorTextBox2, 3, 1, 1, 5)
        
        formLayout2.addWidget(conferenceLabel2, 4, 0)
        formLayout2.addWidget(self.conferenceTextBox2, 4, 1, 1, 5)
        
        formLayout2.addWidget(bibtexLabel2, 5, 0)
        formLayout2.addWidget(extractButton2, 5, 5, alignment=Qt.AlignmentFlag.AlignRight)
        formLayout2.addWidget(self.bibtexTextBox2, 6, 0, 1, 6)

        formLayout2.addWidget(idLabel2, 7, 0)
        formLayout2.addWidget(self.idTextBox2, 7, 1, 1, 2)
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
        self.idTextBox3 = QLineEdit()
        self.idTextBox3.setStyleSheet(textBoxStyle)
        self.idTextBox3.setMaximumWidth(145)

        deleteButton3 = QPushButton("Delete Paper")
        deleteButton3.setFixedWidth(300)
        deleteButton3.clicked.connect(self.deletePaperClicked)
        deleteButton3.setStyleSheet("font-size: 20px; padding: 10px; border-radius: 15px; background-color: #4972FD; color: white;")
        
        # Adding widgets to Grid Layout
        formLayout3.addWidget(scroll3, 0, 0, 4, 6)

        formLayout3.addWidget(idLabel3, 4, 0, 1, 3, alignment=Qt.AlignmentFlag.AlignRight)
        formLayout3.addWidget(self.idTextBox3, 4, 3, 1, 3, alignment=Qt.AlignmentFlag.AlignLeft)
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
        
        nameLabel4 = QLabel("Name")
        nameLabel4.setStyleSheet(labelStyle)
        nameTextBox4 = QLineEdit()
        nameTextBox4.setStyleSheet(textBoxStyle)

        roleLabel4 = QLabel("Job Role")
        roleLabel4.setStyleSheet(labelStyle)
        roleBox4 = QComboBox()
        roleBox4.addItem("")
        roleBox4.setCurrentIndex(0)
        roleBox4.setItemData(0, 0, Qt.ItemDataRole.UserRole - 1)
        roleBox4.addItems(['PhD', 'HiWi', 'Intern'])
        roleBox4.setStyleSheet(textBoxStyle+"padding-left: 15px;")

        researchLabel4 = QLabel("Research Tags")
        researchLabel4.setStyleSheet(labelStyle)
        researchBox4 = MultiSelectComboBox()
        researchBox4.addItems(["Placeholder 1", "Placeholder 2"])
        researchBox4.setStyleSheet(textBoxStyle+"padding-left: 15px;")

        infoLabel4 = QLabel("Additional Info")
        infoLabel4.setStyleSheet(labelStyle)
        infoTextBox4 = QLineEdit()
        infoTextBox4.setStyleSheet(textBoxStyle)
        
        pictureLabel4 = QLabel("Picture Upload")
        pictureLabel4.setStyleSheet(labelStyle)
        pictureUploadButton4 = QPushButton("Upload Image")
        pictureUploadButton4.clicked.connect(self.uploadImage)
        pictureUploadButton4.setStyleSheet("font-size: 20px; padding: 10px; border-radius: 15px; background-color: #4972FD; color: white;")
        pictureUploadButton4.setFixedWidth(300)
        
        aboutLabel4 = QLabel("About")
        aboutLabel4.setStyleSheet(labelStyle)
                
        aboutTextBox4 = QTextEdit()
        aboutTextBox4.setAcceptRichText(False)
        aboutTextBox4.setStyleSheet(textBoxStyle)
        aboutTextBox4.setPlaceholderText("Enter the Background of the Member")

        addMemberButton4 = QPushButton("Add Member")
        addMemberButton4.setFixedWidth(300)
        addMemberButton4.clicked.connect(self.addMemberClicked)
        addMemberButton4.setStyleSheet("font-size: 20px; padding: 10px; border-radius: 15px; background-color: #4972FD; color: white;")
        
        # Adding widgets to Grid Layout
        formLayout4.addWidget(nameLabel4, 0, 0)
        formLayout4.addWidget(nameTextBox4, 0, 1, 1, 5)

        formLayout4.addWidget(roleLabel4, 1, 0, 1, 2)
        formLayout4.addWidget(roleBox4, 1, 1, 1, 2)
        formLayout4.addWidget(researchLabel4, 1, 3, alignment=Qt.AlignmentFlag.AlignRight)
        formLayout4.addWidget(researchBox4, 1, 4, 1, 2)
        
        formLayout4.addWidget(infoLabel4, 2, 0)
        formLayout4.addWidget(infoTextBox4, 2, 1, 1, 5)
        
        formLayout4.addWidget(pictureLabel4, 3, 0)
        formLayout4.addWidget(pictureUploadButton4, 3, 1, 1, 5, alignment=Qt.AlignmentFlag.AlignCenter)
        
        formLayout4.addWidget(aboutLabel4, 4, 0)
        formLayout4.addWidget(aboutTextBox4, 5, 0, 1, 6)

        formLayout4.addWidget(addMemberButton4, 6, 0, 1, 6, alignment=Qt.AlignmentFlag.AlignCenter)
        
        layoutAddMember.addLayout(formLayout4)
        layoutAddMember.setContentsMargins(50, 50, 50, 50)
        tabAddMember.setLayout(layoutAddMember)

        # Tab: Modify Member
        tabModifyMember = QWidget()
        layoutModifyMember = QVBoxLayout()
        
        formLayout5 = QGridLayout()
        
        nameLabel5 = QLabel("Name")
        nameLabel5.setStyleSheet(labelStyle)
        nameTextBox5 = QLineEdit()
        nameTextBox5.setStyleSheet(textBoxStyle)

        roleLabel5 = QLabel("Job Role")
        roleLabel5.setStyleSheet(labelStyle)
        roleBox5 = QComboBox()
        roleBox5.addItem("")
        roleBox5.setCurrentIndex(0)
        roleBox5.setItemData(0, 0, Qt.ItemDataRole.UserRole - 1)
        roleBox5.addItems(['Post Doc', 'PhD', 'HiWi', 'Intern'])
        roleBox5.setStyleSheet(textBoxStyle+"padding-left: 15px;")

        researchLabel5 = QLabel("Research Tags")
        researchLabel5.setStyleSheet(labelStyle)
        researchBox5 = MultiSelectComboBox()
        researchBox5.addItems(["Placeholder 1", "Placeholder 2"])
        researchBox5.setStyleSheet(textBoxStyle+"padding-left: 15px;")

        infoLabel5 = QLabel("Additional Info")
        infoLabel5.setStyleSheet(labelStyle)
        infoTextBox5 = QLineEdit()
        infoTextBox5.setStyleSheet(textBoxStyle)
        
        pictureLabel5 = QLabel("Picture Upload")
        pictureLabel5.setStyleSheet(labelStyle)
        pictureUploadButton5 = QPushButton("Upload Image")
        pictureUploadButton5.clicked.connect(self.uploadImage)
        pictureUploadButton5.setStyleSheet("font-size: 20px; padding: 10px; border-radius: 15px; background-color: #4972FD; color: white;")
        pictureUploadButton5.setFixedWidth(300)
        
        aboutLabel5 = QLabel("About")
        aboutLabel5.setStyleSheet(labelStyle)
                
        aboutTextBox5 = QTextEdit()
        aboutTextBox5.setAcceptRichText(False)
        aboutTextBox5.setStyleSheet(textBoxStyle)
        aboutTextBox5.setPlaceholderText("Enter the Background of the Member")

        addMemberButton5 = QPushButton("Modify Member")
        addMemberButton5.setFixedWidth(300)
        addMemberButton5.clicked.connect(self.addMemberClicked)
        addMemberButton5.setStyleSheet("font-size: 20px; padding: 10px; border-radius: 15px; background-color: #4972FD; color: white;")
        
        # Adding widgets to Grid Layout
        formLayout5.addWidget(nameLabel5, 0, 0)
        formLayout5.addWidget(nameTextBox5, 0, 1, 1, 5)

        formLayout5.addWidget(roleLabel5, 1, 0, 1, 2)
        formLayout5.addWidget(roleBox5, 1, 1, 1, 2)
        formLayout5.addWidget(researchLabel5, 1, 3, alignment=Qt.AlignmentFlag.AlignRight)
        formLayout5.addWidget(researchBox5, 1, 4, 1, 2)
        
        formLayout5.addWidget(infoLabel5, 2, 0)
        formLayout5.addWidget(infoTextBox5, 2, 1, 1, 5)
        
        formLayout5.addWidget(pictureLabel5, 3, 0)
        formLayout5.addWidget(pictureUploadButton5, 3, 1, 1, 5, alignment=Qt.AlignmentFlag.AlignCenter)
        
        formLayout5.addWidget(aboutLabel5, 4, 0)
        formLayout5.addWidget(aboutTextBox5, 5, 0, 1, 6)

        formLayout5.addWidget(addMemberButton5, 6, 0, 1, 6, alignment=Qt.AlignmentFlag.AlignCenter)

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

        idLabel6 = QLabel("Full Name")
        idLabel6.setStyleSheet(labelStyle)
        idTextBox6 = QLineEdit()
        idTextBox6.setStyleSheet(textBoxStyle)

        deleteButton6 = QPushButton("Delete Member")
        deleteButton6.setFixedWidth(300)
        deleteButton6.clicked.connect(self.deletePaperClicked)
        deleteButton6.setStyleSheet("font-size: 20px; padding: 10px; border-radius: 15px; background-color: #4972FD; color: white;")
        
        # Adding widgets to Grid Layout
        formLayout6.addWidget(scroll6, 0, 0, 4, 6)

        formLayout6.addWidget(idLabel6, 4, 0)
        formLayout6.addWidget(idTextBox6, 4, 1, 1, 5)
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
        """
        Handles the event when the 'Submit Paper' button is clicked.
        
        - Checks if all required fields are filled.
        - Imports existing papers from storage.
        - Creates a new paper entry with user-provided details.
        - Appends the new paper to the existing list.
        - Exports the updated paper list back to storage.
        - Displays a success message.
        - Clears the input fields for a new entry.
        """
        
        # List of required input fields to be checked
        checkList = [
            self.linkTextBox, 
            self.titleTextBox, 
            self.authorTextBox, 
            self.conferenceTextBox, 
            self.bibtexTextBox
        ]
        
        # Validate if all required fields are filled
        status = self.checkFields(checkList)

        if status:
            # Import existing papers from storage
            papers = self.importPapers()

            # Create a new paper entry
            newPaper = {
                "id": self.getPaperID(self.titleTextBox.text(), self.dateEdit.date().toString("dd-MM-yyyy")),
                "title": self.titleTextBox.text(),
                "authors": self.authorTextBox.text(),
                "date": self.dateEdit.date().toString("dd-MM-yyyy"),
                "journal": self.conferenceTextBox.text(),
                "link": self.linkTextBox.text(),
                "bibtex": self.bibtexTextBox.toPlainText()
            }

            # Add the new paper to the existing list
            papers.append(newPaper)

            # Export the updated list back to storage
            self.exportPapers(papers)

            # Show a success message to the user
            QMessageBox.information(self, "Success", "Paper Submitted Successfully!")

            # Clear input fields for the next entry
            self.clearFields(checkList)

    def modifyPaperClicked(self):
        """
        Handles the event when the 'Modify Paper' button is clicked.

        - Prints a debug message to indicate the function is triggered.
        - Checks if all required fields are filled.
        - Imports existing papers from storage.
        - Searches for the paper with the specified ID.
        - Updates the paper details with new user-provided values.
        - Exports the updated paper list back to storage.
        - Displays a success message if modification is successful.
        - Clears the input fields after modification.
        - Displays a warning message if any field is empty.
        """

        # Debug message to indicate function execution
        print("Modify Paper Clicked")

        # List of required input fields to be checked
        checkList = [
            self.linkTextBox2, 
            self.titleTextBox2, 
            self.authorTextBox2, 
            self.conferenceTextBox2, 
            self.bibtexTextBox2, 
            self.idTextBox2
        ]
        
        # Validate if all required fields are filled
        status = self.checkFields(checkList)

        if status:
            # Import existing papers from storage
            papers = self.importPapers()

            # Iterate over the paper list to find the matching ID
            for paper in papers:
                if paper["id"] == self.idTextBox2.text():
                    # Update the paper details with new input values
                    paper["title"] = self.titleTextBox2.text()
                    paper["authors"] = self.authorTextBox2.text()
                    paper["date"] = self.dateEdit2.date().toString("dd-MM-yyyy")
                    paper["journal"] = self.conferenceTextBox2.text()
                    paper["link"] = self.linkTextBox2.text()
                    paper["bibtex"] = self.bibtexTextBox2.toPlainText()
                    break  # Exit loop after finding the paper

            # Export the updated paper list back to storage
            self.exportPapers(papers)

            # Show a success message to the user
            QMessageBox.information(self, "Success", "Paper Modified Successfully!")

            # Clear input fields for the next modification
            self.clearFields(checkList)

        else:
            # Show a warning message if any field is empty
            QMessageBox.warning(self, "Warning", "One or more fields are empty!")        
    
    def deletePaperClicked(self):
        """
        Handles the event when the 'Delete Paper' button is clicked.

        - Checks if the Paper ID field is filled.
        - Displays a warning confirmation message.
        - If confirmed, imports existing papers from storage.
        - Filters out the paper with the matching ID.
        - Exports the updated paper list back to storage.
        - Clears the input field after deletion.
        - Displays a warning if the Paper ID is empty.
        """

        # List of required input fields to be checked
        checkList = [self.idTextBox3]

        # Validate if the Paper ID field is filled
        status = self.checkFields(checkList)

        if status:
            # Display a warning confirmation before deletion
            QMessageBox.warning(self, "Warning", "Are you sure you want to delete the paper?")
            
            # Import existing papers from storage
            papers = self.importPapers()

            # Filter out the paper with the matching ID
            updatedPapers = [paper for paper in papers if paper["id"] != self.idTextBox3.text()]

            # Export the updated paper list back to storage
            self.exportPapers(updatedPapers)

            # Clear the Paper ID field after deletion
            self.clearFields(checkList)
        else:
            # Show a warning message if Paper ID is empty
            QMessageBox.warning(self, "Warning", "Paper ID is empty!")
            
    def importPapers(self):
        """
        Imports papers from a JSON file.

        - Reads the paper data from the specified JSON file.
        - Prints the JSON data in a well-formatted manner for debugging.
        - Returns the list of papers.

        Note: Ensure the file path is correctly set before deployment.
        """

        # Define the file path (Replace before deployment if necessary)
        file_path = os.path.join(os.getcwd(), "data", "trial_papers.json")

        # Open and read the JSON file
        with open(file_path, "r") as file:
            papers = json.load(file)  # Load the JSON content as a Python list

        # Print the JSON data in a readable format (for debugging purposes)
        print(json.dumps(papers, indent=4))

        # Return the loaded papers list
        return papers
    
    def parseDate(self, paper):
        """
        Parses the date string from a paper dictionary and converts it to a datetime object.

        - Extracts the "date" field from the given paper dictionary.
        - Converts the date string from the format "dd-mm-yyyy" to a datetime object.

        Args:
            paper (dict): A dictionary containing paper details, including a "date" field.

        Returns:
            datetime: A datetime object representing the parsed date.
        """

        return datetime.strptime(paper["date"], "%d-%m-%Y")
    
    def exportPapers(self, papers):
        """
        Exports the given list of papers to a JSON file after sorting them in reverse chronological order.

        - Sorts the papers list by date in descending order (latest papers first).
        - Writes the sorted list back to the specified JSON file.

        Args:
            papers (list): A list of dictionaries where each dictionary represents a paper.

        Note: Ensure the file path is correctly set before deployment.
        """

        # Sort papers by date in descending order (latest papers first)
        papers.sort(key=self.parseDate, reverse=True)

        # Define the file path (Replace before deployment if necessary)
        file_path = os.path.join(os.getcwd(), "data", "trial_papers.json")

        # Open and write the sorted papers to the JSON file
        with open(file_path, "w") as file:
            json.dump(papers, file, indent=4)
    
    def checkFields(self, fieldsList):
        """
        Checks if all required input fields in the given list are filled.

        - Iterates over each field in `fieldsList`.
        - If the field is a `QLineEdit`, checks if its text is empty after stripping whitespace.
        - If the field is a `QTextEdit`, checks if its plain text is empty after stripping whitespace.
        - Returns `True` if all fields are filled, otherwise returns `False`.

        Args:
            fieldsList (list): A list of input fields (`QLineEdit` or `QTextEdit`) to be checked.

        Returns:
            bool: `True` if all fields are filled, otherwise `False`.
        """

        flag = 0  

        for field in fieldsList:
            if isinstance(field, QLineEdit):  
                if field.text().strip() == "":  
                    flag += 1
            elif isinstance(field, QTextEdit):  
                if field.toPlainText().strip() == "":  
                    flag += 1

        # Return True if no empty fields are found, otherwise return False
        return flag == 0
        
    def clearFields(self, fieldsList):
        """
        Clears the content of all input fields in the given list.

        - Iterates over each field in `fieldsList`.
        - If the field is a `QLineEdit`, clears its text.
        - If the field is a `QTextEdit`, clears its text.

        Args:
            fieldsList (list): A list of input fields (`QLineEdit` or `QTextEdit`) to be cleared.
        """

        for field in fieldsList:
            if isinstance(field, QLineEdit): 
                field.clear()  
            elif isinstance(field, QTextEdit):
                field.clear() 
        
    def getPaperID(self, paperTitle, publicationDate):
        """
        Generates a unique Paper ID based on the publication date and title.

        - Extracts the day and month from the publication date.
        - Removes non-alphanumeric characters from the paper title.
        - Constructs an ID in the format "DDMM-TTTT", where:
        - "DDMM" represents the day and month of publication.
        - "TTTT" represents the first four alphanumeric characters of the title.

        Args:
            paperTitle (str): The title of the paper.
            publicationDate (str): The publication date in the format "DD-MM-YYYY".

        Returns:
            str: A unique paper ID in the format "DDMM-TTTT".
        """

        # Extract day and month from the publication date
        date = publicationDate.split('-')

        # Remove non-alphanumeric characters from the paper title
        title = "".join(char for char in list(paperTitle) if char.isalnum())

        # Generate the Paper ID using the first four characters of the sanitized title
        paper_id = (date[0] + date[1]) + '-' + (title[0:4])

        return paper_id
    

    def extractClicked(self, layout):
        """
        Extracts properties from a BibTeX string including:
        - title
        - authors
        - date (year)
        - journal
        - link (if available)

        Args:
            bibtexString (str): A string containing the BibTeX entry.

        Returns:
            None
        """

        bibtexString = self.bibtexTextBox.toPlainText() if layout == 1 else self.bibtexTextBox2.toPlainText()

        # Extract the title
        title_match = re.search(r'title\s*=\s*{(.*?)}', bibtexString, re.IGNORECASE)
        title = title_match.group(1) if title_match else None
        
        if title != None:
            if layout == 1:
                self.titleTextBox.setText(title)
            elif layout == 2:
                self.titleTextBox2.setText(title)

        # Extract the authors
        authorsMatch = re.search(r'author\s*=\s*{(.*?)}', bibtexString, re.IGNORECASE)
        authors = authorsMatch.group(1) if authorsMatch else None

        if authorsMatch:
            authors = authorsMatch.group(1)
            first_author = authors.split(" and ")[0]
            authors = (first_author.strip().split(",")[0] + first_author.strip().split(",")[1] if "," in first_author else first_author.strip()) + " et al."

        if authors != None:
            if layout == 1:
                self.authorTextBox.setText(authors)
            elif layout == 2:
                self.authorTextBox2.setText(authors)
        
        # Extract the date (year)
        date_match = re.search(r'year\s*=\s*{(\d{4})}', bibtexString, re.IGNORECASE)
        date = date_match.group(1) if date_match else None
        
        print(date)

        # Extract the journal
        journal_match = re.search(r'journal\s*=\s*{(.*?)}', bibtexString, re.IGNORECASE)
        journal = journal_match.group(1) if journal_match else None
        
        if journal != None:
            if layout == 1:
                self.conferenceTextBox.setText(journal)
            elif layout == 2:
                self.conferenceTextBox2.setText(journal)

        # Extract the link (if present)
        link_match = re.search(r'url\s*=\s*{(.*?)}', bibtexString, re.IGNORECASE)
        link = link_match.group(1) if link_match else None
        
        if link != None:
            if layout == 1:
                self.linkTextBox.setText(link)
            elif layout == 2:
                self.linkTextBox2.setText(link)

        return None

    def addPapersFromDatabase(self, layout):
        print("Adding Papers from Database")
        papers = self.importPapers()
        """for i in range(1, 21):
            layout.addWidget(QLabel("This is the function"))
        return layout"""

    def uploadImage(self):
        filePath, _ = QFileDialog.getOpenFileName(self, "Select an Image", "", "Images (*.png *.jpg *.jpeg *.bmp *.gif)")
        print("Upload Image Clicked", filePath)

    def addMemberClicked(self):
        print("Add Member Clicked")
        # Check if all the field are filled. Show warning if not.

    def deleteMemberClicked(self):
        print("Delete Member Clicked")
        # Check if all the field are filled. Show warning if not.

    
        

app = QApplication(sys.argv)
app.setFont(QFont("Montserrat"))
window = MainWindow()
window.show()
sys.exit(app.exec())