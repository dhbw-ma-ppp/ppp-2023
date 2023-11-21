# PART 1:
# Here's a sequence of numbers:
# [35, 20, 15, 25, 47, 40, 62, 55, 65, 95, 102, 117, 150, 182, 127, 219, 299, 277, 309, 576]
# numbers in this list can in general be expressed as a sum of some pair of two numbers
# in the five numbers preceding them.
# For example, the sixth number (40) cam be expressed as 25 + 15
# the seventh number (62) can be expressed as 47 + 15 etc.
# 
# The only exception to this rule for this example is the number 127.
# The five preceding numbers are [95, 102, 117, 150, 182], and no possible sum of two of those
# numbers adds to 127.
#
# You can find the ACTUAL input for this exercise under `data/input_sequence.txt`. For this
# real input you should consider not only the 5 numbers, but the 25 numbers preceding.
# Find the first number in this list which can not be expressed as a
# sum of two numbers out of the 25 numbers before it.
# Please make not of your result in the PR.


import pathlib

here = pathlib.Path(__file__).parent
exercises_dir = here.parent
root_dir = exercises_dir.parent

data_dir = root_dir / "data"



#get data into a list
with open(data_dir / "input_sequence.txt","r") as file:
    data_list = [int(elements) for elements in file.read().split("\n")[:-1]]






#loop through list
idx = 25
for elements in data_list[25:]:

    #flag if the number could be constructed
    constructed = False


    #get index of first to check element going back 25 elements
    beg_elem_idx = idx - 25
    
    #first loop: idx-25 -> idx
    for i in range(beg_elem_idx, idx):
        #second loop (loop trhough rest of list for every element indexed before)
        for j in range(i, idx):
            #check if number can be constructed by two previous numbers
            if data_list[i] + data_list[j] == elements:
                constructed = True
                break
                
        if constructed:
            break

    if not constructed:
        print(f"{elements} could not be constructed by using the previous 25 numbers")

    idx += 1


#1639024365 could not be constructed by using the previous 25 numbers





# PART 2:
# The input to this exercise specifies rules for bags containing other bags.
# It is of the following form:
#
# shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
# dark olive bags contain 3 faded blue bags, 4 dotted black bags.
# vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
# faded blue bags contain no other bags.
# dotted black bags contain no other bags.
#
# You have a single 'shiny gold bag'. Consider the rules above. According
# to those rules your bag contains
# - 1 dark olive bag, in turn containing
#   - 3 faded blue bags (no further content)
#   - 4 dotted black bags (no further content
# - 2 vibrant plum bags, in turn containing
#   - 5 faded blue bags (no further content)
#   - 6 dotted black bags (no further content)
# 
# therefore, your single shiny gold bag contains a total of 32 bags
# (1 dark olive bag, containing 7 other bags, and 2 vibrant plum bags,
# each of which contains 11 bags, so 1 + 1*7 + 2 + 2*11 = 32)
#
# The ACTUAL input to your puzzle is given in `data/input_bags.txt`, and much larger
# and much more deeply nested than the example above. 
# For the actual inputs, how many bags are inside your single shiny gold bag?
# As usual, please list the answer as part of the PR.






def split_line(inpt_line:str, target_dict:dict):
    """
    split a line into a key and a array oftuples containing further keys and their count and add that key to a dictionairy
    """
    curr_bag_tuple = inpt_line.split("contain")#split string into two halves, the key bag and the bags it contains
    curr_bag = curr_bag_tuple[0]#get the current key bag
    contains = curr_bag_tuple[1][1:]#get the bags the key bag contains (as a single string)

    curr_bag_id = "-".join([elements for elements in curr_bag.split(" ") if elements != "bags"][:-1])#generate a key out of the first half

    if contains == "no other bags.":#set the recursive bag array to None
        recursive_bags = None


    else:
        contains_arr = list(contains.split(", "))#split the second string into individual strings to get each bag
        recursive_bags = []
        for bag_str in contains_arr:
            count = int(bag_str[0])#get the count of how many bags are contained
            #get the id for the bag (similar logic as before)
            contain_bag_id = "-".join([elements for elements in bag_str[2:].split(" ") if elements != "bags" or elements != "bag"][:-1])
            contain_tuple = (count, contain_bag_id)#generate a tuple out of the count and the id
            recursive_bags.append(contain_tuple)#append the 

    target_dict[curr_bag_id] = recursive_bags#create a new dictionary entry for the current bag.





def getCount(main_dict:dict, curr_key:str):
    """
    get the count of individual bags inside the bag (bag given by its key)
    """
    curr_arr = main_dict[curr_key]
    if curr_arr == None:
        return 1
    else:
        count = 0
        for elements in curr_arr:
            count += elements[0] * getCount(main_dict, elements[1])

        return count + 1






with open(data_dir / "input_bags.txt","r") as file:
    #retrieve data from the file
    data_list = file.read().split("\n")[:-1]



central_dict = {}


for str_lines in data_list:
    split_line(str_lines, central_dict)#insert the data into the dict


def task2(main_dict:dict):
    """
    wrapper for the count function, subtracts one because the main bag is counted twice
    """
    return getCount(main_dict=main_dict,curr_key="shiny-gold") - 1






print(task2(central_dict))#returns 6260 for given example















