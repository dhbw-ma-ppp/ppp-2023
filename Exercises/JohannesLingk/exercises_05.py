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


def part1_read_sequence():
    """
    Reads the sequence of numbers from input file for part 1
    """
    with open(".\data\input_sequence.txt", "r") as f:
        result = [int(n) for n in f.readlines()]
        f.close()
    return result

def part1_solution(numbers: list, scanr: int):
    """
    Returns the first numbers that cannot be constructed by adding two previous numbers
    """
    for index in range(scanr, len(numbers)):
        checked = numbers[index-scanr: index]
        valid = False
        while checked:
            req = numbers[index] - checked.pop(0)
            if req in checked:
                valid = True
                break
        if not valid:
            return numbers[index]
        
# "small is beautiful" # ( solution only for fun )
def part1_solution_oneline(n: list, s: int):
    return[n[i]for i in range(s,len(n))if not any([a for a in n[i-s:i]if n[i]-a in n[i-s:i]])][0]


numbers = part1_read_sequence()
assert part1_solution(numbers, 25) == 1639024365
assert part1_solution_oneline(numbers, 25) == 1639024365
print("Part 1: ", part1_solution(numbers, 25))


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
testbags = {
    'shiny gold bag': [('dark olive bag', 1), ('vibrant plum bag', 2)], # 8 24 1 = 33
    'dark olive bag': [('faded blue bag', 3), ('dotted black bag', 4)],  #  3 4 1= 8 
    'vibrant plum bag': [('faded blue bag', 5), ('dotted black bag', 6)], #5 6 1 = 12
    'faded blue bag': [], 'dotted black bag': [], # 1 1
}
# therefore, your single shiny gold bag contains a total of 32 bags
# (1 dark olive bag, containing 7 other bags, and 2 vibrant plum bags, 
# each of which contains 11 bags, so 1 + 1*7 + 2 + 2*11 = 32)
#
# The ACTUAL input to your puzzle is given in `data/input_bags.txt`, and much larger
# and much more deeply nested than the example above. 
# For the actual inputs, how many bags are inside your single shiny gold bag?
# As usual, please list the answer as part of the PR.

# start with shiny gold bag

"""
wavy red bags contain 1 light magenta bag, 4 wavy plum bags, 2 vibrant tan bags, 3 dotted turquoise bags.


Possible solutions:
- [ ] backwards evaluation with caching
- [ ] tree node counting
- [-] file line storage
- [ ] dictionary
"""

def part2_scan_file() -> dict[str, list]:
    """
    Parses the input file for part 2 into a dictionary
    """
    bags = {}
    with open(".\data\input_bags.txt", "r") as file:
        while line := file.readline():
            temp = line.split(' contain ')
            name = temp[0].rstrip('s')
            bags[name] = []
            if "no other bags." in temp[1]:
                continue
            for b in temp[1].split(', '):
                temp2 = b.split(' ')
                bags[name].append((" ".join(temp2[1:]).rstrip('\n').rstrip('.').rstrip('s'), int(temp2[0])))
        file.close()
    return bags

def _part2_rec(bags, name):
    if bags[name] == []: return 1
    else: 
        val = 1
        for b in bags[name]:
            val += _part2_rec(bags, b[0]) * b[1]
        return val

def part2_recursive():
    """
    Recursive approach for part 2
    """
    bags = part2_scan_file()

    return _part2_rec(bags, 'shiny gold bag') - 1 # -1 for shiny gold bag

def part2_iterativ():
    """
    Iterativ approach for part 2
    """
    bags = part2_scan_file()
    start_bag = 'shiny gold bag'
    cache: dict[str, int] = {}
    queue = [start_bag]
    while queue:
        entry: tuple[str, int] = bags[queue[0]]
        counter = 1
        for bag in entry:
            if bag[0] in cache and counter:
                counter += cache[bag[0]] * bag[1]
            else: 
                queue.insert(0, bag[0])
                counter = None
        if counter:
            cache[queue.pop(0)] = counter
    return cache[start_bag] - 1 # for shiny gold bag

# solution only for fun
def part2_oneline(bags, start_bag):
    return 0 if bags[start_bag] == [] else sum([(part2_oneline(bags, b[0]) + 1) * b[1] for b in bags[start_bag]])


assert part2_iterativ() == 6260
assert part2_recursive() == 6260
assert part2_oneline(part2_scan_file(), 'shiny gold bag') == 6260
print("Part 2: ", part2_iterativ())