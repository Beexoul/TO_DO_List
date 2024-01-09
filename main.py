import tkinter as tk
from tkinter import simpledialog, messagebox
import json

class Task:
    def __init__(self, number, title, description, priority, completed=False):
        self.number = number
        self.title = title
        self.description = description
        self.priority = priority
        self.completed = completed

class TaskFrame(tk.Frame):
    def __init__(self, master, task, remove_callback, edit_callback):
        super().__init__(master, bd=1, relief="solid", padx=5, pady=5, bg="#000000")  # Black background
        self.task = task
        self.remove_callback = remove_callback
        self.edit_callback = edit_callback

        title_font = ("Arial", 14, "bold")
        description_font = ("Helvetica", 12)

        title_label = tk.Label(self, text=f"{self.task.number}. {self.task.title}", font=title_font, justify="left", bg="#FFFFFF", fg="#000000")  # White text on black background
        title_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        description_text = tk.Text(self, wrap="word", width=70, height=5, font=description_font, bg="#FFFFFF", fg="#000000")  # White text on black background
        description_text.grid(row=1, column=0, padx=5, pady=5, 
        
        sticky="w")
        description_text.insert("1.0", self.task.description)
        description_text.configure(state="disabled")

        button_frame = tk.Frame(self, bg="#FFFFFF")  # Black background
        button_frame.grid(row=0, column=1, rowspan=2, padx=5, pady=5)

        self.edit_button = tk.Button(button_frame, text="Edit", command=self.edit_task, bg="#FFFFFF", fg="#000000")  # White button with black text
        self.edit_button.grid(row=0, column=0, pady=2)

        self.remove_button = tk.Button(button_frame, text="Remove", command=self.remove_task, bg="#FFFFFF", fg="#000000")  # White button with black text
        self.remove_button.grid(row=1, column=0, pady=2)

    def remove_task(self):
        if self.remove_callback:
            self.remove_callback(self.task.number)

    def edit_task(self):
        if self.edit_callback:
            new_title = simpledialog.askstring("Edit Task", "Enter new task title:", initialvalue=self.task.title)
            new_description = simpledialog.askstring("Edit Task", "Enter new task description:", initialvalue=self.task.description)

            if new_title is not None and new_description is not None:
                self.task.title = new_title
                self.task.description = new_description
                self.edit_callback()

class ToDoListApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Fancy To-Do List App")
        self.root.configure(bg="#000000")  # Black background

        self.tasks = self.load_tasks()
        self.filter_low = tk.BooleanVar()
        self.filter_medium = tk.BooleanVar()
        self.filter_high = tk.BooleanVar()

        self.title_label = tk.Label(root, text="Fancy To-Do List", font=("Helvetica", 18, "bold"), bg="#000000", fg="#FFFFFF")  # White text on black background
        self.title_label.pack(pady=10)

        self.task_frame = tk.Frame(root, bg="#000000")  # Black background
        self.task_frame.pack(pady=10)

        self.credit_label = tk.Label(root, text="Developed by NotBeexoul", font=("Helvetica", 10), bg="#000000", fg="#FFFFFF")  # White text on black background
        self.credit_label.pack(side=tk.BOTTOM, pady=5)

        self.add_button = tk.Button(root, text="Add Task", command=self.add_task, bg="#FFFFFF", fg="#000000")  # White button with black text
        self.add_button.pack(side=tk.LEFT, padx=5)

        self.sort_button = tk.Button(root, text="Sort by Priority", command=self.sort_tasks, bg="#FFFFFF", fg="#000000")  # White button with black text
        self.sort_button.pack(side=tk.LEFT, padx=5)

        self.display_button = tk.Button(root, text="Display Tasks", command=self.display_tasks, bg="#FFFFFF", fg="#000000")  # White button with black text
        self.display_button.pack(side=tk.LEFT, padx=5)

        self.save_button = tk.Button(root, text="Save Tasks", command=self.save_tasks, bg="#FFFFFF", fg="#000000")  # White button with black text
        self.save_button.pack(side=tk.LEFT, padx=5)

        self.low_checkbox = tk.Checkbutton(root, text="Low", variable=self.filter_low, bg="#000000", fg="#FFFFFF", selectcolor="#000000")  # White text on black background
        self.low_checkbox.pack(side=tk.LEFT, padx=5)

        self.medium_checkbox = tk.Checkbutton(root, text="Medium", variable=self.filter_medium, bg="#000000", fg="#FFFFFF", selectcolor="#000000")  # White text on black background
        self.medium_checkbox.pack(side=tk.LEFT, padx=5)

        self.high_checkbox = tk.Checkbutton(root, text="High", variable=self.filter_high, bg="#000000", fg="#FFFFFF", selectcolor="#000000")  # White text on black background
        self.high_checkbox.pack(side=tk.LEFT, padx=5)
        self.scrollbar = tk.Scrollbar(self.task_frame, orient="vertical", bg="#000000")  # Black background
        self.scrollbar.pack(side="right", fill="y")

        self.task_list = tk.Listbox(self.task_frame, yscrollcommand=self.scrollbar.set, selectbackground="#333333", selectforeground="#FFFFFF", bg="#000000", fg="#FFFFFF")  # White text on black background
        self.task_list.pack(expand=True, fill="both", pady=20)
        self.task_list.bind("<ButtonRelease-1>", self.display_selected_task)
        self.scrollbar.config(command=self.task_list.yview)
        self.update_task_list()
    def add_task(self):
        title = simpledialog.askstring("Add Task", "Enter task title:")
        description = simpledialog.askstring("Add Task", "Enter task description:")
        priority_options = ["low", "medium", "high"]
        priority_input = simpledialog.askstring("Add Task", f"Enter priority ({', '.join(priority_options)}):").lower()
        while priority_input not in priority_options:
            messagebox.showwarning("Invalid Priority", f"Please enter a valid priority ({', '.join(priority_options)}).")
            priority_input = simpledialog.askstring("Add Task", f"Enter priority ({', '.join(priority_options)}):").lower()
        task_number = len(self.tasks) + 1
        task = Task(task_number, title, description, priority_input)
        self.tasks.append(task)
        self.update_task_list()
        self.save_tasks()
    def mark_as_completed(self):
        selected_index = self.task_list.curselection()
        if selected_index:
            selected_task = self.tasks[selected_index[0]]
            selected_task.completed = True
            self.update_task_list()
            self.save_tasks()
    def display_tasks(self):
        selected_index = self.task_list.curselection()
        if selected_index:
            selected_task = self.tasks[selected_index[0]]
            self.show_task_details(selected_task)
    def show_task_details(self, task):
        task_details_window = tk.Toplevel(self.root)
        task_details_window.title(f"Task {task.number} Details")
        task_details_window.configure(bg="#000000")  # Black background
        title_label = tk.Label(task_details_window, text=f"{task.number}. {task.title}", font=("Arial", 16, "bold"), bg="#000000", fg="#FFFFFF")  # White text on black background
        title_label.pack(pady=10)
        description_label = tk.Label(task_details_window, text=task.description, font=("Helvetica", 14), justify="left", bg="#000000", fg="#FFFFFF")  # White text on black background
        description_label.pack(pady=10)
        priority_label = tk.Label(task_details_window, text=f"Priority: {task.priority.capitalize()}", font=("Helvetica", 14), bg="#000000", fg="#FFFFFF")  # White text on black background
        priority_label.pack(pady=10)
        status_label = tk.Label(task_details_window, text=f"Status: {'Completed' if task.completed else 'Pending'}", font=("Helvetica", 14), bg="#000000", fg="#FFFFFF")  # White text on black background
        status_label.pack(pady=10)
        edit_button = tk.Button(task_details_window, text="Edit", command=lambda: self.edit_task_from_details(task), bg="#FFFFFF", fg="#000000")  # White button with black text
        edit_button.pack(side=tk.LEFT, padx=5)
        remove_button = tk.Button(task_details_window, text="Remove", command=lambda: self.remove_task_from_details(task), bg="#FFFFFF", fg="#000000")  # White button with black text
        remove_button.pack(side=tk.LEFT, padx=5)
        ok_button = tk.Button(task_details_window, text="OK", command=task_details_window.destroy, bg="#FFFFFF", fg="#000000")  # White button with black text
        ok_button.pack(side=tk.LEFT, padx=5)
    def edit_task_from_details(self, task):
        new_title = simpledialog.askstring("Edit Task", "Enter new task title:", initialvalue=task.title)
        new_description = simpledialog.askstring("Edit Task", "Enter new task description:", initialvalue=task.description)
        if new_title is not None and new_description is not None:
            task.title = new_title
            task.description = new_description
            self.update_task_list()
            self.save_tasks()
    def remove_task_from_details(self, task):
        self.tasks.remove(task)
        self.update_task_list()
        self.save_tasks()
    def display_selected_task(self, event):
        selected_index = self.task_list.curselection()
        if selected_index:
            selected_task = self.tasks[selected_index[0]]
            self.show_task_details(selected_task)
    def update_task_list(self):
        self.task_list.delete(0, tk.END)
        for task in self.filtered_tasks():
            self.task_list.insert(tk.END, f"{task.number}. {task.title} - {task.priority.capitalize()}")
    def remove_task_from_details(self, task):
        confirmation = messagebox.askyesno("Remove Task", f"Are you sure you want to remove Task {task.number}?")
        if confirmation:
            self.tasks.remove(task)
            self.update_task_list()
            self.save_tasks()
    def edit_task(self):
        selected_index = self.task_list.curselection()
        if selected_index:
            selected_task = self.tasks[selected_index[0]]
            new_title = simpledialog.askstring("Edit Task", "Enter new task title:", initialvalue=selected_task.title)
            new_description = simpledialog.askstring("Edit Task", "Enter new task description:", initialvalue=selected_task.description)
            if new_title is not None and new_description is not None:
                selected_task.title = new_title
                selected_task.description = new_description
                self.update_task_list()
                self.save_tasks()
    def save_tasks(self):
        with open("tasks.json", "w") as file:
            tasks_data = [{"number": task.number, "title": task.title, "description": task.description,
                           "priority": task.priority, "completed": task.completed} for task in self.tasks]
            json.dump(tasks_data, file)
    def load_tasks(self):
        try:
            with open("tasks.json", "r") as file:
                tasks_data = json.load(file)
                return [Task(
                    task.get("number", 0),
                    task.get("title", ""),
                    task.get("description", ""),
                    task.get("priority", ""),
                    task.get("completed", False)
                ) for task in tasks_data]
        except FileNotFoundError:
            return []
    def sort_tasks(self):
        self.update_task_list()
    def filtered_tasks(self):
        if self.filter_low.get():
            return [task for task in self.tasks if task.priority == "low"]
        elif self.filter_medium.get():
            return [task for task in self.tasks if task.priority == "medium"]
        elif self.filter_high.get():
            return [task for task in self.tasks if task.priority == "high"]
        else:
            return self.tasks

if __name__ == "__main__":
    root = tk.Tk()
    app = ToDoListApp(root)
    root.mainloop()