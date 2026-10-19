from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QTabWidget,
    QTableWidget,
    QTableWidgetItem,
    QPushButton,
)
from PySide6.QtCore import Qt


class IncompletePreviewDialog(QDialog):

    def __init__(self, complete, incomplete, parent=None):
        super().__init__(parent)

        self.complete = complete
        self.incomplete = incomplete

        self.setWindowTitle("Incomplete Rows Preview")
        self.resize(900, 600)

        layout = QVBoxLayout()

        self.tabs = QTabWidget()

        self.add_table(
            "Complete",
            self.complete
        )

        self.add_table(
            "Incomplete",
            self.incomplete
        )

        self.apply_button = QPushButton(
            "Apply"
        )

        self.cancel_button = QPushButton(
            "Cancel"
        )

        self.apply_button.clicked.connect(
            self.accept
        )

        self.cancel_button.clicked.connect(
            self.reject
        )

        layout.addWidget(self.tabs)
        layout.addWidget(self.apply_button)
        layout.addWidget(self.cancel_button)

        self.setLayout(layout)

    def add_table(self, name, data):

        table = QTableWidget()

        table.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAsNeeded
        )

        table.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAsNeeded
        )

        preview_data = data.head(20)

        table.setRowCount(
            preview_data.shape[0]
        )

        table.setColumnCount(
            preview_data.shape[1]
        )

        table.setHorizontalHeaderLabels(
            preview_data.columns.astype(str).tolist()
        )

        for row in range(
            preview_data.shape[0]
        ):
            for column in range(
                preview_data.shape[1]
            ):

                value = preview_data.iloc[
                    row,
                    column
                ]

                table.setItem(
                    row,
                    column,
                    QTableWidgetItem(
                        str(value)
                    )
                )

        self.tabs.addTab(
            table,
            name
        )