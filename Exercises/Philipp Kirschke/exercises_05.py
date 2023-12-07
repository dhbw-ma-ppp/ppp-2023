import logging
import os
from itertools import combinations
from pathlib import Path


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
def find_first_invalid_number():
    # Read the file
    working_dir = Path(os.getcwd()).parent.absolute()
    path = Path(str(working_dir) +  "/data/input_sequence.txt")
    with open(path, 'r') as file:
        # Create a list of numbers
        numbers = [int(line) for line in file.readlines()]
        # Loop through the list
        for index in range(25, len(numbers)):
            current_number = numbers[index]
            if current_number not in [sum(pair) for pair in combinations(numbers[index - 25:index], 2)]:
                return current_number

# print the result
print(find_first_invalid_number())



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
def nestedBags():
    # Read the file
    working_dir = Path(os.getcwd()).parent.absolute()
    path = Path(str(working_dir) +  "/data/input_bags.txt")
    with open(path, 'r') as file:
        # Create a list of numbers
        rules = [line.strip() for line in file.readlines()]
        # Create a dictionary of rules
        rules_dict = {}
        for rule in rules:
            # Split the rule into the bag and the content
            bag, content = rule.split(" bags contain ")
            # Split the content into a list of bags
            content = content.split(", ")
            # Create a list of the bags
            content_list = []
            for bag_content in content:
                # Split the bag content into the number and the bag
                bag_content = bag_content.split(" ")
                # If the bag content is not "no other bags"
                if bag_content[0] != "no":
                    # Create a dictionary of the content
                    content_dict = {
                        "number": int(bag_content[0]),
                        "bag": bag_content[1] + " " + bag_content[2]
                    }
                    # Add the content to the list
                    content_list.append(content_dict)
            # Add the bag and the content to the dictionary
            rules_dict[bag] = content_list
        # Create a function to count the bags
        def count_bags(bag):
            # Get the content of the bag
            content = rules_dict[bag]
            # If the bag contains no other bags
            if len(content) == 0:
                return 0
            # If the bag contains other bags
            else:
                # Create a variable to count the bags
                count = 0
                # Loop through the content
                for bag_content in content:
                    # Add the number of bags to the count
                    count += bag_content["number"]
                    # Add the number of bags times the number of bags inside the bag
                    count += bag_content["number"] * count_bags(bag_content["bag"])
                return count
        return count_bags("shiny gold")

print(nestedBags())