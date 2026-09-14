import platform
import os
from pathlib import Path


# ============ УНІВЕРСАЛЬНІ КОНСТАНТИ КАТЕГОРІЇ ФАЙЛІВ ============
FILE_CATEGORIES = {
    "Images":           [".jpg", ".jpeg", ".gif", ".webp", ".bmp", ".svg", ".ico", ".tiff", ".heic", ".heif", ".png"],
    "Documents":        [".pdf", ".doc", ".docx", ".txt", ".md", ".pages", ".odt", ".rtf", ".epub"],
    "Spreadsheets":     [".xls", ".xlsx", ".numbers", ".csv", ".tsv", ".ods"],
    "Presentations":    [".ppt", ".pptx", ".key"],
    "Video":            [".mp4", ".mkv", ".mov", ".avi", ".flv", ".wmv", ".webm", ".mpeg", ".mpg"],
    "Audio":            [".mp3", ".m4a", ".wav", ".flac", ".aac", ".wma"],
    "Archives":         [".zip", ".rar", ".7z", ".tar", ".gz", ".bz2", ".xz"],
    "Code":             [".py", ".ipynb", ".js", ".ts", ".java", ".cpp", ".c", ".swift", ".go", ".rs", ".html", ".css", ".json"],
    "Other":            []
}

# ============ КОЛЬОРИ КАТЕГОРІЙ ============
CATEGORY_COLORS = {
    "Spreadsheets":  "#91C499",
    "Audio": "#AEECEF",
    "Video": "#AA3E98",
    "Documents": "#188FA7",
    "Images": "#FFBF46",
    "Presentations": "#523249",
    "Archives": "#B49FCC",
    "Code": "#8ACB88",
    "Other": "#CCCCCC",
}


def get_platform() -> str:
    system = platform.system()
    if system == "Darwin":
        return "macos"
    elif system == "Windows":
        return "windows"
    else:
        return "unknown"


# ============ MACOS ============
MACOS_EXCLUDED_DIRS = {
    "/System",
    "/Library",
    "/Volumes",
    "/Applications",
    "/Cores",
    "/private/var",
    "/usr/local/bin",
    "/opt/homebrew",
}

# ============ WINDOWS ============
WINDOWS_EXCLUDED_DIRS = {
    "C:\\Windows",
    "C:\\Program Files",
    "C:\\Program Files (x86)",
    "C:\\ProgramData",
    "C:\\$Recycle.Bin",
    "C:\\System Volume Information",
}

PLATFORM_CONFIG = {
    "macos": {
        "excluded_dirs": MACOS_EXCLUDED_DIRS,
        "path_separator": "/",
        "case_sensitive": True,
        "temp_dir": Path.home() / "Library" / "Caches",
    },
    "windows": {
        "excluded_dirs": WINDOWS_EXCLUDED_DIRS,
        "path_separator": "\\",
        "case_sensitive": False,
        "temp_dir": Path(os.getenv("TEMP", "C:\\Temp")),
    }
}

CURRENT_PLATFORM = get_platform()

CURRENT_CONFIG = PLATFORM_CONFIG.get(CURRENT_PLATFORM, PLATFORM_CONFIG["windows"]) 

EXCLUDED_DIRS = CURRENT_CONFIG["excluded_dirs"]


if __name__ == "__main__":
    print(f"Current Platform: {CURRENT_PLATFORM}")
    print(f"Excluded Dirs: {EXCLUDED_DIRS}")
    print(f"Temp Dir: {CURRENT_CONFIG['temp_dir']}")