from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QPushButton,
)


class ExportDialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Export")
        self.resize(350, 300)

        layout = QVBoxLayout()

        self.excel_button = QPushButton("Excel (.xlsx)")
        self.csv_button = QPushButton("CSV (.csv)")
        self.json_button = QPushButton("JSON (.json)")
        self.html_button = QPushButton("HTML (.html)")
        self.pdf_button = QPushButton("PDF (.pdf)")

        layout.addWidget(self.excel_button)
        layout.addWidget(self.csv_button)
        layout.addWidget(self.json_button)
        layout.addWidget(self.html_button)
        layout.addWidget(self.pdf_button)

        self.excel_button.clicked.connect(
            lambda: self.select_format("xlsx")
        )

        self.csv_button.clicked.connect(
            lambda: self.select_format("csv")
        )

        self.json_button.clicked.connect(
            lambda: self.select_format("json")
        )

        self.html_button.clicked.connect(
            lambda: self.select_format("html")
        )

        self.pdf_button.clicked.connect(
            lambda: self.select_format("pdf")
        )

        self.setLayout(layout)

    def select_format(self, file_format):
        self.selected_format = file_format
        self.accept()