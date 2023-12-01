# You get a recording of a terminal session moving around a file system.
# The filesystem consists of a tree of files (plain data) and directories (which can contain other directories or files). 
# The outermost directory is called /. You can navigate around the filesystem, moving into or out of directories
# and listing the contents of the directory you're currently in.
#
# Within the terminal output, lines that begin with $ are commands you executed, very much like some modern computers:
#
# cd means change directory. This changes which directory is the current directory, but the specific result depends on the argument:
# cd x moves in one level: it looks in the current directory for the directory named x and makes it the current directory.
# cd .. moves out one level: it finds the directory that contains the current directory, then makes that directory the current directory.
# cd / switches the current directory to the outermost directory, /.
# ls means list. It prints out all of the files and directories immediately contained by the current directory:
# 123 abc means that the current directory contains a file named abc with size 123.
# dir xyz means that the current directory contains a directory named xyz.
#
# Here's an example:
#
# $ cd /
# $ ls
# dir a
# 14848514 b.txt
# 8504156 c.dat
# dir d
# $ cd a
# $ ls
# dir e
# 29116 f
# 2557 g
# 62596 h.lst
# $ cd e
# $ ls
# 584 i
# $ cd ..
# $ cd ..
# $ cd d
# $ ls
# 4060174 j
# 8033020 d.log
# 5626152 d.ext
# 7214296 k
#
# Based on this example, you can deduce the directory structure must look something like this:
# - / (dir)
#   - a (dir)
#     - e (dir)
#       - i (file, size=584)
#     - f (file, size=29116)
#     - g (file, size=2557)
#     - h.lst (file, size=62596)
#   - b.txt (file, size=14848514)
#   - c.dat (file, size=8504156)
#   - d (dir)
#     - j (file, size=4060174)
#     - d.log (file, size=8033020)
#     - d.ext (file, size=5626152)
#     - k (file, size=7214296)
#
#
# PART 1:
# Write a function that reads a console session like the example above from a file, 
# and then returns a dictionary listing the size of each directory. Directories should
# be identified by their full path. For the example above:
#
# - The total size of directory `e` is 584 because it contains a single file `i` of size 584 and no other directories.
# - The directory `a` has total size 94853 because it contains files
#     `f` (size 29116), `g` (size 2557), and `h.lst` (size 62596),
#     plus file `i` indirectly (`a` contains `e` which contains `i`).
# - Directory `d` has total size 24933642.
# - As the outermost directory, `/` contains every file. Its total size is 48381165.
#
# Based on that functions output, calculate the total size of all directories where the size of each individual
# directory considered is at most 100000, and mention the result in your PR.
# For the example above the two directories meeting the size requirement are `a` and `e`, while `/` and `d` are too large.
# The sum of the size of a and e would be 95437.

from __future__ import annotations
from pathlib import Path

class Directory:
    def __init__(self, name: str, parent: Directory, path: Path) -> None:
        self.name = name
        self.path = path / name
        self._size = -1
        self._parent = parent
        self._files = []
        self._dirs = []

    def __repr__(self) -> str:
        # Example: "a at /b/dec/a (12345)"
        return f"{self.name} at {self.path} ({self._size})"

    def add_file(self, size: str, name: str):
        if size == "dir":
            # Add new directory
            self._dirs.append(Directory(name, self, self.path))
        else:
            # Add new File
            self._files.append(File(name, int(size)))

    def move_directory(self, param: str) -> Directory:
        # Enables moves inside the Directory Tree
        if param == "..":
            # Move one step up (to parent)
            return self.get_parent()
        elif param == "/":
            # Move to topmost directory (to /)
            return _directory_tree
        else:
            # Move to subdirectory
            return self.get_sub_directory(param)

    def get_size(self):
        if self._size != -1:
            #Size already calculated, can be returned
            return self._size
        else:
            #The total size of the directory is the size of all subdirectories + the size of all files
            self._size = sum(dir.get_size() for dir in self._dirs) + sum(file.get_size() for file in self._files)
            return self._size
        

    def get_parent(self):
        # returnes the parent directory
        return self._parent
    
    def get_sub_directory(self, name: str):
        # returnes a subdirectory with the specified name
        for dir in self._dirs:
            if dir.name == name:
                return dir
            
        # didnt find subdirectory, an error will be raised
        raise NameError(f"Unknown directory {name}")
    
    def build_directory_list(self):
        # generator to flatten the directory tree in a single list of tuples (path, size)
        yield (self.path, self.get_size())

        for dir in self._dirs:
            # adds all the subdirs
            yield from dir.build_directory_list()

    def find_to_delete(self, size: int):
        #find the best directory to be deleted with a size of at least [size]

        if self.get_size() < size: return (None, -1) #The directory is to small!

        best_dir = (self, self.get_size())
        for dir in self._dirs:
            best_subdir = dir.find_to_delete(size)
            if best_subdir[1] > size and best_subdir[1] < best_dir[1]:
                best_dir = best_subdir #if a subdirectory is closer to the size, you should delete it

        return best_dir

class File:
    def __init__(self, name: str, size: int) -> None:
        self.name = name
        self._size = size

    def get_size(self):
        return self._size
    
_directory_tree : Directory = Directory('/', None, Path())

def build_dir_tree(file_path):
    current_dir = _directory_tree
    with file_path.open("r") as ifile:
        for line in (line.strip() for line in ifile):
            if line.startswith('$ '): 
                # line is a command
                line = line[2::]
                if line == "ls": 
                    # dont do anything with "$ ls"
                    pass
                else:
                    # command moves inside the current directory
                    command, param = line.split(' ', 1)
                    if command == "cd": current_dir = current_dir.move_directory(param)
            else:
                # line is not a command -> list of all files and directories inside current directory
                size, name = line.split(' ', 1)
                current_dir.add_file(size, name)

    #returns all directories in the required format
    return {key: value for key, value in _directory_tree.build_directory_list()}

dirs = build_dir_tree(Path('.') / 'ppp-2023' / 'data' / 'terminal_record.txt')
sum = sum(size for size in dirs.values() if size <= 100000)
print(f"The total space of all directorys with a size <= 100000 is {sum}")

# PART 2:
# In part 2 you need to identify a single directory to delete (including all sub-directories of course).
# The total space available to the filesystem is 70000000, and you need to make enough room to fit a file of 
# size 30000000.
#
# In the example above, the total size of the outermost directory (and thus the total amount of used space) is 48381165; 
# this means that the size of the unused space must currently be 21618835, which isn't quite the 30000000 required.
# Therefore, the update still requires a directory with total size of at least 8381165 to be deleted before it can run.
#
# To achieve this, you have the following options:
#
# Delete directory `e`, which would increase unused space by 584.
# Delete directory `a`, which would increase unused space by 94853.
# Delete directory `d`, which would increase unused space by 24933642.
# Delete directory `/`, which would increase unused space by 48381165.
# Directories `e` and `a` are both too small; deleting them would not free up enough space.
# However, directories `d` and `/` are both big enough! 
# Between these, choose the smallest: `d`, increasing unused space by 24933642.
# 
# Mention the total size of the deleted directory in the PR.
# 
# You can find the /actual/ input to both parts in data/terminal_record.txt
###############################################################################

def delete_dir(dir_tree: Directory, required_space: int, available_space: int):
    delete_size: int = required_space + dir_tree.get_size() - available_space

    if delete_size <= 0:
        print("No directory needs to be deleted!")
        return
    
    print(f"Required space to be delete: {delete_size}") 
    print(f"Found directory: {dir_tree.find_to_delete(delete_size)[0]}")
    
delete_dir(_directory_tree, 30000000, 70000000)