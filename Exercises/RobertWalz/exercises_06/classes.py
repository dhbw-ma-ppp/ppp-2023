import weakref
from typing import Self
from pathlib import Path


# class FileSystemObject():
#     def get_full_path(self) -> str:
#         path = [self.name]
#         if self.parent is not None:
#             if self.parent.path
#             path.append(self.parent.get_full_path())
#         return path
        
        

class File():
    def __init__(self, size: int, name: str, cwd) -> None:
        self.size = size
        self.path: Path = cwd.path / Path(name)
        self.name = name


class Directory():
    def __init__(self, name: str, parent: Self) -> None:
        self.content: list[Self | File] = []
        if parent is not None:
            self.path: Path = parent.path / Path(name)
        else: 
            self.path = Path(name)
        self.name = name
        self.size = 0
        self.parent = parent
            # self.parent = weakref.ref(parent)
            

    def listContent(self):
        return self.content
    
    

        


class FileSystem:
    def __init__(self) -> None:
        self.current_dir: Directory = Directory("/", None)

    def add_item_to_currrent_cwd(self, item):
        # doesn't append, if already present
        if item not in self.current_dir.content:
            self.current_dir.content.append(item)

    def ls(self):
        if self.current_dir is None:
            return "No content"
        else:
            return self.current_dir.listContent()

    def change_directory(self, dir_name):
        """Changes the cwd of the FileSystem. If no matching folder is found the new cwd is created.

        Args:
            dir_name (str): The name of the new cwd
        """
        if dir_name == "..":
            new_cwd = self.current_dir.parent
        else:
            new_cwd = next(
                (dir for dir in self.current_dir.content if dir.name == dir_name),
                Directory(dir_name, self.current_dir),
            )
        self.current_dir = new_cwd


# cd, ls
