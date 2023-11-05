#Gerrit Fritz
#03.11.2023

from functools import lru_cache


def get_numbers(path):
    numbers = []
    with open(path) as file:
        for line in file:
            numbers.append(int(line[:-1]))
    return numbers


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


numbers = get_numbers("data//input_sequence.txt")
print(find_num(numbers, 25))



def get_bag_dict(path):
    bag_dict = {}
    with open(path) as file:
        for line in file:
            spliced = line.split("bags contain")
            parent = spliced[0][:-1]
            arguments = spliced[1].split(", ")
            children = [chars.split(" ")[(not i):-1] for i, chars in enumerate(arguments)]
            bag_dict[parent] = children
    return bag_dict


def get_bag_count(root, bag_dict):
    @lru_cache()
    def count_bags(root, parent):
        bag_count = (parent!=root)
        for bag in bag_dict[parent]:
            if len(bag)<=2: continue
            name = f"{bag[1]} {bag[2]}"
            bag_count += int(bag[0]) * count_bags(root, name)
        return bag_count 
    return count_bags(root, root)
    

bag_dict =  get_bag_dict("data//input_bags.txt")
print(get_bag_count("shiny gold",bag_dict))