from PySide6.QtCore import QThread, Signal
from backend.service import FileSystemService


class ScannerWorker(QThread):
    """Worker for scanning directory in the separate thread"""

    finished = Signal(dict)
    error = Signal(str)

    def __init__(self, service: FileSystemService, start_path: str):
        super().__init__()
        self.service = service
        self.start_path = start_path

    def run(self):
        try:
            results = self.service.scan_directory(self.start_path)
            self.finished.emit(results)
        except Exception as e:
            self.error.emit(str(e))