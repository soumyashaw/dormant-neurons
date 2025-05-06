import os
import re
import sys
import json
import shutil
from datetime import datetime
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QLineEdit, QTextEdit, QPushButton, QFileDialog, QFrame,
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
        
################################## Main Context: Paper Area ###################################################
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

        # Widget to hold the scrollable Paper's content
        paperBox2 = QWidget()
        scroll2.setWidget(paperBox2)

        # Layout to hold the content inside paperBox
        self.scrollableLayout2 = QVBoxLayout(paperBox2)

        # Add papers from Database to the scrollable layout
        self.addPapersFromDatabase(self.scrollableLayout2)

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

        # Widget to hold the scrollable Paper's content
        paperBox3 = QWidget()
        scroll3.setWidget(paperBox3)

        # Layout to hold the content inside paperBox
        self.scrollableLayout3 = QVBoxLayout(paperBox3)

        # Add papers from Database to the scrollable layout
        self.addPapersFromDatabase(self.scrollableLayout3)

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
        self.nameTextBox4 = QLineEdit()
        self.nameTextBox4.setStyleSheet(textBoxStyle)

        roleLabel4 = QLabel("Job Role")
        roleLabel4.setStyleSheet(labelStyle)
        self.roleBox4 = QComboBox()
        self.roleBox4.addItem("")
        self.roleBox4.setCurrentIndex(0)
        self.roleBox4.setItemData(0, 0, Qt.ItemDataRole.UserRole - 1)
        self.roleBox4.addItems(['Post Doc','PhD Student', 'HiWi', 'Intern'])
        self.roleBox4.setStyleSheet(textBoxStyle+"padding-left: 15px;")

        researchLabel4 = QLabel("Research Tags")
        researchLabel4.setStyleSheet(labelStyle)
        self.researchBox4 = QLineEdit()
        self.researchBox4.setStyleSheet(textBoxStyle)
        self.researchBox4.setPlaceholderText("Separate with commas")


        infoLabel4 = QLabel("Additional Info")
        infoLabel4.setStyleSheet(labelStyle)
        self.infoTextBox4 = QLineEdit()
        self.infoTextBox4.setStyleSheet(textBoxStyle)
        self.infoTextBox4.setPlaceholderText("Optional")
        
        pictureLabel4 = QLabel("Picture Upload")
        pictureLabel4.setStyleSheet(labelStyle)
        self.pictureUploadButton4 = QPushButton("Default Image")
        self.pictureUploadButton4.clicked.connect(lambda: self.uploadImage(self.pictureUploadButton4))
        self.pictureUploadButton4.setStyleSheet("font-size: 20px; padding: 10px; border-radius: 15px; background-color: #4972FD; color: white;")
        self.pictureUploadButton4.setFixedWidth(260)
        self.imageFilePath = ""

        self.hoverPictureUploadButton4 = QPushButton("Alternate Image")
        self.hoverPictureUploadButton4.clicked.connect(lambda: self.hoverUploadImage(self.hoverPictureUploadButton4))
        self.hoverPictureUploadButton4.setStyleSheet("font-size: 20px; padding: 10px; border-radius: 15px; background-color: #4972FD; color: white;")
        self.hoverPictureUploadButton4.setFixedWidth(260)
        self.hoverImageFilePath = ""
        
        aboutLabel4 = QLabel("About")
        aboutLabel4.setStyleSheet(labelStyle)
                
        self.aboutTextBox4 = QTextEdit()
        self.aboutTextBox4.setAcceptRichText(False)
        self.aboutTextBox4.setStyleSheet(textBoxStyle)
        self.aboutTextBox4.setPlaceholderText("Enter the Background of the Member")

        addMemberButton4 = QPushButton("Add Member")
        addMemberButton4.setFixedWidth(300)
        addMemberButton4.clicked.connect(self.addMemberClicked)
        addMemberButton4.setStyleSheet("font-size: 20px; padding: 10px; border-radius: 15px; background-color: #4972FD; color: white;")
        
        # Adding widgets to Grid Layout
        formLayout4.addWidget(nameLabel4, 0, 0)
        formLayout4.addWidget(self.nameTextBox4, 0, 1, 1, 5)

        formLayout4.addWidget(roleLabel4, 1, 0, 1, 2)
        formLayout4.addWidget(self.roleBox4, 1, 1, 1, 2)
        formLayout4.addWidget(researchLabel4, 1, 3, alignment=Qt.AlignmentFlag.AlignRight)
        formLayout4.addWidget(self.researchBox4, 1, 4, 1, 2)
        
        formLayout4.addWidget(infoLabel4, 2, 0)
        formLayout4.addWidget(self.infoTextBox4, 2, 1, 1, 5)
        
        formLayout4.addWidget(pictureLabel4, 3, 0)
        formLayout4.addWidget(self.pictureUploadButton4, 3, 1, 1, 2, alignment=Qt.AlignmentFlag.AlignCenter)
        formLayout4.addWidget(self.hoverPictureUploadButton4, 3, 4, 1, 2, alignment=Qt.AlignmentFlag.AlignCenter)
        
        formLayout4.addWidget(aboutLabel4, 4, 0)
        formLayout4.addWidget(self.aboutTextBox4, 5, 0, 1, 6)

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
        self.nameTextBox5 = QLineEdit()
        self.nameTextBox5.setStyleSheet(textBoxStyle)

        roleLabel5 = QLabel("Job Role")
        roleLabel5.setStyleSheet(labelStyle)
        self.roleBox5 = QComboBox()
        self.roleBox5.addItem("")
        self.roleBox5.setCurrentIndex(0)
        self.roleBox5.setItemData(0, 0, Qt.ItemDataRole.UserRole - 1)
        self.roleBox5.addItems(['Post Doc', 'PhD Student', 'HiWi', 'Intern'])
        self.roleBox5.setStyleSheet(textBoxStyle+"padding-left: 15px;")

        researchLabel5 = QLabel("Research Tags")
        researchLabel5.setStyleSheet(labelStyle)
        self.researchBox5 = QLineEdit()
        self.researchBox5.setStyleSheet(textBoxStyle)
        self.researchBox5.setPlaceholderText("Separate with commas")

        infoLabel5 = QLabel("Additional Info")
        infoLabel5.setStyleSheet(labelStyle)
        self.infoTextBox5 = QLineEdit()
        self.infoTextBox5.setStyleSheet(textBoxStyle)
        self.infoTextBox5.setPlaceholderText("Optional")
        
        pictureLabel5 = QLabel("Picture Upload")
        pictureLabel5.setStyleSheet(labelStyle)
        self.pictureUploadButton5 = QPushButton("Default Image")
        self.pictureUploadButton5.clicked.connect(lambda: self.uploadImage(self.pictureUploadButton5))
        self.pictureUploadButton5.setStyleSheet("font-size: 20px; padding: 10px; border-radius: 15px; background-color: #4972FD; color: white;")
        self.pictureUploadButton5.setFixedWidth(260)

        self.hoverPictureUploadButton5 = QPushButton("Alternate Image")
        self.hoverPictureUploadButton5.clicked.connect(lambda: self.hoverUploadImage(self.hoverPictureUploadButton5))
        self.hoverPictureUploadButton5.setStyleSheet("font-size: 20px; padding: 10px; border-radius: 15px; background-color: #4972FD; color: white;")
        self.hoverPictureUploadButton5.setFixedWidth(260)
        
        aboutLabel5 = QLabel("About")
        aboutLabel5.setStyleSheet(labelStyle)
                
        self.aboutTextBox5 = QTextEdit()
        self.aboutTextBox5.setAcceptRichText(False)
        self.aboutTextBox5.setStyleSheet(textBoxStyle)
        self.aboutTextBox5.setPlaceholderText("Enter the Background of the Member")

        self.modifyMemberButton5 = QPushButton("Modify Member")
        self.modifyMemberButton5.setFixedWidth(300)
        self.modifyMemberButton5.clicked.connect(self.modifyMemberClicked)
        self.modifyMemberButton5.setStyleSheet("font-size: 20px; padding: 10px; border-radius: 15px; background-color: #4972FD; color: white;")
        
        # Adding widgets to Grid Layout
        formLayout5.addWidget(nameLabel5, 0, 0)
        formLayout5.addWidget(self.nameTextBox5, 0, 1, 1, 5)

        formLayout5.addWidget(roleLabel5, 1, 0, 1, 2)
        formLayout5.addWidget(self.roleBox5, 1, 1, 1, 2)
        formLayout5.addWidget(researchLabel5, 1, 3, alignment=Qt.AlignmentFlag.AlignRight)
        formLayout5.addWidget(self.researchBox5, 1, 4, 1, 2)
        
        formLayout5.addWidget(infoLabel5, 2, 0)
        formLayout5.addWidget(self.infoTextBox5, 2, 1, 1, 5)
        
        formLayout5.addWidget(pictureLabel5, 3, 0)
        formLayout5.addWidget(self.pictureUploadButton5, 3, 1, 1, 2, alignment=Qt.AlignmentFlag.AlignCenter)
        formLayout5.addWidget(self.hoverPictureUploadButton5, 3, 4, 1, 2, alignment=Qt.AlignmentFlag.AlignCenter)
        
        formLayout5.addWidget(aboutLabel5, 4, 0)
        formLayout5.addWidget(self.aboutTextBox5, 5, 0, 1, 6)

        formLayout5.addWidget(self.modifyMemberButton5, 6, 0, 1, 6, alignment=Qt.AlignmentFlag.AlignCenter)

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

        # Widget to hold the scrollable Member's content
        memberBox6 = QWidget()
        scroll6.setWidget(memberBox6)

        # Layout to hold the content inside memberBox
        self.scrollableLayout6 = QVBoxLayout(memberBox6)

        # Add members from Database to the scrollable layout
        self.addMembersFromDatabase(self.scrollableLayout6)

        idLabel6 = QLabel("Full Name")
        idLabel6.setStyleSheet(labelStyle)
        self.idTextBox6 = QLineEdit()
        self.idTextBox6.setStyleSheet(textBoxStyle)

        deleteButton6 = QPushButton("Delete Member")
        deleteButton6.setFixedWidth(300)
        deleteButton6.clicked.connect(self.deleteMemberClicked)
        deleteButton6.setStyleSheet("font-size: 20px; padding: 10px; border-radius: 15px; background-color: #4972FD; color: white;")
        
        # Adding widgets to Grid Layout
        formLayout6.addWidget(scroll6, 0, 0, 4, 6)

        formLayout6.addWidget(idLabel6, 4, 0)
        formLayout6.addWidget(self.idTextBox6, 4, 1, 1, 5)
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

############################### Main Context: Latest News #################################################
        # Tab Widget
        self.tabsLatestNews = QTabWidget()
        
        # Tab: Add Latest News
        tabAddNews = QWidget()
        layoutAddNews = QVBoxLayout()
        
        formLayout7 = QGridLayout()

        dateLabel7 = QLabel("Date")
        dateLabel7.setStyleSheet(labelStyle)
        
        self.dateEdit7 = QDateEdit()
        self.dateEdit7.setCalendarPopup(True)
        self.dateEdit7.setStyleSheet(textBoxStyle)
        self.dateEdit7.setDate(QDate.currentDate())
        
        headerLabel7 = QLabel("News Header")
        headerLabel7.setStyleSheet(labelStyle)
        self.headerTextBox7 = QLineEdit()
        self.headerTextBox7.setStyleSheet(textBoxStyle)
        
        contentsLabel7 = QLabel("Contents")
        contentsLabel7.setStyleSheet(labelStyle)
                
        self.contentsTextBox7 = QTextEdit()
        self.contentsTextBox7.setAcceptRichText(False)
        self.contentsTextBox7.setStyleSheet(textBoxStyle)
        self.contentsTextBox7.setPlaceholderText("Enter the Contents (body) of the News")

        noteLabel7 = QLabel("Note: To add hyperlinks, use the format: [text](link)")

        addNewsButton7 = QPushButton("Add News")
        addNewsButton7.setFixedWidth(300)
        addNewsButton7.clicked.connect(self.addNewsClicked)
        addNewsButton7.setStyleSheet("font-size: 20px; padding: 10px; border-radius: 15px; background-color: #4972FD; color: white;")
        
        # Adding widgets to Grid Layout
        formLayout7.addWidget(dateLabel7, 0, 0)
        formLayout7.addWidget(self.dateEdit7, 0, 1, 1, 5)

        formLayout7.addWidget(headerLabel7, 1, 0, 1, 2)
        formLayout7.addWidget(self.headerTextBox7, 1, 1, 1, 5)
        
        formLayout7.addWidget(contentsLabel7, 2, 0)
        formLayout7.addWidget(self.contentsTextBox7, 3, 0, 1, 6)

        formLayout7.addWidget(noteLabel7, 4, 0, 1, 6)

        formLayout7.addWidget(addNewsButton7, 5, 0, 1, 6, alignment=Qt.AlignmentFlag.AlignCenter)
        
        layoutAddNews.addLayout(formLayout7)
        layoutAddNews.setContentsMargins(50, 50, 50, 50)
        tabAddNews.setLayout(layoutAddNews)

        # Tab: Modify Latest News
        tabModifyNews = QWidget()
        layoutModifyNews = QVBoxLayout()
        
        formLayout8 = QGridLayout()

        scroll8 = QScrollArea()
        scroll8.setWidgetResizable(True)
        scroll8.setStyleSheet("background-color: #d9d9d9; margin-bottom: 30px;")

        # Widget to hold the scrollable Paper's content
        newsBox8 = QWidget()
        scroll8.setWidget(newsBox8)

        # Layout to hold the content inside paperBox
        self.scrollableLayout8 = QVBoxLayout(newsBox8)

        # Add papers from Database to the scrollable layout
        self.addNewsFromDatabase(self.scrollableLayout8)

        idLabel8 = QLabel("News ID")
        idLabel8.setStyleSheet(labelStyle)

        self.idTextBox8 = QLineEdit()
        self.idTextBox8.setStyleSheet(textBoxStyle)
        
        dateLabel8 = QLabel("Date")
        dateLabel8.setStyleSheet(labelStyle)
        
        self.dateEdit8 = QDateEdit()
        self.dateEdit8.setCalendarPopup(True)
        self.dateEdit8.setStyleSheet(textBoxStyle)
        self.dateEdit8.setDate(QDate.currentDate())

        headerLabel8 = QLabel("News Header")
        headerLabel8.setStyleSheet(labelStyle)
        self.headerTextBox8 = QLineEdit()
        self.headerTextBox8.setStyleSheet(textBoxStyle)
        
        contentsLabel8 = QLabel("Contents")
        contentsLabel8.setStyleSheet(labelStyle)
                
        self.contentsTextBox8 = QTextEdit()
        self.contentsTextBox8.setAcceptRichText(False)
        self.contentsTextBox8.setStyleSheet(textBoxStyle)
        self.contentsTextBox8.setPlaceholderText("Enter the Contents (body) of the News")

        noteLabel8 = QLabel("Note: To add hyperlinks, use the format: [text](link)")

        self.modifyNewsButton8 = QPushButton("Modify News")
        self.modifyNewsButton8.setFixedWidth(300)
        self.modifyNewsButton8.clicked.connect(self.modifyNewsClicked)
        self.modifyNewsButton8.setStyleSheet("font-size: 20px; padding: 10px; border-radius: 15px; background-color: #4972FD; color: white;")
        
        # Adding widgets to Grid Layout
        formLayout8.addWidget(scroll8, 0, 0, 1, 6)

        formLayout8.addWidget(idLabel8, 1, 0)
        formLayout8.addWidget(self.idTextBox8, 1, 1, 1, 5)

        formLayout8.addWidget(dateLabel8, 2, 0)
        formLayout8.addWidget(self.dateEdit8, 2, 1, 1, 5)

        formLayout8.addWidget(headerLabel8, 3, 0, 1, 2)
        formLayout8.addWidget(self.headerTextBox8, 3, 1, 1, 5)
        
        formLayout8.addWidget(contentsLabel8, 4, 0)
        formLayout8.addWidget(self.contentsTextBox8, 5, 0, 1, 6)

        formLayout8.addWidget(noteLabel8, 6, 0, 1, 6)

        formLayout8.addWidget(self.modifyNewsButton8, 7, 0, 1, 6, alignment=Qt.AlignmentFlag.AlignCenter)

        layoutModifyNews.addLayout(formLayout8)
        layoutModifyNews.setContentsMargins(50, 50, 50, 50)
        tabModifyNews.setLayout(layoutModifyNews)

        # Tab: Delete News
        tabDeleteNews = QWidget()
        layoutDeleteNews = QVBoxLayout()
        
        formLayout9 = QGridLayout()

        scroll9 = QScrollArea()
        scroll9.setWidgetResizable(True)
        scroll9.setStyleSheet("background-color: #d9d9d9; margin-bottom: 30px;")

        # Widget to hold the scrollable Member's content
        newsBox9 = QWidget()
        scroll9.setWidget(newsBox9)

        # Layout to hold the content inside memberBox
        self.scrollableLayout9 = QVBoxLayout(newsBox9)

        # Add members from Database to the scrollable layout
        self.addNewsFromDatabase(self.scrollableLayout9)

        idLabel9 = QLabel("News ID")
        idLabel9.setStyleSheet(labelStyle+"padding-right: 50px;")
        self.idTextBox9 = QLineEdit()
        self.idTextBox9.setStyleSheet(textBoxStyle)
        self.idTextBox9.setMaximumWidth(145)

        deleteButton9 = QPushButton("Delete News")
        deleteButton9.setFixedWidth(300)
        deleteButton9.clicked.connect(self.deleteNewsClicked)
        deleteButton9.setStyleSheet("font-size: 20px; padding: 10px; border-radius: 15px; background-color: #4972FD; color: white;")
        
        # Adding widgets to Grid Layout
        formLayout9.addWidget(scroll9, 0, 0, 4, 6)

        formLayout9.addWidget(idLabel9, 4, 0, 1, 3, alignment=Qt.AlignmentFlag.AlignRight)
        formLayout9.addWidget(self.idTextBox9, 4, 3, 1, 3, alignment=Qt.AlignmentFlag.AlignLeft)
        formLayout9.addWidget(deleteButton9, 5, 0, 1, 6, alignment=Qt.AlignmentFlag.AlignCenter)
        layoutDeleteNews.addLayout(formLayout9)
        layoutDeleteNews.setContentsMargins(50, 50, 50, 50)
        tabDeleteNews.setLayout(layoutDeleteNews)

        # Add Tabs to the TabWidget
        self.tabsLatestNews.addTab(tabAddNews, "ADD NEWS")
        self.tabsLatestNews.addTab(tabModifyNews, "MODIFY NEWS")
        self.tabsLatestNews.addTab(tabDeleteNews, "DELETE NEWS")

        self.tabsLatestNews.setStyleSheet("""
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

        self.mainContextNews = QWidget()
        newsLayout = QVBoxLayout(self.mainContextNews)
        newsLayout.addWidget(self.tabsLatestNews)
        self.mainContextNews.setLayout(newsLayout)

########################################################################################################
        
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
            # Check if the Paper ID field is present in the database
            if self.isPaperPresent(self.getPaperID(self.titleTextBox.text(), self.dateEdit.date().toString("dd-MM-yyyy"))):
                QMessageBox.warning(self, "Warning", "Paper ID already exists in the database!")
                return

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

            # Refresh the paper list after modification
            self.clearLayout(self.scrollableLayout2)
            self.addPapersFromDatabase(self.scrollableLayout2)
            self.clearLayout(self.scrollableLayout3)
            self.addPapersFromDatabase(self.scrollableLayout3)

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
        #print("Modify Paper Clicked")

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
            # Check if the Paper ID field is present in the database
            if not self.isPaperPresent(self.idTextBox2.text()):
                QMessageBox.warning(self, "Warning", "Paper ID not found in the database!")
                return

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

            # Refresh the paper list after modification
            self.clearLayout(self.scrollableLayout2)
            self.addPapersFromDatabase(self.scrollableLayout2)
            self.clearLayout(self.scrollableLayout3)
            self.addPapersFromDatabase(self.scrollableLayout3)

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
            # Check if the Paper ID field is present in the database
            if not self.isPaperPresent(self.idTextBox3.text()):
                QMessageBox.warning(self, "Warning", "Paper ID not found in the database!")
                return

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

            # Refresh the paper list after modification
            self.clearLayout(self.scrollableLayout2)
            self.addPapersFromDatabase(self.scrollableLayout2)
            self.clearLayout(self.scrollableLayout3)
            self.addPapersFromDatabase(self.scrollableLayout3)
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
        file_path = os.path.join(self.getBasePath(), "data", "papers.json")

        # Open and read the JSON file
        with open(file_path, "r") as file:
            papers = json.load(file)  # Load the JSON content as a Python list

        # Print the JSON data in a readable format (for debugging purposes)
        #print(json.dumps(papers, indent=4))

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
        file_path = os.path.join(self.getBasePath(), "data", "papers.json")

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
        for field in fieldsList:
            if isinstance(field, QLineEdit):
                if not field.text().strip():
                    return False
            elif isinstance(field, QTextEdit):
                if not field.toPlainText().strip():
                    return False
            elif isinstance(field, QComboBox):
                if field.currentIndex() == -1 or not field.currentText().strip():
                    return False
            elif isinstance(field, MultiSelectComboBox):
                if not field.currentData().strip(): 
                    return False
            elif isinstance(field, str):
                if not field.strip():
                    return False
        return True
        
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
            elif isinstance(field, QComboBox):
                field.setCurrentIndex(0)
            elif isinstance(field, MultiSelectComboBox):
                field.setCurrentIndex(0)
            elif isinstance(field, str):
                field = ""
        
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
        # Adding sample content dynamically
        papers = self.importPapers()
        
        for p in papers:
            paperFrame = QFrame()
            paperFrame.setFrameShape(QFrame.Shape.Box)
            paperFrame.setLineWidth(1)
            paperFrame.setStyleSheet("""
                QFrame {
                    background-color: #F3EBEB;
                    padding: 0px;
                    margin-left: 5px;
                    margin-right: 5px;
                    margin-bottom: 1px;
                    margin-top: 0px;
                    color: black;
                    border-radius: 5px;
                }
            """)

            # Label for the ID
            paperIDinBox = QLabel(f"<b>ID</b>: {p['id']}")
            paperIDinBox.setAlignment(Qt.AlignmentFlag.AlignLeft)
            paperIDinBox.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)

            # Label for the Title
            paperTitleinBox = QLabel(f"<b>Title</b>: {p['title']}")
            paperTitleinBox.setAlignment(Qt.AlignmentFlag.AlignLeft)
            paperTitleinBox.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)

            # Label for the Authors
            paperAuthorsinBox = QLabel(f"<b>Authors</b>: {p['authors']}")
            paperAuthorsinBox.setAlignment(Qt.AlignmentFlag.AlignLeft)
            paperAuthorsinBox.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)

            # Label for the Conference
            paperConferenceinBox = QLabel(f"<b>Conference</b>: {p['journal']}")
            paperConferenceinBox.setAlignment(Qt.AlignmentFlag.AlignLeft)
            paperConferenceinBox.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)

            # Layout inside each rectangular box
            frameLayout = QVBoxLayout(paperFrame)
            frameLayout.setSpacing(0)
            frameLayout.setContentsMargins(1, 1, 1, 1)

            frameLayout.addWidget(paperIDinBox)
            frameLayout.addWidget(paperTitleinBox)
            frameLayout.addWidget(paperAuthorsinBox)
            frameLayout.addWidget(paperConferenceinBox)

            # Add rectangle to scrollable layout
            layout.addWidget(paperFrame)
        return None
    
    def clearLayout(self, layout):
        """
        Clears the content of the given layout."
        """
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

    def importMembers(self):
        """
        Imports members from a JSON file.

        - Reads the member data from the specified JSON file.
        - Prints the JSON data in a well-formatted manner for debugging.
        - Returns the list of members.

        Note: Ensure the file path is correctly set before deployment.
        """

        # Define the file path (Replace before deployment if necessary)
        file_path = os.path.join(self.getBasePath(), "data", "members.json")

        # Open and read the JSON file
        with open(file_path, "r") as file:
            members = json.load(file)  # Load the JSON content as a Python list

        # Print the JSON data in a readable format (for debugging purposes)
        #print(json.dumps(members, indent=4))

        # Return the loaded papers list
        return members
    
    def exportMembers(self, members):
        """
        Exports the given list of members to a JSON file after sorting them in importance order.

        - Sorts the members list by importance order (Group Leader, Post Doc, PhD, HiWi, Intern).
        - Writes the sorted list back to the specified JSON file.

        Args:
            members (list): A list of dictionaries where each dictionary represents a member.

        Note: Ensure the file path is correctly set before deployment.
        """

        # Sort members by importance order
        positionOrder = ['Group Leader', 'Post Doc', 'PhD Student', 'HiWi', 'Intern']
        members = sorted(members, key=lambda x: positionOrder.index(x['position']))

        # Define the file path (Replace before deployment if necessary)
        file_path = os.path.join(self.getBasePath(), "data", "members.json")

        # Open and write the sorted papers to the JSON file
        with open(file_path, "w") as file:
            json.dump(members, file, indent=4)

    def uploadImage(self, button):
        self.imageFilePath, _ = QFileDialog.getOpenFileName(self, "Select an Image", "", "Images (*.png *.jpg *.jpeg *.bmp *.gif)")

        if self.imageFilePath:
            button.setText("Image Uploaded ✅")
        
        #print("Upload Image Clicked", self.imageFilePath)
        
    def hoverUploadImage(self, button):
        self.hoverImageFilePath, _ = QFileDialog.getOpenFileName(self, "Select an Image", "", "Images (*.png *.jpg *.jpeg *.bmp *.gif)")

        if self.hoverImageFilePath:
            button.setText("Image Uploaded ✅")
        
        #print("Upload Hover Image Clicked", self.hoverImageFilePath)

    def addMemberClicked(self):
        #print("Add Member Clicked")
        """
        Handles the event when the 'Add member' button is clicked.
        
        - Checks if all required fields are filled.
        - Imports existing members from storage.
        - Creates a new member entry with user-provided details.
        - Appends the new member to the existing list.
        - Exports the updated member list back to storage.
        - Displays a success message.
        - Clears the input fields for a new entry.
        """
        
        # List of required input fields to be checked
        checkList = [
            self.nameTextBox4, 
            self.roleBox4, 
            self.researchBox4, 
            self.aboutTextBox4,
            self.imageFilePath
        ]
        
        # Validate if all required fields are filled
        status = self.checkFields(checkList)

        if status:
            # Check if the name is already present
            if self.isNamePresent(self.nameTextBox4.text()):
                QMessageBox.warning(self, "Warning", "Member already exists!")
                return
            
            if self.nameTextBox4.text() != "":
                # Transfer the image to the website directory location
                #print("self.imageFilePath", self.imageFilePath)
                fileFormat = os.path.splitext(self.imageFilePath)[1]
                shutil.copy(self.imageFilePath, os.path.join(os.getcwd(), "img", "team", self.nameTextBox4.text().lower().replace(" ", "_") + fileFormat))
                
                if self.hoverImageFilePath != "":
                    # Transfer the Hover image to the website directory location
                    #print("self.hoverImageFilePath", self.hoverImageFilePath)
                    fileFormat = os.path.splitext(self.hoverImageFilePath)[1]
                    shutil.copy(self.hoverImageFilePath, os.path.join(os.getcwd(), "img", "team", self.nameTextBox4.text().lower().replace(" ", "_") + "_alt" + fileFormat))
            
            else:
                QMessageBox.warning(self, "Warning", "Member Name is empty! Enter it first")
                return
            
            # Process Research interests
            researchInterests = self.researchBox4.text().split(",")
            researchInterests = [interest.strip() for interest in researchInterests if interest.strip()]

            # Import existing members from storage
            members = self.importMembers()

            # Create a new member entry
            newMember = {
                "name": self.nameTextBox4.text(),
                "position": self.roleBox4.currentText(),
                "image": os.path.join("img", "team", self.nameTextBox4.text().lower().replace(" ", "_") + fileFormat),
                "image_alt": os.path.join("img", "team", self.nameTextBox4.text().lower().replace(" ", "_") + "_alt" + fileFormat),
                "research": str(researchInterests),
                "info": self.infoTextBox4.text(),
                "about": self.aboutTextBox4.toPlainText()
            }

            # Add the new paper to the existing list
            members.append(newMember)

            # Export the updated list back to storage
            self.exportMembers(members)

            # Show a success message to the user
            QMessageBox.information(self, "Success", "Member added Successfully!")

            if self.infoTextBox4.text() != "":
                checkList.append(self.infoTextBox4)
                self.clearFields(checkList)
            else:
                self.clearFields(checkList)

            # Refresh Image Upload Button
            self.pictureUploadButton4.setText("Upload Image")

            # Refresh the member list after modification
            self.clearLayout(self.scrollableLayout6)
            self.addMembersFromDatabase(self.scrollableLayout6)

        else:
            # Show a warning message if any of the fields is empty
            QMessageBox.warning(self, "Warning", "One or more field is empty!")

    def modifyMemberClicked(self):
        #print("Modify Member Clicked")
        """
        Handles the event when the 'Modify member' button is clicked.
        
        - Checks if all required fields are filled.
        - Imports existing members from storage.
        - Creates a new member entry with user-provided details.
        - Appends the new member to the existing list.
        - Exports the updated member list back to storage.
        - Displays a success message.
        - Clears the input fields for a new entry.
        """
        
        # List of required input fields to be checked
        checkList = [
            self.nameTextBox5, 
            self.roleBox5,
            self.researchBox5, 
            self.aboutTextBox5,
            self.imageFilePath
        ]
        
        # Validate if all required fields are filled
        status = self.checkFields(checkList)

        if status:
            # Check if the name is already present
            if self.isNamePresent(self.nameTextBox5.text()):
                QMessageBox.warning(self, "Warning", "Member already exists!")
                return
            
            # Transfer the image to the website directory location
            fileFormat = os.path.splitext(self.imageFilePath)[1]
            shutil.copy(self.imageFilePath, os.path.join(os.getcwd(), "img", "team", self.nameTextBox5.text().lower().replace(" ", "_") + fileFormat))

            # Import existing members from storage
            members = self.importMembers()

            # Create a new member entry
            newMember = {
                "name": self.nameTextBox5.text(),
                "position": self.roleBox5.currentText(),
                "image": os.path.join("img", "team", self.nameTextBox4.text() + fileFormat),
                "research": self.researchBox5.currentData(),
                "info": self.infoTextBox5.text(),
                "about": self.aboutTextBox5.toPlainText()
            }

            # Add the new paper to the existing list
            members.append(newMember)

            # Export the updated list back to storage
            self.exportMembers(members)

            # Show a success message to the user
            QMessageBox.information(self, "Success", "Member added Successfully!")

            # Clear input fields for the next entry
            if self.infoTextBox5.text() != "":
                checkList.append(self.infoTextBox5)
                self.clearFields(checkList)
            else:
                self.clearFields(checkList)

            # Refresh Image Upload Button
            self.pictureUploadButton5.setText("Upload Image")

            # Refresh the member list after modification
            self.clearLayout(self.scrollableLayout6)
            self.addMembersFromDatabase(self.scrollableLayout6)

        else:
            # Show a warning message if any of the fields is empty
            QMessageBox.warning(self, "Warning", "One or more field is empty!")

    def deleteMemberClicked(self):
        #print("Delete Member Clicked")
        """
        Handles the event when the 'Delete Member' button is clicked.

        - Checks if the Member Name field is filled.
        - Displays a warning confirmation message.
        - If confirmed, imports existing members from storage.
        - Filters out the member with the matching ID.
        - Exports the updated member list back to storage.
        - Clears the input field after deletion.
        - Displays a warning if the Member Name is empty.
        """

        # List of required input fields to be checked
        checkList = [self.idTextBox6]

        # Validate if the Member ID field is filled
        status = self.checkFields(checkList)

        if status:
            # Check if the name is already present
            if not self.isNamePresent(self.idTextBox6.text()):
                QMessageBox.warning(self, "Warning", "Member does not exist! Check Spelling.")
                return

            # Display a warning confirmation before deletion
            QMessageBox.warning(self, "Warning", "Are you sure you want to delete the member?")

            # Import existing papers from storage
            members = self.importMembers()

            # Extract the image key from the member dictionary
            for member in members:
                if member["name"] == self.idTextBox6.text():
                    imagePath = member["image"]
                    break
            
            # Delete the image file from the directory
            if os.path.exists(imagePath):
                os.remove(imagePath)
            

            # Filter out the paper with the matching ID
            updatedMembers = [member for member in members if member["name"] != self.idTextBox6.text()]

            # Export the updated paper list back to storage
            self.exportMembers(updatedMembers)

            # Clear the Paper ID field after deletion
            self.clearFields(checkList)

            # Refresh the paper list after modification
            self.clearLayout(self.scrollableLayout6)
            self.addMembersFromDatabase(self.scrollableLayout6)
        else:
            # Show a warning message if Paper ID is empty
            QMessageBox.warning(self, "Warning", "Full Name is empty!")

    def addMembersFromDatabase(self, layout):
        # Adding sample content dynamically
        members = self.importMembers()
        
        for m in members:
            memberFrame = QFrame()
            memberFrame.setFrameShape(QFrame.Shape.Box)
            memberFrame.setLineWidth(1)
            memberFrame.setStyleSheet("""
                QFrame {
                    background-color: #F3EBEB;
                    padding: 0px;
                    margin-left: 5px;
                    margin-right: 5px;
                    margin-bottom: 1px;
                    margin-top: 0px;
                    color: black;
                    border-radius: 5px;
                }
            """)

            # Label for the ID
            memberNameinBox = QLabel(f"<b>Name</b>: {m['name']}")
            memberNameinBox.setAlignment(Qt.AlignmentFlag.AlignLeft)
            memberNameinBox.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)

            # Label for the Title
            memberPositioninBox = QLabel(f"<b>Position</b>: {m['position']}")
            memberPositioninBox.setAlignment(Qt.AlignmentFlag.AlignLeft)
            memberPositioninBox.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)

            # Label for the Authors
            memberResearchinBox = QLabel(f"<b>Research</b>: {m['research']}")
            memberResearchinBox.setAlignment(Qt.AlignmentFlag.AlignLeft)
            memberResearchinBox.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)

            # Label for the Conference
            memberAboutinBox = QLabel(f"<b>About</b>: {m['about']}")
            memberAboutinBox.setAlignment(Qt.AlignmentFlag.AlignLeft)
            memberAboutinBox.setWordWrap(True)
            memberAboutinBox.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)

            # Layout inside each rectangular box
            frameLayout = QVBoxLayout(memberFrame)
            frameLayout.setSpacing(0)
            frameLayout.setContentsMargins(1, 1, 1, 1)

            frameLayout.addWidget(memberNameinBox)
            frameLayout.addWidget(memberPositioninBox)
            frameLayout.addWidget(memberResearchinBox)
            frameLayout.addWidget(memberAboutinBox)

            # Add rectangle to scrollable layout
            layout.addWidget(memberFrame)
        return None
    
    def isNamePresent(self, name):
        """
        Checks if a given name is present in the list of members.

        Args:
            name (str): The name to check.

        Returns:
            bool: True if the name is present, False otherwise.
        """
        members = self.importMembers()
        for member in members:
            if member["name"] == name:
                return True
        return False
    
    def isPaperPresent(self, name):
        """
        Checks if a given paper ID is present in the list of papers.

        Args:
            name (str): The paper ID to check.

        Returns:
            bool: True if the paper ID is present, False otherwise.
        """
        papers = self.importPapers()
        for paper in papers:
            if paper["id"] == name:
                return True
        return False
    
    def addNewsClicked(self):
        """
        Handles the event when the 'Add News' button is clicked.
        
        - Checks if all required fields are filled.
        - Imports existing news from storage.
        - Creates a new news entry with user-provided details.
        - Appends the new news to the existing list.
        - Exports the updated news list back to storage.
        - Displays a success message.
        - Clears the input fields for a new entry.
        """
        
        #print("Add News Clicked")
        # List of required input fields to be checked
        checkList = [
            self.headerTextBox7, 
            self.contentsTextBox7
        ]
        
        # Validate if all required fields are filled
        status = self.checkFields(checkList)

        if status:
            # Import existing papers from storage
            news = self.importNews()

            # Create a new paper entry
            newNews = {
                "id": self.getPaperID(self.headerTextBox7.text(), self.dateEdit7.date().toString("dd-MM-yyyy")),
                "date": self.dateEdit7.date().toString("dd-MM-yyyy"),
                "header": self.headerTextBox7.text(),
                "body": self.contentsTextBox7.toPlainText(),
            }

            # Add the new paper to the existing list
            news.append(newNews)

            # Export the updated list back to storage
            self.exportNews(news)

            # Show a success message to the user
            QMessageBox.information(self, "Success", "News Added Successfully!")

            # Clear input fields for the next entry
            self.clearFields(checkList)

            # Refresh the paper list after modification
            self.clearLayout(self.scrollableLayout8)
            self.addNewsFromDatabase(self.scrollableLayout8)
            self.clearLayout(self.scrollableLayout9)
            self.addNewsFromDatabase(self.scrollableLayout9)

    def modifyNewsClicked(self):
        """
        Handles the event when the 'Modify News' button is clicked.
        
        - Checks if all required fields are filled.
        - Imports existing news from storage.
        - Creates a new news entry with user-provided details.
        - Appends the new news to the existing list.
        - Exports the updated news list back to storage.
        - Displays a success message.
        - Clears the input fields for a new entry.
        """
        
        #print("Modify News Clicked")

        # List of required input fields to be checked
        checkList = [
            self.idTextBox8,
            self.headerTextBox8, 
            self.contentsTextBox8
        ]
        
        # Validate if all required fields are filled
        status = self.checkFields(checkList)

        if status:
            # Check if the News ID field is present in the database
            if not self.isNewsPresent(self.idTextBox8.text()):
                QMessageBox.warning(self, "Warning", "News ID not found in the database!")
                return

            # Import existing papers from storage
            news = self.importNews()

            # Iterate over the paper list to find the matching ID
            for n in news:
                if n["id"] == self.idTextBox8.text():
                    # Update the paper details with new input values
                    n["date"] = self.dateEdit.date().toString("dd-MM-yyyy")
                    n["header"] = self.headerTextBox8.text()
                    n["body"] = self.contentsTextBox8.toPlainText()
                    break  # Exit loop after finding the paper

            # Export the updated paper list back to storage
            self.exportNews(news)

            # Show a success message to the user
            QMessageBox.information(self, "Success", "News Modified Successfully!")

            # Clear input fields for the next modification
            self.clearFields(checkList)

            # Refresh the paper list after modification
            self.clearLayout(self.scrollableLayout8)
            self.addNewsFromDatabase(self.scrollableLayout8)
            self.clearLayout(self.scrollableLayout9)
            self.addNewsFromDatabase(self.scrollableLayout9)

        else:
            # Show a warning message if any field is empty
            QMessageBox.warning(self, "Warning", "One or more fields are empty!")        

    def deleteNewsClicked(self):
        """
        Handles the event when the 'Delete News' button is clicked.

        - Checks if the News ID field is filled.
        - Displays a warning confirmation message.
        - If confirmed, imports existing news from storage.
        - Filters out the news with the matching ID.
        - Exports the updated news list back to storage.
        - Clears the input field after deletion.
        - Displays a warning if the News ID is empty.
        """

        # List of required input fields to be checked
        checkList = [self.idTextBox9]

        # Validate if the Paper ID field is filled
        status = self.checkFields(checkList)

        if status:
            # Check if the Paper ID field is present in the database
            if not self.isNewsPresent(self.idTextBox9.text()):
                QMessageBox.warning(self, "Warning", "News ID not found in the database!")
                return

            # Display a warning confirmation before deletion
            QMessageBox.warning(self, "Warning", "Are you sure you want to delete the news item?")
            
            # Import existing papers from storage
            news = self.importNews()

            # Filter out the paper with the matching ID
            updatedNews = [news for news in news if news["id"] != self.idTextBox9.text()]

            # Export the updated paper list back to storage
            self.exportNews(updatedNews)

            # Clear the Paper ID field after deletion
            self.clearFields(checkList)

            # Refresh the paper list after modification
            self.clearLayout(self.scrollableLayout8)
            self.addNewsFromDatabase(self.scrollableLayout8)
            self.clearLayout(self.scrollableLayout9)
            self.addNewsFromDatabase(self.scrollableLayout9)
        else:
            # Show a warning message if Paper ID is empty
            QMessageBox.warning(self, "Warning", "News ID is empty!")

    def importNews(self):
        """
        Imports news from a JSON file.

        - Reads the news data from the specified JSON file.
        - Prints the JSON data in a well-formatted manner for debugging.
        - Returns the list of news.

        Note: Ensure the file path is correctly set before deployment.
        """

        # Define the file path (Replace before deployment if necessary)
        file_path = os.path.join(self.getBasePath(), "data", "news.json")

        # Open and read the JSON file
        with open(file_path, "r") as file:
            news = json.load(file)  # Load the JSON content as a Python list

        # Print the JSON data in a readable format (for debugging purposes)
        #print(json.dumps(news, indent=4))

        # Return the loaded papers list
        return news
    
    def exportNews(self, news):
        """
        Exports the given list of news to a JSON file after sorting them in reverse chronological order.

        - Sorts the news list by date in descending order (latest news first).
        - Writes the sorted list back to the specified JSON file.

        Args:
            news (list): A list of dictionaries where each dictionary represents a news.

        Note: Ensure the file path is correctly set before deployment.
        """

        # Sort papers by date in descending order (latest papers first)
        news.sort(key=self.parseDate, reverse=True)

        # Define the file path (Replace before deployment if necessary)
        file_path = os.path.join(self.getBasePath(), "data", "news.json")

        # Open and write the sorted papers to the JSON file
        with open(file_path, "w") as file:
            json.dump(news, file, indent=4)

    def addNewsFromDatabase(self, layout):
        # Adding sample content dynamically
        news = self.importNews()
        
        for n in news:
            newsFrame = QFrame()
            newsFrame.setFrameShape(QFrame.Shape.Box)
            newsFrame.setLineWidth(1)
            newsFrame.setStyleSheet("""
                QFrame {
                    background-color: #F3EBEB;
                    padding: 0px;
                    margin-left: 5px;
                    margin-right: 5px;
                    margin-bottom: 1px;
                    margin-top: 0px;
                    color: black;
                    border-radius: 5px;
                }
            """)

            # Label for the ID
            newsIDinBox = QLabel(f"<b>ID</b>: {n['id']}")
            newsIDinBox.setAlignment(Qt.AlignmentFlag.AlignLeft)
            newsIDinBox.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)

            # Label for the Date
            newsDateinBox = QLabel(f"<b>Date</b>: {n['date']}")
            newsDateinBox.setAlignment(Qt.AlignmentFlag.AlignLeft)
            newsDateinBox.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)

            # Label for the Header
            newsHeaderinBox = QLabel(f"<b>Header</b>: {n['header']}")
            newsHeaderinBox.setAlignment(Qt.AlignmentFlag.AlignLeft)
            newsHeaderinBox.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)

            # Label for the Body
            newsBodyinBox = QLabel(f"<b>Body</b>: {n['body']}")
            newsBodyinBox.setAlignment(Qt.AlignmentFlag.AlignLeft)
            newsBodyinBox.setWordWrap(True)
            newsBodyinBox.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)

            # Layout inside each rectangular box
            frameLayout = QVBoxLayout(newsFrame)
            frameLayout.setSpacing(0)
            frameLayout.setContentsMargins(1, 1, 1, 1)

            frameLayout.addWidget(newsIDinBox)
            frameLayout.addWidget(newsDateinBox)
            frameLayout.addWidget(newsHeaderinBox)
            frameLayout.addWidget(newsBodyinBox)

            # Add rectangle to scrollable layout
            layout.addWidget(newsFrame)
        return None
    
    def isNewsPresent(self, name):
        """
        Checks if a given News ID is present in the list of news.

        Args:
            name (str): The news ID to check.

        Returns:
            bool: True if the news ID is present, False otherwise.
        """
        news = self.importNews()
        for n in news:
            if n["id"] == name:
                return True
        return False
    
    def getBasePath(self):
        """
        Returns the base path of the application.

        This method checks if the application is running as a bundled executable
        or from a script and returns the appropriate base path.
        """
        #print("getBasePath", os.path.dirname(sys.executable))
        if getattr(sys, 'frozen', False):
            # If running as bundled exe
            return os.path.dirname(sys.executable)
        else:
            # If running from script
            return os.path.dirname(os.path.abspath(__file__))

    
app = QApplication(sys.argv)
app.setFont(QFont("Montserrat"))
window = MainWindow()
window.show()
sys.exit(app.exec())