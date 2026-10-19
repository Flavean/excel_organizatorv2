from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QPushButton,
)


class AnalyzeDialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Analyze")
        self.resize(350, 250)

        layout = QVBoxLayout()

        self.search_button = QPushButton("Search")
        self.statistics_button = QPushButton("Statistics / Summary")
        self.missing_button = QPushButton("Missing Data")

        layout.addWidget(self.search_button)
        layout.addWidget(self.statistics_button)
        layout.addWidget(self.missing_button)

        self.search_button.clicked.connect(self.search)
        self.statistics_button.clicked.connect(self.statistics)
        self.missing_button.clicked.connect(self.missing)

        self.setLayout(layout)

    def search(self):
        self.selected_action = "search"
        self.accept()

    def statistics(self):
        self.selected_action = "statistics"
        self.accept()

    def missing(self):
        self.selected_action = "missing"
        self.accept()