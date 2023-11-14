from enum import Enum

from classes import Directory, File, FileSystem


def get_data():
    try:
        with open("data/terminal_record.txt") as file:
            data = [line for line in file.readlines()]
    except FileNotFoundError:
        print("Please change your cwd to the base directory of the repository!")
        exit(0)
    return data


class Operations(Enum):
    DEFAULT = 0
    ADDCONTENT = 1
    CHANGEDIR = 2


def evaluateTerminalRecord(data: list[str], fs: FileSystem):
    current_operation = Operations.DEFAULT
    data.pop(0)
    for entry in data:
        entry = entry.rstrip()
        entry_list = entry.split(" ")

        if entry_list[0] == "$":
            if entry_list[1] == "ls":
                current_operation = Operations.ADDCONTENT
                continue
            elif entry_list[1] == "cd":
                current_operation = Operations.CHANGEDIR

        match current_operation:
            case Operations.ADDCONTENT:
                if entry_list[0] == "dir":
                    # [dir, dir_name]
                    fs.add_item_to_currrent_cwd(
                        Directory(entry_list[1], fs.current_dir)
                    )
                else:
                    # [size, file_name]
                    fs.add_item_to_currrent_cwd(File(int(entry_list[0]), entry_list[1], fs.current_dir))

            case Operations.CHANGEDIR:
                # [$, cd, dir_name]
                fs.change_directory(entry_list[2])


result = {}
def get_dir_sizes(dir: Directory, sizes_of_dirs):
    sizes_of_dirs[str(dir.path)] = dir.size
    for content in dir.content:
        if isinstance(content, File):
            dir.size += content.size
        else:
            
            sizes_of_dirs[str(content.path)] = content.size 
            dir.size += get_dir_sizes(content, sizes_of_dirs=sizes_of_dirs)
    return dir.size

data = get_data()
file_system = FileSystem()
evaluateTerminalRecord(data=data, fs=file_system)

print(result)
