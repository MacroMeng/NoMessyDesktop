import datetime
import json
import logging
import os
from tkinter import *
from tkinter.ttk import *
from tkinter import filedialog, messagebox

import sv_ttk
import darkdetect as dd


VERSION = "0.1.3.0a"
VERSION_CODENAME = "Cherry Grove"
VERSION_DESCRIPTION = f"v{VERSION} ({VERSION_CODENAME})"

log_path = f"./logs/{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log"
if not os.path.exists(log_path):
    os.makedirs(os.path.dirname(log_path), exist_ok=True)
logging.basicConfig(level=logging.DEBUG,
                    format="[%(asctime)s %(name)s] (%(levelname)s) %(message)s",
                    filename=f"./logs/{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log",
                    encoding="utf-8")
log = logging.getLogger()


def ask_desktop_path_and_save():
    """
    向用户询问桌面的路径并且保存为JSON配置文件。
    """
    auto_gen_path = os.path.join(os.path.expanduser('~'), 'Desktop')
    log.debug(f"Auto generated desktop folder {auto_gen_path!r}")
    config = {"watch_dir": ""}

    def path_asker():
        config["watch_dir"] = filedialog.askdirectory(
            initialdir=auto_gen_path, title="Choose Desktop Folder...", mustexist=True, parent=initializer)
        log.debug(f"Choosed path: {config['watch_dir']}")
        messagebox.showinfo("Set successful!", f"Desktop folder: \n{config['watch_dir']}")
        initializer.destroy()

    def use_auto_gen_path():
        config["watch_dir"] = auto_gen_path
        messagebox.showinfo("Using auto generated path.", f"Desktop folder: \n{config['watch_dir']}")
        initializer.destroy()

    initializer = Tk()
    initializer.geometry("550x200")
    initializer.resizable(False, False)
    initializer.title(f"Asking Desktop Path... - NoMessyDesktop {VERSION_DESCRIPTION}")
    (Label(initializer, text="Choose the desktop folder to monitor:", font=("MiSans", 15, "bold"))
     .pack(anchor="center", padx=5, pady=(10, 0), fill="none", side="top"))
    (Label(initializer, text=f"Auto generated: {auto_gen_path}", font=("JetBrains Maple Mono", 12))
     .pack(anchor="center", padx=5, pady=5, fill="none", side="top"))
    (Button(initializer, text="Choose...", command=path_asker)
     .pack(anchor="center", padx=20, pady=0, fill="both", side="bottom", ipady=4))
    (Button(initializer, text="Use Auto Generated Path", command=use_auto_gen_path)
     .pack(anchor="center", padx=20, pady=5, fill="both", side="bottom", ipady=4))
    sv_ttk.set_theme(dd.theme())
    initializer.mainloop()

    log.debug(f"Get config: {config}")
    with open("../config/config.json", "w", encoding="utf-8") as fp:
        json.dump(config, fp, indent=4)


def read_config(path: str = "./config/config.json") -> dict:
    """
    读取JSON格式的配置文件。
    :param path: 配置文件的来源。默认为./config/config.json。
    :return: 读取到的配置文件。当找不到配置文件时，返回空字典。
    """
    try:
        with open(path, "r", encoding="utf-8") as fp:
            config = json.load(fp)
    except FileNotFoundError:
        log.warning("Config file not found. Returning {}.")
        return {}  # 返回空值

    log.debug(f"Read config: {config}")
    return config


def check_config(config: dict) -> bool:
    """
    检查配置文件的可用性。
    :param config: 读取的配置，以字典的形式呈现。
    :return: 配置文件是否可用。
    """
    log.debug(f"Checking config: {config}")
    watch_dir = config.get("watch_dir", "")
    if not os.path.exists(watch_dir):
        log.warning(f"Watch directory {watch_dir} not exists. Failed checking.")
        return False
    return True
