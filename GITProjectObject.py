import git
from git import Repo
import giturlparse


class GITProjectObject:
    _giturl: str = ""
    _isB2C: bool = True
    _projectPath: str = ""
    _repoName: str = ""
    _isValid: bool = False

    _repo: Repo

    def __init__(self, giturl: str = "", isb2c: bool = False, repoName: str = ""):
        if repoName is not "":
            self._isB2C = isb2c
            self._projectPath = "/Projects/" if isb2c is True else "/B2BProjects/"
            self._repoName = repoName
            self._repo = git.Repo(self._projectPath + repoName)
            self._isValid = True

            return

        if giturl is None:
            return

        if giturlparse.validate(giturl) is False:
            return

        self._isValid = True
        self._giturl = giturl
        self._isB2C = isb2c
        self._projectPath = "/Projects/" if isb2c is True else "/B2BProjects/"
        self._repoName = giturlparse.parse(giturl).repo

    def print_data(self):
        if self._isValid is True:
            print("\n\n------------------")
            print(self._repoName)
            print(self._giturl)
            print(self._isB2C)
            print(self._projectPath)
            print("------------------\n\n")
        else:
            print("\n\n------------------")
            print("invalid")
            print("------------------\n\n")

    def clone(self):
        if self._isValid is True:
            self._repo = git.Repo.clone_from(
                self._giturl, self._projectPath + self._repoName
            )
            for submodule in self._repo.submodules:
                submodule.update(init=True)

    def get_status_unstaged(self):
        changedFiles = [item.a_path for item in self._repo.index.diff(None)]
        output = ""
        for line in changedFiles:
            output = output + "  " + line + "\n"
        return output

    def get_status_untracked(self):
        changedFiles = self._repo.untracked_files
        output = ""
        for line in changedFiles:
            output = output + "  " + line + "\n"
        return output

    def get_status_staged(self):
        changedFiles = [item.a_path for item in self._repo.index.diff("Head")]
        output = ""
        for line in changedFiles:
            output = output + "  " + line + "\n"
        return output

    def get_active_branch(self):
        return self._repo.active_branch

    def commit_push_changes(self, type: str, code: str, message: str):
        if len(self._repo.index.diff("HEAD")) is 0:
            return

        commitString = (
            "["
            + type
            + ("] " if type == "UPDATE" else (" " + code.strip() + "] "))
            + message
        )
        self._repo.index.commit(commitString)
        self._repo.remotes.origin.push()

    def checkout_project_branch(self, branch: str):
        for ref in self._repo.references:
            if branch == ref.name:
                self._repo.git.checkout(branch)

    def checkout_fw_branch(self, branch: str):
        fw_repo = git.Repo(self._projectPath + self._repoName + "/igb-framework")
        for ref in fw_repo.references:
            if branch == ref.name:
                fw_repo.git.checkout(branch)
