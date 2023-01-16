import customtkinter

from GITProjectObject import GITProjectObject


class TabObject:
    _tabName: str = ""
    _tabData: GITProjectObject
    _repoLabelDir: customtkinter.CTkLabel
    _repoActiveBranch: customtkinter.CTkLabel
    _fetchButton: customtkinter.CTkButton
    _pullButton: customtkinter.CTkButton
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
        self._repoLabelDir.grid(row=0, column=0, padx=0, pady=(0, 0))

        self._repoActiveBranch = customtkinter.CTkLabel(
            self._tabview.tab(self._tabName),
            text="Active Branch: " + str(data.get_active_branch()),
        )
        self._repoActiveBranch.grid(row=1, column=0, padx=0, pady=(0, 0))

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

    def commit_button_event(self):
        self._tabData.commit_push_changes(
            self._commitTypeBox.get(),
            self._commitCodeTextBox.get("1.0", customtkinter.END),
            self._commitTextBox.get("1.0", customtkinter.END),
        )
