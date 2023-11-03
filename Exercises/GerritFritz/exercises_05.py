#Gerrit Fritz
#03.11.2023

import timeit
import pathlib

numbers1 = [35, 20, 15, 25, 47, 40, 62, 55, 65, 95, 102, 117, 150, 182, 127, 219, 299, 277, 309, 576]

def find_num(numbers, dist):
    for i in range(dist,len(numbers)):
        previous = numbers[(i-dist):i]
        is_sum = False
        for num in previous:
            if numbers[i]-num in previous:
                is_sum = True
                break
        if not is_sum:
            return numbers[i]

directory = str(pathlib.Path(__file__).parent.resolve().parent.parent)+"\data\input_sequence.txt"
numbers2 = []
with open(directory) as file:
    for line in file:
        numbers2.append(int(line[:-1]))

print(find_num(numbers1, 5))
print(find_num(numbers2, 25))
print(timeit.timeit(stmt=lambda:find_num(numbers2, 25), number = 1000)/1000)


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

'''Text in Format überfrühren, regex, genestete listen von beuteln, 
theoretisch mit bäumen, die Zeilen gehören alle zusammen, 
man kann contain mit split, rechten teil, linken teil, linker teil in kommas teilen, 
bag und bags kommen in vielfach vor'''