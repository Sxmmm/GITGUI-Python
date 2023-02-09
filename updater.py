import sys
import requests
import time
from urllib.request import urlopen
import os


def check_for_updates_event():
    URL = urlopen("https://sxmhosts.000webhostapp.com/SamGitGUI/")
    data = URL.read().decode("utf-8")

    newVersion = requests.get(
        "https://github.com/Sxmmm/GITGUI-Python/releases/download/v"
        + data
        + "/SamGitGUI.exe"
    )

    open("SamGitGUI.exe", "wb").write(newVersion.content)

    time.sleep(5)

    os.startfile("SamGitGUI.exe")

    sys.exit()


if __name__ == "__main__":
    check_for_updates_event()
