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

seq_directory = str(pathlib.Path(__file__).parent.resolve().parent.parent)+"\data\input_sequence.txt"

numbers = []
with open(seq_directory) as file:
    for line in file:
        numbers.append(int(line[:-1]))

print(find_num(numbers, 25))


class Node():
    def __init__(self, parent):
        self.nodenum = 0
        self.parent = parent
        if self.parent != None:
            self.parent.increase()
    
    def increase(self):
        self.nodenum += 1
        if self.parent != None:
            self.parent.increase()
    
    def get_count(self):
        return self.nodenum


def insert_to_tree(bag_dict, parent, parent_node):
    bags = bag_dict[parent]
    for bag in bags:
        if len(bag)<3: continue
        name = f"{bag[1]} {bag[2]} "
        for node in [Node(parent_node) for n in range(int(bag[0]))]:
            insert_to_tree(bag_dict, name, node)


bag_directory = str(pathlib.Path(__file__).parent.resolve().parent.parent)+"\data\input_bags.txt"

bag_dict = {}
with open(bag_directory) as file:
    for line in file:
        spliced = line.split("bags contain")
        parent = spliced[0]
        arguments = spliced[1].split(", ")
        children = [chars.split(" ")[(not i):-1] for i, chars in enumerate(arguments)]
        bag_dict[parent] = children


root = Node(None)
insert_to_tree(bag_dict, "shiny gold ", root)
print(root.get_count())
