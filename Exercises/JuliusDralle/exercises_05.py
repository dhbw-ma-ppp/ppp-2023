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

def findNumber():
    numbers = []

    with open("data\input_sequence.txt", 'r') as fp:

        lines = fp.read().strip()

        for currentLine in lines.split("\n"):
            numbers.append(int(currentLine))

        isBuildable = True
        for iteratorThroughBigSteps in range(25,len(numbers)):
            isBuildable = False
            for iteratorThroughSmallSteps in range(iteratorThroughBigSteps-26, iteratorThroughBigSteps):
                for iteratorThroughSmallStepsTwo in range(iteratorThroughBigSteps-26, iteratorThroughBigSteps):
                    if numbers[iteratorThroughSmallSteps] + numbers[iteratorThroughSmallStepsTwo] == numbers[iteratorThroughBigSteps] and iteratorThroughSmallSteps != iteratorThroughSmallStepsTwo:
                        isBuildable = True
            if isBuildable == False:
                return f"The number {iteratorThroughBigSteps} cannot be built by the 25 numbers before"
            



print(findNumber())

# Result is: "5 + 16 = 21"


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

with open("data\input_bags.txt") as fp:

    lines_temp = fp.read().strip()

    lines = []


    for current_line in lines_temp.split("\n"):
        lines.append(current_line)


    statement_dict_array = [[],[]]  
    for iterator_lines in lines:
        #print(iterator_lines.split(" contain "))
        current_bag, statement = iterator_lines.split(" contain ")
        current_bag = current_bag[:-5]
        
        
        statement_array = []   
        # The first index of this array is the amount of bags where as the the second index are the names of the bags
        # statement_array = [[1,2],["blue bag","red bag"]] = 1 blue bag and 2 red bags
        for i in statement.split(", "):
            statement_array.append(i[:1])
            if i[-4:] == "bags":
                new_statement = i[2:-5]
                statement_array.append(new_statement)
            elif i[-5:] == "bags.":
                new_statement = i[2:-6]
                statement_array.append(new_statement)
            elif i[-3:] == "bag":
                new_statement = i[2:-4]
                statement_array.append(new_statement)
            elif i[-4:] == "bag.":
                new_statement = i[2:-5]
                statement_array.append(new_statement)
            else:
                statement_array.append(str(i[3:]))
        
        statement_dict_array[0].append(current_bag)
        statement_dict_array[1].append(statement_array)


    #print(statement_dict_array)

    def countBags(bagType):
        counter = 1
        # look for recursion end
        for i in range(0,len(statement_dict_array[0])):
            if statement_dict_array[0][i] ==  bagType and statement_dict_array[1][i][0] == "n":
                return 1
        
        for i in range(0,len(statement_dict_array[0])):
            if statement_dict_array[0][i] ==  bagType:
                for multiplicatorOfBags in range(1,len(statement_dict_array[1][i]),2):
                    counter = counter + int(statement_dict_array[1][i][multiplicatorOfBags-1]) * countBags(statement_dict_array[1][i][multiplicatorOfBags])

        return counter  

print(countBags("shiny gold"))

# Result 6261