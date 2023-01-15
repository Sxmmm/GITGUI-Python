import tkinter
import customtkinter

from GITProjectObject import GITProjectObject

import os

# import git
# from git import Repo
# import giturlparse

customtkinter.set_appearance_mode(
    "System"
)  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme(
    "blue"
)  # Themes: "blue" (standard), "green", "dark-blue"


class CTkInputDialog(customtkinter.CTkInputDialog):
    def _create_widgets(self):
        super()._create_widgets()

        self.isB2C = True
        self.isOkPressed = False

        self._cancel_button = customtkinter.CTkButton(
            master=self,
            width=100,
            border_width=0,
            fg_color=self._button_fg_color,
            hover_color=self._button_hover_color,
            text_color=self._button_text_color,
            text="Cancel",
            command=self._cancel_event,
        )
        self._cancel_button.grid(
            row=2, column=1, columnspan=1, padx=(10, 20), pady=(0, 20), sticky="ew"
        )

        self.radiobutton_frame = customtkinter.CTkFrame(self)
        self.radiobutton_frame.grid(
            row=0, column=3, padx=(20, 20), pady=(20, 0), sticky="nsew"
        )
        self.radio_var = tkinter.IntVar(value=0)
        self.label_radio_group = customtkinter.CTkLabel(
            master=self.radiobutton_frame, text="Game Type"
        )
        self.label_radio_group.grid(
            row=0, column=2, columnspan=1, padx=10, pady=10, sticky=""
        )
        self.radio_button_1 = customtkinter.CTkRadioButton(
            master=self.radiobutton_frame,
            variable=self.radio_var,
            value=0,
            text="B2C",
            command=self._set_b2c,
        )
        self.radio_button_1.grid(row=1, column=2, pady=10, padx=20, sticky="n")
        self.radio_button_2 = customtkinter.CTkRadioButton(
            master=self.radiobutton_frame,
            variable=self.radio_var,
            value=1,
            text="B2B",
            command=self._set_b2b,
        )
        self.radio_button_2.grid(row=2, column=2, pady=10, padx=20, sticky="n")

    def _ok_event(self, event=None):
        self.isOkPressed = True
        super()._ok_event()

    def _set_b2c(self):
        self.isB2C = True

    def _set_b2b(self):
        self.isB2C = False


class TabObject:
    _tabName: str = ""
    _tabData: GITProjectObject
    _repoLabelDir: customtkinter.CTkButton
    _testButton: customtkinter.CTkButton
    _tabview: customtkinter.CTkTabview
    _statusTextBox: customtkinter.CTkTextbox

    def __init__(self, data: GITProjectObject, tabview: customtkinter.CTkTabview):
        self._tabName = data._repoName + ("-b2c" if data._isB2C is True else "-b2b")
        self._tabData = data
        self._tabview = tabview

        self._repoLabelDir = customtkinter.CTkLabel(
            self._tabview.tab(self._tabName), text=data._projectPath + data._repoName
        )
        self._repoLabelDir.grid(row=0, column=0, padx=0, pady=(0, 0))

        self._testButton = customtkinter.CTkButton(
            self._tabview.tab(self._tabName),
            text="test",
            command=self.test_button_event,
        )
        self._testButton.grid(row=1, column=0, padx=20, pady=(0, 10))

        self._statusButton = customtkinter.CTkButton(
            self._tabview.tab(self._tabName),
            text="Status",
            command=self.status_button_event,
        )
        self._statusButton.grid(row=2, column=0, padx=20, pady=(0, 10))

        self._statusTextBox = customtkinter.CTkTextbox(
            self._tabview.tab(self._tabName), width=250
        )
        self._statusTextBox.grid(
            row=0, rowspan=3, column=1, padx=20, pady=(20, 0), sticky="nsew"
        )
        self._statusTextBox.configure(state="disabled")

    def test_button_event(self):
        print(self._tabData._repoName)

    def status_button_event(self):
        self._statusTextBox.configure(state="normal", text_color="#FF0000")
        self._statusTextBox.delete("1.0", customtkinter.END)
        self._statusTextBox.insert("0.0", self._tabData.get_status_untracked())
        self._statusTextBox.insert("0.0", "Untracked files:\n")
        self._statusTextBox.insert("0.0", self._tabData.get_status_unstaged())
        self._statusTextBox.insert("0.0", "Changes not staged for commit:\n")
        self._statusTextBox.configure(state="disabled")


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self._gitProjectTabs = []

        # configure window
        self.title("Sam GIT GUI")
        self.geometry(f"{1100}x{580}")
        self.resizable(False, False)

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
        self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame, text="Load")
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)
        self.sidebar_button_3 = customtkinter.CTkButton(
            self.sidebar_frame, text="Load All", command=self.loadall_button_event
        )
        self.sidebar_button_3.grid(row=3, column=0, padx=20, pady=10)

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

    def test_button_event(self, text: str):
        print(text)


if __name__ == "__main__":
    app = App()
    app.mainloop()
