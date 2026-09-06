from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QTableWidget,
    QTableWidgetItem,
    QPushButton,
)
from PySide6.QtCore import Qt


class PreviewDialog(QDialog):

    def __init__(self, data, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Preview")
        self.resize(900, 600)
        self.data = data
        layout = QVBoxLayout()
        self.table = QTableWidget()
        self.table.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.apply_button = QPushButton("Apply")
        self.cancel_button = QPushButton("Cancel")
        self.apply_button.clicked.connect(self.apply_changes)
        self.cancel_button.clicked.connect(self.reject)


        layout.addWidget(self.table)
        layout.addWidget(self.apply_button)
        layout.addWidget(self.cancel_button)


        self.setLayout(layout)


        self.show_data()

    def show_data(self):

        print("Preview rows:", self.data.shape[0])
        print("Preview columns:", self.data.shape[1])

        self.table.setRowCount(self.data.shape[0])
        self.table.setColumnCount(self.data.shape[1])

        self.table.setHorizontalHeaderLabels(
            self.data.columns.astype(str).tolist()
        )

        for row in range(self.data.shape[0]):
            for column in range(self.data.shape[1]):
                value = self.data.iloc[row, column]

                self.table.setItem(
                    row,
                    column, 
                    QTableWidgetItem(str(value))
                )
    def apply_changes(self):
        self.accept()