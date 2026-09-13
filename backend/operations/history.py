import json
from pathlib import Path
from datetime import datetime
from getpass import getuser
from typing import List


class DeletionHistory:
    """File deletion management"""

    def __init__(self, history_file: str = "deletion_history.json"):
        self.history_file_path = Path(history_file)
        self.ensure_file_exists()

    def ensure_file_exists(self):
        """Create history file if it doesn't exist"""
        if not self.history_file_path.exists():
            self.history_file_path.write_text(json.dumps({"deletions": []}, indent=2))

    def add_deletion(self, deleted_files: List[dict], freed_size: int) -> bool:
        """Add deletion record to the history

        Args:
            deleted_files: list of files with information about deletion

            Список словників з інформацією про видалені файли
            freed_size: total size of deleted files (in bytes)

        Returns:
            True if deletion successful
        """
        try:
            with open(self.history_file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            deletion_record = {
                "timestamp": datetime.now().isoformat(),
                "user": getuser(),
                "total_size_freed_bytes": freed_size,
                "files_deleted_count": len(deleted_files),
                "files_failed_count": 0,
                "deleted_files": [
                    {
                        "path": f["path"],
                        "size_bytes": f["size"],
                        "status": "deleted"
                    }
                    for f in deleted_files
                ]
            }

            data["deletions"].append(deletion_record)

            with open(self.history_file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

            return True

        except Exception as e:
            print(f"Error saving deletion history: {e}")
            return False