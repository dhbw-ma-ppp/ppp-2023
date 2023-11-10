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

import re # Used for Task 2
from pathlib import Path


def open_file():
    try:
        filepath = Path (__file__).parents[2] / 'data' / 'input_sequence.txt'
        with open(filepath, 'r') as file: # Opens file in read mode
            numbers = [int(line.strip()) for line in file] # Reading each line, then stripping whitespace, then converts to int and adds to a list
        return numbers
    except:
        raise Exception("Error, can't find file. Change your custom working directory.")

def find_invalid_number():
    numbers = open_file() # Calling "open_file"
    preceding_length = 25 # Length of preceding numbers to check
    
    for element in range(preceding_length, len(numbers)): # Iterating, starting from 26th element
        
        if not any(numbers[element] - numbers[element2] in numbers[element2+1:element] for element2 in range(element - preceding_length, element)): # Checks if current number is not the sum of any two of the preceding 25 numbers
            return numbers[element]
    return None


print(find_invalid_number())

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


def parse_bag_rules(filename):
    bag_rules = {}
    filepath = Path (__file__).parents[2] / 'data' / filename
    with open(filepath, 'r') as file:
        for line in file.readlines():
            bag_color = re.match(r"(\w+ \w+) bags contain", line).groups()[0]
            contains = re.findall(r"(\d+) (\w+ \w+) bag", line)
            bag_rules[bag_color] = {color: int(quantity) for quantity, color in contains}
    return bag_rules

def count_bags(bag_rules, color):
    return sum(quantity * (1 + count_bags(bag_rules, contained_color)) for contained_color, quantity in bag_rules[color].items())

bag_rules = parse_bag_rules('input_bags.txt')
print(count_bags(bag_rules, 'shiny gold'))