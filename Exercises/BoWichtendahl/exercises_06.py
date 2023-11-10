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

import re
from pathlib import Path


def cwd_and_upstream_paths(in_path: str) -> str:
    while in_path != '/':
        yield in_path
        in_path = re.match(r'(.*/).*/$', in_path).group(1)
    yield '/'


def deduce_directory_sizes(input_history_path: Path) -> dict:
    directory_sizes = {'/': 0}
    current_dir = '/'
    with input_history_path.open() as input_history:
        last_command = ''
        while (current_line := input_history.readline().strip().split(' '))[0] != '':
            if current_line[0] == '$':
                last_command = current_line[1]
                ls_first_iter = True
            if last_command == 'cd':
                match current_line[2]:
                    case '/':
                        current_dir = '/'
                    case '..':
                        try:
                            current_dir = re.match(r'(.*/).*/$', current_dir).group(1)
                        except AttributeError:
                            current_dir = '/'
                    case _:
                        current_dir += current_line[2] + '/'
                        if current_dir not in directory_sizes.keys():
                            directory_sizes[current_dir] = 0
            elif last_command == 'ls':
                if ls_first_iter:
                    ls_first_iter = False
                else:
                    match current_line[0]:
                        case 'dir':
                            pass
                        case _:
                            for dir_path in cwd_and_upstream_paths(current_dir):
                                directory_sizes[dir_path] += int(current_line[0])
            else:
                raise RuntimeError('This should never be reached. The terminal history probably contained some unknown '
                                   'commands')
    return directory_sizes


def dir_size_sum(dir_sizes_dict: dict, max_dir_size: int) -> int:
    return sum([dir_size for dir_size in dir_sizes_dict.values() if dir_size <= max_dir_size])


def determine_directory_to_delete(dir_sizes_dict: dict, file_system_size: int, needed_space: int) -> str:
    free_space = file_system_size - dir_sizes_dict['/']
    size_to_delete = needed_space - free_space
    min_offset = file_system_size
    current_determined_path = ''
    for path, dir_size in dir_sizes_dict.items():
        offset = dir_size - size_to_delete
        if 0 <= offset < min_offset:
            min_offset = offset
            current_determined_path = path
    return current_determined_path


terminal_history_path = Path(__file__).parents[2] / 'data' / 'terminal_record.txt'
directory_sizes_dict = deduce_directory_sizes(terminal_history_path)

max_directory_size = 100000
print(f'The sum of the sizes of all directories with a maximal size of {max_directory_size} is:'
      f' {dir_size_sum(directory_sizes_dict, max_directory_size)}')

fs_size = 70000000
required_space = 30000000
dir_path_to_delete = determine_directory_to_delete(directory_sizes_dict, fs_size, required_space)
print(f'The directory to delete has the following path: {dir_path_to_delete}')
print(f'{directory_sizes_dict[dir_path_to_delete]} Storage Units will be freed, leaving '
      f'{fs_size - required_space - directory_sizes_dict['/'] + directory_sizes_dict[dir_path_to_delete]}'
      f' free after the Update')
