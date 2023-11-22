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

from pathlib import Path

# Function to open a file and read it
def open_file():
    filepath = Path (__file__).parents[2] / 'data' / 'terminal_record.txt'
    with open(filepath, 'r') as file:
        lines = file.readlines()
    return lines

# Function to calculate sizes of directories
def directory_sizes(lines):
    directory_sizes = {'': 0}
    current_path = []

    for line in lines:
        if line.startswith('$ cd'): # directory change command if "$ cd"
            dir_name = line.split()[2] # Getting directory name
            if dir_name == '/': # reset current path is "/"
                current_path = []
            elif dir_name == '..': # remove last directory from current path
                current_path.pop() 
            else:
                current_path.append(dir_name) # Else adds directory to current path
        elif line.startswith('dir'): # dir: directory creations command
            dir_name = line.split()[1] # Getting directory name
            # Adding directory to directory sizes with size 0
            directory_sizes['/'.join((current_path + [dir_name]) if current_path else [dir_name])] = 0
        elif line[0].isdigit(): # If line starts with digit, file creation with file size
            file_size = int(line.split()[0]) # Getting file size
            directory_sizes['/'.join(current_path if current_path else [''])] += file_size #  Adding file size to current directory size

    for dir_path, size in directory_sizes.items(): # Loop through each directory and size
        parent_dir = '/'.join(dir_path.split('/')[:-1]) # Getting the parent directory
        if parent_dir in directory_sizes: # If parent dir in directory sizes dict, adding directory size
            directory_sizes[parent_dir] += size

    return directory_sizes

# Function to calculate total size of all directories
def total_size(directory_sizes):
    # sum sizes of all directory that are less or equal to 100.000, 
    total_size = sum(size for size in directory_sizes.values() if size <= 100000)
    return total_size


lines = open_file() # Open file and read
directory_sizes = directory_sizes(lines) # Calculate sizes of directories
total_size = total_size(directory_sizes) # Calculate total size of all directories
print(total_size)
        
    

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

def find_directory_to_delete(directory_sizes, total_space=70000000, space_needed=30000000):
    total_used_space = sum(directory_sizes.values())
    current_unused_space = total_space - total_used_space
    additional_space_needed = max(0, space_needed - current_unused_space)

    # Looking for smallest directory that is big enough for the requirement
    suitable_directories = {dir_path: size for dir_path, size in directory_sizes.items() if size >= additional_space_needed}
    
    if not suitable_directories:
        return None, None

    directory_to_delete = min(suitable_directories, key=suitable_directories.get)

    return directory_to_delete, suitable_directories[directory_to_delete]

directory_to_delete, deleted_directory_size = find_directory_to_delete(directory_sizes)

if directory_to_delete is None:
    print("No suitable directory found to delete.")
else:
    print(f"Delete directory `{directory_to_delete}`, increasing unused space by {deleted_directory_size}.")