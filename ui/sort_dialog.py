from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QComboBox,
    QPushButton,
)


class SortDialog(QDialog):

    def __init__(self, columns, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Sort Data")
        self.resize(350, 250)

        layout = QVBoxLayout()

        self.column_label = QLabel("Select column:")
        self.column_combo = QComboBox()
        self.column_combo.addItems(columns)

        self.order_label = QLabel("Sort order:")
        self.order_combo = QComboBox()
        self.order_combo.addItems([
            "Ascending",
            "Descending"
        ])

        self.confirm_button = QPushButton("Confirm")
        self.confirm_button.clicked.connect(self.confirm)

        layout.addWidget(self.column_label)
        layout.addWidget(self.column_combo)

        layout.addWidget(self.order_label)
        layout.addWidget(self.order_combo)

        layout.addWidget(self.confirm_button)

        self.setLayout(layout)

    def confirm(self):
        self.selected_column = self.column_combo.currentText()
        self.ascending = self.order_combo.currentText() == "Ascending"

        self.accept()