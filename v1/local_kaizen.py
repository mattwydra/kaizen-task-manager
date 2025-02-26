import tkinter as tk
from tkinter import messagebox
import json

TASKS_FILE = "tasks.json"

# Default daily tasks
daily_tasks = ["Physical Win", "Mental Win", "Spiritual Win"]

def load_tasks():
    try:
        with open(TASKS_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"custom": [], "daily": daily_tasks}

def save_tasks():
    with open(TASKS_FILE, "w") as f:
        json.dump(tasks, f, indent=4)

def add_task():
    task = entry.get().strip()
    if task and task not in tasks["custom"]:
        tasks["custom"].append(task)
        save_tasks()
        update_list()
    entry.delete(0, tk.END)

def delete_task():
    selected = listbox.curselection()
    if selected:
        task_text = listbox.get(selected[0])
        if task_text in tasks["custom"]:
            tasks["custom"].remove(task_text)
        save_tasks()
        update_list()

def mark_done():
    selected = listbox.curselection()
    if selected:
        task_text = listbox.get(selected[0])
        listbox.itemconfig(selected[0], {'fg': 'gray'})

def update_list():
    listbox.delete(0, tk.END)
    for task in tasks["daily"]:
        listbox.insert(tk.END, task)
    for task in tasks["custom"]:
        listbox.insert(tk.END, task)

# Load tasks on startup
tasks = load_tasks()

# GUI Setup
root = tk.Tk()
root.title("Kaizen Task Manager")

frame = tk.Frame(root)
frame.pack(pady=10)

listbox = tk.Listbox(frame, width=50, height=10)
listbox.pack(side=tk.LEFT)

scrollbar = tk.Scrollbar(frame, orient=tk.VERTICAL, command=listbox.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
listbox.config(yscrollcommand=scrollbar.set)

entry = tk.Entry(root, width=50)
entry.pack(pady=5)

btn_frame = tk.Frame(root)
btn_frame.pack()

add_btn = tk.Button(btn_frame, text="Add Task", command=add_task)
add_btn.pack(side=tk.LEFT, padx=5)

delete_btn = tk.Button(btn_frame, text="Delete Task", command=delete_task)
delete_btn.pack(side=tk.LEFT, padx=5)

mark_btn = tk.Button(btn_frame, text="Mark Done", command=mark_done)
mark_btn.pack(side=tk.LEFT, padx=5)

update_list()
root.mainloop()
