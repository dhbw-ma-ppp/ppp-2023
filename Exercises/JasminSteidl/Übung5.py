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

file = open("input_sequence.txt", "r")
number_sequence = [int(line.strip()) for line in file]


def find_first_unsummed_number(number_sequence):
    input_numbers = set(number_sequence[:25])

    for index in range(25, len(number_sequence)):
        target_number = number_sequence[index]
        found = False

        for num in input_numbers:
            if target_number - num in input_numbers:
                found = True
                break

        if not found:
            return target_number

        input_numbers.remove(number_sequence[index - 25])
        input_numbers.add(target_number)

    return target_number


result = find_first_unsummed_number(number_sequence)
print("The first number that doesn't match the pattern is:", result)
#1639024365
""" in case of uncertainty about the existence of an unsummed number:
if result is not None:
    print (as above)
else:
    print("input_sequence completely matches pattern") """
file.close()

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


def count_bags_inside(bag_input, bag_colour):
    if bag_colour not in bag_input:
        return 0
    total_bags = 0

    for inner_bag, quantity in bag_input[bag_colour].items():
        total_bags += quantity + quantity * count_bags_inside(bag_input, inner_bag)

    return total_bags


def contain_rules():
    file = open("input_bags.txt", "r")
    bag_input = {}
    for line in file:
        line = line.strip()
        outer_bag, inner_bags = line.split(" bags contain ")
        if inner_bags != "no other bags.":
            inner_bags = inner_bags.split(", ")
            inner_rules = {}
            for inner_bag in inner_bags:
                parts = inner_bag.split(" ")
                quantity = int(parts[0])
                colour = " ".join(parts[1:3])
                inner_rules[colour] = quantity
            bag_input[outer_bag] = inner_rules
        else:
            bag_input[outer_bag] = {}
    file.close()
    return bag_input


rules = contain_rules()
shiny_gold_total = count_bags_inside(rules, "shiny gold")
print("Total bags inside a shiny gold bag:", shiny_gold_total)
#6260
