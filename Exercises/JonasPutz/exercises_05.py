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

from pathlib import Path

def _check_number(number_id, numbers, check_length):
    """checks if the number in the array 'numbers' at 'number_id' is a sum with 2 of the prior 'check_length' numbers"""
    for sum1 in range(number_id - check_length, number_id):
        for sum2 in range(sum1 + 1, number_id):
            if numbers[sum1] + numbers[sum2] == numbers[number_id]: return True
    return False

def number_sum_checker(numbers, check_length):
    """checks if all 'numbers' in the array can be written as a sum of 2 of the prior 'check_length' numbers"""
    for check_value in range(check_length, len(numbers)):
        if not _check_number(check_value, numbers, check_length):
            print(f"numbers[{check_value}] = {numbers[check_value]} is not a sum of 2 out of {check_length} prior numbers")
            return False
    return True

file_path = Path('.') / 'ppp-2023' / 'data' / 'input_sequence.txt'
with file_path.open("r") as ifile:
    numbers = [int(line.strip()) for line in ifile]
    number_sum_checker(numbers, 25)
# numbers[653] = 1639024365 is not a sum of 2 out of 25 prior numbers

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

_global_bag_dict = {}   #stores all bags mentioned by the rules
class Bag:
    def __init__(self, bags):
        self._bags = bags       #an array of the bags inside this bag in the format [(count, name),...]
        self._bag_count = -1    #the count of the bags inside this bag (-1 if currently unknown)

    def __repr__(self):
        return f"{self._bags}"
    
    def count_bags(self):
        """returns the number of bags inside this bag"""
        if self._bag_count != -1: return self._bag_count #value already known. Can return it
        else: 
            #Value unknown. Calculate it as the sum of the bagcount * number of bags inside the subbag + 1
            self._bag_count = sum(count * (_global_bag_dict[name].count_bags() + 1) for count, name in self._bags)
            return self._bag_count

def count_bags(lines, bag_key):
    for line in lines:
        bag_name, bag_content = line.split(" bags contain ")

        if bag_content == "no other bags":
            #add empty bag
            _global_bag_dict[bag_name] = Bag([])
        else:
            contained_bags = []
            for bag in bag_content.split(', '):
                count, name = bag.split(' ', 1)
                count = int(count)
                if count == 1: contained_bags.append((1, name.rstrip("bag")[:-1]))
                else: contained_bags.append((count, name.rstrip("bags")[:-1]))

            #add bag with subbag
            _global_bag_dict[bag_name] = Bag(contained_bags)

    #return the number of bags inside the requested bag
    return _global_bag_dict[bag_key.rstrip('bag')[:-1]].count_bags()

file_path = Path('.') / 'ppp-2023' / 'data' / 'input_bags.txt'
with file_path.open("r") as ifile:
    lines = [line.strip()[:-1] for line in ifile]
    print(f"the shiny gold bag contains {count_bags(lines, 'shiny gold bag')} bags")
# the shiny gold bag contains 6260 bags