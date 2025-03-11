import tkinter as tk
from tkinter import messagebox, ttk, colorchooser, filedialog
import json
import time
from datetime import datetime, timedelta
import threading
import os

TASKS_FILE = "tasks.json"
SETTINGS_FILE = "settings.json"

default_settings = {
    "theme": "light",
    "custom_color": "#ffffff",
    "reset_hour": 0,  # Default reset at midnight (0:00)
    "reset_minute": 0,
    "window_width": 600,
    "window_height": 400,
    "tab_order": ["Dailies"]
}

# Default daily tasks
daily_tasks = ["Physical Win", "Mental Win", "Spiritual Win"]

def load_json(file, default):
    try:
        with open(file, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return default

def save_json(file, data):
    with open(file, "w") as f:
        json.dump(data, f, indent=4)

def import_json(file_type):
    """Import JSON file for tasks or settings"""
    file_path = filedialog.askopenfilename(
        title=f"Import {file_type.capitalize()}",
        filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
    )
    if not file_path:
        return None
    
    try:
        with open(file_path, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        messagebox.showerror("Error", f"Failed to import file: {e}")
        return None

# Load tasks and settings
tasks = load_json(TASKS_FILE, {"Dailies": daily_tasks})
task_states = load_json("task_states.json", {})
settings = load_json(SETTINGS_FILE, default_settings)

# Ensure tab_order exists in settings
if "tab_order" not in settings:
    settings["tab_order"] = list(tasks.keys())

def save_tasks():
    save_json(TASKS_FILE, tasks)

def save_settings():
    save_json(SETTINGS_FILE, settings)

def save_task_states():
    save_json("task_states.json", task_states)

def add_task(tab_name, entry_widget, listbox):
    task = entry_widget.get().strip()
    if task and task not in tasks[tab_name]:
        tasks[tab_name].append(task)
        save_tasks()
        update_list(tab_name, listbox)
    entry_widget.delete(0, tk.END)

def delete_task(tab_name, listbox):
    selected = listbox.curselection()
    if selected:
        task_text = listbox.get(selected[0])
        tasks[tab_name].remove(task_text)
        # Remove task state if exists
        task_key = f"{tab_name}:{task_text}"
        if task_key in task_states:
            del task_states[task_key]
            save_task_states()
        save_tasks()
        update_list(tab_name, listbox)

def mark_done(tab_name, listbox):
    selected = listbox.curselection()
    if selected:
        idx = selected[0]
        task_text = listbox.get(idx)
        task_key = f"{tab_name}:{task_text}"
        
        # Toggle completion state
        if task_key in task_states and task_states[task_key]["completed"]:
            task_states[task_key]["completed"] = False
            listbox.itemconfig(idx, {'fg': 'black' if settings["theme"] == "light" else 'white'})
        else:
            task_states[task_key] = {"completed": True, "date_completed": datetime.now().strftime("%Y-%m-%d")}
            listbox.itemconfig(idx, {'fg': 'gray'})
        
        save_task_states()

def update_list(tab_name, listbox):
    listbox.delete(0, tk.END)
    for task in tasks[tab_name]:
        listbox.insert(tk.END, task)
        
        # Apply completed state if task is marked as done
        task_key = f"{tab_name}:{task}"
        if task_key in task_states and task_states[task_key]["completed"]:
            idx = listbox.size() - 1
            listbox.itemconfig(idx, {'fg': 'gray'})

def add_tab():
    new_tab_name = tab_entry.get().strip()
    if new_tab_name and new_tab_name not in tasks:
        tasks[new_tab_name] = []
        # Add to tab order
        settings["tab_order"].append(new_tab_name)
        save_tasks()
        save_settings()
        create_tab(new_tab_name)
    tab_entry.delete(0, tk.END)

def delete_tab():
    current_tab_idx = notebook.index(notebook.select())
    if current_tab_idx >= 0:
        tab_name = notebook.tab(current_tab_idx, "text")
        
        # Prevent deletion of "Dailies" tab
        if tab_name == "Dailies":
            messagebox.showinfo("Cannot Delete", "The Dailies tab cannot be deleted.")
            return
        
        # Confirm deletion
        if messagebox.askyesno("Confirm Delete", f"Delete tab '{tab_name}' and all its tasks?"):
            notebook.forget(current_tab_idx)
            
            # Remove from tasks and task_states
            if tab_name in tasks:
                del tasks[tab_name]
                # Remove all task states for this tab
                for key in list(task_states.keys()):
                    if key.startswith(f"{tab_name}:"):
                        del task_states[key]
                
                # Remove from tab order
                if tab_name in settings["tab_order"]:
                    settings["tab_order"].remove(tab_name)
                
                save_tasks()
                save_task_states()
                save_settings()

def create_tab(tab_name):
    frame = ttk.Frame(notebook)
    notebook.add(frame, text=tab_name)
    
    listbox = tk.Listbox(frame, width=50, height=10, bg=settings["custom_color"],
                        fg="black" if settings["theme"] == "light" else "white")
    listbox.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
    update_list(tab_name, listbox)
    
    scrollbar = tk.Scrollbar(frame, orient=tk.VERTICAL, command=listbox.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    listbox.config(yscrollcommand=scrollbar.set)
    
    entry = tk.Entry(frame, width=50)
    entry.pack(pady=5)
    
    btn_frame = tk.Frame(frame, bg=settings["custom_color"])
    btn_frame.pack()
    
    add_btn = tk.Button(btn_frame, text="Add Task", 
                      command=lambda: add_task(tab_name, entry, listbox))
    add_btn.pack(side=tk.LEFT, padx=5)
    
    delete_btn = tk.Button(btn_frame, text="Delete Task", 
                        command=lambda: delete_task(tab_name, listbox))
    delete_btn.pack(side=tk.LEFT, padx=5)
    
    mark_btn = tk.Button(btn_frame, text="Toggle Completion", 
                      command=lambda: mark_done(tab_name, listbox))
    mark_btn.pack(side=tk.LEFT, padx=5)
    
    # Return a dictionary of widgets for this tab for easier theme management
    return {
        "frame": frame,
        "listbox": listbox,
        "entry": entry,
        "btn_frame": btn_frame,
        "buttons": [add_btn, delete_btn, mark_btn]
    }

# Dictionary to keep track of all tab widgets
tab_widgets = {}

def toggle_theme():
    settings["theme"] = "dark" if settings["theme"] == "light" else "light"
    save_settings()
    apply_theme()

def get_all_widgets(parent):
    """Recursively get all widgets inside a parent widget"""
    all_widgets = [parent]
    if hasattr(parent, 'winfo_children'):
        children = parent.winfo_children()
        for child in children:
            all_widgets.extend(get_all_widgets(child))
    return all_widgets

def apply_theme():
    bg_color = "#333" if settings["theme"] == "dark" else "#fff"
    fg_color = "#fff" if settings["theme"] == "dark" else "#000"
    
    style = ttk.Style()
    style.configure("TFrame", background=bg_color)
    style.configure("TNotebook", background=bg_color)
    style.configure("TNotebook.Tab", background=bg_color, foreground=fg_color)
    
    root.configure(bg=bg_color)
    
    # Update all frames and their children with the new theme
    for tab_id in notebook.tabs():
        tab = notebook.nametowidget(tab_id)
        for widget in get_all_widgets(tab):
            if isinstance(widget, tk.Frame) or isinstance(widget, ttk.Frame):
                try:
                    widget.configure(bg=bg_color)
                except:
                    pass  # Some ttk widgets might not have bg option
            if hasattr(widget, 'configure'):
                try:
                    if 'fg' in widget.config():
                        widget.configure(fg=fg_color)
                    if 'bg' in widget.config() and not isinstance(widget, tk.Listbox):
                        widget.configure(bg=bg_color)
                except:
                    pass  # Ignore widgets that don't have these configs
    
    # Update main UI elements
    for widget in [theme_btn, color_btn, tab_entry, add_tab_btn, import_settings_btn, 
                  import_tasks_btn, delete_tab_btn, hour_entry, minute_entry, reset_btn,
                  top_frame, tab_frame, reset_frame, reset_all_btn]:
        if widget and hasattr(widget, 'configure'):
            try:
                if 'bg' in widget.config():
                    widget.configure(bg=bg_color)
                if 'fg' in widget.config():
                    widget.configure(fg=fg_color)
            except:
                pass  # Ignore if can't configure
    
    # Update any top-level frames
    for widget in get_all_widgets(root):
        if isinstance(widget, tk.Label):
            try:
                widget.configure(bg=bg_color, fg=fg_color)
            except:
                pass
    
    # Apply custom color to listboxes
    apply_custom_color()

def pick_color():
    color_code = colorchooser.askcolor(title="Choose Background Color")[1]
    if color_code:
        settings["custom_color"] = color_code
        save_settings()
        apply_custom_color()

def apply_custom_color():
    # Update all listboxes with the custom color
    for tab_id in notebook.tabs():
        tab = notebook.nametowidget(tab_id)
        for widget in get_all_widgets(tab):
            if isinstance(widget, tk.Listbox):
                widget.config(bg=settings["custom_color"])

def set_reset_time():
    try:
        hour = int(hour_entry.get())
        minute = int(minute_entry.get())
        
        if 0 <= hour < 24 and 0 <= minute < 60:
            settings["reset_hour"] = hour
            settings["reset_minute"] = minute
            save_settings()
            messagebox.showinfo("Success", "Reset time updated!")
        else:
            messagebox.showerror("Error", "Hours must be 0-23 and minutes 0-59.")
    except ValueError:
        messagebox.showerror("Error", "Enter valid numbers for hour and minute.")

def reset_all_tasks():
    if messagebox.askyesno("Confirm Reset", "Reset all tasks to uncompleted state?"):
        # Clear all task states
        global task_states
        task_states = {}
        save_task_states()
        
        # Refresh all listboxes
        for tab_id in notebook.tabs():
            tab = notebook.nametowidget(tab_id)
            for widget in get_all_widgets(tab):
                if isinstance(widget, tk.Listbox):
                    tab_name = notebook.tab(notebook.index(tab_id), "text")
                    update_list(tab_name, widget)

def reset_dailies():
    """Reset daily tasks to their default state"""
    if "Dailies" in tasks:
        tasks["Dailies"] = daily_tasks.copy()
        
        # Reset completion states for daily tasks
        for task in daily_tasks:
            task_key = f"Dailies:{task}"
            if task_key in task_states:
                del task_states[task_key]
        
        save_tasks()
        save_task_states()
        
        # Update the Dailies listbox if it exists
        for tab_id in notebook.tabs():
            tab_name = notebook.tab(notebook.index(tab_id), "text")
            if tab_name == "Dailies":
                tab = notebook.nametowidget(tab_id)
                for widget in get_all_widgets(tab):
                    if isinstance(widget, tk.Listbox):
                        update_list("Dailies", widget)
                        break
                break

def scheduled_reset():
    """Handles daily, weekly, and monthly task resets"""
    last_reset_day = datetime.now().day
    last_reset_week = datetime.now().isocalendar()[1]  # ISO week number
    last_reset_month = datetime.now().month
    
    while True:
        now = datetime.now()
        current_day = now.day
        current_week = now.isocalendar()[1]
        current_month = now.month
        
        # Check for daily reset time
        if now.hour == settings["reset_hour"] and now.minute == settings["reset_minute"]:
            if current_day != last_reset_day:
                reset_dailies()
                last_reset_day = current_day
                
                # Reset any tab marked as "Daily"
                for tab_name in tasks.keys():
                    if tab_name.lower().endswith("daily") or tab_name == "Dailies":
                        # Clear completion states for this tab
                        for key in list(task_states.keys()):
                            if key.startswith(f"{tab_name}:"):
                                del task_states[key]
        
        # Weekly reset (check if week number changed)
        if current_week != last_reset_week:
            for tab_name in tasks.keys():
                if tab_name.lower().endswith("weekly"):
                    # Clear completion states for weekly tabs
                    for key in list(task_states.keys()):
                        if key.startswith(f"{tab_name}:"):
                            del task_states[key]
            last_reset_week = current_week
        
        # Monthly reset (check if month changed)
        if current_month != last_reset_month:
            for tab_name in tasks.keys():
                if tab_name.lower().endswith("monthly"):
                    # Clear completion states for monthly tabs
                    for key in list(task_states.keys()):
                        if key.startswith(f"{tab_name}:"):
                            del task_states[key]
            last_reset_month = current_month
        
        # Save state changes if any resets occurred
        save_task_states()
        
        # Sleep for a bit to prevent high CPU usage
        time.sleep(30)

def on_tab_reorder(event):
    """Handle tab reordering via drag and drop"""
    x, y = event.x_root, event.y_root
    tab_idx = notebook.index("@%d,%d" % (x, y))
    
    if tab_idx >= 0:
        # Get the currently selected tab
        selected_tab = notebook.select()
        selected_idx = notebook.index(selected_tab)
        
        if selected_idx != tab_idx:
            # Get tab names
            tab_name = notebook.tab(selected_idx, "text")
            
            # Update the tab order in settings
            tab_order = settings["tab_order"]
            if tab_name in tab_order:
                tab_order.remove(tab_name)
                tab_order.insert(tab_idx, tab_name)
                settings["tab_order"] = tab_order
                save_settings()
            
            # Actually reorder the tab in the notebook
            notebook.forget(selected_idx)
            create_tab(tab_name)
            notebook.select(tab_idx)

def import_settings_from_file():
    """Import settings from a JSON file"""
    new_settings = import_json("settings")
    if new_settings:
        global settings
        # Validate imported settings
        for key in default_settings:
            if key not in new_settings:
                new_settings[key] = default_settings[key]
        
        settings = new_settings
        save_settings()
        
        # Apply imported settings
        apply_theme()
        apply_custom_color()
        
        # Update UI elements
        hour_entry.delete(0, tk.END)
        hour_entry.insert(0, str(settings["reset_hour"]))
        
        minute_entry.delete(0, tk.END)
        minute_entry.insert(0, str(settings["reset_minute"]))
        
        messagebox.showinfo("Import Successful", "Settings imported successfully!")

def import_tasks_from_file():
    """Import tasks from a JSON file"""
    new_tasks = import_json("tasks")
    if new_tasks:
        global tasks
        tasks = new_tasks
        save_tasks()
        
        # Clear and recreate tabs
        for tab_id in notebook.tabs():
            notebook.forget(0)  # Remove all tabs
        
        # Update tab order if needed
        if "tab_order" not in settings or not settings["tab_order"]:
            settings["tab_order"] = list(tasks.keys())
            save_settings()
        
        # Create tabs in the correct order
        for tab_name in settings["tab_order"]:
            if tab_name in tasks:
                create_tab(tab_name)
        
        messagebox.showinfo("Import Successful", "Tasks imported successfully!")

def auto_resize_window():
    """Resize window based on number of tasks"""
    total_tasks = sum(len(task_list) for task_list in tasks.values())
    
    # Base size
    width = max(600, min(800, 600 + (total_tasks * 5)))
    height = max(400, min(700, 400 + (total_tasks * 10)))
    
    # Update settings
    settings["window_width"] = width
    settings["window_height"] = height
    save_settings()
    
    # Set the new window size
    root.geometry(f"{width}x{height}")

# GUI Setup
root = tk.Tk()
root.title("Kaizen Task Manager")
root.geometry(f"{settings.get('window_width', 600)}x{settings.get('window_height', 400)}")

# Main top frame for controls
top_frame = tk.Frame(root)
top_frame.pack(fill=tk.X, pady=5)

theme_btn = tk.Button(top_frame, text="Toggle Theme", command=toggle_theme)
theme_btn.pack(side=tk.LEFT, padx=5)

color_btn = tk.Button(top_frame, text="Choose Custom Color", command=pick_color)
color_btn.pack(side=tk.LEFT, padx=5)

import_settings_btn = tk.Button(top_frame, text="Import Settings", command=import_settings_from_file)
import_settings_btn.pack(side=tk.LEFT, padx=5)

import_tasks_btn = tk.Button(top_frame, text="Import Tasks", command=import_tasks_from_file)
import_tasks_btn.pack(side=tk.LEFT, padx=5)

reset_all_btn = tk.Button(top_frame, text="Reset All Tasks", command=reset_all_tasks)
reset_all_btn.pack(side=tk.RIGHT, padx=5)

delete_tab_btn = tk.Button(top_frame, text="Delete Current Tab", command=delete_tab)
delete_tab_btn.pack(side=tk.RIGHT, padx=5)

# Create notebook and tabs
notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill="both")

# Enable tab reordering with mouse drag
notebook.bind("<B1-Motion>", on_tab_reorder)

# Tab creation controls
tab_frame = tk.Frame(root)
tab_frame.pack(fill=tk.X, pady=5)

tab_entry = tk.Entry(tab_frame, width=20)
tab_entry.pack(side=tk.LEFT, padx=5)

add_tab_btn = tk.Button(tab_frame, text="Add Tab", command=add_tab)
add_tab_btn.pack(side=tk.LEFT)

# Reset time UI
reset_frame = tk.Frame(root)
reset_frame.pack(pady=5, fill=tk.X)

tk.Label(reset_frame, text="Daily Reset Time (HH:MM)").pack(side=tk.LEFT, padx=5)

hour_entry = tk.Entry(reset_frame, width=3)
hour_entry.insert(0, str(settings["reset_hour"]))
hour_entry.pack(side=tk.LEFT)

tk.Label(reset_frame, text=":").pack(side=tk.LEFT)

minute_entry = tk.Entry(reset_frame, width=3)
minute_entry.insert(0, str(settings["reset_minute"]))
minute_entry.pack(side=tk.LEFT)

reset_btn = tk.Button(reset_frame, text="Set Time", command=set_reset_time)
reset_btn.pack(side=tk.LEFT, padx=5)

# Create tabs based on tab_order setting
for tab_name in settings["tab_order"]:
    if tab_name in tasks:
        create_tab(tab_name)

# Start reset thread
threading.Thread(target=scheduled_reset, daemon=True).start()

# Auto-resize based on task count every 2 minutes
def resize_timer():
    auto_resize_window()
    root.after(120000, resize_timer)  # 2 minutes in milliseconds

root.after(1000, resize_timer)  # Start after 1 second

# Apply theme and custom color
apply_theme()
apply_custom_color()

root.mainloop()