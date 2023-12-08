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
example = """
$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k
"""

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
PART1_MAX_DIRECTORY_SIZE = 100000
# For the example above the two directories meeting the size requirement are `a` and `e`, while `/` and `d` are too large.
# The sum of the size of a and e would be 95437.
#

from collections.abc import Iterable

class File:
    """ Stores name, size and parent of a single file. """
    def __init__(self, name: str, size: int, parent: "Directory") -> None:
        self.name = name
        self.size = size
        self.parent = parent

    def absolute_path(self) -> str:
        """Absolute path to file."""
        if not self.parent: return self.name
        return self.parent.absolute_path() + self.name

class Directory:
    """
    Stores name, parent, sub-directories and files of this directory.
    Total size of this directory + sub-directories can be retrieved.
    """
    def __init__(self, name: str, parent: "Directory" = None) -> None:
        self.name = name
        self.directories: list[Directory] = []
        self.files: list[File] = []
        self.parent = parent
        self.size = None

    def add_directory(self, name: str) -> "Directory":
        """Adds a sub-directory."""
        self.directories.append( result := Directory(name, self) )
        return result

    def add_file(self, name: str, size: int) -> File:
        """Adds a file."""
        self.files.append( result := File(name, size, self) )
        return result
    
    def calculate_size(self) -> int:
        """Recursively calculates the size of this directory."""
        temp_size = 0
        for file in self.files:
            temp_size += file.size
        for dir in self.directories:
            temp_size += dir.get_size()
        self.size = temp_size
        return temp_size
    
    def get_size(self) -> int:
        """
        Returns size of directory if already calculated. 
        Otherwise calculate size.
        """
        if self.size == None:
            return self.calculate_size()
        else:
            return self.size
 
    def get_directory(self, name: str) -> "Directory":
        """Returns sub-directory with name."""
        for dir in self.directories:
            if dir.name == name:
                return dir
        return None
    
    def absolute_path(self) -> str:
        """Absolute path to directory."""
        if not self.parent: return "/"
        return self.parent.absolute_path() + self.name + "/"


class Environment:
    """Stores root directory and current working directory"""
    def __init__(self) -> None:
        self.filesystem = Directory("/") # root directory
        self.cwd = self.filesystem       # current working directory

    def change_directory(self, path: str) -> None:
        """Changes the current working directory (cd command)"""
        if path == "/": 
            # Return to top level directory
            self.cwd = self.filesystem

        elif path == "..":
            # Go up one directory
            self.cwd = self.cwd.parent

        else:
            # Go to directory with path
            new_dir = self.cwd.get_directory(path)
            if new_dir == None:
                raise DirectoryNotFoundError(f"{self.cwd.absolute_path()}{path}/")
            self.cwd = new_dir
                


    def register_directory(self, dir: Directory) -> None:
        """Tell the filesystem that this directory exists."""
        self.cwd.add_directory(dir)

    def register_file(self, name: str, size: int) -> None:
        """Tell the filesystem that this file exists."""
        self.cwd.add_file(name, size)

    def interpret_terimal_record(self, instructions: Iterable[str]) -> None:
        """Reconstruct the filesystem tree from a terminal log."""
        for line in instructions:
            if line == "": pass

            elif line.startswith("$"):
                if line.startswith("$ cd"):
                    self.change_directory(line[5:])
            
            else:
                if line.startswith("dir"):
                    self.register_directory(line[4:])
                
                else:
                    split = line.split(" ")
                    self.register_file(split[1], int(split[0]))

class DirectoryNotFoundError(Exception):
    """Raised when trying to change to a non existent directory."""
    pass


env = Environment()

with open("data/terminal_record.txt", "r") as file:
    env.interpret_terimal_record((l.rstrip("\n") for l in file.readlines()))


def _part_1_recursive(dir: Directory, valid_dirs: list) -> int:
    # Check if file has valid size
    if dir.get_size() <= PART1_MAX_DIRECTORY_SIZE:
        valid_dirs.append(dir)
    # Recusively check sub-directories
    for sub_dir in dir.directories:
        _part_1_recursive(sub_dir, valid_dirs)


def part_1():
    valid_dirs = []
    _part_1_recursive(env.filesystem, valid_dirs)
    total_size = sum((dir.size for dir in valid_dirs))
    print(f"Total size = {total_size}")
    return total_size

assert part_1() == 1778099





#
# PART 2:
# In part 2 you need to identify a single directory to delete (including all sub-directories of course).
# The total space available to the filesystem is 70_000_000, and you need to make enough room to fit a file of 
# size 30_000_000.
PART2_TOTAL_SPACE = 70_000_000
PART2_REQUIRED_SPACE = 30_000_000
#
# In the example above, the total size of the outermost directory (and thus the total amount of used space) is 48_381_165; 
# this means that the size of the unused space must currently be 21_618_835, which isn't quite the 30_000_000 required.
# Therefore, the update still requires a directory with total size of at least 8_381_165 to be deleted before it can run.
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
#

def _part_2_recursive(dir: Directory, possible_dirs: list, space_to_free: int) -> None:
    # Check if directory is sufficiently large
    if dir.get_size() >= space_to_free:
        # Insert directory into sorted list
        i = 0
        while i < len(possible_dirs) and dir.get_size() >= possible_dirs[i].get_size():
            i += 1
        possible_dirs.insert(i, dir)
    # Recursively check sub-directories
    for sub_dir in dir.directories:
        _part_2_recursive(sub_dir, possible_dirs, space_to_free)


def part_2() -> int:
    possible_dirs: list[Directory] = []
    space_to_free = PART2_REQUIRED_SPACE - PART2_TOTAL_SPACE + env.filesystem.get_size()
    _part_2_recursive(env.filesystem, possible_dirs, space_to_free)
    dir_to_delete = possible_dirs[0]
    
    print(f"Space to free: {space_to_free}")
    print(f"Directory to delete: {dir_to_delete.absolute_path()}")
    print(f"Size of directory: {dir_to_delete.get_size()}")

    return dir_to_delete.get_size()

assert part_2() == 1623571