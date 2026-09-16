from PySide6.QtWidgets import(
    QDialog,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
)



class SearchDialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Search")
        self.resize(350, 180)

        layout = QVBoxLayout()

        self.label = QLabel("Enter Search term:")

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search...")

        self.confirm_button = QPushButton("Search")
        self.confirm_button.clicked.connect(self.confirm)

        layout.addWidget(self.label)
        layout.addWidget(self.search_input)
        layout.addWidget(self.confirm_button)

        self.setLayout(layout)

    def confirm(self):
        self.search_term = self.search_input.text()
        self.accept()