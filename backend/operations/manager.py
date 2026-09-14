from backend.operations.scanner import FileScanner
import send2trash
from pathlib import Path

class FileManager:
    """File management after scanning"""

    @staticmethod
    def update_scan_results(scan_result: dict, deleted_paths: list[str]) -> dict:
        """ Update scan results after file deletion

        Args:
            scan_result: scanning result
            deleted_paths: paths to deleted files

        Returns:
            Updated scanning result
        """
        scan_result["all_files"] = [
            f for f in scan_result["all_files"]
            if f["path"] not in deleted_paths
        ]

        scanner = FileScanner.Scanner("")
        scanner.all_files = scan_result["all_files"]
        scan_result["statistics"] = scanner.calculate_statistics()

        return scan_result

    @staticmethod
    def delete_files(file_paths: list[str]) -> dict:
        """Delete files

        Args:
            file_paths: paths to selected files

        Returns:
            dict with deletion result:
            {
                "success": bool,
                "deleted": list,
                "failed": list,
                "total_freed_bytes": int
            }
        """
        deleted_files = []
        failed_files = []
        total_freed_bytes = 0

        for file_path in file_paths:
            try:
                file_size = Path(file_path).stat().st_size
                send2trash.send2trash(file_path)

                deleted_files.append({
                    "path": file_path,
                    "size": file_size
                })
                total_freed_bytes += file_size

            except Exception as e:
                failed_files.append({
                    "path": file_path,
                    "error": str(e)
                })

        return {
            "success": len(failed_files) == 0,
            "deleted": deleted_files,
            "failed": failed_files,
            "total_freed_bytes": total_freed_bytes
        }