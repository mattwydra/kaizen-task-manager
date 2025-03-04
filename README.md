# Kaizen Task Manager

Kaizen Task Manager is a lightweight and customizable to-do list application designed for personal productivity. Inspired by the Kaizen philosophy of continuous improvement, this tool helps users manage daily, weekly, and custom tasks efficiently.

## Features & Goals
The goal of Kaizen Task Manager is to provide an intuitive and flexible task management experience, including:
- **Daily and Custom Tasks**: Predefined daily tasks with the ability to add user-defined ones.
- **Persistent Storage**: Saves tasks locally in `tasks.json`.
- **Task Management**: Add, delete, and mark tasks as completed.
- **Tab System**: Organize tasks into multiple categories.

---

## Links to each README
- **[v1](v1/README.md)**
- **[v2](v2/README.md)**
- **[v3](v3/README.md)**

---

## Planned Updates (v3.0 and beyond)
- **Customization & UI Improvements**: Dark mode, drag-and-drop tab reordering, and adaptive UI scaling.
- **Persistent State**: Remember task completion states on restart.
- **Reset Tasks**: Toggle to reset all tasks as "undone."
- **Scheduled Refresh**: Daily, weekly, and monthly resets for respective tabs.
- **Dark Mode**: UI redesigned with a dark theme.
- **Auto-Scaling Window**: Adjusts dynamically based on task count.
- **Rearrange Tabs**: Click and drag to reorder categories.
- **Delete Tabs**: Option to remove tabs (except the default "Dailies" tab).

---

## Building the Executable
To create a standalone `.exe` file for Windows, use PyInstaller:
```sh
python -m PyInstaller --onefile -w .\local_kaizen.py
```
- `--onefile`: Packages everything into a single executable.
- `-w`: Runs the app without a terminal window (for GUI applications).
- `local_kaizen.py`: Replace with the actual script filename if different.

After running the command, the executable will be available in the `dist/` directory.

---

🚀 **Kaizen = Continuous Improvement!**

