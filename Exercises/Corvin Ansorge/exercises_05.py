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

def part1_read_input():
    with open("./../../data/input_sequence.txt") as f:
        return [int(line) for line in f.readlines()]

def find_first_invalid_number(numbers, preamble_length):
    for i in range(preamble_length, len(numbers)):
        preamble = numbers[i-preamble_length:i]
        if not any([numbers[i] - x in preamble for x in preamble]):
            return numbers[i]

print(find_first_invalid_number(part1_read_input(), 25))


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

def get_bag_dict(fp):
    with open(fp, 'r') as file:
        bagdict = {}
        for line in file:
            key = line.split("contain")[0].replace(" ","").replace("bags","bag")
            value = line.split("contain")[1].replace(".\n", "").replace(" ","").replace("bags","bag")
            bagdict[key] = value
        return bagdict

def get_bag_count(bagdict, bag):
    if bagdict[bag] == "nootherbag":
        return 0
    else:
        count = 0
        for innerbag in bagdict[bag].split(","):
            count += int(innerbag[0]) + int(innerbag[0]) * get_bag_count(bagdict, innerbag[1:])
        return count

def nestedBags(fp):
    bagdict = get_bag_dict(fp)
    return get_bag_count(bagdict, "shinygoldbag")

print(nestedBags("./../../data/input_bags.txt"))