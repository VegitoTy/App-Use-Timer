import time
import psutil
import json

class AppTracker:
    def __init__(self):
        with open("./data/tracker_data.json", "r+") as e:
            self.data = json.load(e)
        for app, appdata in self.data.items():
            appdata["last_opened"] = time.time() if self.running(app) else appdata["last_opened"] if appdata else None
            self.data[app] = appdata

    def running(self, app):
        return True if app in (i.name() for i in psutil.process_iter()) else False
    
    def nextday_check(self, app):
        current = time.gmtime()
        last_opened = time.gmtime(self.data[app]["last_opened"])
        if self.data[app]["last_closed"]:
            last_closed = time.gmtime(self.data[app]["last_closed"])
            if not (current.tm_year == last_closed.tm_year and current.tm_mon == last_closed.tm_mon and current.tm_mday == last_closed.tm_mday):
                return True
        if self.data[app]["last_opened"]:
            last_opened = time.gmtime(self.data[app]["last_opened"])
            if not (current.tm_year == last_opened.tm_year and current.tm_mon == last_opened.tm_mon and current.tm_mday == last_opened.tm_mday):
                return True
        return False

    def count_usage(self):
        app_statuses = {x: False for x in self.data}
        btime = time.time()
        while True:
            if time.time() - btime >= 1:
                btime = time.time()
                for app, appdata in self.data.items():
                    if self.running(app):
                        if app_statuses[app] == False:
                            self.data[app]["last_opened"] = time.time()
                            app_statuses[app] = True
                        if self.nextday_check(app):
                            appdata["todays_usage"] = 0
                        else:
                            appdata["todays_usage"] += 1
                        appdata["total_usage"] += 1
                        self.data[app] = appdata
                    else:
                        if app_statuses[app] == True:
                            app_statuses[app] = False
                            self.data[app]["last_closed"] = time.time()
                self.global_save()

    def save(self, app):
        with open("./data/tracker_data.json", "r+") as e:
            data = json.load(e)
            e.seek(0)
            data[app] = self.data[app]
            json.dump(data, e)
            e.truncate()

    def global_save(self):
        with open("./data/tracker_data.json", "w") as e:
            e.seek(0)
            json.dump(self.data, e)
            e.truncate()
    
    def app_main(self):
        self.count_usage()
    
    def exit(self):
        for app in self.data.keys():
            self.data[app]["last_closed"] = time.time()
        self.global_save()

def add_app(app):
    with open("./data/tracker_data.json", "r+") as e:
        data = json.load(e)
        if app in data.keys():
            raise FileExistsError("App already exists!")
        data[app] = {"last_opened": None, "last_closed": None, "total_usage": 0, "todays_usage": 0}
        e.seek(0)
        json.dump(data, e)
        e.truncate()

def remove_app(app):
    with open("./data/tracker_data.json", "r+") as e:
        data = json.load(e)
        if app not in data.keys():
            raise FileNotFoundError("App does not exist!")
        data.pop(app)
        e.seek(0)
        json.dump(data, e)
        e.truncate()


if __name__ == "__main__":
    with open("./data/tracker_data.json") as e:
        tracker_data = json.load(e)
        for app in tracker_data.keys():
            print(f"Tracking {app}")