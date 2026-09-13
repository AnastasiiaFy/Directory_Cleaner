from backend.operations.scanner import FileScanner
from backend.operations.filter import FileFilter
from backend.operations.manager import FileManager
from backend.operations.history import DeletionHistory


class FileSystemService:
    """Service for work with file system"""

    def __init__(self, history_file: str = "deletion_history.json"):
        self.scanner = FileScanner()
        self.filter = FileFilter()
        self.manager = FileManager()
        self.history = DeletionHistory(history_file)
        self.current_scan_result = None

    # ==================== СКАНУВАННЯ ====================
    def scan_directory(self, start_path: str) -> dict:
        self.current_scan_result = self.scanner.scan(start_path)
        return self.current_scan_result

    def rescan_directory(self, start_path: str) -> dict:
        return self.scan_directory(start_path)

    # ==================== ФІЛЬТРАЦІЯ І СОРТУВАННЯ ====================
    def apply_sort(self, files: list[dict], sort_by: str):
        return self.filter.sort_files(files, sort_by)

    def apply_filter_by_time(self, files: list[dict], days: int, older: bool = False) -> list[dict]:
        """
        Filters files by last modification time

        Args:
            files: list of files
            days: number of days
            older: True for files older than N days

        Returns:
            filtered list of files
        """
        return self.filter.filter_by_time(files, days, older)

    # ==================== ВИДАЛЕННЯ ФАЙЛІВ ====================
    def delete_selected_files(self, file_paths: list[str]) -> dict:
        """Delete selected files

        Args:
            file_paths: list of paths to selected files

        Returns:
            status of deletion
        """
        result = self.manager.delete_files(file_paths)

        # Зберігаємо в історію якщо успішно видалилось
        if result["deleted"]:
            self.history.add_deletion(result["deleted"], result["total_freed_bytes"])

        # Оновлюємо поточний результат сканування
        if self.current_scan_result:
            self.current_scan_result = self.manager.update_scan_results(
                self.current_scan_result,
                file_paths
            )

        return result

    def get_current_scan_result(self) -> dict:
        return self.current_scan_result