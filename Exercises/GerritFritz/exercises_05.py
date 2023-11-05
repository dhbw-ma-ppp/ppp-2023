#Gerrit Fritz
#03.11.2023

import pathlib

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

seq_directory = str(pathlib.Path(__file__).parent.resolve().parent.parent)+"/data/input_sequence.txt"

numbers = []
with open(seq_directory) as file:
    for line in file:
        numbers.append(int(line[:-1]))
print(find_num(numbers, 25))


def count_bags(bag_dict, parent):
    bags = bag_dict[parent]
    for bag in bags:
        if len(bag)<3: continue
        name = f"{bag[1]} {bag[2]} "
        for sub_bags in range(int(bag[0])):
            global bag_counter
            bag_counter += 1
            count_bags(bag_dict, name)
    
bag_directory = str(pathlib.Path(__file__).parent.resolve().parent.parent)+"/data/input_bags.txt"
bag_dict = {}
with open(bag_directory) as file:
    for line in file:
        spliced = line.split("bags contain")
        parent = spliced[0]
        arguments = spliced[1].split(", ")
        children = [chars.split(" ")[(not i):-1] for i, chars in enumerate(arguments)]
        bag_dict[parent] = children

bag_counter = 0
count_bags(bag_dict, "shiny gold ")
print(bag_counter)
