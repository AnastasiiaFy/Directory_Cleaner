from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from utils.helpers import format_size


class DeleteConfirmationDialog(QDialog):
    """Dialog window for deletion confirmation"""

    def __init__(self, file_count: int, total_size: int, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Confirm Deletion")
        self.setModal(True)
        self.setMinimumWidth(420)
        self.confirmed = False

        self.init_ui(file_count, total_size)

    def init_ui(self, file_count: int, total_size: int):
        layout = QVBoxLayout()
        layout.setContentsMargins(32, 28, 32, 28)
        layout.setSpacing(0)

        # Icon
        trash_icon_label = QLabel()
        trash_pixmap = QPixmap("resources/delete.png").scaled(
            50, 50, Qt.KeepAspectRatio, Qt.SmoothTransformation
        )
        trash_icon_label.setPixmap(trash_pixmap)
        trash_icon_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(trash_icon_label)
        layout.addSpacing(12)

        # Title
        title = QLabel("Delete Files")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 18px; "
                            "font-weight: bold; "
                            "color: #000000;")
        layout.addWidget(title)
        layout.addSpacing(28)

        # Information about files number and total size
        info_layout = QVBoxLayout()
        info_layout.setSpacing(6)
        lbl_selected = QLabel(f"You selected {file_count} file(s) to delete.")
        lbl_selected.setStyleSheet("font-size: 13px; font-weight: 600; color: #000000;")

        formatted_size = format_size(total_size)
        lbl_memory = QLabel(f"You will clean {formatted_size} of memory")
        lbl_memory.setStyleSheet("font-size: 13px; font-weight: 600; color: #000000;")

        info_layout.addWidget(lbl_selected)
        info_layout.addWidget(lbl_memory)
        layout.addLayout(info_layout)
        layout.addSpacing(16)

        # Warning
        warning_layout = QHBoxLayout()
        warning_layout.setContentsMargins(0, 0, 0, 0)
        warning_layout.setSpacing(10)
        warning_layout.setAlignment(Qt.AlignLeft | Qt.AlignTop)

        warn_icon_label = QLabel()
        warn_pixmap = QPixmap("resources/warning.png").scaled(
            22, 22, Qt.KeepAspectRatio, Qt.SmoothTransformation
        )
        warn_icon_label.setPixmap(warn_pixmap)
        warn_icon_label.setFixedSize(22, 22)

        warn_text = QLabel("This action will delete selected files.\nThis action cannot be undone.")
        warn_text.setStyleSheet("font-size: 13px; font-weight: 600; color: #000000; line-height: 1.3;")

        warning_layout.addWidget(warn_icon_label)
        warning_layout.addWidget(warn_text)
        layout.addLayout(warning_layout)
        layout.addSpacing(32)

        # Buttons (Cancel / Delete)
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(16)

        # Cancel
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setFixedHeight(44)
        cancel_btn.setStyleSheet("""
                    QPushButton {
                        background-color: #D9D9D9;
                        color: #000000;
                        border: none;
                        border-radius: 8px;
                        font-size: 15px;
                        font-weight: bold;
                    }
                    QPushButton:hover {
                        background-color: #CCCCCC;
                    }
                    QPushButton:pressed {
                        background-color: #BFBFBF;
                    }
                """)
        cancel_btn.clicked.connect(self.reject)

        # Delete
        delete_btn = QPushButton("Delete")
        delete_btn.setFixedHeight(44)
        delete_btn.setStyleSheet("""
                    QPushButton {
                        background-color: #A31D1D;
                        color: #FFFFFF;
                        border: none;
                        border-radius: 8px;
                        font-size: 15px;
                        font-weight: bold;
                    }
                    QPushButton:hover {
                        background-color: #8C1818;
                    }
                    QPushButton:pressed {
                        background-color: #731313;
                    }
                """)
        delete_btn.clicked.connect(self.accept)

        buttons_layout.addWidget(cancel_btn, stretch=1)
        buttons_layout.addWidget(delete_btn, stretch=1)
        layout.addLayout(buttons_layout)
        self.setLayout(layout)


    def is_confirmed(self) -> bool:
        """Returns: True if user confirmed deletion """
        return self.result() == QDialog.Accepted