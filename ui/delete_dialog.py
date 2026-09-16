from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QPushButton,
    QListWidget,
    QListWidgetItem,
)


class DeleteDialog(QDialog):

    def __init__(self, columns=None, parent=None):
        super().__init__(parent)

        self.columns = columns or []
        self.column_list = QListWidget()
        self.column_list.addItems(self.columns)
        self.column_list.setSelectionMode(
        QListWidget.SelectionMode.MultiSelection
        )

        self.setWindowTitle("Delete")
        self.resize(300, 180)

        layout = QVBoxLayout()

        self.rows_button = QPushButton("Delete Rows")
        self.columns_button = QPushButton("Delete Columns")

        self.rows_button.clicked.connect(self.delete_rows)
        self.columns_button.clicked.connect(self.delete_columns)

        layout.addWidget(self.column_list)
        layout.addWidget(self.rows_button)
        layout.addWidget(self.columns_button)


        self.setLayout(layout)

    def delete_rows(self):
        self.selected_action = "rows"
        self.accept()

    def delete_columns(self):
        self.selected_columns = [
            item.text()
            for item in self.column_list.selectedItems()
        ]

        if self.selected_columns:
            self.selected_action = "columns"
            self.accept()