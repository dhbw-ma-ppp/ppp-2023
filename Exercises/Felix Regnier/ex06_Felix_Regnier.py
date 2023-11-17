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

#{'/': a, b.txt, c.dat, d}
#{'b.txt: 14848514}
#... alle dateien
#{'a': e,f,g,h.lst}
#{'e': i}
#{'d': j,d.log,d.ext,k}
#
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

from pathlib import Path

console_path = Path(__file__).parent.parent.parent / 'data' / 'terminal_record.txt'
#console_path =Path(__file__).parent / 'console_input.txt'

def fill_data_dict(console_path):
    data_dict ={}
    is_active = False
    current_dir = ''
    content = []
    with open(console_path,'r') as input_file:
        while (input_line := input_file.readline()) != '':
            if is_active and input_line.startswith('$'):
                data_dict[current_dir] = content
                current_dir = ""
                content = []
                is_active = False
            if input_line.startswith('$ cd'):
                current_dir = input_line.removeprefix('$ cd ').removesuffix('\n')
            elif is_active:
                substrings = input_line.rsplit()
                content.append(substrings[1])
            if input_line.rsplit()[0] != "$" and input_line.rsplit()[0] != "dir": 
                substrings = input_line.rsplit()
                data_dict[substrings[1]] = substrings[0]
            if input_line.startswith('$ ls'):
                is_active = True
        data_dict[current_dir] = content
        return data_dict
#print(fill_data_dict(console_path))
def size_of_dict(current_dict, data_dict ):
    current_size = 0    
    if type(data_dict[current_dict]) == str:
        current_size += int(data_dict[current_dict])
    else:
        for key in data_dict[current_dict]:
            current_size += size_of_dict(key,data_dict)
            print("current_size: ", current_size)
    return current_size
print(size_of_dict('gts',fill_data_dict(console_path)))
def get_fitting_dict(data_dict, limit,mode,total_space):
    best_size1 = 0
    best_size2 = total_space
    best_dir = ''
    for key in data_dict:
        if size_of_dict(key,data_dict) < limit and size_of_dict(key,data_dict) > best_size1 and mode == 1:
            best_size = size_of_dict(key,data_dict)
            best_size1 = size_of_dict(key,data_dict)
            best_dir = key
        elif size_of_dict(key,data_dict) > limit and size_of_dict(key,data_dict) < best_size2 and mode == 2:
            best_size = size_of_dict(key,data_dict)
            best_size2 = size_of_dict(key,data_dict)
            best_dir = key
    return best_dir, best_size
        

data_dict= fill_data_dict(console_path)

#print(get_fitting_dict(data_dict ,100000,1,0))
# prints: ('lrrl.lth, 99946)
        
def find_delete_dir(total_space, required_space, data_dict):
    print("Limit: ",required_space ,'-', total_space ,'+', size_of_dict('/',data_dict))
    limit = required_space - total_space + size_of_dict('/',data_dict)
    return get_fitting_dict(data_dict,limit,2,total_space)

#print(find_delete_dir(70000000,30000000,data_dict))


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
##################################################