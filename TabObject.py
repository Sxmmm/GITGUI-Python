import tkinter
import customtkinter
import os

from GITProjectObject import GITProjectObject
from InputBoxes import CTkCheckoutDialog


class TabObject:
    _tabName: str = ""
    _tabData: GITProjectObject
    _repoLabelDir: customtkinter.CTkLabel
    _repoActiveBranch: customtkinter.CTkLabel
    _fetchButton: customtkinter.CTkButton
    _pullButton: customtkinter.CTkButton
    _statusButton: customtkinter.CTkButton
    _addAllButton: customtkinter.CTkButton
    _addSelectionButton: customtkinter.CTkButton
    _unstageSelectionButton: customtkinter.CTkButton
    _unstageAllButton: customtkinter.CTkButton
    _vscodeButton: customtkinter.CTkButton
    _checkoutButton: customtkinter.CTkButton
    _checkoutFWButton: customtkinter.CTkButton
    _checkoutB2BButton: customtkinter.CTkButton
    _tabview: customtkinter.CTkTabview
    _unstagedStatusTextBox: customtkinter.CTkTextbox
    _commitTextBox: customtkinter.CTkTextbox
    _commitButton: customtkinter.CTkButton
    _commitTypeBox: customtkinter.CTkOptionMenu
    _commitCodeTextBox: customtkinter.CTkTextbox

    def __init__(self, data: GITProjectObject, tabview: customtkinter.CTkTabview):
        self._tabName = data._repoName + ("-b2c" if data._isB2C is True else "-b2b")
        self._tabData = data
        self._tabview = tabview

        self._repoLabelDir = customtkinter.CTkLabel(
            self._tabview.tab(self._tabName), text=data._projectPath + data._repoName
        )
        self._repoLabelDir.grid(row=0, column=0, columnspan=2, padx=0, pady=(0, 0))

        self._repoActiveBranch = customtkinter.CTkLabel(
            self._tabview.tab(self._tabName),
            text="Active Branch: " + str(data.get_active_branch()),
        )
        self._repoActiveBranch.grid(row=1, column=0, columnspan=2, padx=0, pady=(0, 0))

        self._fetchButton = customtkinter.CTkButton(
            self._tabview.tab(self._tabName),
            text="Fetch",
            command=self.fetch_button_event,
            width=100,
        )
        self._fetchButton.grid(row=2, column=0, padx=20, pady=(0, 10))

        self._pullButton = customtkinter.CTkButton(
            self._tabview.tab(self._tabName),
            text="Pull",
            command=self.fetch_button_event,
            width=100,
        )
        self._pullButton.grid(row=2, column=1, padx=20, pady=(0, 10))

        self._statusButton = customtkinter.CTkButton(
            self._tabview.tab(self._tabName),
            text="Status",
            command=self.status_button_event,
            width=100,
        )
        self._statusButton.grid(row=3, column=0, padx=20, pady=(0, 10))

        self._addAllButton = customtkinter.CTkButton(
            self._tabview.tab(self._tabName),
            text="Add all",
            command=self.add_all_button_event,
            width=100,
        )
        self._addAllButton.grid(row=4, column=0, padx=20, pady=(0, 10))

        self._addSelectionButton = customtkinter.CTkButton(
            self._tabview.tab(self._tabName),
            text="Add select",
            command=self.add_selection_button_event,
            width=100,
        )
        self._addSelectionButton.grid(row=5, column=0, padx=20, pady=(0, 10))

        self._unstageAllButton = customtkinter.CTkButton(
            self._tabview.tab(self._tabName),
            text="Unstage all",
            command=self.unstage_all_button_event,
            width=100,
        )
        self._unstageAllButton.grid(row=4, column=1, padx=20, pady=(0, 10))

        self._unstageSelectionButton = customtkinter.CTkButton(
            self._tabview.tab(self._tabName),
            text="Unstage select",
            command=self.unstage_selection_button_event,
            width=100,
        )
        self._unstageSelectionButton.grid(row=5, column=1, padx=20, pady=(0, 10))

        self._vscodeButton = customtkinter.CTkButton(
            self._tabview.tab(self._tabName),
            text="VSCode",
            command=self.open_code_button_event,
            width=100,
        )
        self._vscodeButton.grid(row=7, column=0, padx=20, pady=(0, 10))

        self._checkoutButton = customtkinter.CTkButton(
            self._tabview.tab(self._tabName),
            text="Checkout",
            command=self.checkout_project_branch,
            width=100,
        )
        self._checkoutButton.grid(row=6, column=0, padx=20, pady=(0, 10))

        self._checkoutFWButton = customtkinter.CTkButton(
            self._tabview.tab(self._tabName),
            text="Checkout FW",
            command=self.checkout_fw_branch,
            width=100,
        )
        self._checkoutFWButton.grid(row=6, column=1, padx=20, pady=(0, 10))

        self._checkoutB2BButton = customtkinter.CTkButton(
            self._tabview.tab(self._tabName),
            text="Checkout B2B",
            # command=self.open_code_button_event,
            width=100,
        )
        self._checkoutB2BButton.grid(row=6, column=2, padx=20, pady=(0, 10))

        self._stagedStatusTextBox = customtkinter.CTkTextbox(
            self._tabview.tab(self._tabName), width=350, height=150
        )
        self._stagedStatusTextBox.grid(
            row=0,
            rowspan=4,
            column=3,
            columnspan=4,
            padx=20,
            pady=(20, 0),
            sticky="nsew",
        )
        self._stagedStatusTextBox.configure(state="disabled")
        self._stagedStatusTextBox.configure(text_color="#00FF00")

        self._unstagedStatusTextBox = customtkinter.CTkTextbox(
            self._tabview.tab(self._tabName), width=350, height=150
        )
        self._unstagedStatusTextBox.grid(
            row=4,
            rowspan=4,
            column=3,
            columnspan=4,
            padx=20,
            pady=(20, 0),
            sticky="nsew",
        )
        self._unstagedStatusTextBox.configure(state="disabled")
        self._unstagedStatusTextBox.configure(text_color="#FF0000")

        self._commitTextBox = customtkinter.CTkTextbox(
            self._tabview.tab(self._tabName), width=350, height=28
        )
        self._commitTextBox.grid(
            row=9, column=2, columnspan=3, padx=(20, 0), pady=(20, 0), sticky="nsew"
        )

        self._commitButton = customtkinter.CTkButton(
            self._tabview.tab(self._tabName),
            text="Commit",
            command=self.commit_button_event,
        )
        self._commitButton.grid(row=9, column=6, padx=(20, 20), pady=(25, 10))

        self._commitTypeBox = customtkinter.CTkOptionMenu(
            self._tabview.tab(self._tabName),
            values=["TASK", "BUGFIX", "UPDATE"],
            width=100,
        )
        self._commitTypeBox.grid(row=9, column=0, padx=(20, 0), pady=(25, 10))

        self._commitCodeTextBox = customtkinter.CTkTextbox(
            self._tabview.tab(self._tabName), width=125, height=28
        )
        self._commitCodeTextBox.grid(
            row=9, column=1, padx=(20, 20), pady=(20, 0), sticky="nsew"
        )
        self._commitCodeTextBox.insert("0.0", "XXXX-XX")

        # Check status on init
        self.status_button_event()

    def fetch_button_event(self):
        for remote in self._tabData._repo.remotes:
            remote.fetch()
        # print(self._tabData._repoName)
        print("Fetched all remotes.")

    def status_button_event(self):
        self._unstagedStatusTextBox.configure(state="normal")
        self._unstagedStatusTextBox.delete("1.0", customtkinter.END)
        self._unstagedStatusTextBox.insert("0.0", self._tabData.get_status_untracked())
        self._unstagedStatusTextBox.insert("0.0", "Untracked files:\n")
        self._unstagedStatusTextBox.insert("0.0", self._tabData.get_status_unstaged())
        self._unstagedStatusTextBox.insert("0.0", "Changes not staged for commit:\n")
        self._unstagedStatusTextBox.configure(state="disabled")
        self._stagedStatusTextBox.configure(state="normal")
        self._stagedStatusTextBox.delete("1.0", customtkinter.END)
        self._stagedStatusTextBox.insert("0.0", self._tabData.get_status_staged())
        self._stagedStatusTextBox.insert("0.0", "Changes to be committed:\n")
        self._stagedStatusTextBox.configure(state="disabled")

    def add_all_button_event(self):
        self._tabData._repo.git.add("--all")
        self.status_button_event()

    def add_selection_button_event(self):
        tkinter.Tk().withdraw()  # prevents an empty tkinter window from appearing
        path = tkinter.filedialog.askopenfilename()
        self._tabData._repo.git.add(path)
        self.status_button_event()

    def unstage_selection_button_event(self):
        tkinter.Tk().withdraw()  # prevents an empty tkinter window from appearing
        path = tkinter.filedialog.askopenfilename()
        self._tabData._repo.git.reset(path)
        # self._tabData._repo.git.execute(["git", "commit", "-m", path])
        self.status_button_event()

    def unstage_all_button_event(self):
        self._tabData._repo.git.reset()
        self.status_button_event()

    def open_code_button_event(self):
        os.system("code " + self._tabData._projectPath + self._tabData._repoName)

    def checkout_project_branch(self):
        dialog = CTkCheckoutDialog(text="Checkout Branch", title="Checkout Branch")
        branch_name = dialog.get_input()

        if branch_name is "":
            return

        self._tabData.checkout_project_branch(branch_name)
        self.update_branches()

    def checkout_fw_branch(self):
        dialog = CTkCheckoutDialog(
            text="Checkout FW Branch", title="Checkout FW Branch"
        )
        branch_name = dialog.get_input()

        if branch_name is "":
            return

        self._tabData.checkout_fw_branch(branch_name)
        self.update_branches()

    def update_branches(self):
        self._repoActiveBranch.configure(
            text="Active Branch: " + str(self._tabData.get_active_branch())
        )

    def commit_button_event(self):
        self._tabData.commit_push_changes(
            self._commitTypeBox.get(),
            self._commitCodeTextBox.get("1.0", customtkinter.END),
            self._commitTextBox.get("1.0", customtkinter.END),
        )
        self.status_button_event()
