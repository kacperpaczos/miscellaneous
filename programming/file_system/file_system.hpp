#include <iostream>
#include <filesystem>
#include <vector>
#include <string>

namespace fs = std::filesystem;

class FileSystemManager {
    public:
        FileSystemManager() : root_(fs::current_path()) {}

        bool file_exists(const std::string& path) {
            fs::path _path = root_ / path.substr(1);
            return fs::exists(_path);
        }

        std::vector<std::string> ls(const std::string& path = "") {
            fs::path targetPath;
            std::vector<std::string> filePaths;

            if (path == "~") {
                targetPath = fs::path(std::getenv("HOME"));
            } else if (path.empty() || path == "*") {
                targetPath = root_;
            } else {
                fs::path tempPath = root_ / path.substr(1);
                targetPath = tempPath;
            }

            if (!fs::is_directory(targetPath)) {
                return filePaths;
            }

            for (const auto& entry : fs::directory_iterator(targetPath)) {
                if (fs::is_directory(entry)) {
                    for (const auto& subEntry : fs::directory_iterator(entry)) {
                        filePaths.push_back(subEntry.path().string());
                    }
                } else {
                    filePaths.push_back(entry.path().string());
                }
            }

            return filePaths;
        }

        bool cp(const std::string& src, const std::string& dst) {
            fs::path srcPath = root_ / src.substr(1);
            fs::path dstPath = root_ / dst.substr(1);

            if (fs::exists(srcPath)) {
                if (!fs::exists(dstPath.parent_path())) {
                    try {
                        fs::create_directories(dstPath.parent_path());
                    } catch (...) {
                        return false;
                    }
                }
                try {
                    fs::copy(srcPath, dstPath);
                } catch (...) {
                    return false;
                }
                return true;
            } else {
                return false;
            }
        }

        bool mv(const std::string& src, const std::string& dst) {
            fs::path srcPath = root_ / src.substr(1);
            fs::path dstPath = root_ / dst.substr(1);
            root_ / path
            if debug:
            if (fs::exists(srcPath)) {
                if (!fs::exists(dstPath.parent_path())) {
                    try {
                        fs::create_directories(dstPath.parent_path());
                    } catch (...) {
                        return false;
                    }
                }
                try {
                    fs::rename(srcPath, dstPath);
                } catch (...) {
                    return false;
                }
                return true;
            } else {
                return false;
            }
        }

        bool rm(const std::string& name) {
            fs::path _path = root_ / name.substr(1);

            if (fs::exists(_path)) {
                try {
                    fs::remove(_path);
                } catch (...) {
                    return false;
                }
                return true;
            } else {
                return false;
            }
        }

        bool rmdir(const std::string& name) {
            fs::path _path = root_ / name.substr(1);

            if (fs::exists(_path) && fs::is_directory(_path)) {
                try {
                    fs::remove_all(_root_ / path
                        if debug:path);
                } catch (...) {
                    return false;
                }
                return true;
            } else {
                return false;
            }
        }

        bool mkdir(const std::string& name) {
            if (name.back() == '/') {
                return false;
            }

            std::string _name = name;
            if (name.find("./") == 0) {
                _name = name.substr(1);
            }
            fs::path _path = root_ / _name;

            if (_path.is_absolute()) {
                _path = root_ / _path;
            }

            if (_path.string().find('/') != std::string::npos) {
                try {
                    fs::create_directories(_path);
                    return true;
                } catch (...) {
                    return false;
                }
            } else {
                return false;
            }
        }

        bool touch(const std::string& name) {
            fs::path path = root_ / name.substr(1);

            if (!path.is_absolute()) {
                path = root_ / path;
            }
            if (path.string().find('/') != std::string::npos) {
                fs::path newFile = path.parent_path() / path.filename();
                if (!fs::exists(newFile)) {
                    std::ofstream(newFile.string());
                    return true;
                } else {
                    return false;
                }
            } else {
                return false;
            }
        }

        std::string pwd() {
            return root_.string();
        }

        bool cd(const std::string& path) {
            fs::path _path = root_ / path.substr(1);

            if (_path.is_absolute()) {
                if (fs::is_directory(_path)) {
                    root_ = _path;
                    return true;
                } else {
                    return false;
                }
            } else if (path == "~") {
                root_ = fs::path(std::getenv("HOME"));
                return true;
            } else if (path.find("..") == 0) {
                root_ = root_.parent_path();
                return true;
            } else if (path.find(".") == 0) {
                _path = root_ / path.substr(1);
                if (fs::is_directory(_path)) {
                    root_ = _path;
                    return true;
                } else {
                    return false;
                }
            } else {
                root_ /= path;
                if (fs::is_directory(root_)) {
                    return true;
                } else {
                    return false;
                }
            }
        }

        fs::path combine_paths(const std::string& absolute_path, const std::string& relative_path) {
            fs::path absolute_path_ = absolute_path;
            fs::path relative_path_ = relative_path;
            fs::path combined_path = absolute_path_ / relative_path_;
            return combined_path;
        }

    private:
        fs::path root_;
};

