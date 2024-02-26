from common.common import ic
import os
import shutil
from pathlib import Path
from common.config import debug

class FileSystemManager:
    def __init__(self):
        if debug:
            ic(f"Call function: __init__")
        self.root_ = Path.cwd()
        if debug:
            ic(f"Initialized root path: {self.root_}")
        self.absolutePaths_ = []

    def file_exists(self, path):
        if debug:
            ic(f"Call function: file_exists")
        _path = Path(self.root_.as_posix() + str(path)[1:])
        if debug:
            ic(f"Converted path: {_path}")
        return _path.exists()

    def ls(self, path=""):
        if debug:
            ic(f"Call function: ls")
        targetPath = None
        filePaths = []

        if path == "~":
            homeDir = Path.home()
            if homeDir is None:
                if debug:
                    ic("Failed to get home directory.")
                return filePaths
            targetPath = homeDir
        elif path == "" or path == "*":
            targetPath = self.root_
        else:
            tempPath = Path(self.root_.as_posix() + path[1:])
            if debug:
                ic(f"Converted path: {tempPath}")
            if tempPath.is_relative_to(self.root_):
                targetPath = self.root_ / tempPath
            else:
                targetPath = tempPath

        if not targetPath.is_dir():
            if debug:
                ic(f"Provided path is not a directory: {targetPath}")
            return filePaths

        for entry in targetPath.iterdir():
            if entry.is_dir():
                for subEntry in entry.iterdir():
                    filePaths.append(str(subEntry))
            else:
                filePaths.append(str(entry))

        return filePaths

    def cp(self, src, dst):
        if debug:
            ic(f"Call function: cp")

        srcPath = Path(self.root_.as_posix() + src[1:])
        dstPath = Path(self.root_.as_posix() + dst[1:])
        if debug:
            ic(f"Converted source path: {srcPath}")
            ic(f"Converted destination path: {dstPath}")
        if srcPath.exists():
            if not dstPath.parent.exists():
                try:
                    os.makedirs(dstPath.parent)
                except Exception as e:
                    if debug:
                        ic(f"Failed to create directory: {dstPath.parent}")
                    return False
            try:
                shutil.copy2(srcPath, dstPath)
            except Exception as e:
                if debug:
                    ic(f"Failed to copy file: {src}")
                return False
            return True
        else:
            if debug:
                ic(f"Source file does not exist: {src}")
            return False

    def mv(self, src, dst):
        if debug:
            ic(f"Call function: mv")

        srcPath = Path(self.root_.as_posix() + src[1:])
        dstPath = Path(self.root_.as_posix() + dst[1:])
        if debug:
            ic(f"Converted source path: {srcPath}")
            ic(f"Converted destination path: {dstPath}")
        if srcPath.exists():
            if not dstPath.parent.exists():
                try:
                    os.makedirs(dstPath.parent)
                except Exception as e:
                    if debug:
                        ic(f"Failed to create directory: {dstPath.parent}")
                    return False
            try:
                shutil.move(srcPath, dstPath)
            except Exception as e:
                if debug:
                    ic(f"Failed to move file: {src}")
                return False
            return True
        else:
            if debug:
                ic(f"Source file does not exist: {src}")
            return False

    def rm(self, name):
        if debug:
            ic(f"Call function: rm")

        _path = Path(self.root_.as_posix() + name[1:])
        if debug:
            ic(f"Converted path: {_path}")
        if _path.exists():
            try:
                os.remove(_path)
            except Exception as e:
                if debug:
                    ic(f"Failed to remove file: {name}")
                return False
            return True
        else:
            if debug:
                ic(f"File does not exist: {name}")
            return False

    def rmdir(self, name):
        if debug:
            ic(f"Call function: rmdir")

        _path = Path(self.root_.as_posix() + name[1:])
        if debug:
            ic(f"Converted path: {_path}")
        if _path.exists() and _path.is_dir():
            try:
                shutil.rmtree(_path)
            except Exception as e:
                if debug:
                    ic(f"Failed to remove directory: {name}")
                return False
            return True
        else:
            if debug:
                ic(f"Directory does not exist: {name}")
            return False

    def mkdir(self, name):
        if debug:
            ic(f"Call function: mkdir")

        if str(name).endswith('/'):
            if debug:
                ic(f"Path ends with '/': {name}")
            return False

        _name = str(name)
        if str(name).startswith("./"):
            _name = str(name)[1:]
        _path = Path(self.root_.as_posix() + str(_name))
        if debug:
            ic(f"Converted path: {_path}")

        if not _path.is_absolute():
            _path = self.root_ / _path

        if '/' in _path.as_posix():
            try:
                _path.mkdir(parents=True, exist_ok=False)
                if debug:
                    ic(f"Created directory: {_path}")
                return True
            except Exception as e:
                if debug:
                    ic(f"Failed to create directory: {_path} Error: {e}")
                return False
        else:
            if debug:
                ic(f"Path is not in Unix format: {_path}")
            return False

    def touch(self, name):
        if debug:
            ic(f"Call function: touch")

        path = Path(self.root_.as_posix() + name[1:])
        if debug:
            ic(f"Converted path: {path}")
        if not path.is_absolute():
            path = self.root_ / path
        if '/' in path.as_posix():
            newFile = path.parent / path.name
            if not newFile.exists():
                newFile.touch()
                return True
            else:
                if debug:
                    ic(f"File already exists: {newFile}")
                return False
        else:
            if debug:
                ic(f"Path is not in Unix format: {path}")
            return False

    def pwd(self):
        if debug:
            ic(f"Call function: pwd")
        return str(self.root_)

    def cd(self, path):
        if debug:
            ic(f"Call function: cd")
        _path = Path(self.root_.as_posix() + path[1:])
        if debug:
            ic(f"Converted path: {_path}")
        if _path.is_absolute():
            if _path.is_dir():
                self.root_ = _path
                if debug:
                    ic(f"Changed to: {_path}")
                return True
            else:
                if debug:
                    ic(f"Path does not exist or is not a directory: {_path}")
                return False

        elif path == "~":
            self.root_ = Path.home()
            if debug:
                ic(f"Changed to: {_path}")
            return True

        elif path.startswith(".."):
            self.root_ = self.root_.parents[1]
            if debug:
                ic(f"Changed to: {_path}")
            return True

        elif path.startswith("."):
            _path = Path(self.root_.as_posix() + path[1:])
            if debug:
                ic(f"Converted path: {_path}")
            if _path.is_dir():
                self.root_ = _path
                if debug:
                    ic(f"Changed to: {_path}")
                return True
            else:
                if debug:
                    ic(f"Path does not exist or is not a directory: {_path}")
                return False

        else:
            self.root_ = self.root_ / path
            if debug:
                ic(f"Changed root path to: {self.root_}")
            if self.root_.is_dir():
                if debug:
                    ic(f"Changed to: {_path}")
                return True
            else:
                if debug:
                    ic(f"Path does not exist or is not a directory: {_path}")
                return False
            
    def combine_paths(self, absolute_path: str, relative_path: str) -> Path:
        if debug:
            ic(f"Call function: combine_paths")
        absolute_path = Path(absolute_path)
        relative_path = Path(relative_path)
        combined_path = absolute_path / relative_path
        if debug:
            ic(f"Combined path: {combined_path}")
        return combined_path

