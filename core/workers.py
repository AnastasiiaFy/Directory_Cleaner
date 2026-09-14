from PySide6.QtCore import QThread, Signal
from backend.service import FileSystemService
import traceback

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



class ImageAnalysisWorker(QThread):
    """Worker for analysing similar images in the separate thread"""

    finished = Signal(dict)  # dict з дублікатами
    error = Signal(str)

    def __init__(self, service: FileSystemService, files: list):
        super().__init__()
        self.service = service
        self.files = files

    def run(self):
        try:
            duplicates = self.service.find_similar_images(self.files)
            self.finished.emit(duplicates)
        except Exception as e:
            error_traceback = traceback.format_exc()
            print(f"ImageAnalysisWorker Error:\n{error_traceback}")
            self.error.emit(f"{str(e)}\n\nDetails:\n{error_traceback}")