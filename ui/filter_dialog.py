from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QComboBox,
    QLineEdit,
    QPushButton,
)


class FilterDialog(QDialog):

    def __init__(self, columns, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Filter")
        self.resize(350, 220)

        layout = QVBoxLayout()

        self.column_label = QLabel("Select column:")
        self.column_combo = QComboBox()
        self.column_combo.addItems(columns)

        self.value_label = QLabel("Enter value:")
        self.value_input = QLineEdit()
        self.value_input.setPlaceholderText("Value...")

        self.confirm_button = QPushButton("Filter")
        self.confirm_button.clicked.connect(self.confirm)

        layout.addWidget(self.column_label)
        layout.addWidget(self.column_combo)
        layout.addWidget(self.value_label)
        layout.addWidget(self.value_input)
        layout.addWidget(self.confirm_button)

        self.setLayout(layout)

    def confirm(self):
        self.selected_column = self.column_combo.currentText()
        self.selected_value = self.value_input.text()

        self.accept()