from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QTabWidget,
    QTableWidget,
    QTableWidgetItem,
    QPushButton,
)
from PySide6.QtCore import Qt


class SplitPreviewDialog(QDialog):

    def __init__(self, sheets, parent=None):
        super().__init__(parent)

        self.sheets = sheets

        self.setWindowTitle("Split Preview")
        self.resize(900, 600)

        layout = QVBoxLayout()

        self.tabs = QTabWidget()

        for sheet_name, data in sheets.items():

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
                str(sheet_name)
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