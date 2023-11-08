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
# Please make note of your result in the PR.

with open(".\data\input_sequence.txt", "r") as file:
    sequence = [int(a) for a in file.readlines()] #creating a list, that contains all integers of the file
    #file.close()

if len(sequence) < 26:
    raise IndexError("The list of Integers is too short")

def check_if_sum(sequence):
    """checks the list, it needs as argument, for integers, which build no sum. For that, the function takes the first element of the list-part
    that contains the 25 integers to be checked, substracts it from the potential sum, and then searchs the rest of the list-part for the missing
    value."""

    for counter in range(25,len(sequence)):
        first_index = counter-25                            #index of the first element that needs to be checked for the current element at the index counter
        last_index = counter-1                              #and that's the last element
        #value1_index = first_index+1                       #for the code checking every commbination of integers only once
        found_smth = 0                                      #boolean-like varaible for checking, if a pair of values was found to build the sum
        for value1_index in range(first_index,last_index):  #going through the list and taking the current element as the first value for the addition
            value1 = sequence[value1_index]                 #current value to be the first of the potential combination
            missing_rest = sequence[counter]-value1         #the rest of the subtraction is the missing part of the combination
            #if value1_index < last_index:
            for value2_index in range(value1_index+1,last_index+1):
                value2 = sequence[value2_index]         #index of the 2nd value for addition
                if value2 == missing_rest:              #checking if the value2 equals to the missing rest
                    found_smth += 1
        if found_smth == 0:
            return (f"the integer at sequence[{counter}] = {sequence[counter]} can't be build out of the 25 Integers in front of it!")
            #value1_index += 1

#print(check_if_sum(sequence))
#print(sequence)



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

with open(".\data\input_bags.txt", "r") as file_bags:
    list_of_lines = [a.rstrip("\n") for a in file_bags.readlines()] #method rstrip("\n") removes every \n from the end of every String

amount_of_sgb = 0   #sgb= shiny gold bag
set_of_bags = set()
dict_of_bags = dict()

#print(list_of_lines)

def listAllBags():
    """takes the global list of lines that describe the bags as argument and lists every bag once in a global set"""

    for i in range(len(list_of_lines)):
        element_raw = list_of_lines[i]
        element_splitted = element_raw.split(" bags contain ")
        set_of_bags.add(element_splitted[0])
    #return set_of_bags

def createDict():
    """creates a global dictionary out of the global set of bags. The keys are the name of each bag and the values all equal 0. Those will later be
    counters for the amount of similar bags"""

    set_of_bags_as_list = list(set_of_bags)
    for i in range(len(set_of_bags_as_list)):
        element = set_of_bags_as_list[i]
        dict_of_bags.update({(f"{element}"): 0})

def countIntoDict():
    """goes through the global list of bag-descriptions and counts the amount of bags of every kind in the global dictionary already containing all bags once as keys. 
    at the end the global dictionary contains all bags as keys and their amount"""

    for element in list_of_lines:
        splitted_whole_element = element.split(" bags contain ")            #splits the element to seperate the bag from it's content (inner bags)
        splitted_content = splitted_whole_element[1].split(", ")            #splits the inner bags
        for bag_name in splitted_content:
            if bag_name != ("no other bags."):
                splitted_instruction = bag_name.split()                     #splits the String (e.g. 5 faded blue bags) into words
                amount = splitted_instruction[0]                       #amount of bags of one kind
                amount = int(amount)
                key = f"{splitted_instruction[1]} {splitted_instruction[2]}"#name of the bag to be used as key in dictionary
                value = dict_of_bags.get(f"{key}")                          #amound of bags added to the current value in the dict
                value += amount
                dict_of_bags.update({f"{key}": value})                      #update the dict with the new value

def evaluateDict():
    """adds the total amount of all bags (without shiny gold bags) into one counter and divides it by the amount of shiny gold bags. The result is than the amount of bags
    in one shiny gold bag"""

    bag_counter = 0
    list_of_keys = dict_of_bags.keys()
    for key in list_of_keys:
        if key != "shiny gold":                         #to exclude all shiny bags.
            bag_counter += int(dict_of_bags.get(f"{key}"))

    amount_of_sgb = dict_of_bags.get("shiny gold")      #sgb= shiny gold bag
    bag_counter //= amount_of_sgb

    return int(bag_counter)

def mainFunction():     #not necessary in Python, but easier to understand later on

    listAllBags()
    createDict()
    countIntoDict()
    bags_in_gold_bag = evaluateDict()
    gold_bags = dict_of_bags.get("shiny gold")
    bag_counter = 0

    list_of_keys = dict_of_bags.keys()
    for key in list_of_keys:
        bag_counter += int(dict_of_bags.get(f"{key}"))

    print(f"Every shiny gold bag contains {bags_in_gold_bag} other bags.")
    print(f"Info: There are {gold_bags} shiny gold bags in total.")
    print(f"There are {bag_counter} bags in total")

mainFunction()