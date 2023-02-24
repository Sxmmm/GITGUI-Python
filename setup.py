import pathlib
import os
import sys
import requests
import time
from urllib.request import urlopen
import winshell
import win32com.client
import pythoncom


def create_directory():
    appDirectory = mainDrive + "/SamsApps"

    if not os.path.exists(appDirectory):
        os.makedirs(appDirectory)


def download_application():
    URL = urlopen("https://sxmhosts.000webhostapp.com/SamGitGUI/")
    data = URL.read().decode("utf-8")

    newVersion = requests.get(
        "https://github.com/Sxmmm/GITGUI-Python/releases/download/v"
        + data
        + "/SamGitGUI.exe"
    )

    filePath = mainDrive + "/SamsApps/SamGitGUI.exe"
    open(filePath, "wb").write(newVersion.content)

    time.sleep(5)


def create_shortcut():
    filePath = mainDrive + "/SamsApps/SamGitGUI.exe"

    desktop = winshell.desktop()
    path = os.path.join(desktop, "SamGitGUI.lnk")

    shell = win32com.client.Dispatch("WScript.Shell")
    shortcut = shell.CreateShortCut(path)
    shortcut.Targetpath = filePath
    shortcut.IconLocation = filePath
    shortcut.save()

    sys.exit()


def get_main_drive():
    return pathlib.Path.home().drive


if __name__ == "__main__":
    mainDrive = get_main_drive()
    create_directory()
    download_application()
    create_shortcut()
