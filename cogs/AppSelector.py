import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
import json
from utils import encryption

class MainMenuDialog(tk.Toplevel):
    def __init__(self, parent, choices):
        super().__init__(parent)
        self.choices = choices
        self.selection = None
        self.title("Action")
        self.choice_var = tk.StringVar(value=self.choices[0])
        self.create_widgets()

    def create_widgets(self):
        label = tk.Label(self, text="Select an action:")
        label.pack()

        for choice in self.choices:
            radio_button = tk.Radiobutton(
                self,
                text=choice,
                variable=self.choice_var,
                value=choice
            )
            radio_button.pack(anchor='w')

        ok_button = tk.Button(self, text="OK", command=self.ok)
        ok_button.pack(pady=10)

    def ok(self):
        self.selection = self.choice_var.get()
        self.destroy()

class AppSelector:
    def __init__(self):
        self.password = None
        self.apps = {}

    def read_settings(self):
        try:
            with open("./data/app_data.json", "r") as file:
                data = json.load(file)
                self.password = data["password"]
                self.apps = data["apps"]
        except FileNotFoundError:
            self.setup()

    def save_settings(self):
        data = {
            "password": self.password,
            "apps": self.apps
        }
        data["password"] = (self.password).decode("utf-8") if type(data["password"]) == bytes else data["password"]
        with open("./data/app_data.json", "w") as file:
            json.dump(data, file)

    def ask_password(self, first_time:bool=False):
        if first_time:
            password = simpledialog.askstring("Password", "Set the password", show="*")
            return password
        else:
            password = simpledialog.askstring("Password", "Enter the password", show="*")
            return encryption.verify_password(password, (self.password).encode("utf-8") if type(self.password) == str else self.password)

    def add_app(self):
        app = simpledialog.askstring("Add App", "Enter the name of the app to limit")
        if app:
            if app in self.apps.keys():
                return messagebox.showerror("Already Exists", "App already exists!")
            limit = simpledialog.askstring("Limit", "Enter the time limit on the app (s/m/h)")
            try:
                time = int(limit)
            except:
                convertTimeList = {'s':1, 'm':60, 'h':3600, 'S':1, 'M':60, 'H':3600}
                try:
                    time = int(limit[:-1]) * convertTimeList[limit[-1]]
                except:
                    return messagebox.showerror("Invalid Limit", "Make sure you enter the limit in a correct format! (Eg: 60s, 60m, 1h)")
                
            self.apps[app] = time
            messagebox.showinfo("App Added", f"App '{app}' added successfully with a limit of {limit}!")

    def remove_app(self):
        app = simpledialog.askstring("Remove App", "Enter the name of the app to remove the limit of")
        if app:
            if app in self.apps.keys():
                self.apps.pop(app)
                messagebox.showinfo("App Removed", f"App '{app}' removed successfully!")
            else:
                messagebox.showerror("Error", f"App '{app}' is not in the limited apps list!")

    def setup(self):
        self.password = encryption.encrypt(self.ask_password(True))
        self.apps = {}
        self.save_settings()
        messagebox.showinfo("Password Set", "Password has been set successfully!")

    def start(self):
        self.read_settings()
        root = tk.Tk()
        root.geometry("400x200")
        root.withdraw()
        if not self.ask_password():
            return messagebox.showerror("Error", "Invalid Password!")
        while True:
            choices = ["Add an app to limit", "Remove an app from limit", "Save"]
            dialog = MainMenuDialog(root, choices)
            root.wait_window(dialog)
            action = dialog.selection

            if action == choices[0]:
                self.add_app()
            elif action == choices[1]:
                self.remove_app()
            elif action == choices[2]:
                self.save_settings()
                break

if __name__ == "__main__":
    selector = AppSelector()
    selector.start()