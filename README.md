# Directory Cleaner - Desktop Application

## About this project:

This is a **professional practice project** developed during a technology internship at **ELEKS** — a leading software development company. The project demonstrates full-stack desktop application development using modern Python technologies and machine learning techniques.

## Overview:

**Directory Cleaner** is a cross-platform desktop application designed to help users analyze, organize, and manage files on their computer. The application provides file management capabilities, including duplicate detection, file filtering, sorting, and secure deletion.

### Key Highlights:
- **Cross-platform support**: macOS and Windows
- **Intelligent image analysis**: Uses ResNet18 for finding visually similar images
- **Comprehensive file management**: Delete, filter, sort, and organize files
- **Deletion history**: Tracks all deleted files with timestamps and user information
- **Professional UI**: Modern PySide6-based interface

---
## Features:

### Core Functionality
- **Directory Scanning**: Recursive scanning of directories with real-time statistics
- **File Statistics**: Categorized file analysis (Images, Documents, Video, Audio, Archives, Code, etc.)
- **Category Visualization**: Interactive bar charts showing file distribution by category
- **Deletion History**: JSON-based tracking of all deleted files with user, timestamp and list of deleted files (check deletion_history_sample.json)
- **Rescan**: Update file list after external changes

### Filtering & Sorting
- **Time-based Filtering**: Filter files by modification time (Last 24h, 3 days, week, month, year, or older)
- **Multiple Sort Options**: Sort by name, size, date modified, or file extension

### Duplicate Detection
- **DL-Powered Image Analysis**: Uses ResNet18 to extract image embeddings
- **Similarity Detection**: Cosine similarity algorithm to find visually similar images
- **Smart Recommendations**: Highlights potential duplicate images group with different color for deletion

### File Selection & Management
- **Multi-select**: Checkbox selection for files with live counter
- **Confirmation Dialog**: Preview files and total size before deletion
- **Real-time Updates**: UI updates automatically after file operations

**Note:** Features cannot be used at the same time!

---

## Technology Stack

### Frontend
- **PySide6** - Modern Qt6-based GUI framework

### Backend
- **Python 3.8+** - Core programming language
- **PyTorch** - Deep learning framework for image embeddings
- **TorchVision** - Computer vision utilities and ResNet models
- **scikit-learn** - Machine learning library for cosine similarity
- **Pillow (PIL)** - Image processing library
- **send2trash** - Cross-platform trash/recycle bin interface

### Architecture
- **Thread-based Architecture**: Asynchronous operations with QThread workers
- **Service Layer Pattern**: Centralized backend service (`FileSystemService`)
- **MVC-like Structure**: Clean separation of UI and business logic

---

## System Requirements

- **Python**: 3.8 or higher
- **OS**: macOS or Windows
- **RAM**: Minimum 4GB (8GB+ recommended for large directory analysis)
- **GPU** (optional): CUDA-capable GPU or Apple Silicon for faster image analysis

---

## Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/AnastasiiaFy/Directory_Cleaner.git
cd Directory_Cleaner
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the Application

```bash
python3 main.py
```

When you launch the application, a dialog window will appear asking you to select the directory you want to analyze.

---

## Project Structure:
```bash
Directory_Cleaner/
├── backend/                 # Business logic layer
│ ├── service.py             # Central service facade
│ └── operations/
│   ├── scanner.py           # Directory scanning
│   ├── filter.py            # File filtering & sorting
│   ├── manager.py           # File operations (deletion, update)
│   ├── history.py           # Deletion history management
│   └── image_analyzer.py    # Image analysis & duplicate detection
│
├── ui/                      # User interface layer
│ ├── main_window.py         # Main application window
│ ├── widgets/
│ │ ├── chart.py             # File categories visualization
│ │ ├── selection_badge.py   # Badge for counting selected files
│ │ ├── file_list.py         # File table widget
│ │ └── sidebar.py           # Sidebar with file statistics
│ └── dialogs/
│   └── delete_confirmation_dialog.py  # Dialog widow for deletion confirmation
│
├── core/
│ └── worker.py             # QThread workers
│
├── utils/
│ ├── file_constants.py     # File categories & colors
│ └── helpers.py            # Utility functions
│
├── resources/              # UI resources (icons, images)
├── main.py                 # Application entry point
├── requirements.txt        # Python dependencies
├── deletion_history.json   # Deletion history (auto-generated)
└── README.md
```
