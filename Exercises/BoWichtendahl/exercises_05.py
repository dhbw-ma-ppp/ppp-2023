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

import itertools
import re
from pathlib import Path


def find_invalid_number(file_path, scan_length):
    with file_path.open() as input_file:
        current_nums = []
        for num in range(scan_length):
            current_nums.append(int(input_file.readline()))
        replace_pointer = 0
        while (in_str := input_file.readline()) != '':
            num_to_check = int(in_str)
            permutations = list(itertools.permutations(current_nums, 2))
            if num_to_check not in [sum(perm) for perm in permutations]:
                return num_to_check
            current_nums[replace_pointer] = num_to_check
            replace_pointer = (replace_pointer + 1) % scan_length


numbers_path = Path('../../data/input_sequence.txt')
print(f'The first invalid number in the given file is: {find_invalid_number(numbers_path, 25)}')

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


def count_bags(bag_dict, bag):
    if bag_dict[bag][0][0] == 'no':
        return None
    total_bags = 0
    for content in bag_dict[bag]:
        contained_bags = count_bags(bag_dict, content[1])
        amount_bags = int(content[0])
        total_bags += amount_bags + contained_bags * amount_bags if contained_bags else amount_bags
    return total_bags


def fill_bag_dict(file_path):
    bag_dict = {}
    with open(file_path, 'r') as input_file:
        while (input_line := input_file.readline()) != '':
            input_line = re.split(r' bags\.| bag\.| bags, | bag, | bags contain ', input_line)[:-1]
            key = input_line[0]
            data = [re.split(r' ', content, 1) for content in input_line[1:]]
            bag_dict[key] = data
    return bag_dict


bags_path = Path('../../data/input_bags.txt')
my_bag_dict = fill_bag_dict(bags_path)

test_bag_dict = {'shiny gold': [['1', 'dark olive'], ['2', 'vibrant plum']],
                 'dark olive': [['3', 'faded blue'], ['4', 'dotted black']],
                 'vibrant plum': [['5', 'faded blue'], ['6', 'dotted black']],
                 'faded blue': [['no', 'other']],
                 'dotted black': [['no', 'other']]}

print(f'The test shiny gold bag contains {count_bags(test_bag_dict, 'shiny gold')} bags.')
print(f'The real shiny gold bag contains {count_bags(my_bag_dict, 'shiny gold')} bags.')
