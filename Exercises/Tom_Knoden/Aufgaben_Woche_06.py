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
# Based on that function's output, calculate the total size of all directories where the size of each individual
# directory considered is at most 100000.

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

from collections import defaultdict
from pathlib import Path

def process_terminal_session(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    directory_sizes = defaultdict(int)
    current_directory = '/'
    stack = []

    for line in lines:
        line = line.strip()
        if line.startswith('$ cd'):
            destination = line.split()[-1]
            if destination == '..':
                stack.pop()
                current_directory = stack[-1] if stack else '/'
            else:
                current_directory = Path(current_directory) / destination
                stack.append(current_directory)
        elif line.startswith('dir'):
            directory_name = line.split()[-1]
            current_directory = Path(current_directory) / directory_name
            stack.append(current_directory)
        elif line.startswith('$ ls'):
            continue
        else:
            size, file_name = line.split()
            directory_sizes[current_directory] += int(size)

    return directory_sizes

def calculate_total_size(directory_sizes, max_individual_size):
    total_size = sum(size for size in directory_sizes.values() if size <= max_individual_size)
    return total_size

def find_directory_to_delete(directory_sizes, required_space):
    for directory, size in sorted(directory_sizes.items(), key=lambda x: x[1]):
        if size >= required_space:
            return directory, size

    return None, 0

def main():
    console_session_file = Path(input("Enter the path to the console session file: "))

    directory_sizes = process_terminal_session(console_session_file)
    max_individual_size = 100000
    total_size_within_limit = calculate_total_size(directory_sizes, max_individual_size)
    print(f"Total size of directories within limit: {total_size_within_limit}")

    total_space_available = 70000000
    file_size_to_fit = 30000000
    unused_space = total_space_available - total_size_within_limit
    directory_to_delete, deleted_size = find_directory_to_delete(directory_sizes, unused_space + file_size_to_fit)

    print(f"Directory to delete: {directory_to_delete}")
    print(f"Size of deleted directory: {deleted_size}")

if __name__ == "__main__":
    main()
