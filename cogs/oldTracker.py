import time
import psutil
import json
import multiprocessing

class App:
    def __init__(self, name:str, data:dict=None):
        self.name = name
        self.data = data
        last_opened = time.time() if self.running() else data["last_opened"] if data else None
        if not self.data:
            self.data = {
                    "last_opened": last_opened,
                    "last_closed": None,
                    "total_usage": 0,
                    "todays_usage": 0,
                }
        else:
            data["last_opened"] = last_opened

    def running(self):
        return True if self.name in (i.name() for i in psutil.process_iter()) else False
    
    def nextday_check(self):
        if not self.data["last_closed"]:
            return False
        current = time.gmtime()
        last_opened = time.gmtime(self.data["last_opened"])
        last_closed = time.gmtime(self.data["last_closed"])
        if self.data["last_closed"]:
            if not (current.tm_year == last_closed.tm_year and current.tm_mon == last_closed.tm_mon and current.tm_mday == last_closed.tm_mday):
                return True
        if not (current.tm_year == last_opened.tm_year and current.tm_mon == last_opened.tm_mon and current.tm_mday == last_opened.tm_mday):
            return True
        return False

    def count_usage(self):
        while self.running():
            if self.nextday_check():
                self.data["todays_usage"] = 0
            else:
                self.data["todays_usage"] += 1
                self.data["total_usage"] += 1
                print(1)
                time.sleep(1)
            self.save()

    def save(self, closed:bool=False):
        if closed:
            self.data["last_closed"] = time.time()

        with open("./app_data.json", "r+") as e:
            data = json.load(e)
            e.seek(0)
            try:
                if not self.data["total_usage"] == data[self.name]["total_usage"]:
                    data[self.name] = self.data
                    json.dump(data, e)
            except KeyError:
                data[self.name] = self.data
                json.dump(data, e)
            e.truncate()
    
    def app_main(self):
        self.count_usage()
        self.save(closed=True)

if __name__ == "__main__":
    with open("./app_data.json", "r+") as data:
        data = json.load(data)
        discord = App("Discord.exe", data["Discord.exe"])
        opera = App("opera.exe", data["opera.exe"])
    discord_process = multiprocessing.Process(target=discord.app_main, daemon=True)
    opera_process = multiprocessing.Process(target=opera.app_main, daemon=True)
    discord_process.start()
    opera_process.start()
    discord_process.join()
    opera_process.join()