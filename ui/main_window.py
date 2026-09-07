from PySide6.QtWidgets import (
    QMainWindow,
    QPushButton,
    QFileDialog,
    QTableWidget,
    QTableWidgetItem,
)

from core.excel_handler import load_excel
from core.cleaner import clean_data
from ui.clear_dialog import CleanDialog
from ui.preview_dialog import PreviewDialog
from ui.sort_dialog import SortDialog


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Excel Organizer V2")
        self.resize(900, 600)

        self.open_button = QPushButton("Open Excel", self)
        self.open_button.setGeometry(350, 450, 200, 50)
        self.clear_button = QPushButton("Clean", self)
        self.clear_button.setGeometry(350, 510, 200, 50)
        self.sort_button = QPushButton("Sort", self)
        self.sort_button.setGeometry(350, 570, 200, 50)
        self.clear_button.clicked.connect(self.open_clean_dialog)
        self.sort_button.clicked.connect(self.open_clean_dialog)
        self.table = QTableWidget(self)
        self.table.setGeometry(50, 50, 800,350)


        self.open_button.clicked.connect(self.open_excel)

    def open_excel(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Excel File",
            "",
            "Excel File (*.xlsx *.xls)"
        )

        if file_path:
            self.data = load_excel(file_path)

            self.table.setRowCount(self.data.shape[0])
            self.table.setColumnCount(self.data.shape[1])

            self.table.setHorizontalHeaderLabels(self.data.columns.astype(str).tolist())

        for row in range(self.data.shape[0]):
            for column in range(self.data.shape[1]):
                value = self.data.iloc[row, column]
                self.table.setItem(
                    row,
                    column,
                    QTableWidgetItem(str(value))
                )
    def open_clean_dialog(self):
        dialog = CleanDialog(self)

        if dialog.exec():
            selected_options = dialog.selected_options

            preview_data = clean_data(self.data.copy(), selected_options)

            preview_dialog = PreviewDialog(preview_data, self)

            if preview_dialog.exec():
                self.data = preview_data
                self.update_table()

    def update_table(self):
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

    def open_sort_dialog(self):
        dialog = SortDialog(
            self.data.columns.astype(str).tolist(),
            self
        )

        if dialog.exec():
            selected_column = dialog.selected_column
            ascending = dialog.ascending

            from core.sorter import sort_data

            sorted_data = sort_data(
                self.data.copy(),
                selected_column,
                ascending
            ) 

            preview_dialog = PreviewDialog(sorted_data, self)

            if preview_dialog.exec():
                self.data = sorted_data
                self.update_table()


