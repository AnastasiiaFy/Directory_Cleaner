from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QColor, QFont
from utils.helpers import format_size

from utils.file_constants import CATEGORY_COLORS

class CategoryChart(QWidget):
    """Bar chart with files size by category"""

    def __init__(self):
        super().__init__()
        self.categories = {}
        self.total_size = 0
        self.setMinimumHeight(200)

    def update_data(self, categories: dict):
        self.categories = {}
        self.total_size = sum(cat["size"] for cat in categories.values()) + \
                          (categories.get("other", {}).get("size", 0) if "other" in categories else 0)

        for category_name, category_data in categories.items():
            if category_data["size"] > 0:
                self.categories[category_name] = {
                    "size": category_data["size"],
                    "count": category_data["count"]
                }

        self.update()

    def paintEvent(self, event):
        """Draw bar chart"""
        if not self.categories:
            return

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        padding = 10
        bar_height = 20
        spacing = 8

        y_pos = padding
        for category_name, category_data in self.categories.items():
            size = category_data["size"]
            percentage = (size / self.total_size * 100) if self.total_size > 0 else 0

            bar_width = (self.width() - 2 * padding - 100) * (percentage / 100)

            color = CATEGORY_COLORS.get(category_name, QColor(128, 128, 128))
            painter.fillRect(padding, y_pos, bar_width, bar_height, color)

            label_text = f"{category_name.capitalize()}"
            size_text = f"{format_size(size)} ({percentage:.1f}%)"

            painter.setFont(QFont("Arial", 10))
            painter.drawText(
                padding + bar_width + 10,
                y_pos + bar_height - 5,
                f"{label_text}"
            )

            painter.setFont(QFont("Arial", 8))
            painter.setPen(QColor(128, 128, 128))
            painter.drawText(
                padding + bar_width + 10,
                y_pos + bar_height + 8,
                size_text
            )

            y_pos += bar_height + spacing