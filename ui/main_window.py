import pandas as pd

from PySide6.QtWidgets import (
    QMainWindow,
    QPushButton,
    QFileDialog,
    QTableWidget,
    QTableWidgetItem,
    QWidget,
    QVBoxLayout,
    QMessageBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QStyle,
)
from PySide6.QtCore import Qt

from core.excel_handler import (
    load_excel,
    save_excel,
    save_pdf,
)

from core.cleaner import (
    clean_data,
    delete_columns,
)

from core.sorter import sort_data
from core.searcher import search_data
from core.filter import filter_data
from core.merger import merge_files as merge_excel_files
from core.splitter import split_into_sheets
from core.incomplete import separate_incomplete_rows

from ui.preview_dialog import PreviewDialog
from ui.edit_dialog import EditDialog
from ui.organize_dialog import OrganizeDialog
from ui.analyze_dialog import AnalyzeDialog
from ui.export_dialog import ExportDialog
from ui.split_preview_dialog import SplitPreviewDialog
from ui.incomplete_preview_dialog import IncompletePreviewDialog


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Excel Organizer 2.0.0")
        self.setMinimumSize(900, 600)

        self.original_data = None
        self.data = None

        # History
        self.undo_stack = []
        self.redo_stack = []

        # Main buttons
        self.open_button = QPushButton("Open Excel")

        self.open_button.setIcon(
            self.style().standardIcon(
                QStyle.StandardPixmap.SP_DialogOpenButton
            )
        )

        self.open_button.setMinimumHeight(45)

        self.open_button.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 15px;
                font-weight: bold;
                padding: 8px 14px;
            }

            QPushButton:hover {
                background-color: #42A5F5;
            }

            QPushButton:pressed {
                background-color: #1976D2;
            }
        """)

        self.clean_button = QPushButton("Clean")

        self.clean_button.setIcon(
            self.style().standardIcon(
                QStyle.StandardPixmap.SP_TrashIcon
            )
        )

        self.clean_button.setMinimumHeight(45)

        self.clean_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 15px;
                font-weight: bold;
                padding: 8px 14px;
            }

            QPushButton:hover {
                background-color: #66BB6A;
            }

            QPushButton:pressed {
                background-color: #388E3C;
            }
        """)

        self.edit_button = QPushButton("Edit")

        self.edit_button.setIcon(
            self.style().standardIcon(
                QStyle.StandardPixmap.SP_FileDialogDetailedView
            )
        )

        self.edit_button.setMinimumHeight(45)

        self.edit_button.setStyleSheet("""
            QPushButton {
                background-color: #FF9800;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 15px;
                font-weight: bold;
                padding: 8px 14px;
            }

            QPushButton:hover {
                background-color: #FFB74D;
            }

            QPushButton:pressed {
                background-color: #F57C00;
            }
        """)

        self.organize_button = QPushButton("Organize")

        self.organize_button.setIcon(
            self.style().standardIcon(
                QStyle.StandardPixmap.SP_FileDialogListView
            )
        )

        self.organize_button.setMinimumHeight(45)

        self.organize_button.setStyleSheet("""
            QPushButton {
                background-color: #9C27B0;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 15px;
                font-weight: bold;
                padding: 8px 14px;
            }

            QPushButton:hover {
                background-color: #AB47BC;
            }

            QPushButton:pressed {
                background-color: #7B1FA2;
            }
        """)

        self.analyze_button = QPushButton("Analyze")

        self.analyze_button.setIcon(
            self.style().standardIcon(
                QStyle.StandardPixmap.SP_FileDialogInfoView
            )
        )

        self.analyze_button.setMinimumHeight(45)

        self.analyze_button.setStyleSheet("""
            QPushButton {
                background-color: #00ACC1;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 15px;
                font-weight: bold;
                padding: 8px 14px;
            }

            QPushButton:hover {
                background-color: #26C6DA;
            }

            QPushButton:pressed {
                background-color: #00838F;
            }
        """)

        self.export_button = QPushButton("Export")

        self.export_button.setIcon(
            self.style().standardIcon(
                QStyle.StandardPixmap.SP_DialogSaveButton
            )
        )

        self.export_button.setMinimumHeight(45)

        self.export_button.setStyleSheet("""
            QPushButton {
                background-color: #607D8B;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 15px;
                font-weight: bold;
                padding: 8px 14px;
            }

            QPushButton:hover {
                background-color: #78909C;
            }

            QPushButton:pressed {
                background-color: #455A64;
            }
        """)
        
        self.reset_button = QPushButton("Reset")

        self.reset_button.setIcon(
            self.style().standardIcon(
                QStyle.StandardPixmap.SP_BrowserReload
            )
        )

        self.reset_button.setMinimumHeight(45)

        self.reset_button.setStyleSheet("""
            QPushButton {
                background-color: #E53935;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 15px;
                font-weight: bold;
                padding: 8px 14px;
            }

            QPushButton:hover {
                background-color: #EF5350;
            }

            QPushButton:pressed {
                background-color: #C62828;
            }
        """)

        # Connections
        self.open_button.clicked.connect(
            self.open_excel
        )

        self.clean_button.clicked.connect(
            self.open_clean
        )

        self.edit_button.clicked.connect(
            self.open_edit_dialog
        )

        self.organize_button.clicked.connect(
            self.open_organize_dialog
        )

        self.analyze_button.clicked.connect(
            self.open_analyze_dialog
        )

        self.export_button.clicked.connect(
            self.open_export_dialog
        )

        self.reset_button.clicked.connect(
            self.reset_data
        )

        # Table
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

        # Main layout
        central_widget = QWidget()
        main_layout = QHBoxLayout()

        # Sidebar
        sidebar = QFrame()
        sidebar.setFixedWidth(220)

        sidebar_layout = QVBoxLayout()

        sidebar_title = QLabel("Excel Organizer")
        sidebar_title.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        sidebar_layout.addWidget(sidebar_title)

        
        sidebar_layout.addWidget(self.clean_button)
        sidebar_layout.addWidget(self.edit_button)
        sidebar_layout.addWidget(self.organize_button)
        sidebar_layout.addWidget(self.analyze_button)
        sidebar_layout.addWidget(self.export_button)

        sidebar_layout.addStretch()

        sidebar_layout.addWidget(self.reset_button)

        sidebar.setLayout(sidebar_layout)

        # Main content
        content = QWidget()
        content_layout = QVBoxLayout()

        # Excel drop zone
        drop_zone = QFrame()
        

        drop_zone.setStyleSheet("""
            QFrame {
                background-color: #20252B;
                border: 1px solid #3A414A;
                border-radius: 15px;
            }
        """)

        drop_layout = QVBoxLayout()

        drop_title = QLabel("Open an Excel file")
        drop_title.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        drop_title.setStyleSheet("""
            QLabel {
                font-size: 24px;
                font-weight: bold;
                color: #FFFFFF;
                border: none;
                backround: transparent;
            }
        """)

        drop_text = QLabel(
        "Drag & drop an Excel file here\n"
        "or click the button below"
        )

        drop_text.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        drop_text.setStyleSheet("""
            QLabel {
                font-size: 15px;
                color: #607D8B;
                border: none;
                backround; transparent;
            }
        """)

        drop_layout.addStretch()
        drop_layout.addWidget(drop_title)
        drop_layout.addWidget(drop_text)

        drop_layout.addWidget(
        self.open_button,
        alignment=Qt.AlignmentFlag.AlignCenter
        )

        drop_layout.addStretch()

        drop_zone.setLayout(drop_layout)

        content_layout.addWidget(drop_zone, 1)
        content_layout.addWidget(self.table, 3)

        content.setLayout(content_layout)

        # Combine
        main_layout.addWidget(sidebar)
        main_layout.addWidget(content)

        central_widget.setLayout(main_layout)

        self.setCentralWidget(central_widget)

    # --------------------------------------------------
    # DATA
    # --------------------------------------------------

    def load_excel_file(self, file_path):

        try:
            self.data = load_excel(file_path)
            self.original_data = self.data.copy()

            self.undo_stack.clear()
            self.redo_stack.clear()

            self.update_table()

        except Exception as error:
            QMessageBox.critical(
                self,
                "Error",
                f"Could not open the file:\n\n{error}"
            )

    def dragEnterEvent(self, event):

        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):

        urls = event.mimeData().urls()

        if not urls:
            return

        file_path = urls[0].toLocalFile()

        if file_path.lower().endswith((".xlsx", ".xls")):
            self.load_excel_file(file_path)

        event.acceptProposedAction()
    
    def open_excel(self):

        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Excel File",
            "",
            "Excel Files (*.xlsx *.xls)"
        )

        if not file_path:
            return

        self.load_excel_file(file_path)

    def update_table(self):

        if self.data is None:
            self.table.clear()
            self.table.setRowCount(0)
            self.table.setColumnCount(0)
            return

        self.table.clear()

        self.table.setRowCount(
            self.data.shape[0]
        )

        self.table.setColumnCount(
            self.data.shape[1]
        )

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

    def require_data(self):

        if self.data is None:

            QMessageBox.information(
                self,
                "No Data",
                "Please open an Excel file first."
            )

            return False

        return True

    # --------------------------------------------------
    # HISTORY
    # --------------------------------------------------

    def save_history(self):

        if self.data is not None:

            self.undo_stack.append(
                self.data.copy()
            )

            self.redo_stack.clear()

    def undo(self):

        if not self.undo_stack:
            return

        self.redo_stack.append(
            self.data.copy()
        )

        self.data = self.undo_stack.pop()

        self.update_table()

    def redo(self):

        if not self.redo_stack:
            return

        self.undo_stack.append(
            self.data.copy()
        )

        self.data = self.redo_stack.pop()

        self.update_table()

    # --------------------------------------------------
    # CLEAN
    # --------------------------------------------------

    def open_clean(self):

        if not self.require_data():
            return

        from PySide6.QtWidgets import (
            QDialog,
            QVBoxLayout,
            QCheckBox,
            QPushButton,
            QSpinBox,
            QLabel,
        )

        dialog = QDialog(self)

        dialog.setWindowTitle("Clean Options")
        dialog.resize(350, 350)

        layout = QVBoxLayout()

        remove_empty_rows = QCheckBox(
            "Remove empty rows"
        )

        remove_empty_columns = QCheckBox(
            "Remove empty columns"
        )

        remove_duplicates = QCheckBox(
            "Remove duplicate rows"
        )

        clean_spaces = QCheckBox(
            "Clean extra spaces"
        )

        remove_sparse_columns = QCheckBox(
            "Remove columns with too many empty cells"
        )

        threshold_label = QLabel(
            "Empty cell threshold (%)"
        )

        threshold = QSpinBox()

        threshold.setRange(1, 100)
        threshold.setValue(80)
        threshold.setSuffix("%")
        threshold.setEnabled(False)

        remove_sparse_columns.stateChanged.connect(
            lambda state: (
                threshold.setEnabled(state == 2),
                threshold_label.setEnabled(state == 2)
            )
        )

        confirm_button = QPushButton("Preview")

        layout.addWidget(remove_empty_rows)
        layout.addWidget(remove_empty_columns)
        layout.addWidget(remove_duplicates)
        layout.addWidget(clean_spaces)
        layout.addWidget(remove_sparse_columns)
        layout.addWidget(threshold_label)
        layout.addWidget(threshold)
        layout.addWidget(confirm_button)

        dialog.setLayout(layout)

        def confirm():

            options = {
                "remove_empty_rows":
                    remove_empty_rows.isChecked(),

                "remove_empty_columns":
                    remove_empty_columns.isChecked(),

                "remove_duplicates":
                    remove_duplicates.isChecked(),

                "clean_spaces":
                    clean_spaces.isChecked(),

                "remove_sparse_columns":
                    remove_sparse_columns.isChecked(),

                "threshold":
                    threshold.value() / 100,
            }

            preview_data = clean_data(
                self.data.copy(),
                options
            )

            preview = PreviewDialog(
                preview_data,
                self
            )

            if preview.exec():

                self.save_history()

                self.data = preview_data

                self.update_table()

            dialog.accept()

        confirm_button.clicked.connect(confirm)

        dialog.exec()

    # --------------------------------------------------
    # EDIT
    # --------------------------------------------------

    def open_edit_dialog(self):

        if not self.require_data():
            return

        dialog = EditDialog(
            self.data.columns.astype(str).tolist(),
            self
        )

        if not dialog.exec():
            return

        action = dialog.selected_action

        if action == "clean":

            self.open_clean()

        elif action == "delete":

            self.delete_data()

        elif action == "undo":

            self.undo()

        elif action == "redo":

            self.redo()

    def delete_data(self):

        selected_rows = sorted(
            {
                item.row()
                for item in self.table.selectedItems()
            }
        )

        if selected_rows:

            self.save_history()

            self.data = (
                self.data.drop(
                    self.data.index[selected_rows]
                )
                .reset_index(drop=True)
            )

            self.update_table()

            return

        QMessageBox.information(
            self,
            "Delete",
            "Select one or more rows to delete."
        )

    # --------------------------------------------------
    # ORGANIZE
    # --------------------------------------------------

    def open_organize_dialog(self):

        if not self.require_data():
            return

        dialog = OrganizeDialog(self)

        if not dialog.exec():
            return

        action = dialog.selected_action

        if action == "sort":

            self.open_sort()

        elif action == "filter":

            self.open_filter()

        elif action == "merge":

            self.merge_files()

        elif action == "split":

            self.split_into_sheets()

        elif action == "incomplete":

            self.separate_incomplete_rows()

    def merge_files(self):

        file_paths, _ = QFileDialog.getOpenFileNames(
            self,
            "Select Excel Files",
            "",
            "Excel Files (*.xlsx *.xls)"
        )

        if not file_paths:
            return

        try:
            merged_data = merge_excel_files(file_paths)

            preview = PreviewDialog(
                merged_data,
                self
            )

            if preview.exec():
                self.save_history()
                self.data = merged_data
                self.update_table()

        except Exception as e:
            QMessageBox.critical(
                self,
                "Merge Error",
                str(e)
            )

    def split_into_sheets(self):

        if not self.require_data():
            return

        from PySide6.QtWidgets import (
            QDialog,
            QVBoxLayout,
            QLabel,
            QComboBox,
            QPushButton,
        )

        dialog = QDialog(self)
        dialog.setWindowTitle("Split Into Sheets")
        dialog.resize(350, 200)

        layout = QVBoxLayout()

        label = QLabel("Select column:")

        column_combo = QComboBox()
        column_combo.addItems(
            self.data.columns.astype(str).tolist()
        )

        confirm_button = QPushButton("Preview")

        layout.addWidget(label)
        layout.addWidget(column_combo)
        layout.addWidget(confirm_button)

        dialog.setLayout(layout)

        def confirm():

            column = column_combo.currentText()

            sheets = split_into_sheets(
                self.data.copy(),
                column
            )

            if not sheets:
                QMessageBox.warning(
                    self,
                    "Split Into Sheets",
                    "No data was found to split."
                )
                return

            preview = SplitPreviewDialog(
                sheets,
                self
            )

            if preview.exec():

                output_path, _ = QFileDialog.getSaveFileName(
                self,
                "Save Split Excel File",
                "",
                "Excel Files (*.xlsx)"
            )

            if not output_path:
                return

            try:
                with pd.ExcelWriter(
                    output_path,
                    engine="openpyxl"
                ) as writer:

                    for sheet_name, sheet_data in sheets.items():
                        sheet_data.to_excel(
                            writer,
                            sheet_name=sheet_name[:31],
                            index=False
                        )

                QMessageBox.information(
                    self,
                    "Split Complete",
                    "Excel file created successfully."
                )

            except Exception as e:
                QMessageBox.critical(
                    self,
                    "Split Error",
                    str(e)
                )

        dialog.accept()

        confirm_button.clicked.connect(confirm)

        dialog.exec()

    def separate_incomplete_rows(self):

        if not self.require_data():
            return

        from PySide6.QtWidgets import (
            QDialog,
            QVBoxLayout,
            QLabel,
            QListWidget,
            QListWidgetItem,
            QPushButton,
        )

        dialog = QDialog(self)
        dialog.setWindowTitle("Separate Incomplete Rows")
        dialog.resize(400, 400)

        layout = QVBoxLayout()

        label = QLabel(
            "Select required columns:"
        )

        columns_list = QListWidget()
        columns_list.setSelectionMode(
            QListWidget.SelectionMode.MultiSelection
        )

        for column in self.data.columns:
            item = QListWidgetItem(str(column))
            columns_list.addItem(item)

        preview_button = QPushButton("Preview")

        layout.addWidget(label)
        layout.addWidget(columns_list)
        layout.addWidget(preview_button)

        dialog.setLayout(layout)

        def preview():

            selected_columns = [
                item.text()
                for item in columns_list.selectedItems()
            ]

            if not selected_columns:
                QMessageBox.warning(
                    self,
                    "Separate Incomplete Rows",
                    "Select at least one required column."
                )
                return

            complete, incomplete = separate_incomplete_rows(
                self.data.copy(),
                selected_columns
            )

            preview_dialog = IncompletePreviewDialog(
                complete,
                incomplete,
                self
            )

            if preview_dialog.exec():
              output_path, _ = QFileDialog.getSaveFileName(
                self,
                "Save Incomplete Rows",
                "",
                "Excel Files (*.xlsx)"
            )

            if not output_path:
                return

            try:
                with pd.ExcelWriter(
                    output_path,
                    engine="openpyxl"
                ) as writer:

                    complete.to_excel(
                        writer,
                        sheet_name="Complete",
                        index=False
                    )

                    incomplete.to_excel(
                        writer,
                        sheet_name="Incomplete",
                        index=False
                    )

                QMessageBox.information(
                    self,
                    "Complete",
                    "Excel file created successfully."
                )

            except Exception as e:
                QMessageBox.critical(
                    self,
                    "Error",
                    str(e)
                )  

        preview_button.clicked.connect(preview)

        dialog.exec()

    def open_sort(self):

        from PySide6.QtWidgets import (
            QDialog,
            QVBoxLayout,
            QLabel,
            QComboBox,
            QPushButton,
        )

        dialog = QDialog(self)

        dialog.setWindowTitle("Sort Data")
        dialog.resize(350, 250)

        layout = QVBoxLayout()

        column_label = QLabel(
            "Select column:"
        )

        column_combo = QComboBox()

        column_combo.addItems(
            self.data.columns.astype(str).tolist()
        )

        order_label = QLabel(
            "Sort order:"
        )

        order_combo = QComboBox()

        order_combo.addItems([
            "Ascending",
            "Descending"
        ])

        confirm_button = QPushButton(
            "Preview"
        )

        layout.addWidget(column_label)
        layout.addWidget(column_combo)
        layout.addWidget(order_label)
        layout.addWidget(order_combo)
        layout.addWidget(confirm_button)

        dialog.setLayout(layout)

        def confirm():

            column = column_combo.currentText()

            ascending = (
                order_combo.currentText()
                == "Ascending"
            )

            sorted_data = sort_data(
                self.data.copy(),
                column,
                ascending
            )

            preview = PreviewDialog(
                sorted_data,
                self
            )

            if preview.exec():

                self.save_history()

                self.data = sorted_data

                self.update_table()

            dialog.accept()

        confirm_button.clicked.connect(
            confirm
        )

        dialog.exec()

    def open_filter(self):

        from PySide6.QtWidgets import (
            QDialog,
            QVBoxLayout,
            QLabel,
            QComboBox,
            QLineEdit,
            QPushButton,
        )

        dialog = QDialog(self)

        dialog.setWindowTitle("Filter")
        dialog.resize(350, 250)

        layout = QVBoxLayout()

        column_label = QLabel(
            "Select column:"
        )

        column_combo = QComboBox()

        column_combo.addItems(
            self.data.columns.astype(str).tolist()
        )

        value_label = QLabel(
            "Enter value:"
        )

        value_input = QLineEdit()

        value_input.setPlaceholderText(
            "Value..."
        )

        confirm_button = QPushButton(
            "Preview"
        )

        layout.addWidget(column_label)
        layout.addWidget(column_combo)
        layout.addWidget(value_label)
        layout.addWidget(value_input)
        layout.addWidget(confirm_button)

        dialog.setLayout(layout)

        def confirm():

            column = column_combo.currentText()
            value = value_input.text()

            filtered_data = filter_data(
                self.data.copy(),
                column,
                value
            )

            preview = PreviewDialog(
                filtered_data,
                self
            )

            if preview.exec():

                self.save_history()

                self.data = filtered_data

                self.update_table()

            dialog.accept()

        confirm_button.clicked.connect(
            confirm
        )

        dialog.exec()

    # --------------------------------------------------
    # ANALYZE
    # --------------------------------------------------

    def open_analyze_dialog(self):

        if not self.require_data():
            return

        dialog = AnalyzeDialog(self)

        if not dialog.exec():
            return

        action = dialog.selected_action

        if action == "search":

            self.open_search()

        elif action == "statistics":

            self.show_not_ready(
                "Statistics / Summary"
            )

        elif action == "missing":

            self.show_not_ready(
                "Missing Data"
            )

    def open_search(self):

        from PySide6.QtWidgets import (
            QDialog,
            QVBoxLayout,
            QLabel,
            QLineEdit,
            QPushButton,
        )

        dialog = QDialog(self)

        dialog.setWindowTitle("Search")
        dialog.resize(350, 180)

        layout = QVBoxLayout()

        label = QLabel(
            "Enter search term:"
        )

        search_input = QLineEdit()

        search_input.setPlaceholderText(
            "Search..."
        )

        search_button = QPushButton(
            "Search"
        )

        layout.addWidget(label)
        layout.addWidget(search_input)
        layout.addWidget(search_button)

        dialog.setLayout(layout)

        def search():

            search_term = search_input.text()

            if not search_term:
                return

            results = search_data(
                self.data.copy(),
                search_term
            )

            preview = PreviewDialog(
                results,
                self
            )

            if preview.exec():

                self.save_history()

                self.data = results

                self.update_table()

            dialog.accept()

        search_button.clicked.connect(
            search
        )

        dialog.exec()

    # --------------------------------------------------
    # EXPORT
    # --------------------------------------------------

    def open_export_dialog(self):

        if not self.require_data():
            return

        dialog = ExportDialog(self)

        if not dialog.exec():
            return

        file_format = dialog.selected_format

        filters = {
            "xlsx": "Excel Files (*.xlsx)",
            "csv": "CSV Files (*.csv)",
            "json": "JSON Files (*.json)",
            "html": "HTML Files (*.html)",
            "pdf": "PDF Files (*.pdf)",
        }

        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save File",
            "",
            filters[file_format]
        )

        if not file_path:
            return

        try:

            if file_format == "pdf":

                save_pdf(
                    self.data,
                    file_path
                )

            else:

                save_excel(
                    self.data,
                    file_path
                )

            QMessageBox.information(
                self,
                "Export",
                "File saved successfully."
            )

        except Exception as error:

            QMessageBox.critical(
                self,
                "Export Error",
                f"Could not save the file:\n\n{error}"
            )

    # --------------------------------------------------
    # RESET
    # --------------------------------------------------

    def reset_data(self):

        if self.original_data is None:
            return

        self.data = (
            self.original_data.copy()
        )

        self.undo_stack.clear()
        self.redo_stack.clear()

        self.update_table()

    # --------------------------------------------------
    # HELPERS
    # --------------------------------------------------

    def show_not_ready(self, feature):

        QMessageBox.information(
            self,
            feature,
            f"{feature} is prepared in the new UI "
            "but its processing module will be "
            "implemented next."
        )