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
                value2 = sequence[value2_index]             #index of the 2nd value for addition
                if value2 == missing_rest:                  #checking if the value2 equals to the missing rest
                    found_smth += 1
        if found_smth == 0:
            return (f"the integer at sequence[{counter}] = {sequence[counter]} can't be build out of the 25 Integers in front of it!")
            #value1_index += 1

print(check_if_sum(sequence))

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
    list_of_lines = [a.rstrip(".\n") for a in file_bags.readlines()]

dict_of_bags = dict()
dict_of_values = dict()

def dictAllBags():
    """edits the dictionary by writing the names of the bags as string-key and the description as string-value"""

    for element_raw in list_of_lines:
        element_splitted = element_raw.split(" bags contain ")
        dict_of_bags.update({(f"{element_splitted[0]}"): element_splitted[1]})
        dict_of_values.update({(f"{element_splitted[0]}"): 0})


def recursive_counter(key):
    """adds the amount of inner bags out of one line of the list_of_lines and returns the amount of bags in the current bag (key)"""
    
    description = str(dict_of_bags.get(f"{key}"))
    description = description.split(", ")

    if description[0] != ("no other bags"): #recursion's break
        return_value = 0
        for part in description:
            part = part.split()
            next_bag = f"{part[1]} {part[2]}"
            content = recursive_counter(next_bag)
            amount = int(part[0])
            dict_of_values.update({f"{key}": f"{amount}"})
            return_value += amount + amount * content
        return return_value
            
    else:
        return 0


dictAllBags()

print(recursive_counter("shiny gold")) 