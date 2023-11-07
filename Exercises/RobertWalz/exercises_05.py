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


lower_bound = 0
upper_bound = 25
for index in range(25, len(numbers)):
    sums = calc_sums(numbers[lower_bound:upper_bound])
    if numbers[index] not in sums:
        print(f"Found {numbers[index]} at {index}")
        break
    lower_bound += 1
    upper_bound += 1      
          
# import logging


# def find_non_matching_sums(numbers_to_look_at):




#     def generate_sum_sequence(length):
#         sequence = [0]

#         for i in range(0, length - 1):
#             sequence.append(sequence[i] + length)
#             length -= 1

#         return sequence

#     sum_sequence = generate_sum_sequence(numbers_to_look_at - 1)

#     def fill_sums(sums, numbers):
#         for index, number in enumerate(numbers):
#             for summand in numbers[index + 1 :]:
#                 sums.append(number + summand)

#     sums = []
#     fill_sums(sums=sums, numbers=numbers[:numbers_to_look_at])

#     def replace_sums(old_value, new_value, position_of_sum_block):
#         sums_replaced = 0
#         move_up = 0
#         block_replaced = False
#         indexes_replaced = []
#         while sums_replaced < 24:
#             # this replaces the last entry manually, to avoid index erros
#             if (position_of_sum_block == numbers_to_look_at - 2) and not block_replaced:
#                 # print(f"old value was {sums[len(sums)-1]}")
#                 # print(f"replaced at {len(sums)-1}")
#                 # sums[len(sums) - 1] = "replaced"
#                 sums[len(sums)-1] -= old_value
#                 sums[len(sums)-1] += new_value
#                 indexes_replaced.append(len(sums)-1)
#                 block_replaced = True
#                 sums_replaced += 1

#             # this replaces the big block of sums
#             if not block_replaced:
#                 for i, _ in enumerate(
#                     sums[
#                         sum_sequence[position_of_sum_block] : sum_sequence[
#                             position_of_sum_block + 1
#                         ]
#                     ],
#                     start=sum_sequence[position_of_sum_block],
#                 ):
#                     # print(f"old value was {sums[i]}")
#                     # print(f"replaced at {i}")
#                     # sums[i] = "replaced"
#                     sums[i] -= old_value
#                     sums[i] += new_value
#                     indexes_replaced.append(i)
                    
#                     sums_replaced += 1
#             else:
#                 value = sum_sequence[position_of_sum_block - move_up] + move_up
#                 # print(f"old value was {sums[value]}")

#                 # print(f"replaced at {value}")

#                 sums[value] -= old_value
#                 sums[value] += new_value
#                 indexes_replaced.append(value)
#                 sums_replaced += 1
#                 move_up += 1
#             block_replaced = True
#             # print(f"replaced {sums_replaced} sums")
#         print(f"Sums replaced: {indexes_replaced}")
    
#     for index, _ in enumerate(
#         numbers, start=numbers_to_look_at - 1
#     ):  # zero based
#         if numbers[index] not in sums:
#             return numbers[index]
#         else:
#             print(num_block := index  % (numbers_to_look_at- 1))
#             replace_sums(numbers[index - numbers_to_look_at + 1], numbers[index], num_block)
#             # print(sums)


# print(f"Found number: {find_non_matching_sums(25)}!")


# def fill_correct_sums(sums, numbers):
#         for index, number in enumerate(numbers):
#             for summand in numbers[index + 1 :]:
#                 sums.append(number + summand)





# # PART 2:
# # The input to this exercise specifies rules for bags containing other bags.
# # It is of the following form:
# #
# # shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
# # dark olive bags contain 3 faded blue bags, 4 dotted black bags.
# # vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
# # faded blue bags contain no other bags.
# # dotted black bags contain no other bags.
# #
# # You have a single 'shiny gold bag'. Consider the rules above. According
# # to those rules your bag contains
# # - 1 dark olive bag, in turn containing
# #   - 3 faded blue bags (no further content)
# #   - 4 dotted black bags (no further content
# # - 2 vibrant plum bags, in turn containing
# #   - 5 faded blue bags (no further content)
# #   - 6 dotted black bags (no further content)
# #
# # therefore, your single shiny gold bag contains a total of 32 bags
# # (1 dark olive bag, containing 7 other bags, and 2 vibrant plum bags,
# # each of which contains 11 bags, so 1 + 1*7 + 2 + 2*11 = 32)
# #
# # The ACTUAL input to your puzzle is given in `data/input_bags.txt`, and much larger
# # and much more deeply nested than the example above.
# # For the actual inputs, how many bags are inside your single shiny gold bag?
# # As usual, please list the answer as part of the PR.


# # Example usage:
