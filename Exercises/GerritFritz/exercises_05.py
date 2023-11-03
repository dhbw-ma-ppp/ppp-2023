#Gerrit Fritz
#03.11.2023

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

seq_directory = str(pathlib.Path(__file__).parent.resolve().parent.parent)+"\data\input_sequence.txt"

numbers2 = []
with open(seq_directory) as file:
    for line in file:
        numbers2.append(int(line[:-1]))

print(find_num(numbers2, 25))


class Node():
    def __init__(self, parent, name):
        self.name = name
        self.nodenum = 0
        self.subnodes = []
        self.parent = parent
        if self.parent != None:
            self.parent.add_node(self)
            self.parent.increase()

    def add_node(self, node):
        self.subnodes.append(node)
    
    def increase(self):
        self.nodenum += 1
        if self.parent != None:
            self.parent.increase()
    
    def get_count(self):
        return self.nodenum
    
    def __str__(self):
        return f"{self.name}: \n({', '.join([str(node)for node in self.subnodes])})\n"


def insert_to_tree(bag_dict, parent, proot):
    bags = bag_dict[parent]
    for bag in bags:
        if len(bag)<3: continue
        name = f"{bag[1]} {bag[2]} "
        for node in [Node(proot, name) for n in range(int(bag[0]))]:
            insert_to_tree(bag_dict, name, node)


bag_directory = str(pathlib.Path(__file__).parent.resolve().parent.parent)+"\data\input_bags.txt"

bag_dict = {}
with open(bag_directory) as file:
    for line in file:
        spliced = line.split("bags contain")
        parent = spliced[0]
        kid = [chars.split(" ")[(1 if i == 0 else 0):-1] for i, chars in enumerate(spliced[1].split(", "))]
        bag_dict[parent] = kid         


root = Node(None, "shiny gold ")
insert_to_tree(bag_dict, root.name, root)
print(root.get_count())
