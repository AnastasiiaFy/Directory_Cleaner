from PySide6.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView, QCheckBox, QWidget, QHBoxLayout
from PySide6.QtCore import Qt, Signal
from datetime import datetime
from pathlib import Path
import subprocess
import platform
from utils.helpers import format_size


class FileListWidget(QTableWidget):
    """Table with information about files """

    selection_changed = Signal(int)

    def __init__(self):
        super().__init__()
        self.files_data = []
        self.init_ui()

    def init_ui(self):
        self.setColumnCount(6)
        self.setHorizontalHeaderLabels(["Select", "Name", "Size", "Modified", "Category", "Path"])

        # Налаштування колонок
        header = self.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)  # Select
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)  # Name
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)  # Size
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)  # Modified
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)  # Category
        header.setSectionResizeMode(5, QHeaderView.Stretch)           # Path

        # Стилі
        self.setStyleSheet("""
            QTableWidget {
                border: 1px solid #ddd;
                gridline-color: #eee;
            }
            QHeaderView::section {
                background-color: #f0f0f0;
                padding: 5px;
                border: none;
                font-weight: bold;
            }
        """)

        self.setAlternatingRowColors(True)
        self.setEditTriggers(QTableWidget.NoEditTriggers)   # Забороняємо редагування клітинок
        self.setSelectionMode(QTableWidget.NoSelection)     # Забороняємо будь-яке виділення клітинок
        self.setFocusPolicy(Qt.NoFocus)                     # Забороняємо фокус на клітинках під час кліку

        # Підключаємо сигнали
        self.doubleClicked.connect(self.on_file_double_clicked)


    def populate_files(self, files: list):
        """Заповнює таблицю файлами"""

        self.clear_selection()

        self.files_data = files
        self.setRowCount(len(files))

        for row, file_info in enumerate(files):
            # ========== КОЛОНА 0: CHECKBOX ==========
            checkbox = QCheckBox()
            checkbox.setChecked(False)
            checkbox.file_path = file_info["path"]      # Зберігаємо шлях до файлу у checkbox

            checkbox.stateChanged.connect(self.on_checkbox_state_changed)

            # Помістимо checkbox в центр клітинки
            checkbox_widget = QWidget()
            checkbox_layout = QHBoxLayout(checkbox_widget)
            checkbox_layout.setContentsMargins(0, 0, 0, 0)
            checkbox_layout.addWidget(checkbox, alignment=Qt.AlignCenter)

            self.setCellWidget(row, 0, checkbox_widget)

            # ========== КОЛОНА 1: ІМ'Я ==========
            name_item = QTableWidgetItem(file_info["name"])
            name_item.setFlags(name_item.flags() | Qt.ItemIsSelectable)
            name_item.setData(Qt.UserRole, file_info["path"])
            self.setItem(row, 1, name_item)

            # ========== КОЛОНА 2: РОЗМІР ==========
            size_item = QTableWidgetItem(format_size(file_info["size"]))
            size_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.setItem(row, 2, size_item)

            # ========== КОЛОНА 3: ДАТА ==========
            modified_time = datetime.fromtimestamp(file_info["modified_time"])
            date_item = QTableWidgetItem(modified_time.strftime("%d.%m.%Y %H:%M"))
            self.setItem(row, 3, date_item)

            # ========== КОЛОНА 4: КАТЕГОРІЯ ==========
            category_item = QTableWidgetItem(file_info["category"])
            self.setItem(row, 4, category_item)

            # ========== КОЛОНА 5: ШЛЯХ ==========
            path_item = QTableWidgetItem(file_info["path"])
            path_item.setToolTip(file_info["path"])
            self.setItem(row, 5, path_item)


    def on_checkbox_state_changed(self):
        """Called when anу checkbox changes a state"""
        selected_count = len(self.get_selected_files())
        self.selection_changed.emit(selected_count)         # Видаємо сигнал з кількістю обраних файлів


    def on_file_double_clicked(self, index):
        """ Open a file after double-click on any table cell,
        except checkbox cell"""
        row = index.row()
        column = index.column()

        if column == 0:
            return

        # Отримуємо шлях до файлу
        name_item = self.item(row, 1)  # Name в колоні 1
        if name_item:
            file_path = name_item.data(Qt.UserRole)
            if file_path:
                self.open_file(file_path)

    @staticmethod
    def open_file(file_path: str):
        try:
            if not Path(file_path).exists():
                print(f"File not found: {file_path}")
                return

            system = platform.system()

            if system == "Darwin":
                subprocess.Popen(["open", file_path])
            elif system == "Windows":
                import os
                os.startfile(file_path)

        except Exception as e:
            print(f"Error opening file {file_path}: {e}")

    def get_selected_files(self) -> list[str]:
        """
        Returns:
            list of files with selected checkboxes
        """
        selected_files = []

        for row in range(self.rowCount()):
            checkbox_widget = self.cellWidget(row, 0)
            if checkbox_widget:
                checkbox = checkbox_widget.findChild(QCheckBox)
                if checkbox and checkbox.isChecked():
                    selected_files.append(checkbox.file_path)

        return selected_files

    def clear_selection(self):
        for row in range(self.rowCount()):
            checkbox_widget = self.cellWidget(row, 0)
            if checkbox_widget:
                checkbox = checkbox_widget.findChild(QCheckBox)
                if checkbox:
                    # checkbox.setChecked(False)
                    checkbox.blockSignals(True)  # Блокуємо сигнали
                    checkbox.setChecked(False)
                    checkbox.blockSignals(False)  # Розблоковуємо
        self.selection_changed.emit(0)
