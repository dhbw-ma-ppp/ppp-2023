def get_numarray(filepath):
    with open(filepath, 'r') as file:
        numarr =[]
        for line in file:
            numarr.append(int(line))
        return numarr
    
def find_num(numarray,sequencelength):
    for index in range(sequencelength,len(numarray)):
        flag= False
        for element in range(index-sequencelength,index):
            targetnum = numarray[index] - numarray[element]
            precursors = numarray[index-sequencelength:index]
            if targetnum in precursors and targetnum != numarray[element] or precursors.count(targetnum)>1:
                flag = True
        if flag == False: return numarray[index]
    return "all numbers work" 

print(find_num(get_numarray("data//input_sequence.txt"),25))

def get_bag_dict(fp):
    with open(fp, 'r') as file:
        bagdict = {}
        for line in file:
            key = line.split("contain")[0].replace(" ","").replace("bags","bag")
            value = line.split("contain")[1].replace(".\n", "").replace(" ","").replace("bags","bag")
            bagdict[key] = value
        return bagdict
    
def count_of_bags(bag,bagdict):
    global count
    subbags=bagdict[bag].split(",")
    for element in subbags:
        numofelements=element[0]
        if numofelements != "n":
            count+=int(numofelements)
            for subbagcount in range(int(numofelements)):
                count_of_bags(element[1:], bagdict)
    return count
        
count=0
print(count_of_bags("shinygoldbag",get_bag_dict("data//input_bags.txt")))