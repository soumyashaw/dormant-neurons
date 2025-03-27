import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QScrollArea, QVBoxLayout, QLabel, QFrame
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

class ScrollRectangles(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Scrollable Numbers in Rectangles")
        self.resize(400, 300)

        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)

        # Create Scroll Area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)

        # Widget to hold content
        content_widget = QWidget()
        scroll_area.setWidget(content_widget)

        # Layout for content
        content_layout = QVBoxLayout(content_widget)
        content_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Add rectangles with numbers
        for i in range(1, 21):
            number_frame = QFrame()
            number_frame.setFrameShape(QFrame.Shape.Box)
            number_frame.setLineWidth(1)
            number_frame.setStyleSheet("""
                QFrame {
                    background-color: #F0F8FF;
                    border-radius: 8px;
                    padding: 10px;
                }
            """)

            # Label for the number
            number_label = QLabel(f"Number {i}")
            number_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            number_label.setFont(QFont("Arial", 12, weight=QFont.Weight.Bold))

            # Layout inside each rectangle
            frame_layout = QVBoxLayout(number_frame)
            frame_layout.addWidget(number_label)

            # Add rectangle to scrollable layout
            content_layout.addWidget(number_frame)

        layout.addWidget(scroll_area)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ScrollRectangles()
    window.show()
    sys.exit(app.exec())