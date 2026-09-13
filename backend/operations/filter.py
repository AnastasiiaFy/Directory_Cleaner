from time import time

class FileFilter:
    """Filter and Sort list of files"""

    @staticmethod
    def sort_files(files: list[dict], sort_by: str = "modified_time") -> list[dict]:
        """Sort files by parameter"""
        if sort_by == "modified_time":
            return sorted(files, key=lambda f: f["modified_time"], reverse=True)
        elif sort_by == "name":
            return sorted(files, key=lambda f: f["name"])
        elif sort_by == "size":
            return sorted(files, key=lambda f: f["size"], reverse=True)
        elif sort_by == "extension":
            return sorted(files, key=lambda f: f["extension"])
        return files

    @staticmethod
    def filter_by_time(files: list[dict], days: int, older: bool = False) -> list[dict]:
        """Filter files by last modification time

        Args:
            files: list of files
            days: the number of days
            older:
                - False (by default): files modified for last N days
                - True: files modified more than N days ago
        Returns:
            List of filtered files
        """
        cutoff_time = time() - (days * 24 * 3600)

        if older:
            return [f for f in files if f["modified_time"] < cutoff_time]
        else:
            return [f for f in files if f["modified_time"] > cutoff_time]



# Тестування
if __name__ == "__main__":
    results = [
        {'path': '/Users/anastasiiafylypiv/Documents/TEST/spots.png',
         'name': 'spots.png',
         'size': 15774,
         'extension': '.png',
         'category': 'Images',
         'modified_time': 1785532853.2975307,
         'is_selected': False},
        {'path': '/Users/anastasiiafylypiv/Documents/TEST/ -2.jpg',
         'name': ' -2.jpg',
         'size': 188615,
         'extension': '.jpg',
         'category': 'Images',
         'modified_time': 1731614870.7118936,
         'is_selected': False},
        {'path': '/Users/anastasiiafylypiv/Documents/TEST/photo_2026-08-06 20.06.01.jpeg',
         'name': 'photo_2026-08-06 20.06.01.jpeg',
         'size': 81710,
         'extension': '.jpeg',
         'category': 'Images',
         'modified_time': 1786035952.533495,
         'is_selected': False},
        {'path': '/Users/anastasiiafylypiv/Documents/TEST/TEST_inner/Clip_8.mov',
         'name': 'Clip_8.mov',
         'size': 89285517,
         'extension': '.mov',
         'category': 'Video',
         'modified_time': 1477515153.0,
         'is_selected': False}
        ]

    print(FileFilter.filter_by_time(results,60))