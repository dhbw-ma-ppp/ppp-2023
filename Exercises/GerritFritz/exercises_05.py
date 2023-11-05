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


def get_numbers(path):
    numbers = []
    with open(seq_directory) as file:
        for line in file:
            numbers.append(int(line[:-1]))
    return numbers


seq_directory = str(pathlib.Path(__file__).parent.resolve().parent.parent)+"/data/input_sequence.txt"
numbers = get_numbers(seq_directory)
print(find_num(numbers, 25))


def get_bag_dict(path):
    bag_dict = {}
    with open(bag_directory) as file:
        for line in file:
            spliced = line.split("bags contain")
            parent = spliced[0]
            arguments = spliced[1].split(", ")
            children = [chars.split(" ")[(not i):-1] for i, chars in enumerate(arguments)]
            bag_dict[parent] = children
    return bag_dict


def get_bag_count(root, bag_dict):

    def count_bags(bag_dict, parent):
        bags = bag_dict[parent]
        for bag in bags:
            if len(bag)<3: continue
            nonlocal bag_count
            name = f"{bag[1]} {bag[2]} "
            for sub_bags in range(int(bag[0])):
                bag_count += 1
                count_bags(bag_dict, name)

    bag_count = 0
    count_bags(bag_dict, root)
    return bag_count
    
bag_directory = str(pathlib.Path(__file__).parent.resolve().parent.parent)+"/data/input_bags.txt"
bag_dict =  get_bag_dict(bag_directory)
print(get_bag_count("shiny gold ",bag_dict))
