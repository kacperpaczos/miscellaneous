**FileSystemManager**

The **FileSystemManager** class provides methods for managing the file system. 
Below is a list of the available functions:

1. **ls**(const std::string &path = ""): 
   Lists files and directories in the given path. If no path is provided, it lists the contents of the current directory.

2. **cp**(const std::string &src, const std::string &dst): 
   Copies a file from src location to dst location. Returns true if the operation is successful, false otherwise.

3. **mv**(const std::string &src, const std::string &dst): 
   Moves a file from src location to dst location. Returns true if the operation is successful, false otherwise.

4. **rm**(const std::string &name): 
   Removes a file with the given name. Returns true if the operation is successful, false otherwise.

5. **rmdir**(const std::string &name): 
   Removes a directory with the given name. Returns true if the operation is successful, false otherwise.

6. **mkdir**(const std::string &name): 
   Creates a directory with the given name. Returns true if the operation is successful, false otherwise.

7. **touch**(const std::string &name): 
   Creates a new file with the given name. Returns true if the operation is successful, false otherwise.

8. **pwd**() const: 
   Returns the current directory.

9. **cd**(const std::filesystem::path &path): 
   Changes the current directory to the given one. Returns true if the operation is successful, false otherwise.
