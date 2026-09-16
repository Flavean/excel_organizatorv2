from PySide6.QtWidgets import (
    QMainWindow,
    QPushButton,
    QFileDialog,
    QTableWidget,
    QTableWidgetItem,
    QWidget, 
    QVBoxLayout,
)

from core.excel_handler import load_excel, save_excel, save_pdf
from core.cleaner import clean_data
from ui.clear_dialog import CleanDialog
from ui.preview_dialog import PreviewDialog
from ui.sort_dialog import SortDialog
from ui.search_dialog import SearchDialog
from ui.filter_dialog import FilterDialog
from ui.organize_dialog import OrganizeDialog
from ui.delete_dialog import DeleteDialog
from core.searcher import search_data
from core.filter import filter_data
from PySide6.QtCore import Qt


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.original_data = None
        self.data = None

        self.setWindowTitle("Excel Organizer V2")
        self.resize(900, 700)

        self.open_button = QPushButton("Open Excel")
        self.clear_button = QPushButton("Clean")
        self.organize_button = QPushButton("Organizer")
        self.search_button = QPushButton("Search")
        self.save_button = QPushButton("Save As")
        self.reset_button = QPushButton("Reset")
        self.delete_button = QPushButton("Delete")

        self.clear_button.clicked.connect(self.open_clean_dialog)
        self.organize_button.clicked.connect(self.open_organize_dialog)
        self.search_button.clicked.connect(self.open_search_dialog)
        self.save_button.clicked.connect(self.save_as_excel)
        self.open_button.clicked.connect(self.open_excel)
        self.delete_button.clicked.connect(self.open_delete_dialog)
        self.reset_button.clicked.connect(self.reset_data)

        self.table = QTableWidget()
        
        self.table.setSelectionBehavior(
            QTableWidget.SelectionBehavior.SelectRows
        )

        self.table.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAsNeeded
        )

        self.table.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAsNeeded
        )

        central_widget = QWidget()
        layout = QVBoxLayout()

        layout.addWidget(self.table)

        layout.addWidget(self.open_button)
        layout.addWidget(self.clear_button)
        layout.addWidget(self.organize_button)
        layout.addWidget(self.search_button)
        layout.addWidget(self.delete_button)
        layout.addWidget(self.reset_button)
        layout.addWidget(self.save_button)

        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
        


    def open_excel(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Excel File",
            "",
            "Excel File (*.xlsx *.xls)"
        )

        if file_path:
            self.data = load_excel(file_path)
            self.original_data = self.data.copy()

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

    def open_search_dialog(self):
        dialog = SearchDialog(self)

        if dialog.exec():
            search_term = dialog.search_term

            search_results = search_data(
                self.data.copy(),
                search_term
            )

            preview_dialog = PreviewDialog(search_results, self)

            if preview_dialog.exec():
                self.data = search_results
                self.update_table()

    def save_as_excel(self):
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Excel File",
            "",
            "Excel Files (*.xlsx);;CSV File (*.csv);;JSON Files(*.json);;HTML File (*.html);;PDF File (*.pdf)"
        )

        if file_path:
            if file_path.endswith(".pdf"):
                save_pdf(self.data, file_path)
            else:
                save_excel(self.data, file_path)

    def reset_data(self):
        if self.original_data is not None:
            self.data = self.original_data.copy()
            self.update_table()

    def open_filter_dialog(self):
        dialog = FilterDialog(
            self.data.columns.astype(str).tolist(),
            self
        )

        if dialog.exec():
            selected_column = dialog.selected_column
            selected_value = dialog.selected_value

            filtered_data = filter_data(
                self.data.copy(),
                selected_column,
                selected_value
            )

            preview_dialog = PreviewDialog(filtered_data, self)

            if preview_dialog.exec():
                self.data = filtered_data
                self.update_table()

    def open_delete_dialog(self):
        dialog = DeleteDialog(
        self.data.columns.astype(str).tolist(),
        self
        )

        if dialog.exec():
            if dialog.selected_action == "rows":
                self.delete_selected_rows()

            elif dialog.selected_action == "columns":
                self.delete_selected_columns(dialog.selected_columns)

    def open_organize_dialog(self):
        dialog = OrganizeDialog(self)

        if dialog.exec():
            if dialog.selected_action == "sort":
                self.open_sort_dialog()

            elif dialog.selected_action == "filter":
                self.open_filter_dialog()


    def delete_selected_rows(self):
        selected_rows = set()

        for item in self.table.selectedItems():
            selected_rows.add(item.row())

        if selected_rows:
            self.data = self.data.drop(
                self.data.index[list(selected_rows)]
            ).reset_index(drop=True)

            self.update_table()

    def delete_selected_columns(self, columns):
        from core.cleaner import delete_columns

        self.data = delete_columns(
            self.data,
            columns
        )

        self.update_table()