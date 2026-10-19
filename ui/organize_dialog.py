from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QPushButton,
)


class OrganizeDialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Organize")
        self.resize(350, 350)

        layout = QVBoxLayout()

        self.sort_button = QPushButton("Sort")
        self.filter_button = QPushButton("Filter")
        self.merge_button = QPushButton("Merge Files")
        self.split_button = QPushButton("Split Into Sheets")
        self.incomplete_button = QPushButton(
            "Separate Incomplete Rows"
        )

        layout.addWidget(self.sort_button)
        layout.addWidget(self.filter_button)
        layout.addWidget(self.merge_button)
        layout.addWidget(self.split_button)
        layout.addWidget(self.incomplete_button)

        self.sort_button.clicked.connect(self.sort)
        self.filter_button.clicked.connect(self.filter)
        self.merge_button.clicked.connect(self.merge)
        self.split_button.clicked.connect(self.split)
        self.incomplete_button.clicked.connect(self.incomplete)

        self.setLayout(layout)

    def sort(self):
        self.selected_action = "sort"
        self.accept()

    def filter(self):
        self.selected_action = "filter"
        self.accept()

    def merge(self):
        self.selected_action = "merge"
        self.accept()

    def split(self):
        self.selected_action = "split"
        self.accept()

    def incomplete(self):
        self.selected_action = "incomplete"
        self.accept()