import sys
from pathlib import Path
from PySide6.QtWidgets import QApplication, QFileDialog
from ui.main_window import MainWindow


def get_initial_directory():
    """Shows a dialog window for selection folder at startup"""
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)

    folder = QFileDialog.getExistingDirectory(
        None,
        "Select a directory to analyze",
        str(Path.home()),
        QFileDialog.ShowDirsOnly
    )

    return folder


def main():
    app = QApplication(sys.argv)
    selected_folder = get_initial_directory()

    if not selected_folder:
        print("No folder selected. Exiting.")
        sys.exit(0)

    window = MainWindow(selected_folder)
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()