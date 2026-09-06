from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QCheckBox,
    QPushButton,
    QSpinBox,
    QLabel,
)


class CleanDialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Clean Options")
        self.resize(350, 250)

        layout = QVBoxLayout()

        self.remove_empty_rows = QCheckBox("Remove empty rows")
        self.remove_empty_columns = QCheckBox("Remove empty columns")
        self.remove_duplicates = QCheckBox("Remove duplicate rows")
        self.clean_spaces = QCheckBox("Clean extra spaces")
        self.remove_sparse_columns = QCheckBox(
            "Remove columns with too many empty cells"
        )

        self.threshold_label = QLabel("Empty cell threshold (%)")

        self.threshold = QSpinBox()
        self.threshold.setRange(1, 100)
        self.threshold.setValue(80)
        self.threshold.setSuffix("%")

        self.threshold.setEnabled(False)

        self.remove_sparse_columns.stateChanged.connect(
            self.toggle_threshold
        )

        self.confirm_button = QPushButton("Confirm")
        self.confirm_button.clicked.connect(self.confirm)

        layout.addWidget(self.remove_empty_rows)
        layout.addWidget(self.remove_empty_columns)
        layout.addWidget(self.remove_duplicates)
        layout.addWidget(self.clean_spaces)
        layout.addWidget(self.remove_sparse_columns)
        layout.addWidget(self.threshold_label)
        layout.addWidget(self.threshold)


        layout.addWidget(self.confirm_button)
        

        self.setLayout(layout)
    def confirm(self):
        self.selected_options = {
            "remove_empty_rows": self.remove_empty_rows.isChecked(),
            "remove_empty_columns": self.remove_empty_columns.isCheckable(),
            "remove_duplicates": self.remove_duplicates.isChecked(),
            "clean_spaces": self.clean_spaces.isChecked(),
            "remove_sparse_columns": self.remove_sparse_columns.isChecked(),
            "threshold": self.threshold.value() / 100,
        }

        self.accept()

    def toggle_threshold(self, state):
        enabled = state == 2

        self.threshold_label.setEnabled(enabled)
        self.threshold.setEnabled(enabled)
        
        