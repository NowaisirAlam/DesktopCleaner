# 🧹 Desktop Cleaner — Automated File Organizer (Python)

DesktopCleaner is a lightweight Python tool that automatically organizes and sorts files on your desktop.  
It monitors your desktop folder in real time and moves files (images, documents, videos, audio, zips, etc.) into categorized folders.

This keeps your desktop clean, organized, and clutter-free — automatically.

---

## 🚀 Features

- 📂 **Auto-Sort Files** by type (Images, Documents, Videos, Audio, Archives, Code, etc.)
- 🔄 **Real-Time Monitoring** using `watchdog`
- 🧠 **Duplicate File Handling** (smart rename: file(1).png, file(2).png…)
- ⚡ **Fast, silent, background operation**
- 🪟 **Windows-friendly** paths & OS handling
- 📝 **Log messages** to track movements

---

## 🛠️ Tech Stack

- **Python 3**
- `watchdog` (file system event monitoring)
- `os`, `shutil`, `time` (core file operations)
- `pathlib` (clean path handling)
- **(Optional)** Tkinter UI (if you add one later)

---

## 📦 Installation

Clone the repository:

```bash
git clone https://github.com/NowaisirAlam/DesktopCleaner.git
cd DesktopCleaner
