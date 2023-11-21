# PART 1:
# Here's a sequence of numbers:
l = [35, 20, 15, 25, 47, 40, 62, 55, 65, 95, 102, 117, 150, 182, 127, 219, 299, 277, 309, 576]
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
import re
from pathlib import Path
  

def find_pair(file_path, preceding_numbers):
    """
    args: txt file, count of preceding numbers
    this function reads a text file with 1000 lines, each consisting of an integer
    it tries to find two different integers whithin the range of the count of preceding numbers given,
      that sum up to the pointer at position (preceding_numbers).
    if it finds fitting numbers, it prints them out.
    if not it returns the value, the pointer is looking at. 
    """
    pointer = preceding_numbers
    with file_path.open() as input_file:
        arr = []
        i = 0

        while i < 1000:
            arr.append(int(input_file.readline()))
            i += 1

    while pointer < len(arr):
        preceding_array = arr[pointer-preceding_numbers:pointer]
        element = 0
        element2 = 0
        
        while element in range(0,len(preceding_array)):
            
            while element2 in range(0,len(preceding_array)):
                
                if element != element2 and preceding_array[element] + preceding_array[element2] == arr[pointer]:
                    print(preceding_array[element], " + ", preceding_array[element2], " = ", arr[pointer])
                    pointer += 1
                    preceding_array = arr[pointer-preceding_numbers:pointer]
                    element = 0
                    element2 = 0        

                elif element == len(preceding_array)-1 and element2 == len(preceding_array)-1:
                    return arr[pointer]
                
                elif element2 < len(preceding_array)-1:
                    element2 += 1

                else:
                    element2 = 0
                    element += 1

            if element < len(preceding_array)-1:
                element += 1

numbers_path = Path(__file__).parent.parent.parent / 'data' / 'input_sequence.txt'                          #sets numbers_path as path for input txt file
                
print(find_pair(numbers_path,25), "kann nicht mit den vorherigen dargestellt werden")
                    

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

bags_path = Path(__file__).parent.parent.parent / 'data' / 'input_bags.txt'

def fill_bag_dict(file_path):
    """
    args: file path
    this function gets the path of a txt file consistiong of unknown lines in the form "word1 word2 bag contains" x * "integer word3 word4 bags" 
    and puts it in dictionary with: {"word1 word2": ["integer",x*("word3 word4")]}
    it returns this dictionary
    """
    bag_dict = {}
    with open(file_path, 'r') as input_file:
        while (input_line := input_file.readline()) != '':
            key = re.match(r"([^ ]* [^ ]*)", input_line)[0]
            data = re.findall(r"(\d+) ([^ ]* [^ ]*)", input_line)
            bag_dict[key] = data
    return bag_dict

def count_bags(bag_dict,start_bag):
    """
    args: dictionary of bags, starting bag
    this function gets a dictionary key (starting bag) and "opens" it.
    Then it runs itself with the given bags inside as new starting bags and sums up the amount of the coloured bag times the bags in it
    returns: amount of bags in the given starting bag
    """
    bags = 0
    for bag in bag_dict[start_bag]:
        if bag[0] != "no":
            bags += int(bag[0]) * count_bags(bag_dict,bag[1]) + int(bag[0])
        else:
            bags = int(bag[0])
    return bags

print(count_bags(fill_bag_dict(bags_path),"shiny gold"))
    