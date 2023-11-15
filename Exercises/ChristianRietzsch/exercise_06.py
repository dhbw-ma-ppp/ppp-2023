def concat(value1, value2):
    value1[[*value2.keys()][0]] = [*value2.values()][0]
    return value1

def count_dir_size(dir, orig_dir, path, size_dir):
    size = 0
    keys = [*dir.keys()]    
    for key in keys:
        if type(dir[key]) == type(""):           
            zw = path.copy()
            path.append(key)
            dir_path = "/"+"/".join(path[1:])            
            s_size = count_dir_size(orig_dir[dir_path], orig_dir, path, size_dir)
            size_dir[dir_path] = s_size
            size += s_size
            path = zw
        else: 
            size += dir[key][1]
    return size

def count_all(commands):
    dir_size = {}
    dir_content = {}
    dir_path= []
    for line in commands:
        if "$ cd" in line.strip():
            if ".." in line:
                dir_path.pop()    
            else: 
                dir_path.append(line.split()[2])
        elif "$ ls" in line:
            continue
        else:
            fs = ()
            if "dir" in line:
                file, name = line.strip().split()
                fs = {name:(file)}
            else:
                size = int(line.split()[0])
                name = line.split()[1]
                file = line.split(".")[1] if "." in line else "file"
                fs = {name:(file,size)}
            path = "/"+"/".join(dir_path[1:])
            if path in dir_content:
                dir_content[path] = concat(dir_content[path], fs)
            else: 
                dir_content[path] = fs               
    dirs = dir_content
    slash_size = count_dir_size(dir_content["/"], dir_content, ["/"], dir_size)
    dir_size["/"] = slash_size
    return dir_size

def task1():
    with open("terminal_record.txt", "r") as file: 
        dir_sizes = count_all(file.readlines())
        values = [*dir_sizes.values()]
        return (sum([value for value in values if value <= 100000]))

assert(task1() == 1778099)

def task2():
    with open("terminal_record.txt", "r") as file: 
        dir_sizes = count_all(file.readlines())
        slash_size = dir_sizes["/"]
        max_size = 70000000
        req_free_space = 30000000 
        free_space = max_size - slash_size
        if free_space < req_free_space:
            needed_space = req_free_space - free_space
            return min([dir_sizes[key] for key in [*dir_sizes.keys()] if dir_sizes[key] >= needed_space])
        
assert(task2() == 1623571)
