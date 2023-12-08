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
#
#
from collections.abc import Iterable

class File:
    def __init__(self, name: str, size: int, parent: "Directory") -> None:
        self.name, self.size, self.parent = name, size, parent

    def absolute_path(self) -> str:
        return self.name if not self.parent else self.parent.absolute_path() + self.name


class Directory:
    def __init__(self, name: str, parent: "Directory" = None) -> None:
        self.name, self.parent, self.size = name, parent, None
        self.directories, self.files = [], []

    def add_directory(self, name: str) -> "Directory":
        self.directories.append(result := Directory(name, self))
        return result

    def add_file(self, name: str, size: int) -> File:
        self.files.append(result := File(name, size, self))
        return result

    def get_size(self) -> int:
        if self.size is None:
            self.size = sum(file.size for file in self.files) + sum(dir.get_size() for dir in self.directories)
        return self.size

    def get_directory(self, name: str) -> "Directory":
        return next((dir for dir in self.directories if dir.name == name), None)

    def absolute_path(self) -> str:
        return "/" if not self.parent else self.parent.absolute_path() + self.name + "/"


class Environment:
    def __init__(self) -> None:
        self.filesystem, self.cwd = Directory("/"), None

    def change_directory(self, path: str) -> None:
        if path == "/": 
            self.cwd = self.filesystem
        elif path == "..":
            self.cwd = self.cwd.parent if self.cwd and self.cwd.parent else self.cwd
        else:
            new_dir = self.cwd.get_directory(path) if self.cwd else None
            self.cwd = new_dir if new_dir else self.cwd

    def register_directory(self, directory: Directory) -> None:
        if self.cwd:
            self.cwd.directories.append(directory)

    def register_file(self, name: str, size: int) -> None:
        self.cwd.files.append(File(name, size, self.cwd))

    def interpret_terminal_record(self, instructions: Iterable[str]) -> None:
        for line in instructions:
            if line.startswith("$ cd"):
                self.change_directory(line[5:])
            elif line.startswith("dir"):
                self.register_directory(Directory(line[4:], self.cwd))
            else:
                split = line.split()
                if len(split) >= 2 and split[0].isdigit():
                    self.register_file(split[1], int(split[0]))

env = Environment()
with open("C:\\Users\\PC\\Documents\\GitHub\\ppp-2023\\Exercises\\Henriette_Neumann\\terminal_record.txt", "r") as file:
    env.interpret_terminal_record((line.strip() for line in file.readlines()))

PART1_MAX_DIRECTORY_SIZE = 100000

def part_1_recursive(dir: Directory, max_size: int) -> int:
    valid_dirs = []
    
    if dir.get_size() <= max_size:
        valid_dirs.append(dir)
        print(f"Directory '{dir.absolute_path()}' size: {dir.get_size()}")

    for sub_dir in dir.directories:
        part_1_recursive(sub_dir, max_size)
    
    total_size = sum(dir.size for dir in valid_dirs)

    return total_size


result = part_1_recursive(env.filesystem, PART1_MAX_DIRECTORY_SIZE)


#def get_valid_directory_combinations(directory: Directory, max_size: int, current_size: int, current_combination: list, valid_combinations: list) -> None:
#    current_size += directory.get_size()
#   current_combination.append(directory.name)
#
#    if current_size <= max_size:
#        valid_combinations.append(current_combination.copy())
#    
#    for sub_dir in directory.directories:
#        get_valid_directory_combinations(sub_dir, max_size, current_size, current_combination, valid_combinations)
#    
#    current_combination.pop()

#valid_combinations = []
#get_valid_directory_combinations(env.filesystem, PART1_MAX_DIRECTORY_SIZE, 0, [], valid_combinations)

#for combination in valid_combinations:
#    print(f"Valid combination: {combination}")

if result <= PART1_MAX_DIRECTORY_SIZE:
    print(f"Total size of valid directories ({result}) meets the size limit of {PART1_MAX_DIRECTORY_SIZE}")
else:
    print(f"Total size of valid directories ({result}) exceeds the size limit of {PART1_MAX_DIRECTORY_SIZE}")

def get_valid_directory_sizes(directory: Directory, max_size: int, current_size: int, valid_sizes: list) -> int:
    current_size += directory.get_size()
    valid_sizes.append(current_size)
    
    for sub_dir in directory.directories:
        get_valid_directory_sizes(sub_dir, max_size, current_size, valid_sizes)

valid_sizes = []
get_valid_directory_sizes(env.filesystem, PART1_MAX_DIRECTORY_SIZE, 0, valid_sizes)

total_size = sum(valid_sizes) if valid_sizes else 0

print(f"Total size of all directories: {total_size}")
total_size






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

FILE_SIZE = 30000000
TOTAL_SPACE = 70000000

# Function to find the directory to delete
def find_directory_for_deletion(directory: Directory, required_space: int) -> int:
    if directory.get_size() <= required_space:
        return directory.get_size()

    for sub_dir in directory.directories:
        size = find_directory_for_deletion(sub_dir, required_space)
        if size:
            directory.directories.remove(sub_dir)
            return size
    
    return 0

# Search for the directory to delete
deleted_size = find_directory_for_deletion(env.filesystem, TOTAL_SPACE - FILE_SIZE)

if deleted_size:
    print(f"Total size of deleted directory: {deleted_size}")
else:
    print("No directory was deleted to free up space.")
    