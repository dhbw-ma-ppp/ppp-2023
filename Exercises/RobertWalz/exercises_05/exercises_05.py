# # PART 1:
# # Here's a sequence of numbers:
# # [35, 20, 15, 25, 47, 40, 62, 55, 65, 95, 102, 117, 150, 182, 127, 219, 299, 277, 309, 576]
# # numbers in this list can in general be expressed as a sum of some pair of two numbers
# # in the five numbers preceding them.
# # For example, the sixth number (40) cam be expressed as 25 + 15
# # the seventh number (62) can be expressed as 47 + 15 etc.
# #
# # The only exception to this rule for this example is the number 127.
# # The five preceding numbers are [95, 102, 117, 150, 182], and no possible sum of two of those
# # numbers adds to 127.
# #
# # You can find the ACTUAL input for this exercise under `data/input_sequence.txt`. For this
# # real input you should consider not only the 5 numbers, but the 25 numbers preceding.
# # Find the first number in this list which can not be expressed as a
# # sum of two numbers out of the 25 numbers before it.
# # Please make not of your result in the PR.



def calc_sums(numbers):
    sums = []
    for index, number in enumerate(numbers):
        for summand in numbers[index + 1 :]:
            sums.append(number + summand)
    return sums


def get_data():
    try:
        with open("data/input_sequence.txt") as file:
            data = [int(line) for line in file.readlines()]
    except FileNotFoundError:
        print("Please change your cwd to the base directory of the repository!")
        exit(0)
    except ValueError:
        print("The data has to be integer only!")
        exit(0)
    return data


numbers = get_data()


# lower_bound = 0
# upper_bound = 25
# for index in range(25, len(numbers)):
#     sums = calc_sums(numbers[lower_bound:upper_bound])
#     if numbers[index] not in sums:
#         print(f"Found {numbers[index]} at {index}")
#         break
#     lower_bound += 1
#     upper_bound += 1      
          





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


# Example usage:


from bag import Bag

def get_data():
    try:
        with open("data/input_bags.txt") as file:
            data = [line.split(" bags contain ") for line in file.readlines()]
    except FileNotFoundError:
        print("Please change your cwd to the base directory of the repository!")
        exit(0)
    except ValueError:
        print("The data has to be integer only!")
        exit(0)
    return data


data = get_data()



for entry in data:
    bag_instance = Bag.get_instance_by_name(entry[0])
    content_list = entry[1].replace("\n", "").replace(" bags", "").replace(" bag", "").replace(".", "").split(", ")
    if content_list[0] == "no other":
        continue
    for item in content_list:  
        content = item.split(" ", 1) # splits in [amount, name]
        content_bag_instance = Bag.get_instance_by_name(content[1].rstrip())
        bag_instance.add_content(content_bag_instance, int(content[0]))

    

shiny_gold_bag = Bag.get_instance_by_name("shiny gold")
print(shiny_gold_bag.count_content())
