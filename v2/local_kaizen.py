import tkinter as tk
from tkinter import messagebox, ttk
import json

TASKS_FILE = "tasks.json"

# Default daily tasks{
daily_tasks = ["Physical Win", "Mental Win", "Spiritual Win"]

def load_tasks():
    try:
        with open(TASKS_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"Dailies": daily_tasks}

def save_tasks():
    with open(TASKS_FILE, "w") as f:
        json.dump(tasks, f, indent=4)

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
    
    listbox = tk.Listbox(frame, width=50, height=10)
    listbox.pack(side=tk.LEFT)
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

# Load tasks on startup
tasks = load_tasks()

# GUI Setup
root = tk.Tk()
root.title("Kaizen Task Manager")

notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill="both")

# Create tabs for existing categories
for category in tasks.keys():
    create_tab(category)

# Add new tab section
tab_control_frame = tk.Frame(root)
tab_control_frame.pack(pady=10)

tab_entry = tk.Entry(tab_control_frame, width=30)
tab_entry.pack(side=tk.LEFT, padx=5)

tab_add_btn = tk.Button(tab_control_frame, text="Add Category", command=add_tab)
tab_add_btn.pack(side=tk.LEFT)

root.mainloop()
