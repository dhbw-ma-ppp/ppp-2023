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

#with open("./data/terminal_record.txt", "r") as input_file:
    #terminal_list = [line for line in input_file.readlines()]

#test cases:
#terminal_list = ["$ cd /", "$ ls", "dir subdir1", "123 subfile1", "dir subdir2", "$ cd subdir1", "$ ls", "234 subsubfile1", "dir subsubdir1"]
terminal_list = ["$ cd /", "$ ls", "dir subdir1", "123 subfile1.bs", "dir subdir2", "$ cd subdir1", "$ ls", "234 subsubfile1.fg", "dir subsubdir1"]

#globals:
folder_structure = {"/": list()}
dir_sizes = dict()

def create_folder_structure():
    """this method reads all lines of the input file, analyzes it and adds the described path in the golabl dictionary "folder_structure" """
    
    helping_counter = 0 #for making doubled dir/file names unique
    current_dir = None
    current_path = list()   #the current path is stored in this list, acting as a stack

    for line in terminal_list:  #going trough terminal_list and adding all dirs and files to the dict folder_structure
        line = line.split()
        former_change_of_dir = ""
        if line[1] == "cd":
            if line[2] == "..":
                if former_change_of_dir == "..":    #if there is a "cd .." following another, don't remove the current path before pop'ing from the stack
                    new_dir = current_path.pop()    #gets the upper directory out of the list/stack of the path
                    current_dir = new_dir
                else:
                    current_path.pop()
                    new_dir = current_path.pop()
                    current_dir = new_dir
            else:
                current_dir = f"{line[2]}"
                current_path.append(current_dir)
            former_change_of_dir = line[2]
                
        elif line[1] == "ls":   #can be ignored -> lines starting with dir or a numer (for a file) can only exist behind a "$ ls".
            pass

        elif line[0] == "dir":
            if f"{line[1]}" not in folder_structure: #or folder_structure[f"{line[1]}"] == []:    to make sure, no existing dir is beeing overwritten
                folder_structure[f"{line[1]}"] = [f"{current_path}"]    #adding the dir to the dict with a list containing it's path for the subelements
                temp = folder_structure[f"{current_dir}"]
                temp.append((f"{line[0]}", f"{line[1]}")) #adding the dir as a tuple (dir, <name>, <[path as list]>) to its parent-dir
                folder_structure[f"{current_dir}"] = temp
                
            else:   #a dir with the same name is already existing.
                other_dir = folder_structure[f"{line[1]}"]   #other_dir is the describing list
                other_path = other_dir[0]   #the path of every dir in the folder structure is written in first position
                if current_path == other_path:  #if this exact dir was already analyzed: Skip it
                    pass
                else:   #same name but other dir (in another path). In this case, make it's name unique for the dict and add it then
                    helping_counter += 1
                    new_name = f"{line[1]} {helping_counter}" #e.g. "exampledict 1".            

                    folder_structure[f"{new_name}"] = current_path    
                    
                    temp = folder_structure[f"{current_dir}"]
                    temp.append((f"{line[0]}", f"{new_name}")) #adding the new named dir as a tuple to its parent-dir
                    folder_structure[f"{current_dir}"] = temp

        else:   #element has to be a file
            temp = folder_structure[f"{current_dir}"]
            temp.append((int(line[0]),f"{line[1]}"))   #adding a tuple with size and name of the file to the current dir
            folder_structure[f"{current_dir}"] = temp

def recursive_calculate_size(current_directory = "/"):
    """recursive function that calculates the size of each directory in the main directory (/) and fills those in the dictionary dir_sizes. The standard directory is / """
    
    if current_directory not in dir_sizes:
            dir_sizes.update({current_directory: 0})

    for subelement in folder_structure[current_directory][1:]: #going through all subelements (in the form of tuples) of the current dir
        
        if type(subelement[0]) == int:  #add the size of the file to it's parent-dir
            temp = dir_sizes[current_directory]
            temp += subelement[0]
            dir_sizes[current_directory] = temp

        elif subelement[0] == "dir":
            subelement_size = recursive_calculate_size(subelement[1])
            temp = dir_sizes[current_directory] + subelement_size
            dir_sizes[current_directory] = temp
    
    return dir_sizes[current_directory]

def run_and_return_dict():
    """runs the upper functions to analyze the input file into the folder structure and calculate the size of the dir "/" and all of it's subdirs
    and returns the directory of sizes. That's postulated by the exercise."""
    create_folder_structure()
    recursive_calculate_size()
    return dir_sizes

def sum_dirs_of_criteria(dictionary: dict):
    """Sums sizes of all directories in the given dictionary which sizes are at most 100000 and returns the total sum"""
    sum = 0
    for dir_name in dictionary:
        if int(dictionary[dir_name]) <= 100000:
            sum += int(dictionary[dir_name])
    return sum

print(sum_dirs_of_criteria(run_and_return_dict()))

#print(dir_sizes["/"])

#print(folder_structure)

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