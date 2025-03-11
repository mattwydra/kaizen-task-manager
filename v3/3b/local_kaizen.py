import tkinter as tk
from tkinter import messagebox, ttk, colorchooser
import json
import time
from datetime import datetime
import threading

TASKS_FILE = "tasks.json"
SETTINGS_FILE = "settings.json"

default_settings = {
    "theme": "light",
    "custom_color": "#ffffff",
    "reset_hour": 0,  # Default reset at midnight (0:00)
    "reset_minute": 0
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

tasks = load_json(TASKS_FILE, {"Dailies": daily_tasks})
settings = load_json(SETTINGS_FILE, default_settings)

def save_tasks():
    save_json(TASKS_FILE, tasks)

def save_settings():
    save_json(SETTINGS_FILE, settings)

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
        save_tasks()
        update_list(tab_name, listbox)

def mark_done(listbox):
    selected = listbox.curselection()
    if selected:
        listbox.itemconfig(selected[0], {'fg': 'gray'})

def update_list(tab_name, listbox):
    listbox.delete(0, tk.END)
    for task in tasks[tab_name]:
        listbox.insert(tk.END, task)

def add_tab():
    new_tab_name = tab_entry.get().strip()
    if new_tab_name and new_tab_name not in tasks:
        tasks[new_tab_name] = []
        save_tasks()
        create_tab(new_tab_name)
    tab_entry.delete(0, tk.END)

def create_tab(tab_name):
    frame = ttk.Frame(notebook)
    notebook.add(frame, text=tab_name)
    
    listbox = tk.Listbox(frame, width=50, height=10, bg=settings["custom_color"])
    listbox.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
    update_list(tab_name, listbox)
    
    scrollbar = tk.Scrollbar(frame, orient=tk.VERTICAL, command=listbox.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    listbox.config(yscrollcommand=scrollbar.set)
    
    entry = tk.Entry(frame, width=50)
    entry.pack(pady=5)
    
    btn_frame = tk.Frame(frame)
    btn_frame.pack()
    
    add_btn = tk.Button(btn_frame, text="Add Task", command=lambda: add_task(tab_name, entry, listbox))
    add_btn.pack(side=tk.LEFT, padx=5)
    
    delete_btn = tk.Button(btn_frame, text="Delete Task", command=lambda: delete_task(tab_name, listbox))
    delete_btn.pack(side=tk.LEFT, padx=5)
    
    mark_btn = tk.Button(btn_frame, text="Mark Done", command=lambda: mark_done(listbox))
    mark_btn.pack(side=tk.LEFT, padx=5)

def toggle_theme():
    settings["theme"] = "dark" if settings["theme"] == "light" else "light"
    save_settings()
    apply_theme()

def apply_theme():
    bg_color = "#333" if settings["theme"] == "dark" else "#fff"
    fg_color = "#fff" if settings["theme"] == "dark" else "#000"
    root.configure(bg=bg_color)
    for widget in root.winfo_children():
        widget.configure(bg=bg_color, fg=fg_color)

def pick_color():
    color_code = colorchooser.askcolor(title="Choose Background Color")[1]
    if color_code:
        settings["custom_color"] = color_code
        save_settings()
        apply_custom_color()

def apply_custom_color():
    for tab in notebook.winfo_children():
        for widget in tab.winfo_children():
            if isinstance(widget, tk.Listbox):
                widget.config(bg=settings["custom_color"])

def set_reset_time():
    try:
        settings["reset_hour"] = int(hour_entry.get())
        settings["reset_minute"] = int(minute_entry.get())
        save_settings()
        messagebox.showinfo("Success", "Reset time updated!")
    except ValueError:
        messagebox.showerror("Error", "Enter valid numbers for hour and minute.")

def reset_tasks():
    while True:
        now = datetime.now()
        if now.hour == settings["reset_hour"] and now.minute == settings["reset_minute"]:
            tasks["Dailies"] = daily_tasks.copy()
            save_tasks()
            for tab in notebook.winfo_children():
                for widget in tab.winfo_children():
                    if isinstance(widget, tk.Listbox):
                        update_list("Dailies", widget)
            time.sleep(60)  # Prevent multiple resets in one minute
        time.sleep(30)

# GUI Setup
root = tk.Tk()
root.title("Kaizen Task Manager")
root.geometry("600x400")

theme_btn = tk.Button(root, text="Toggle Theme", command=toggle_theme)
theme_btn.pack(pady=5)

color_btn = tk.Button(root, text="Choose Custom Color", command=pick_color)
color_btn.pack(pady=5)

notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill="both")

tab_entry = tk.Entry(root, width=20)
tab_entry.pack(pady=5)

for category in tasks.keys():
    create_tab(category)

# Reset time UI
reset_frame = tk.Frame(root)
reset_frame.pack(pady=10)
tk.Label(reset_frame, text="Set Reset Time (HH:MM)").pack()

hour_entry = tk.Entry(reset_frame, width=5)
hour_entry.insert(0, str(settings["reset_hour"]))
hour_entry.pack(side=tk.LEFT, padx=2)

tk.Label(reset_frame, text=":").pack(side=tk.LEFT)

minute_entry = tk.Entry(reset_frame, width=5)
minute_entry.insert(0, str(settings["reset_minute"]))
minute_entry.pack(side=tk.LEFT, padx=2)

reset_btn = tk.Button(reset_frame, text="Set Time", command=set_reset_time)
reset_btn.pack(side=tk.LEFT, padx=5)

# Start reset thread
threading.Thread(target=reset_tasks, daemon=True).start()

apply_theme()
apply_custom_color()
root.mainloop()