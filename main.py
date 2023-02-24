from pathlib import Path
import shutil
import sys
import tkinter
import customtkinter

import requests
import time
from urllib.request import urlopen

from GITProjectObject import GITProjectObject
from InputBoxes import CTkInputDialog
from TabObject import TabObject

import os


customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme(
    "blue"
)  # Themes: "blue" (standard), "green", "dark-blue"

currentVersion = "0.0.3"
latestUpdater = (
    "https://github.com/Sxmmm/GITGUI-Python/releases/download/Updater/updater.exe"
)


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        def resource_path(relative_path):
            try:
                base_path = sys._MEIPASS
            except Exception:
                base_path = os.path.abspath(".")

            return os.path.join(base_path, relative_path)

        self._gitProjectTabs = []

        # configure window
        self.title("Sam GIT GUI")
        self.geometry(f"{1100}x{580}")
        self.resizable(False, False)
        self.wm_iconbitmap(resource_path("logo.ico"))

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = customtkinter.CTkLabel(
            self.sidebar_frame,
            text="Sam GIT GUI",
            font=customtkinter.CTkFont(size=20, weight="bold"),
        )
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.sidebar_button_1 = customtkinter.CTkButton(
            self.sidebar_frame, text="Clone", command=self.open_input_dialog_event
        )
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)
        self.sidebar_button_2 = customtkinter.CTkButton(
            self.sidebar_frame, text="Load", command=self.load_button_event
        )
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)
        self.sidebar_button_3 = customtkinter.CTkButton(
            self.sidebar_frame, text="Load All", command=self.loadall_button_event
        )
        self.sidebar_button_3.grid(row=3, column=0, padx=20, pady=10)
        self.sidebar_button_4 = customtkinter.CTkButton(
            self.sidebar_frame,
            text="Check for updates",
            command=self.check_for_updates_event,
        )
        self.sidebar_button_4.grid(row=6, column=0, padx=20, pady=10)
        self.version_label = customtkinter.CTkLabel(
            self.sidebar_frame,
            text="v" + currentVersion + "\nSamBaker",
            font=customtkinter.CTkFont(size=10),
        )
        self.version_label.grid(row=7, column=0, padx=20, pady=(20, 10))

        # create tabview
        self.tabview = customtkinter.CTkTabview(self, width=250, height=500)
        self.tabview.grid(row=0, column=1, padx=(20, 20), pady=(20, 0), sticky="nsew")

    def open_input_dialog_event(self):
        dialog = CTkInputDialog(text=".git url")

        dialog_data = GITProjectObject(dialog.get_input(), dialog.isB2C)
        # dialog_data.print_data()
        dialog_data.clone()
        self.add_tab(dialog_data)

    def add_tab(self, data: GITProjectObject, skipCheck: bool = False):
        if skipCheck is False:
            if data._giturl is "":
                return

        repoName = data._repoName + ("-b2c" if data._isB2C is True else "-b2b")
        self.tabview.add(repoName)
        self.tabview.tab(repoName).grid_columnconfigure(0, weight=1)
        self._gitProjectTabs.append(TabObject(data, self.tabview))

    def loadall_button_event(self):
        for dir in next(os.walk("/Projects/"))[1]:
            data = GITProjectObject(isb2c=True, repoName=dir)
            self.add_tab(data, True)
        for dir in next(os.walk("/B2BProjects/"))[1]:
            data = GITProjectObject(isb2c=False, repoName=dir)
            self.add_tab(data, True)

    def load_button_event(self):
        tkinter.Tk().withdraw()  # prevents an empty tkinter window from appearing
        folder_path = tkinter.filedialog.askdirectory()
        if folder_path is "":
            return

        b2c: bool = True

        if "B2B" in folder_path:
            b2c = False

        data = GITProjectObject(isb2c=b2c, repoName=os.path.basename(folder_path))
        self.add_tab(data, True)

    def test_button_event(self, text: str):
        print(text)

    def check_for_updates_event(self):
        URL = urlopen("https://sxmhosts.000webhostapp.com/SamGitGUI/")
        data = URL.read().decode("utf-8")

        if data == currentVersion:
            print("App is up to date!")
        else:
            updater = requests.get(latestUpdater)

            open("updater.exe", "xb").write(updater.content)
            os.startfile("updater.exe")
            time.sleep(1)
            sys.exit()


if __name__ == "__main__":
    my_file = Path("updater.exe")
    if my_file.is_file():
        os.remove("updater.exe")
    app = App()
    app.mainloop()
