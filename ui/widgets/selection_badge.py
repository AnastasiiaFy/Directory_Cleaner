from PySide6.QtWidgets import QLabel
from PySide6.QtCore import Qt


class SelectionBadge(QLabel):
    """Badge with counter of selected files"""

    def __init__(self):
        super().__init__("0")
        self.setAlignment(Qt.AlignCenter)
        self.setFixedSize(40, 40)
        self.update_style(0)

    def set_count(self, count: int):
        """Updates the number of selected files"""
        self.setText(str(count))
        self.update_style(count)

    def update_style(self, count: int):
        """Updates the style and visibility of badge"""
        if count == 0:
            self.hide()
        else:
            self.show()

            self.setStyleSheet(f"""
                SelectionBadge {{
                    background-color: #75BBDF;
                    border-radius: 10px;
                    color: white;
                    font-weight: bold;
                    font-size: 14px;
                    
                    margin: 0px;
                    padding: 0px
                }}
            """)