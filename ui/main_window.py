from pathlib import Path
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QPushButton, QFileDialog, QLabel, QSpacerItem, QSizePolicy,
    QMenu, QMessageBox, QDialog
)

from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon, QPixmap

from ui.widgets.sidebar import Sidebar
from ui.widgets.selection_badge import SelectionBadge
from ui.widgets.file_list import FileListWidget
from ui.dialogs.delete_confirmation_dialog import DeleteConfirmationDialog

from core.worker import ScannerWorker
from backend.service import FileSystemService
from utils.helpers import format_size


class MainWindow(QMainWindow):
    """ App main window"""

    def __init__(self, initial_path: str):
        super().__init__()
        self.setWindowTitle("Directory Cleaner")
        self.setGeometry(100, 100, 1400, 800)

        # Дані та елементи
        self.current_path = Path(initial_path)
        self.scan_results = None
        self.worker = None

        self.sidebar = None
        self.sidebar_visible = True
        self.toggle_btn = None

        self.status_label = ""
        self.btn_select = None
        self.selection_badge = None

        self.btn_recommendations = None
        self.btn_sort = None
        self.btn_filter = None
        self.btn_rescan =None

        self.file_list = None

        self.service = FileSystemService("deletion_history.json")

        self.init_ui()
        self.start_scan()

    def init_ui(self):
        """UI Initialization"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Основний layout (горизонтальний)
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # ======================================================================
        #        ЛІВА ЧАСТИНА: SIDEBAR + TOGGLE КНОПКА
        # ======================================================================
        sidebar_container = QHBoxLayout()
        sidebar_container.setContentsMargins(0, 0, 0, 0)
        sidebar_container.setSpacing(0)

        # Sidebar
        self.sidebar = Sidebar()
        self.sidebar.select_another_directory.connect(self.select_another_directory)
        sidebar_container.addWidget(self.sidebar)

        # Toggle кнопка
        self.toggle_btn = QPushButton()
        self.toggle_btn.setFixedSize(40, 50)
        self.toggle_btn.setIcon(QIcon("resources/chevron-left.png"))
        self.toggle_btn.setIconSize(QSize(20, 20))

        self.toggle_btn.setStyleSheet("""
            QPushButton {
                background-color: #F8F8F8;
                border: none;
                border-top-right-radius: 10px;
                border-bottom-right-radius: 10px;
                padding: 0px;
            }
            QPushButton:hover {
                background-color: #dcdcdc;
            }
            QPushButton:pressed {
                background-color: #cccccc;
            }
        """)
        self.toggle_btn.clicked.connect(self.toggle_sidebar)
        sidebar_container.addWidget(self.toggle_btn, alignment=Qt.AlignTop)

        main_layout.addLayout(sidebar_container)

        # ======================================================================
        #            ПРАВА ЧАСТИНА: ОСНОВНА ОБЛАСТЬ
        # ======================================================================
        right_layout = QVBoxLayout()
        right_layout.setContentsMargins(20, 20, 20, 20)
        right_layout.setSpacing(16)

        # Статус сканування
        self.status_label = QLabel("Scanning...")
        self.status_label.setStyleSheet("""
            QLabel {
                font-size: 13px;
                color: #666666;
                padding: 8px;
            }
        """)
        right_layout.addWidget(self.status_label)

        # ========== TOOLBAR З КНОПКАМИ ==========
        toolbar_layout = QHBoxLayout()
        toolbar_layout.setContentsMargins(0, 0, 0, 0)
        toolbar_layout.setSpacing(0)

        # Кнопка видалення + лічильник обраних файлів
        self.btn_select = self._create_toolbar_button("resources/delete.png", "Delete Selected Files")
        self.selection_badge = SelectionBadge()
        self.selection_badge.hide()

        select_group_layout = QHBoxLayout()
        select_group_layout.setContentsMargins(0, 0, 0, 0)
        select_group_layout.setSpacing(0)
        select_group_layout.addWidget(self.btn_select)
        select_group_layout.addWidget(self.selection_badge)

        select_group_container = QWidget()
        select_group_container.setLayout(select_group_layout)

        toolbar_layout.addWidget(select_group_container)
        toolbar_layout.addSpacing(12)

        # Інші 3 кнопки
        self.btn_recommendations = self._create_toolbar_button("resources/recommend_for_deletion.png", "Not Available")
        self.btn_sort = self._create_toolbar_button("resources/sort.png", "Sort")
        self.btn_filter = self._create_toolbar_button("resources/filter_by_time.png", "Filter by Modification Time")

        toolbar_layout.addWidget(self.btn_recommendations)
        toolbar_layout.addSpacing(12)
        toolbar_layout.addWidget(self.btn_sort)
        toolbar_layout.addSpacing(12)
        toolbar_layout.addWidget(self.btn_filter)

        # Спейсер для розділення кнопок
        spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        toolbar_layout.addItem(spacer)

        # 1 кнопка праворуч
        self.btn_rescan = self._create_toolbar_button("resources/refresh.png", "Rescan folder")
        toolbar_layout.addWidget(self.btn_rescan)

        # Підключення сигналів до кнопок
        self.btn_select.clicked.connect(self.on_select_clicked)
        self.btn_recommendations.clicked.connect(self.on_recommendations_clicked)
        self.btn_sort.clicked.connect(self.on_sort_clicked)
        self.btn_filter.clicked.connect(self.on_filter_clicked)
        self.btn_rescan.clicked.connect(self.on_rescan_clicked)

        right_layout.addLayout(toolbar_layout)

        # ======================================================================
        #            ТАБЛИЦЯ ФАЙЛІВ
        # ======================================================================
        self.file_list = FileListWidget()
        self.file_list.selection_changed.connect(self.on_selection_changed)
        right_layout.addWidget(self.file_list, 1)

        main_layout.addLayout(right_layout, 1)
        central_widget.setLayout(main_layout)


    def start_scan(self):
        """ Start scanning directory in separate thread """
        self.status_label.setText("Scanning...")

        self.worker = ScannerWorker(self.service, str(self.current_path))
        self.worker.finished.connect(self.on_scan_finished)
        self.worker.error.connect(self.on_scan_error)
        self.worker.start()

    def on_scan_finished(self, results):
        """Called when the scan is complete """

        self.status_label.setText("")
        self.scan_results = results

        # Оновлюємо sidebar
        self.sidebar.set_path(str(self.current_path))
        self.sidebar.update_statistics(results["statistics"])

        # Показуємо файли
        self.file_list.populate_files(results["all_files"])


    def on_scan_error(self, error):
        """Handles scan error"""
        self.status_label.setText(f"Error: {error}")

    def toggle_sidebar(self):
        """Hide/Show Sidebar"""
        if self.sidebar_visible:
            self.sidebar.hide()
            self.toggle_btn.setIcon(QIcon("resources/chevron-right.png"))
        else:
            self.sidebar.show()
            self.toggle_btn.setIcon(QIcon("resources/chevron-left.png"))

        self.sidebar_visible = not self.sidebar_visible

    def select_another_directory(self):
        """ Shows the dialog window for selecting another folder """
        folder = QFileDialog.getExistingDirectory(
            self,
            "Select another directory",
            str(self.current_path),
            QFileDialog.ShowDirsOnly
        )

        if folder:
            self.current_path = Path(folder)
            self.start_scan()

    @staticmethod
    def _create_toolbar_button(icon_path: str, tooltip: str) -> QPushButton:
        """Create a button for toolbar """
        btn = QPushButton()
        btn.setIcon(QIcon(icon_path))
        btn.setIconSize(QSize(20, 20))

        btn.setFixedSize(48, 40)
        btn.setToolTip(tooltip)
        btn.setStyleSheet("""
            QPushButton {
                background-color: #E2C9C9;
                border-radius: 10px;
                padding: 0px;
            }
            QPushButton:hover {
                background-color: #CEB4B4;
            }
            QPushButton:pressed {
                background-color: #BCA0A0;
            }
        """)
        return btn

    # ======================================================================
    #                        ОБРОБНИКИ КНОПОК
    # ======================================================================
    def on_select_clicked(self):
        """Button 'Select for Deletion' handler """
        selected_files = self.file_list.get_selected_files()

        if not selected_files:
            # self.status_label.setText("No files selected for deletion")
            msg_box = QMessageBox(self)
            msg_box.setWindowTitle("No Selection")
            msg_box.setText("Please select files you want to delete.")
            msg_box.setIconPixmap(QPixmap("resources/select_instruction.png").scaled(400, 170))
            msg_box.exec()
            return

        # Отримуємо інформацію про обрані файли
        file_infos = [
            f for f in self.scan_results["all_files"]
            if f["path"] in selected_files
        ]

        total_size = sum(f["size"] for f in file_infos)
        file_count = len(file_infos)

        print(total_size, file_count)

        # Показуємо діалог підтвердження
        dialog = DeleteConfirmationDialog(file_count, total_size, parent=self)

        # if dialog.is_confirmed():
        if dialog.exec() == QDialog.Accepted:
            self.delete_selected_files(file_infos)


    def on_recommendations_clicked(self):
        """Button 'Get Recommendations' handler"""
        print("Recommendations clicked")
        # TODO: Реалізувати логіку рекомендацій

    def on_sort_clicked(self):
        """Button 'Sort' handler """
        menu = QMenu(self)
        menu.setStyleSheet("""
            QMenu {
                background-color: #ffffff;
                border: 1px solid #d0d0d0;
                border-radius: 6px;
                font-size: 15px;
            }
            QMenu::item:selected {
                background-color: #E2C9C9;
            }
        """)

        # Дії для сортування
        action_by_name = menu.addAction("Sort by Name")
        action_by_size = menu.addAction("Sort by Size")
        action_by_date = menu.addAction("Sort by Modification Time")
        action_by_extension = menu.addAction("Sort by Extension")

        # Підключаємо дії
        action_by_name.triggered.connect(lambda: self._apply_sort("name"))
        action_by_size.triggered.connect(lambda: self._apply_sort("size"))
        action_by_date.triggered.connect(lambda: self._apply_sort("modified_time"))
        action_by_extension.triggered.connect(lambda: self._apply_sort("extension"))

        # Показуємо меню під кнопкою
        menu.exec(self.btn_sort.mapToGlobal(self.btn_sort.rect().bottomLeft()))

    def on_filter_clicked(self):
        """Button 'Filter by Time' handler"""
        menu = QMenu(self)
        menu.setStyleSheet("""
            QMenu {
                background-color: #ffffff;
                border: 1px solid #d0d0d0;
                border-radius: 6px;
                padding: 4px;
                font-size: 15px;
            }
            QMenu::item:selected {
                background-color: #E2C9C9;
            }
        """)

        # Параметри для фільтрації
        action_24h = menu.addAction("Last 24 Hours")
        action_3d = menu.addAction("Last 3 Days")
        action_1w = menu.addAction("Last Week")
        action_2w = menu.addAction("Last 2 Weeks")
        action_1m = menu.addAction("Last Month")
        action_1y = menu.addAction("Last Year")
        action_older = menu.addAction("Older than 1 Year")

        # Підключення дій
        action_24h.triggered.connect(lambda: self._apply_filter(1))
        action_3d.triggered.connect(lambda: self._apply_filter(3))
        action_1w.triggered.connect(lambda: self._apply_filter(7))
        action_2w.triggered.connect(lambda: self._apply_filter(14))
        action_1m.triggered.connect(lambda: self._apply_filter(30))
        action_1y.triggered.connect(lambda: self._apply_filter(365))
        action_older.triggered.connect(lambda: self._apply_filter(365, older=True))

        # Показ меню
        menu.exec(self.btn_filter.mapToGlobal(self.btn_filter.rect().bottomLeft()))


    def on_rescan_clicked(self):
        """Button 'Rescan' handler"""
        self.start_scan()

    # ======================================================================
    #                   ДОПОМІЖНІ ФУНКЦІЇ ДЛЯ ОБРОБНИКІВ КНОПОК
    # ======================================================================
    def delete_selected_files(self, files_to_delete: list):
        """Deletes selected files and save history

        Args:
            files_to_delete: list of files for deletion
        """
        file_paths = [f["path"] for f in files_to_delete]
        result = self.service.delete_selected_files(file_paths)

        self.scan_results = self.service.get_current_scan_result()

        if result["success"]:
            self.file_list.populate_files(self.scan_results["all_files"])
            self.sidebar.update_statistics(self.scan_results["statistics"])

            # Очищуємо вибір
            self.file_list.clear_selection()
            self.selection_badge.hide()

        else:
            # Частково успішне видалення
            deleted_count = len(result["deleted"])
            failed_count = len(result["failed"])
            freed_size = format_size(result["total_freed_bytes"])


            self.file_list.populate_files(self.scan_results["all_files"])
            self.sidebar.update_statistics(self.scan_results["statistics"])

            self.file_list.clear_selection()
            self.selection_badge.hide()

            error_msg = (
                f"Deleted: {deleted_count} files ({freed_size})\n"
                f"Failed: {failed_count} files\n\n"
                "Some files could not be deleted. "
                "They may be in use or you don't have permission."
            )
            QMessageBox.warning(self, "Partial Deletion", error_msg)


    def _apply_sort(self, sort_by: str):
        """Sorts list of files

        Args:
            sort_by: Parameter for sorting (name, size, modified_time, extension)
        """
        if not self.scan_results:
            return

        files = self.scan_results["all_files"]
        files_sorted = self.service.apply_sort(files, sort_by)

        self.file_list.populate_files(files_sorted)


    def _apply_filter(self, days: int, older: bool = False):
        """Filters list of files"""
        if not self.scan_results:
            return

        files = self.scan_results["all_files"]
        files_filtered = self.service.apply_filter_by_time(files, days, older=older)

        self.file_list.populate_files(files_filtered)


    def on_selection_changed(self, selected_count: int):
        """
        The handler updates the number of selected files in the table.
        Changes the number inside badge

        Args:
            selected_count: number of selected files
        """
        if selected_count == 0:
            self.selection_badge.hide()
        else:
            self.selection_badge.set_count(selected_count)