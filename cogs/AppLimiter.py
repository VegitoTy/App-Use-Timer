from tkinter import messagebox
import os
import json
import psutil
import time

class AppLimiter:

    def __init__(self, tracker_data, app_data):
        self.tracker_data = tracker_data
        self.app_data = app_data

    def get_tracker(self, app):
        try:
            with open(self.tracker_data, "r") as e:
                return json.load(e)[app]
        except:
            time.sleep(0.2)
            return self.get_tracker(app)
        
    def get_apps(self):
        try:
            with open(self.app_data, "r") as e:
                return json.load(e)["apps"]
        except:
            time.sleep(0.2)
            return self.get_apps()

    def app_check(self, app):
        tracker_data = self.get_tracker(app)
        app_data = self.get_apps()
        return True if tracker_data["todays_usage"]>=app_data[app] else False
    
    def main(self):
        btime = time.time()
        while True:
            if time.time() - btime >= 1:
                print(1)
                btime = time.time()
                apps = self.get_apps()
                for app in apps.keys():
                    if self.app_check(app):
                        if app in (i.name() for i in psutil.process_iter()):
                            os.system(f"taskkill /IM {app} /F")
                            messagebox.showwarning("Limit Reached", f"You have hit your limit of using {app} for today!")

if __name__ == "__main__":
    AppLimiter("./data/tracker_data.json", "./data/app_data.json").main()