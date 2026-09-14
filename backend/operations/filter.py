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
