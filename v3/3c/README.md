# Kaizen Task Manager v3.2

## Bug Fixes and Core Functionality:
1. **Persistent Task States**: Tasks now remember their completion status between sessions
2. **Theme Consistency**: Fixed issues with theme application to all widgets
3. **Proper Reset Functionality**: Both manual and scheduled resets are now working correctly

## Implemented New Features:
1. **Tab Management**:
   - Tab reordering via drag and drop
   - Tab deletion (with protection for the "Dailies" tab)
   - Proper tab order persistence

2. **Scheduled Resets**:
   - Daily, weekly, and monthly tab resets based on naming convention
   - Configurable reset time that persists between sessions

3. **Import Functionality**:
   - Added ability to import settings from JSON files
   - Added ability to import task lists from JSON files

4. **UI Improvements**:
   - Auto-scaling window based on task count
   - Better theme application across all widgets
   - Toggle completion instead of just marking done
   - More intuitive button layout

5. **Task Management**:
   - Reset all tasks button
   - Better organization of task states

## Issues:
   - Dark mode hides tasks

## How to Use:
- To create tabs with special reset intervals, use naming conventions like "Weekly" or "Monthly" at the end (e.g., "WorkWeekly", "ProjectsMonthly")
- Drag tabs to reorder them
- Toggle task completion instead of just marking as done
- All settings and tasks will persist between sessions
