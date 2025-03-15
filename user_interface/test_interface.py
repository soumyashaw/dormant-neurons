from PyQt6.QtWidgets import QApplication, QComboBox, QListWidget, QListWidgetItem, QVBoxLayout, QWidget
from PyQt6.QtCore import Qt
import sys

class MultiSelectComboBox(QComboBox):
    def __init__(self):
        super().__init__()
        self.setEditable(True)  # Allow text display
        self.lineEdit().setReadOnly(True)  # Prevent manual input
        self.listWidget = QListWidget()

        # Add options
        for item in ["Option 1", "Option 2", "Option 3"]:
            listItem = QListWidgetItem(item)
            listItem.setCheckState(Qt.CheckState.Unchecked) # Initially unchecked
            self.listWidget.addItem(listItem)

        self.setModel(self.listWidget.model())
        self.setView(self.listWidget)

        # Update text when selection changes
        self.listWidget.itemChanged.connect(self.updateText)

    def updateText(self):
        selectedItems = [self.listWidget.item(i).text() for i in range(self.listWidget.count())
                         if self.listWidget.item(i).checkState()]
        self.setEditText(", ".join(selectedItems))

# Run Application
app = QApplication(sys.argv)
window = QWidget()
layout = QVBoxLayout()
comboBox = MultiSelectComboBox()
layout.addWidget(comboBox)
window.setLayout(layout)
window.show()
sys.exit(app.exec())