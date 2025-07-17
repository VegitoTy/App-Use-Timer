from cogs import AppTracker, AppLimiter, AppSelector
import atexit, json
from tkinter import messagebox
import threading

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def setup_tracker():
    with open("./data/app_data.json") as e:
        app_data = json.load(e)
    with open("./data/tracker_data.json") as e:
        tracker_data = json.load(e)

    for app in app_data["apps"].keys():
        if app not in tracker_data.keys():
            AppTracker.add_app(app)
    
    for app in tracker_data.keys():
        if app not in app_data["apps"].keys():
            if messagebox.askyesno("App Tracker", f"{app} has been removed from the usage limit, would you like to delete its tracker data?"):
                AppTracker.remove_app(app)
                messagebox.showinfo("App Tracker", f"Tracker data of {app} deleted.")
            else:
                messagebox.showinfo("App Tracker", f"I will continue to track the usage of {app}")
    
if messagebox.askyesno("App Limiter", f"Run app selector?"):
    print(f"{bcolors.WARNING}Turning on App Selector..")
    AppSelector.AppSelector().start()

print(f"{bcolors.WARNING}Turning on App Tracker..")
setup_tracker()
tracker = AppTracker.AppTracker()
atexit.register(tracker.exit)
tracker_process = threading.Thread(target=tracker.app_main, daemon=True)
tracker_process.start()
print(f"{bcolors.OKGREEN}Turned on App Tracker!")

print(f"{bcolors.WARNING}Turning on App Limiter..")
limiter = AppLimiter.AppLimiter("./data/tracker_data.json", "./data/app_data.json")
limiter_process = threading.Thread(target=limiter.main, daemon=True)
limiter_process.start()
print(f"{bcolors.OKGREEN}Turned on App Limiter!")
print()

tracker_process.join()