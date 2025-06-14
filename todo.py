import tkinter as tk
from tkinter import simpledialog, messagebox
from PIL import Image, ImageTk
import json
import os

USERS_FILE = "users.json"
TASKS_FILE = "tasks.json"
CATEGORIES = ["School", "Personal", "Work", "Other"]

# --- USER HANDLING ---

def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    return {}

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f)

# --- LOGIN WINDOW ---

class LoginWindow:
    def __init__(self, root, on_success):
        self.root = root
        self.on_success = on_success
        self.root.title("Login")
        self.root.geometry("700x500")  # Wider to fit the form in the right area
        self.users = load_users()

        # Load background image
        self.bg_image = Image.open("login.jpg").resize((1300, 700), Image.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)

        # Create canvas and set background
        self.canvas = tk.Canvas(root, width=700, height=500)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")

        # Place form in center-right (adjust relx/rely as needed)
        relx = 0.91
        rely = 0.6

        # Title
        self.canvas.create_text(relx * 700, rely * 500 - 80, text="Login", font=("Arial", 22, "bold"), fill="white")

        # Username label and entry
        self.canvas.create_text(relx * 700, rely * 500 - 40, text="Username", fill="black", font=("Arial", 11))
        self.username_entry = tk.Entry(root, width=25)
        self.canvas.create_window(relx * 700, rely * 500 - 15, window=self.username_entry)

        # Password label and entry
        self.canvas.create_text(relx * 700, rely * 500 + 15, text="Password", fill="black", font=("Arial", 11))
        self.password_entry = tk.Entry(root, show="*", width=25)
        self.canvas.create_window(relx * 700, rely * 500 + 40, window=self.password_entry)

        # Login Button
        login_button = tk.Button(root, text="Login", command=self.login, width=15)
        self.canvas.create_window(relx * 700, rely * 500 + 80, window=login_button)

        # Register Button
        register_button = tk.Button(root, text="Register", command=self.register, width=15)
        self.canvas.create_window(relx * 700, rely * 500 + 115, window=register_button)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if username in self.users and self.users[username] == password:
            self.root.destroy()
            self.on_success()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

    def register(self):
        self.root.destroy()
        RegisterWindow()


# --- REGISTER WINDOW ---

class RegisterWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Register")
        self.root.geometry("350x250")
        self.users = load_users()

        tk.Label(self.root, text="New Username").pack(pady=5)
        self.username_entry = tk.Entry(self.root)
        self.username_entry.pack()

        tk.Label(self.root, text="New Password").pack(pady=5)
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.pack()

        tk.Button(self.root, text="Register", command=self.register).pack(pady=15)
        tk.Button(self.root, text="Back to Login", command=self.back_to_login).pack()

        self.root.mainloop()

    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if not username or not password:
            messagebox.showerror("Error", "All fields are required")
            return
        if username in self.users:
            messagebox.showerror("Error", "Username already exists")
            return
        self.users[username] = password
        save_users(self.users)
        messagebox.showinfo("Success", "Registration successful!")
        self.root.destroy()
        main()  # Go back to login

    def back_to_login(self):
        self.root.destroy()
        main()

# --- TO-DO APP ---

class ToDoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List with Categories and Time Management")
        self.root.geometry("1000x600")

        self.bg_image = Image.open("image1.jpg").resize((1300, 700), Image.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)

        self.canvas = tk.Canvas(root, width=1000, height=600)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")

        self.category_frames = {}
        self.listboxes = {}
        self.colors = {
            "School": "#AED6F1",
            "Personal": "#F9E79F",
            "Work": "#F5B7B1",
            "Other": "#D5F5E3"
        }

        for i, cat in enumerate(CATEGORIES):
            frame = tk.Frame(root, bg=self.colors[cat], bd=2)
            frame.place(relx=0.05 + i * 0.23, rely=0.15, relwidth=0.21, relheight=0.6)

            label = tk.Label(frame, text=cat, bg=self.colors[cat], font=("Arial", 12, "bold"))
            label.pack(pady=5)

            listbox = tk.Listbox(frame)
            listbox.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)

            self.category_frames[cat] = frame
            self.listboxes[cat] = listbox

        btn_frame = tk.Frame(root, bg="white")
        btn_frame.place(relx=0.5, rely=0.85, anchor="center")

        tk.Button(btn_frame, text="Add Task", command=self.add_task).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Edit Task", command=self.edit_task).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="Delete Task", command=self.delete_task).grid(row=0, column=2, padx=5)
        tk.Button(btn_frame, text="Mark Done", command=self.mark_done).grid(row=0, column=3, padx=5)
        tk.Button(btn_frame, text="Exit", command=self.exit_app).grid(row=0, column=4, padx=5)

        self.tasks = self.load_tasks()
        self.refresh_tasks()

    def load_tasks(self):
        if os.path.exists(TASKS_FILE):
            with open(TASKS_FILE, "r") as f:
                return json.load(f)
        return []

    def save_tasks(self):
        with open(TASKS_FILE, "w") as f:
            json.dump(self.tasks, f, indent=4)

    def refresh_tasks(self):
        for lb in self.listboxes.values():
            lb.delete(0, tk.END)
        for task in self.tasks:
            due_str = f" | Due: {task.get('due_date', 'No Deadline')}"
            display = f"[{'✓' if task['completed'] else '✗'}] {task['description']} ({task['priority']}){due_str}"
            self.listboxes[task["category"]].insert(tk.END, display)

    def add_task(self):
        desc = simpledialog.askstring("Task", "Description:")
        if not desc:
            return
        cat = simpledialog.askstring("Category", f"Enter category ({', '.join(CATEGORIES)}):")
        if cat not in CATEGORIES:
            cat = "Other"
        prio = simpledialog.askstring("Priority", "Priority (High/Medium/Low):") or "Low"
        due = simpledialog.askstring("Due Date", "Enter due date/time (e.g., 2025-06-01 14:30):") or "No Deadline"
        self.tasks.append({
            "description": desc,
            "category": cat,
            "priority": prio.capitalize(),
            "due_date": due,
            "completed": False
        })
        self.refresh_tasks()

    def get_selected(self):
        for cat in CATEGORIES:
            sel = self.listboxes[cat].curselection()
            if sel:
                idx = sel[0]
                task = [t for t in self.tasks if t["category"] == cat][idx]
                return task
        messagebox.showwarning("Warning", "Select a task first.")
        return None

    def edit_task(self):
        task = self.get_selected()
        if not task:
            return
        new_desc = simpledialog.askstring("Edit Task", "New description:", initialvalue=task["description"])
        new_due = simpledialog.askstring("Edit Due Date", "New due date/time (e.g., 2025-06-01 14:30):", initialvalue=task.get("due_date", "No Deadline"))
        if new_desc:
            task["description"] = new_desc
        if new_due:
            task["due_date"] = new_due
        self.refresh_tasks()

    def delete_task(self):
        task = self.get_selected()
        if task:
            self.tasks.remove(task)
            self.refresh_tasks()

    def mark_done(self):
        task = self.get_selected()
        if task:
            task["completed"] = True
            self.refresh_tasks()

    def exit_app(self):
        self.save_tasks()
        self.root.destroy()

# --- MAIN ENTRY POINT ---

def start_main_app():
    root = tk.Tk()
    ToDoApp(root)
    root.mainloop()

def main():
    login_root = tk.Tk()
    LoginWindow(login_root, on_success=start_main_app)
    login_root.mainloop()

if __name__ == "__main__":
    main()

