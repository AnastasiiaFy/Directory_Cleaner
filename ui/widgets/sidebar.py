from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QPalette
from utils.helpers import format_size
from utils.file_constants import CATEGORY_COLORS


class SegmentedCategoryBar(QWidget):
    """Custom widget of vertical color distribution strip"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(1)

        self.setStyleSheet("""
            SegmentedCategoryBar {
                background-color: #e0e0e0;
                border-radius: 4px;
                padding: 3px;
            }
        """)

    def set_data(self, categories_data):
        """Updates segments based on categories data

        Args:
            categories_data: list of dict with color key та size value
        """
        # Очищення попередніх віджетів
        while self.layout.count():
            item = self.layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        if not categories_data:
            return

        # Розраховуємо загальний розмір
        total = sum(cat.get("size", 0) for cat in categories_data) or 1

        # Розраховуємо "ідеальні" висоти
        ideal_heights = []
        for cat in categories_data:
            if cat.get("size", 0) > 0:
                ratio = cat.get("size", 0) / total
                ideal_heights.append(ratio)
            else:
                ideal_heights.append(0)

        # Штучно збільшуємо малі категорії, щоб зробити їх видимими
        adjusted_heights = []
        for height in ideal_heights:
            if 0 < height < 0.05:            # Якщо < 5%
                adjusted_heights.append(height * 1.5)
            else:
                adjusted_heights.append(height)

        # Нормалізуємо (щоб сума = 1.0)
        total_adjusted = sum(adjusted_heights)
        if total_adjusted > 0:
            adjusted_heights = [h / total_adjusted for h in adjusted_heights]

        for i, cat in enumerate(categories_data):
            if cat.get("size", 0) > 0:
                frame = QWidget()
                frame.setStyleSheet(
                    f"background-color: {cat.get('color', '#ccc')}; "
                    f"border-radius: 4px;"
                )
                self.layout.addWidget(frame, int(adjusted_heights[i] * 1000))


class Sidebar(QWidget):
    """Sidebar with folder information and vertical chart"""

    select_another_directory = Signal()

    def __init__(self):
        super().__init__()

        self.path_label = None
        self.file_count_label = None
        self.total_size_label = None
        self.category_bar = None
        self.select_another_btn = None
        self.categories_layout = None

        self.setMinimumWidth(300)
        self.setMaximumWidth(340)

        self.setObjectName("sidebar")
        palette = self.palette()
        palette.setColor(QPalette.Window, "#F8F8F8")
        self.setAutoFillBackground(True)
        self.setPalette(palette)

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 28, 24, 24)
        layout.setSpacing(20)

        # Заголовок і шлях
        header_layout = QVBoxLayout()
        header_layout.setSpacing(4)

        title_label = QLabel("Current Folder:")
        title_label.setStyleSheet("font-weight: bold; font-size: 15px; color: #000000;")

        self.path_label = QLabel("/Users/user/Downloads")
        self.path_label.setWordWrap(True)
        self.path_label.setStyleSheet("color: #666666; font-size: 13px; line-height: 1.4;")

        header_layout.addWidget(title_label)
        header_layout.addWidget(self.path_label)
        layout.addLayout(header_layout)

        # Загальна статистика (Quantity + Size)
        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(10)

        # Кількість файлів
        self.file_count_label = QLabel("Files: 0")
        self.file_count_label.setStyleSheet("""
                    font-size: 14px;
                    color: black;
                    font-weight: 500;
                """)

        # Загальний розмір
        self.total_size_label = QLabel("Total: 0 B")
        self.total_size_label.setStyleSheet("""
                    font-size: 14px;
                    color: black;
                    font-weight: 500;
                """)

        stats_layout.addWidget(self.file_count_label)
        stats_layout.addWidget(self.total_size_label)
        layout.addLayout(stats_layout)

        # 3. Блок із діаграмою та легендою (категоріями)
        chart_container = QHBoxLayout()
        chart_container.setSpacing(16)

        # Вертикальний бар категорій
        self.category_bar = SegmentedCategoryBar()
        self.category_bar.setFixedWidth(24)
        self.category_bar.setMinimumHeight(200)
        chart_container.addSpacing(5)
        chart_container.addWidget(self.category_bar)

        # Контейнер під тексти категорій
        self.categories_layout = QVBoxLayout()
        self.categories_layout.setSpacing(12)
        self.categories_layout.setAlignment(Qt.AlignTop)

        chart_container.addLayout(self.categories_layout)
        chart_container.addStretch()

        layout.addLayout(chart_container, stretch=1)

        # 4. Кнопка "Обрати інший каталог"
        self.select_another_btn = QPushButton("Select Another Folder")
        self.select_another_btn.setFixedHeight(45)
        self.select_another_btn.setStyleSheet("""
            QPushButton {
                background-color: #75BBDF;
                color: white;
                border: none;
                border-radius: 10px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #6BACCE;
            }
            QPushButton:pressed {
                background-color: #5497BB;
            }
        """)
        self.select_another_btn.clicked.connect(self.select_another_directory.emit)
        layout.addWidget(self.select_another_btn)

        self.setLayout(layout)

    def set_path(self, path: str):
        """Updates the displayed path label"""
        self.path_label.setText(path)

    def update_statistics(self, statistics: dict):
        """
        Updates bar chart and category list

        Args:
            statistics: dict with categories statistics
        """
        # Оновлюємо загальну статистику
        total_count = statistics.get("total_count", 0)
        total_size = statistics.get("total_size", 0)

        self.file_count_label.setText(f"Files: {total_count}")
        self.total_size_label.setText(f"Total: {format_size(total_size)}")

        progress_data = []
        categories_list = []

        # Обробляємо категорії
        for category, data in statistics.get("by_category", {}).items():
            if data["count"] > 0:
                progress_data.append({
                    "color": CATEGORY_COLORS.get(category, "#CCCCCC"),
                    "size": data["size"]
                })

                categories_list.append({
                    "name": category,
                    "size_bytes": data["size"],
                    "color": CATEGORY_COLORS.get(category, "#CCCCCC")
                })


        self.category_bar.set_data(progress_data)
        self._update_categories_list(categories_list)

    def _update_categories_list(self, categories: list):
        """Updates the list of categories on the side of the chart"""

        # Очищаємо попередній список
        while self.categories_layout.count():
            item = self.categories_layout.takeAt(0)

            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                self._clear_layout(item.layout())

        # Додаємо категорії
        for cat in categories:
            row_layout = QHBoxLayout()
            row_layout.setSpacing(8)

            # Кольоровий круг
            color_dot = QLabel()
            color_dot.setFixedSize(10, 10)
            color_dot.setStyleSheet(f"""
                background-color: {cat["color"]};
                border-radius: 5px;
            """)

            # Назва категорії
            name_lbl = QLabel(cat["name"])
            name_lbl.setStyleSheet("""
                font-weight: bold;
                font-size: 12px;
                color: #000000;
            """)

            row_layout.addWidget(color_dot)
            row_layout.addWidget(name_lbl)
            row_layout.addStretch()

            # Розмір файлів
            size_lbl = QLabel(format_size(cat["size_bytes"]))
            size_lbl.setStyleSheet("""
                font-size: 12px;
                color: #444444;
            """)

            cat_box = QVBoxLayout()
            cat_box.setSpacing(2)
            cat_box.addLayout(row_layout)
            cat_box.addWidget(size_lbl)

            self.categories_layout.addLayout(cat_box)

        self.categories_layout.addStretch()

    def _clear_layout(self, layout):
        """Clear layout recursively"""
        while layout.count():
            item = layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                self._clear_layout(item.layout())