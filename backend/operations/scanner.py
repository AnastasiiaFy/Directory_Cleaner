from pathlib import Path
from utils.file_constants import FILE_CATEGORIES, EXCLUDED_DIRS


class FileScanner:
    """Scan directory and collect statistics about file categories"""

    @staticmethod
    def scan(start_path: str) -> dict:
        """Recursively scan directory"""
        scanner = FileScanner.Scanner(start_path)
        return scanner.scan()

    class Scanner:
        def __init__(self, start_path: str):
            """
            Args:
                start_path: path to directory
            """
            self.start_path = Path(start_path)
            self.all_files = None

        def scan(self) -> dict:
            """Recursively scan directory"""
            self.all_files = []
            self._walk_directory(self.start_path)

            return {
                "all_files": self.all_files,
                "statistics": self.calculate_statistics()
            }


        def calculate_statistics(self):
            """Calculate statistics from list of files"""
            stats = {
                "total_size": 0,
                "total_count": len(self.all_files),
                "by_category": {category: {"size": 0, "count": 0}
                                for category in FILE_CATEGORIES}
            }

            for file_info in self.all_files:
                size = file_info["size"]
                stats["total_size"] += size

                category = file_info["category"]

                stats["by_category"][category]["size"] += size
                stats["by_category"][category]["count"] += 1

            return stats


        def _walk_directory(self, path: Path) -> None:
            try:
                for item in path.iterdir():
                    # Пропускаємо приховані файли
                    if  self.is_excluded(item) or item.name.startswith('.'):
                        continue

                    if item.is_dir():
                        self._walk_directory(item)
                    elif item.is_file():
                        self._process_file(item)

            except Exception as e:
                print(f"Error walking {path}: {e}")


        def _process_file(self, file_path: Path) -> None:
            """Processes one file"""
            try:
                file_stat = file_path.stat()         # Метадані файлу
                size = file_stat.st_size
                modified_time = file_stat.st_mtime   # Unix timestamp

                extension = file_path.suffix.lower()
                category = self.get_category(extension)

                file_info = {
                    "path": str(file_path),
                    "name": file_path.name,
                    "size": size,
                    "extension": extension,
                    "category": category,
                    "modified_time": modified_time,
                    "is_selected": False
                }
                self.all_files.append(file_info)

            except Exception as e:
                print(f"Error processing file {file_path}: {e}")

        @staticmethod
        def get_category(extension: str) -> str:
            """Defines file category by extension"""
            for category, extensions in FILE_CATEGORIES.items():
                if extension in extensions:
                    return category
            return "other"

        @staticmethod
        def is_excluded(path: Path) -> bool:
            """Checks if the directory is excluded"""
            return str(path) in EXCLUDED_DIRS