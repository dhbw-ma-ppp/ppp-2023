#Gerrit Fritz
#15.11.2023

from __future__ import annotations

class Directory():
    def __init__(self, parent: Directory, name: str) -> None:
        self.path, self.root = (parent.path + f"{name}/",parent.root) if parent else (name, self)
        self.parent = parent
        self.size = 0
        self.files = [] 
        self.folders = {} 
    
    def add_content(self, files: list) -> None:
        for file in files:
            if file[0]=="dir": self.folders[file[1]] = Directory(self, file[1])
            elif file[0].isnumeric(): 
                self.files.append(file)
                self.update_size(int(file[0]))
            else: raise RuntimeError(f"Wrong file prefix: {file[0]}")
            
    def update_size(self, size: int) -> None:
        self.size += size
        if self.parent != None: self.parent.update_size(size) 
    
    def get_dir(self, folder: str) -> Directory:
        if folder in self.folders.keys(): return self.folders[folder]
        elif folder == "..": return self.parent
        elif folder == "/": return self.root
        else: raise RuntimeError(f"No such dir: {folder}")
    
    def get_dict(self) -> dict:
        current_dict = {self.path: self.size}
        for child_dict in [folder.get_dict() for folder in self.folders.values()]:
            current_dict.update(child_dict)
        return(current_dict)
    

def get_record(path: str)-> list:
    commands = []
    with open(path) as file:
        for line in file:
            if line[0] == "$": commands+=[line[2:].replace("\n","").split(" ")]
            else: commands[-1]+=[tuple(line.replace("\n","").split(" "))]
    return commands 

def build_filesys(commands: list) -> Directory:
    root = Directory(None,"/")
    current = root
    for command in commands:
        match command[0]:
            case "cd": current = current.get_dir(command[1])
            case "ls": current.add_content(command[1:])
            case _: raise RuntimeError(f"Wrong command: {command[0]}")
    return root


def get_sum(size_dict:dict)->int: 
    return sum([size for size in size_dict.values() if size <= 100000])


def get_mindir(size_dict:dict, max:int, free:int)->int: 
    return min([val for val in size_dict.values() if val >= size_dict["/"]+free-max])

    

root = build_filesys(get_record("data//terminal_record.txt"))
size_dict = root.get_dict()
print(get_sum(size_dict))
print(get_mindir(size_dict,70000000, 30000000))