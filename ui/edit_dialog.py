from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QPushButton,
    QListWidget,
    QCheckBox,
    QSpinBox,
    QLabel,
)


class EditDialog(QDialog):

    def __init__(self, columns=None, parent=None):
        super().__init__(parent)

        self.columns = columns or []

        self.setWindowTitle("Edit")
        self.resize(350, 450)

        layout = QVBoxLayout()

        # Clean
        self.clean_button = QPushButton("Clean")

        # Delete
        self.delete_button = QPushButton("Delete")

        # Undo / Redo
        self.undo_button = QPushButton("Undo")
        self.redo_button = QPushButton("Redo")

        layout.addWidget(self.clean_button)
        layout.addWidget(self.delete_button)
        layout.addWidget(self.undo_button)
        layout.addWidget(self.redo_button)

        self.clean_button.clicked.connect(self.clean)
        self.delete_button.clicked.connect(self.delete)
        self.undo_button.clicked.connect(self.undo)
        self.redo_button.clicked.connect(self.redo)

        self.setLayout(layout)

    def clean(self):
        self.selected_action = "clean"
        self.accept()

    def delete(self):
        self.selected_action = "delete"
        self.accept()

    def undo(self):
        self.selected_action = "undo"
        self.accept()

    def redo(self):
        self.selected_action = "redo"
        self.accept()