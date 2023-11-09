# PART 1:
# Here's a sequence of numbers:
# [35, 20, 15, 25, 47, 40, 62, 55, 65, 95, 102, 117, 150, 182, 127, 219, 299, 277, 309, 576]
# numbers in this list can in general be expressed as a sum of some pair of two numbers
# in the five numbers preceding them.
# For example, the sixth number (40) cam be expressed as 25 + 15
# the seventh number (62) can be expressed as 47 + 15 etc.

# The only exception to this rule for this example is the number 127.
# The five preceding numbers are [95, 102, 117, 150, 182], and no possible sum of two of those
# numbers adds to 127.
#
# You can find the ACTUAL input for this exercise under `data/input_sequence.txt`. For this
# real input you should consider not only the 5 numbers, but the 25 numbers preceding.
# Find the first number in this list which can not be expressed as a
# sum of two numbers out of the 25 numbers before it.
# Please make not of your result in the PR.

from itertools import combinations


def read_document():
    with open('input_sequence.txt', 'r') as file:
        elements = file.readlines()
        numbers = [int(x) for x in elements]
    return numbers


def comb():
    numbers = read_document()
    start = 0

    for nums in numbers:
        end = start+25
        checksum = numbers[start + 25]
        count = 0
        realnum = []
        for num in range(start, end):
            realnum.append(numbers[num])

        perm = combinations(realnum, 2)
        for elements in perm:
            sum = elements[0] + elements[1]
            if sum == checksum:
                count += 1
        start += 1

        if count == 0:
            print(checksum)
            return 0


comb()

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
#   - 4 dotted black bags (no further content)
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


def read_document2():
    with open('input_bags.txt', 'r', encoding='utf8') as file:
        elements = file.readlines()
        # print(elements)
        return elements


def count_bags(bagdict, bagcolor):
    if bagcolor not in bagdict:
        return 0
    count = 0
    for amount, bag in bagdict[bagcolor]:
        count += amount+amount * count_bags(bagdict, bag)

    return count


def main():
    bag_dict = {}
    elements = read_document2()

    for element in elements:
        element = element.strip()
        obags, ibags = element.split(" bags contain ")
        if ibags != "no other bags.":
            ibag2 = ibags.replace(" bags.", "").replace(" bag.", "").replace(" bags", "").replace(" bag", "")
            ibag = ibag2.split(", ")
            baglist = []
            for bag in ibag:
                amount, color = bag.split(" ", 1)
                amount2 = int(amount)
                baglist.append((amount2, color))
                bag_dict[obags] = baglist
        else:
            bag_dict[obags] = {}
    # print(bag_dict)
    return bag_dict


dict = main()
shiny_gold_total = count_bags(dict, "shiny gold")
print(f"the shiny gold bagd contains {shiny_gold_total} bags")
