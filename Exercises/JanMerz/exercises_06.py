import pathlib
import re
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

class Directory:
    size: int = 0
    #while the contents could easily be added to the directories, its not needed for the task and therefore not implemented
    #contents = []
    name: str = ""

    def __init__(self, name: str, size: int = 0, contents = []):
        self.name = name
        self.size = size
        #self.contents = contents

    def add_content(self, directory_dictionary: dict, name: str, size: int = 0):
        if(size == 0):
            directory_dictionary[name] = Directory(name)
        else:
            self.change_own_size(size, directory_dictionary)
        return directory_dictionary

    def change_own_size(self, size: int, directory_dictionary: dict):
        self.size += size
        #could be done with try except instead
        if(self.name != '/'):
            self._change_parent_size(size, directory_dictionary)

    def _change_parent_size(self, change_in_size: int, directory_dictionary: dict):
        #matches everything before last slash. Example: /\pcqjnl\lrrl\nwjggvr\bwmglvmt is /\pcqjnl\lrrl\nwjggvr
        parent_path = re.match(r'.*(?=\\)', self.name).group()
        directory_dictionary[parent_path].change_own_size(change_in_size, directory_dictionary)



def build_directory(console_input: list[str]):
    directory_dictionary = {}
    #substracts the cd part of the string. Example: $ cd / is substracted to /
    path = re.sub(r'^(.*?)\$ cd ', '', console_input[0])
    #since the commands always have to start with the uppermost directory, the uppermost directories name is initialized here
    directory_dictionary[path] = Directory(path)
    in_ls_output = False

    for line in console_input[1:]:

        if(line == ''):
            continue

        if(in_ls_output):
            if(line[0].isdigit()):

                #matches the number (file size) of a file. Example: 68377 jvdqjhr.jvp is 68377
                file_size = int(re.match(r'\d*', line).group())
                #substracts everything thats the number (file size) and following white space and adds the remainin string to a path.
                #Example: 68377 jvdqjhr.jvp is /\jvdqjhr.jvp
                file_name = path + "\\" + re.sub(r'^\S* ', '', line)
                directory_dictionary = directory_dictionary[path].add_content(directory_dictionary, file_name, file_size)

                continue

            elif(line[0] == "$"):
                in_ls_output = False

            

        if(line.startswith("$ cd")):
            if(line.endswith("..")):
                path = path[0:path.rfind("\\")]
            else:
                old_path = path
                #substracts the cd command and only leaves the dir name, which is added to the path.
                #Example: $ cd bwmglvmt is bwmglvmt, which is added to the path: /\pcqjnl\lrrl\nwjggvr\bwmglvmt
                path += "\\" + re.sub(r'^(.*?)\$ cd ', '', line)
                if(path not in directory_dictionary):
                    directory_dictionary = directory_dictionary[old_path].add_content(directory_dictionary, path)

        elif(line.startswith("$ ls")):
            in_ls_output = True
        
    return directory_dictionary


root_dir = pathlib.Path().absolute().parents[1]
with open(root_dir / "data" / "terminal_record.txt", "r") as file:
    console_input = [elements for elements in file.read().split("\n")] 

directory_dictionary = build_directory(console_input)
#the directory_size_dictionary is not neeeded for the program. Its still included since it technically is required by the task.
directory_size_dictionary = {}
total_size = 0

#part 1:
for key in directory_dictionary:
    directory_size_dictionary[key] = directory_dictionary[key].size
    if directory_dictionary[key].size <= 100000:
        total_size += directory_dictionary[key].size
print("the total size of all directorys <= 100000 is:", total_size)

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
total_used_space = directory_size_dictionary["/"]
available_space = 70000000 - total_used_space
file_size = 30000000
room_to_free = file_size - available_space
best_directory_size = total_used_space
directory_to_delete = "/"

for key in directory_size_dictionary:
    if(directory_size_dictionary[key] < best_directory_size and directory_size_dictionary[key] > room_to_free):
        best_directory_size = directory_size_dictionary[key]
        directory_to_delete = key

print("the path of the directory that has to be deleted is", directory_to_delete, "which has the size", best_directory_size)
