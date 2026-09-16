from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QPushButton,
)


class OrganizeDialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Organize")
        self.resize(300, 180)

        layout = QVBoxLayout()

        self.sort_button = QPushButton("Sort")
        self.filter_button = QPushButton("Filter")

        self.sort_button.clicked.connect(self.open_sort)
        self.filter_button.clicked.connect(self.open_filter)

        layout.addWidget(self.sort_button)
        layout.addWidget(self.filter_button)

        self.setLayout(layout)

    def open_sort(self):
        self.selected_action = "sort"
        self.accept()

    def open_filter(self):
        self.selected_action = "filter"
        self.accept()