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
