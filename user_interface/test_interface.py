import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QScrollArea, QLabel, QLineEdit, QPushButton

class ScrollableForm(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("QScrollArea Example")
        self.setGeometry(100, 100, 400, 300)

        # Create a scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)  # Allows dynamic resizing

        # Create a widget to hold the content
        contentWidget = QWidget()
        contentLayout = QVBoxLayout(contentWidget)

        # Add multiple widgets (simulating a long form)
        for i in range(1, 21):  # Adding 20 input fields
            label = QLabel(f"Field {i}:")
            inputField = QLineEdit()
            contentLayout.addWidget(label)
            contentLayout.addWidget(inputField)

        # Add submit button
        submitButton = QPushButton("Submit")
        contentLayout.addWidget(submitButton)

        # Set content widget inside scroll area
        scroll.setWidget(contentWidget)

        # Main layout
        mainLayout = QVBoxLayout(self)
        mainLayout.addWidget(scroll)

app = QApplication(sys.argv)
window = ScrollableForm()
window.show()
sys.exit(app.exec())