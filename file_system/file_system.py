import os
import shutil
from pathlib import Path

class FileSystemManager:
    def __init__(self):
        self.root_ = Path.cwd()
        self.absolutePaths_ = []

    def ls(self, path=""):
        targetPath = None
        filePaths = []

        if path == "~":
            homeDir = Path.home()
            if homeDir is None:
                print("Failed to get home directory.")
                return filePaths
            targetPath = homeDir
        elif path == "" or path == "*":
            targetPath = self.root_
        else:
            tempPath = Path(path)
            if tempPath.is_relative_to(self.root_):
                targetPath = self.root_ / tempPath
            else:
                targetPath = tempPath

        if not targetPath.is_dir():
            print(f"Provided path is not a directory: {str(targetPath)}")
            return filePaths

        for entry in targetPath.iterdir():
            if entry.is_dir():
                for subEntry in entry.iterdir():
                    filePaths.append(str(subEntry))
            else:
                filePaths.append(str(entry))

        return filePaths

    def cp(self, src, dst):
        srcPath = Path(src)
        dstPath = Path(dst)
        if srcPath.exists():
            if not dstPath.parent.exists():
                try:
                    os.makedirs(dstPath.parent)
                except Exception as e:
                    print(f"Failed to create directory: {str(dstPath.parent)}")
                    return False
            try:
                shutil.copy2(srcPath, dstPath)
            except Exception as e:
                print(f"Failed to copy file: {src}")
                return False
            return True
        else:
            print(f"Source file does not exist: {src}")
            return False

    def mv(self, src, dst):
        srcPath = Path(src)
        dstPath = Path(dst)
        if srcPath.exists():
            if not dstPath.parent.exists():
                try:
                    os.makedirs(dstPath.parent)
                except Exception as e:
                    print(f"Failed to create directory: {str(dstPath.parent)}")
                    return False
            try:
                shutil.move(srcPath, dstPath)
            except Exception as e:
                print(f"Failed to move file: {src}")
                return False
            return True
        else:
            print(f"Source file does not exist: {src}")
            return False

    def rm(self, name):
        _path = Path(name)
        if _path.exists():
            try:
                os.remove(_path)
            except Exception as e:
                print(f"Failed to remove file: {name}")
                return False
            return True
        else:
            print(f"File does not exist: {name}")
            return False

    def rmdir(self, name):
        _path = Path(name)
        if _path.exists() and _path.is_dir():
            try:
                shutil.rmtree(_path)
            except Exception as e:
                print(f"Failed to remove directory: {name}")
                return False
            return True
        else:
            print(f"Directory does not exist: {name}")
            return False

    def mkdir(self, name):
        if name.endswith('/'):
            print(f"Path ends with '/': {name}")
            return False

        _name = name
        _path = None
        if _name.startswith("./"):  # If name starts with "./"
            print("Converted relative path to absolute")
            try:
                _name = _name[1:]
                path = Path(_name)
                path = self.root_ / path.relative_to(self.root_)
                path = path.relative_to(self.root_)
                _path = path
            except Exception as e:
                print(f"Failed to create path. Error: {str(e)}")
                return False
        else:
            try:
                path = Path(_name)
                _path = path
            except Exception as e:
                print(f"Failed to create path. Error: {str(e)}")
                return False

        if '/' in _path.as_posix():
            newDir = _path
            intermediatePath = Path()
            for component in newDir.parts:
                intermediatePath /= component
                try:
                    if not intermediatePath.exists():
                        os.mkdir(intermediatePath)
                        print(f"Created directory: {str(intermediatePath)}")
                except Exception as e:
                    print(f"Failed to create directory: {str(intermediatePath)}. Error: {str(e)}")
                    return False
            return True
        else:
            print(f"Path is not in Unix format: {str(_path)}")
            return False

    def touch(self, name):
        path = Path(name)
        if not path.is_absolute():
            path = self.root_ / path
        if '/' in path.as_posix():
            newFile = path.parent / path.name
            if not newFile.exists():
                newFile.touch()
                return True
            else:
                print(f"File already exists: {str(newFile)}")
                return False
        else:
            print(f"Path is not in Unix format: {str(path)}")
            return False

    def pwd(self):
        return self.root_

    def cd(self, path):
        _path = Path(path)
        if _path.exists() and _path.is_dir():
            self.root_ = _path
            return True
        else:
            print(f"Path does not exist or is not a directory: {str(_path)}")
            return False

