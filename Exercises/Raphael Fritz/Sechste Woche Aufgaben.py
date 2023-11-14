from pathlib import Path
#Usage of filepaths as keys because of directories with identical names but different sizes and filepaths.

def get_terminal_session(filepath):     
    #gives out the terminal_record.txt file as a list
    with open(filepath, 'r') as file:
        sessionlist = []
        for line in file:
            sessionlist.append(line.replace("\n",""))
        return sessionlist

def get_filepath_deeper(sessionlist,index,filepath):    
    #returns filepath to be used as a key of the subdirectory in dirdict
    filepath = filepath + (sessionlist[index-1].replace("$ cd ","") + ("/"))
    return filepath

def get_filepath_parent(filepath):  
    #returns filepath of the parent directory (in "$ cd .. " command)
    filepath = "/".join(filepath.split('/')[0:-2]) + "/"
    return filepath

def get_value(index,sessionlist):   
    #returns a (value) list that contains all sub files and subdirectories (after "$ ls" command) 
    value = []
    for index2 in range(index+1,len(sessionlist)):
        if (sessionlist[index2])[0] != "$":
            if (sessionlist[index2])[0] == "d":
                subpath = sessionlist[index2].replace("dir ","")
            elif (sessionlist[index2])[0].isdigit():
                subpath = int(sessionlist[index2].split(" ")[0])
            value.append(subpath)
        else:
            break
    return value

def get_dirdict(sessionlist):   
    #returns a dictionary mapping a filepath to all its subdirectories and subfiles
    dirdict = {}
    filepath = str()
    for index in range (len(sessionlist)):
        if sessionlist[index] == '$ cd ..':
            filepath = get_filepath_parent(filepath)
        elif sessionlist[index] == '$ ls':
            filepath = get_filepath_deeper(sessionlist,index,filepath)
            value = get_value(index,sessionlist)
            dirdict[filepath] = value
    return dirdict

def get_dirsizedict(dirdict, dirsizedict,dir):  
    #recursive function, returns a dictionary with a filepath as key and its total size as value
    value = 0
    for element in dirdict[dir]:
        if str(element).isdigit():
            value += element
        else:
            value += get_dirsizedict(dirdict,dirsizedict,dir+element+"/")[dir+element+"/"]
    dirsizedict[dir] = value
    return dirsizedict
    
def task_1(dirsizedict):    
    #returns sum of all directories under or equal to 100000 in size
    sum = 0
    for value in dirsizedict.values():  
        if value <= 100000:
            sum += value
    return sum

def task_2(dirsizedict):
    #returns smallest file size that if deleted would allow for 30000000 of free space
    deletionlist = []
    unused = 70000000 - dirsizedict["//"]
    required = 30000000
    for value in dirsizedict.values():
        if unused + value >= required:
            deletionlist.append(value)
    return min(deletionlist)

path = Path("data//terminal_record.txt")
#print(get_terminal_session("data//terminal_record.txt"))#for testing
sessionlist = get_terminal_session(path)
dirdict = get_dirdict(sessionlist)
#print(get_dirdict(sessionlist))#for testing
dirsizedict = {}
#print(get_dirsizedict(dirdict,dirsizedict,"//"))#for testing
dirsizedict = get_dirsizedict(dirdict,dirsizedict,"//")
print(task_1(dirsizedict))
print(task_2(dirsizedict))