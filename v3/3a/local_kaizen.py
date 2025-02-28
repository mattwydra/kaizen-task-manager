import tkinter as tk
from tkinter import messagebox, ttk
import json
import datetime
import threading

TASKS_FILE = "tasks.json"
SETTINGS_FILE = "settings.json"

daily_tasks = ["Physical Win", "Mental Win", "Spiritual Win"]

def load_tasks():
    try:
        with open(TASKS_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"Dailies": {"tasks": daily_tasks, "completed": []}}

def save_tasks():
    with open(TASKS_FILE, "w") as f:
        json.dump(tasks, f, indent=4)

def load_settings():
    try:
        with open(SETTINGS_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"theme": "light"}

def save_settings():
    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f, indent=4)

def add_task(tab_name, entry_widget, listbox):
    task = entry_widget.get().strip()
    if task and task not in tasks[tab_name]["tasks"]:
        tasks[tab_name]["tasks"].append(task)
        save_tasks()
        update_list(tab_name, listbox)
    entry_widget.delete(0, tk.END)

def delete_task(tab_name, listbox):
    selected = listbox.curselection()
    if selected:
        task_text = listbox.get(selected[0])
        tasks[tab_name]["tasks"].remove(task_text)
        if task_text in tasks[tab_name]["completed"]:
            tasks[tab_name]["completed"].remove(task_text)
        save_tasks()
        update_list(tab_name, listbox)

def mark_done(tab_name, listbox):
    selected = listbox.curselection()
    if selected:
        task_text = listbox.get(selected[0])
        if task_text in tasks[tab_name]["completed"]:
            tasks[tab_name]["completed"].remove(task_text)
        else:
            tasks[tab_name]["completed"].append(task_text)
        save_tasks()
        update_list(tab_name, listbox)

def update_list(tab_name, listbox):
    listbox.delete(0, tk.END)
    for task in tasks[tab_name]["tasks"]:
        listbox.insert(tk.END, task)
        if task in tasks[tab_name]["completed"]:
            listbox.itemconfig(tk.END, {'fg': 'gray'})

def add_tab():
    new_tab_name = tab_entry.get().strip()
    if new_tab_name and new_tab_name not in tasks:
        tasks[new_tab_name] = {"tasks": [], "completed": []}
        save_tasks()
        create_tab(new_tab_name)
    tab_entry.delete(0, tk.END)

def create_tab(tab_name):
    frame = ttk.Frame(notebook)
    notebook.add(frame, text=tab_name)
    
    listbox = tk.Listbox(frame, width=50, height=10)
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
    
    mark_btn = tk.Button(btn_frame, text="Mark Done", command=lambda: mark_done(tab_name, listbox))
    mark_btn.pack(side=tk.LEFT, padx=5)

def toggle_theme():
    if settings["theme"] == "light":
        root.tk_setPalette("#2E2E2E")
        settings["theme"] = "dark"
    else:
        root.tk_setPalette("#FFFFFF")
        settings["theme"] = "light"
    save_settings()

def midnight_reset():
    while True:
        now = datetime.datetime.now()
        midnight = datetime.datetime(now.year, now.month, now.day, 0, 0, 0)
        if now > midnight:
            midnight += datetime.timedelta(days=1)
        wait_time = (midnight - now).total_seconds()
        threading.Timer(wait_time, reset_dailies).start()
        break

def reset_dailies():
    tasks["Dailies"] = {"tasks": daily_tasks, "completed": []}
    save_tasks()
    for tab in notebook.tabs():
        if notebook.tab(tab, "text") == "Dailies":
            update_list("Dailies", notebook.nametowidget(tab).winfo_children()[0])
    midnight_reset()

tasks = load_tasks()
settings = load_settings()

root = tk.Tk()
root.title("Kaizen Task Manager")
root.geometry("600x400")

notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill="both")

for category in tasks.keys():
    create_tab(category)

tab_control_frame = tk.Frame(root)
tab_control_frame.pack(pady=10)

tab_entry = tk.Entry(tab_control_frame, width=30)
tab_entry.pack(side=tk.LEFT, padx=5)

tab_add_btn = tk.Button(tab_control_frame, text="Add Category", command=add_tab)
tab_add_btn.pack(side=tk.LEFT)

theme_btn = tk.Button(root, text="Toggle Theme", command=toggle_theme)
theme_btn.pack(pady=5)

midnight_reset()

root.mainloop()
