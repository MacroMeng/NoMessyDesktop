import json
import os
import time
from datetime import datetime
from tkinter import *
from tkinter.ttk import *

from tkinter import messagebox, filedialog
import logging

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

logging.basicConfig(level=logging.DEBUG,
                    format="[%(asctime)s %(name)s] (%(levelname)s) %(message)s")
log = logging.getLogger()

VERSION = "0.1.0.3"
VERSION_CODENAME = "Cherry Grove"
VERSION_DESCRIPTION = f"v{VERSION} ({VERSION_CODENAME})"


class NewFileHandler(FileSystemEventHandler):
    def __init__(self, callback):
        self.callback = callback
        super().__init__()

    def on_created(self, event):
        if not event.is_directory:
            # 稍微延迟一下以确保文件完全写入
            time.sleep(0.1)
            self.callback(event.src_path)


def get_desktop_path() -> str:
    # 获取桌面路径
    res = os.path.join(os.path.expanduser('~'), 'Desktop')
    log.info(f"Generated desktop folder {res!r}")
    if input(f"Is {res!r} your Desktop path?[y/n]") == "y":
        log.debug(f"Auto generated is true.")
        return res
    else:
        return input("If that's not, enter it: ")


class NoMessyDesktopApp:
    def __init__(self, config: dict):
        try:
            self.desktop_path = config["watch_dir"]
        except KeyError:
            log.error("No desktop path found in config. Ask again and save it.")
            ask_desktop_path_and_save()
            self.desktop_path = read_config()["watch_dir"]
        self.observer = Observer()

        # 初始化主窗口但不显示
        self.root = Tk()
        self.root.withdraw()  # 隐藏主窗口
        self.pending_files = []  # 存储待处理的文件
        self.processing = False  # 标记是否正在处理文件

    def start_monitoring(self):
        event_handler = NewFileHandler(self.on_new_file)
        self.observer.schedule(event_handler, self.desktop_path, recursive=False)
        self.observer.start()
        log.info(f"Start monitoring {self.desktop_path}")

        # 定期检查是否有新文件需要处理
        self.root.after(100, self.process_pending_files)

        try:
            # 启动GUI主循环
            self.root.mainloop()
        except KeyboardInterrupt:
            self.stop_monitoring()

    def on_new_file(self, file_path):
        # 将新文件添加到待处理列表
        log.debug(f"New file: {file_path}")
        self.pending_files.append(file_path)

    def process_pending_files(self):
        # 在主线程中处理待处理的文件
        if self.pending_files and not self.processing:
            self.processing = True
            file_path = self.pending_files.pop(0)
            self.show_file_dialog(file_path)
            self.processing = False

        # 继续定期检查
        self.root.after(100, self.process_pending_files)

    def show_file_dialog(self, file_path):
        # 创建并显示文件信息对话框
        dialog = Toplevel(self.root)
        dialog.title(f"New file {os.path.basename(file_path)} at {self.desktop_path}"
                     f" - NoMessyDesktop {VERSION_DESCRIPTION}")
        dialog.geometry("500x150")
        dialog.resizable(False, False)
        dialog.attributes('-topmost', True)  # 窗口置顶

        # 获取文件信息
        file_stat = os.stat(file_path)

        log.info(f"New file stat: {file_stat}")

        # 文件名
        Label(dialog, text="New File Detected", font=("MiSans", 20, "bold")).pack(pady=(10, 5))

        # 文件路径
        Label(dialog, text=file_path, font=("JetBrains Maple Mono", 12), foreground="#101060").pack(pady=5)

        # 操作框架
        action_frame = Frame(dialog)
        action_frame.pack(pady=10)

        def show_details():
            # 显示详细属性窗口
            self.show_file_details(file_path)

        def move_file():
            # 选择目标文件夹
            destination_folder = filedialog.askdirectory(
                title="Choose target folder",
                initialdir=os.path.dirname(self.desktop_path)
            )
            log.debug("Select Moving")
            if destination_folder:
                try:
                    # 移动文件
                    file_name = os.path.basename(file_path)
                    destination_path = os.path.join(destination_folder, file_name)

                    # 如果目标文件已存在，添加数字后缀
                    counter = 1
                    base_name, extension = os.path.splitext(file_name)
                    while os.path.exists(destination_path):
                        new_name = f"{base_name}_{counter}{extension}"
                        destination_path = os.path.join(destination_folder, new_name)
                        counter += 1

                    os.rename(file_path, destination_path)
                    messagebox.showinfo("Done!", f"File moved successfully to:\n{destination_path}")
                    log.info(f"Move file {file_path!r} to {destination_path!r}")
                    dialog.destroy()
                except Exception as e:
                    messagebox.showerror("Error!", f"Failed to move to:\n{str(e)}")

        def ignore_file():
            log.debug("Select Ignore, Closing dialog")
            dialog.destroy()

        Button(action_frame, text="Property", command=show_details, width=15).pack(side="left", padx=5)
        Button(action_frame, text="Move to…", command=move_file, width=15).pack(side="left", padx=5)
        Button(action_frame, text="Ignore", command=ignore_file, width=15).pack(side="left", padx=5)

        # 居中显示对话框
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (dialog.winfo_width() // 2)
        y = (dialog.winfo_screenheight() // 2) - (dialog.winfo_height() // 2)
        dialog.geometry(f"+{x}+{y}")

        # 确保窗口获得焦点
        dialog.focus_force()

    def show_file_details(self, file_path):
        # 创建并显示文件详细信息对话框
        details_dialog = Toplevel(self.root)
        details_dialog.title(f"Property of {os.path.basename(file_path)} - NoMessyDesktop {VERSION_DESCRIPTION}")
        details_dialog.geometry("500x300")
        details_dialog.resizable(False, False)
        details_dialog.attributes('-topmost', True)  # 窗口置顶

        # 获取文件详细信息
        file_stat = os.stat(file_path)
        file_size = file_stat.st_size
        creation_time = datetime.fromtimestamp(file_stat.st_ctime)
        modification_time = datetime.fromtimestamp(file_stat.st_mtime)

        try:
            # 尝试获取访问时间
            access_time = datetime.fromtimestamp(file_stat.st_atime)
        except Exception as exc:
            access_time = "Unavailable"
            log.warning(f"Get access time error: {exc}")

        Label(details_dialog, text=f"Property of {os.path.basename(file_path)}:",
              font=("MiSans", 15, "bold")).pack(pady=(10, 10))

        info_frame = Frame(details_dialog)
        info_frame.pack(pady=10, padx=20, fill="x")

        (Label(info_frame, text="File Name:", anchor="w", font=("JetBrains Maple Mono", 10))
         .grid(row=0, column=0, sticky="w"))
        (Label(info_frame, text=os.path.basename(file_path), anchor="w", foreground="#101060",
               font=("JetBrains Maple Mono", 10)).grid(row=0, column=1, sticky="w"))

        (Label(info_frame, text="File Path:", anchor="w", font=("JetBrains Maple Mono", 10)).
         grid(row=1, column=0, sticky="w"))
        (Label(info_frame, text=file_path, anchor="w", font=("JetBrains Maple Mono", 10))
         .grid(row=1, column=1, sticky="w"))

        (Label(info_frame, text="File Size:", anchor="w", font=("JetBrains Maple Mono", 10)).
         grid(row=2, column=0, sticky="w"))
        (Label(info_frame, text=f"{file_size} 字节", anchor="w", font=("JetBrains Maple Mono", 10))
         .grid(row=2, column=1, sticky="w"))

        (Label(info_frame, text="Create T.:", anchor="w", font=("JetBrains Maple Mono", 10)).
         grid(row=3, column=0, sticky="w"))
        (Label(info_frame, text=creation_time.strftime("%Y-%m-%d %H:%M:%S"), anchor="w",
               font=("JetBrains Maple Mono", 10))
         .grid(row=3, column=1, sticky="w"))

        (Label(info_frame, text="Edit Time:", anchor="w", font=("JetBrains Maple Mono", 10)).
         grid(row=4, column=0, sticky="w"))
        (Label(info_frame, text=modification_time.strftime("%Y-%m-%d %H:%M:%S"), anchor="w",
               font=("JetBrains Maple Mono", 10))
         .grid(row=4, column=1, sticky="w"))

        (Label(info_frame, text="Read Time:", anchor="w", font=("JetBrains Maple Mono", 10)).
         grid(row=5, column=0, sticky="w"))
        (Label(info_frame, text=access_time if access_time == "Unavailable" else
        access_time.strftime("%Y-%m-%d %H:%M:%S"), anchor="w", font=("JetBrains Maple Mono", 10))
         .grid(row=5, column=1, sticky="w"))

        close_btn = Button(details_dialog, text="Close", command=details_dialog.destroy, width=15)
        close_btn.pack(pady=20)

        # 居中显示对话框
        details_dialog.update_idletasks()
        x = (details_dialog.winfo_screenwidth() // 2) - (details_dialog.winfo_width() // 2)
        y = (details_dialog.winfo_screenheight() // 2) - (details_dialog.winfo_height() // 2)
        details_dialog.geometry(f"+{x}+{y}")

        details_dialog.focus_force()

    def stop_monitoring(self):
        self.observer.stop()
        self.observer.join()
        log.info("App stopped")
        self.root.quit()
        exit()


def ask_desktop_path_and_save():
    config = {"watch_dir": get_desktop_path()}
    with open("./config/config.json", "w", encoding="utf-8") as fp:
        json.dump(config, fp, indent=4)


def read_config() -> dict:
    with open("./config/config.json", "r", encoding="utf-8") as fp:
        config = json.load(fp)
    return config


if __name__ == "__main__":
    os.makedirs("./config", exist_ok=True)
    if os.path.exists("./config/config.json"):
        config = read_config()
    else:
        ask_desktop_path_and_save()
        config = read_config()

    app = NoMessyDesktopApp(config)
    app.start_monitoring()
