import os
import datetime
from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox

import utils
from src.pycses import cses


class NoMessyDesktop:
    def __init__(self, config: dict):
        self.schedule = None
        self.watch_dir = config["watch_dir"]
        self.next_check_time = datetime.time(23, 59, 59)
        self.popup_window = Tk()

    def run(self):
        """
        运行程序，开始监控桌面文件。
        """
        utils.log.info("Starting NoMessyDesktop...")
        utils.log.debug(f"Watching directory: {self.watch_dir}")
        self.check_time()

    def check_desktop(self):
        pass

    def check_time(self):
        if datetime.datetime.now().time() >= self.next_check_time:
            utils.log.debug("Time's up, checking desktop.")
            self.next_check_time = datetime.time(23, 59, 59)
            self.check_desktop()
        else:
            self.popup_window.after(30000, self.check_time)

    def read_today_schedule_from_cses(self, path: str):
        """
        读取CSES格式的课表文件。
        :param path: CSES课表文件的路径。
        """
        if not cses.CSESParser.is_cses_file(path):
            messagebox.showwarning("Invalid CSES File", "The file you selected is not a valid CSES file.")
            utils.log.warning(f"Invalid CSES file {path}")
            return
        schedule = cses.CSESParser.parse_cses_file(path)
        utils.log.info(f"Successfully read schedule from {path}")
        self.schedule = schedule

if __name__ == "__main__":
    os.makedirs("../config", exist_ok=True)
    while True:
        config = utils.read_config()
        if utils.check_config(config):
            break
        else:
            utils.ask_desktop_path_and_save()
            continue

    NoMessyDesktop(config).run()
