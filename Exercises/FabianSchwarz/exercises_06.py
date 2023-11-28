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

import pathlib





here = pathlib.Path(__file__).parent
exercises_dir = here.parent
root_dir = exercises_dir.parent
data_dir = root_dir / "data"






def get_to_path(inpt_path:list[str], file_structure:dict[dict]) -> dict[dict]:
    """
    Goes to a specified path and returns a dict of the file structure starting there
    """
    curr_dict = file_structure
    for elements in inpt_path:
        curr_dict = curr_dict[elements]

    return curr_dict





def get_filestructure(path_to_terminal_log:pathlib.Path) -> dict[str, dict]:
    """
    get the filestructure (nested dictionairy) using a 'terminal log'
    """
    central_dict = {"/": {}}

    curr_path = []
    dir_sizes_dict = {}


    with open(path_to_terminal_log, "r") as file:
        for lines in file:
            curr_line = lines.rstrip()#remove \n
            command_mode = curr_line.startswith("$ ")
            content = curr_line[command_mode*2:]#get the current content
            command = curr_line[2:] if command_mode else None
            #TODO: add condition to skip run if command is ls

            if command and command.startswith("cd"):#command is a cd command
                destination = command[3:]

                #update current path
                if destination == "..":
                    curr_path.pop()#move one folder up
                else:
                    curr_path.append(destination)#move into new directory
            elif not command:#no command -> add files to structure
                curr_dict = get_to_path(curr_path, central_dict)#TODO: 'cache' current directory instead of re-generating it every time
                
                if content.startswith("dir"):#create sub-directory
                    dirname = content[4:]
                    curr_dict[dirname] = {}
                else:#create file
                    # interpret files as tuples of filetype[technically unnecessary but nice to have] and file size
                    file_size_str, file_name = content.split(" ")
                    file_ending = file_name[file_name.find("."):]


                    #save file ending
                    if not file_ending.startswith("."):
                        file_ending = ""
                    else:
                        file_ending = file_ending.replace(".","")


                    curr_dict[file_name] = (int(file_size_str),file_ending)#save current file as tuple of filesize and file ending


                    path_str = "/".join(curr_path)[1:]#convert current path array to a string
                    curr_dir_size = dir_sizes_dict.get(path_str)
                    curr_dir_size = 0 if not curr_dir_size else curr_dir_size
                    dir_sizes_dict[path_str] = curr_dir_size + int(file_size_str)#TODO: remove second type cast and cast into a int just once
                    
                    #go back and add the current file size to the parent directories
                    if path_str.count("/") > 1:
                        #get recursive path array
                        progressive_path = [path_str[:i].rstrip('/') for i in range(1, len(path_str) + 1) if path_str[i - 1] == '/' or i == len(path_str)][1:-1]
                        for path in progressive_path:
                            curr_dir_size = dir_sizes_dict.get(path)#get the current parent size (WITHOUT the current file size)
                            curr_dir_size = 0 if not curr_dir_size else curr_dir_size#if the value is not present, set value 0
                            dir_sizes_dict[path] = curr_dir_size + int(file_size_str)#re-assign new value



    dir_sizes_dict["/"] = dir_sizes_dict.pop("")
    return (central_dict, dir_sizes_dict)#TODO write wrapper function that only returns the dict as the task states only the dict should be returned.



def recursive_size(inpt_dict:dict) -> int:
    """
    Calculate the total size of a directory recursivly
    """
    if inpt_dict =={}:
        return 0
    
    #loop through items in the dict:
    dict_size = 0
    for _ ,items in inpt_dict.items():
        if type(items) == dict:
            if items != {}:
                dict_size += recursive_size(items)
        else:
            dict_size += items[0]

    return dict_size




def task1_get_max_dir_sizes(dir_sizes_dict:dict[str, int], max_size:int):
    total_size = 0
    used_dicts = []#save the high-level dicts that have been used

    #test edge case root dir is smaller than the limit
    if dir_sizes_dict["/"] < max_size: return dir_sizes_dict["/"]



    for keys in dir_sizes_dict:#loop through keys in the dictionairy
        
        value = dir_sizes_dict[keys]

        if value < max_size:
            used_dicts.append(keys)
            total_size += value

    return total_size








exercise_log_path = data_dir / "terminal_record.txt"
exercises_file_structure = get_filestructure(exercise_log_path)
filesize_dict = exercises_file_structure[1]
file_system = exercises_file_structure[0]
MAX_SIZE = 100000
print(task1_get_max_dir_sizes(filesize_dict,MAX_SIZE))#1778099


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
#TODO task2




def make_space(file_system: dict[str, dict],filesize:int, dir_sizes: dict[str, int]):
    """
    Calculate which directory to delete to make space for a file that might not fit in the current state of the file system
    """
    used_space = recursive_size(file_system)#get total size of file system used
    fs_space = 70000000
    free_space = fs_space - used_space
    required_space = filesize - free_space#get the amount of space that has to be freed
    smallest_path = ("/", float("inf"))
    for key, element in dir_sizes.items():
        if element < smallest_path[1] and element >= required_space:
            smallest_path = (key, element)


    return smallest_path


print(make_space(file_system,30000000, filesize_dict))#('/pcqjnl/lrrl/nwjggvr/bwmglvmt', 1623571)