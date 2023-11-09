#Aufgabenteil 1

def find_first_invalid_number(numbers, preamble_length):
    for i in range(preamble_length, len(numbers)):
        current_number = numbers[i]
        valid = False

        for j in range(i - preamble_length, i):
            for k in range(j + 1, i):
                if numbers[j] + numbers[k] == current_number:
                    valid = True
                    break

        if not valid:
            return current_number

    return None

# Auslesen der Eingabe aus der Datei
with open('data/input_sequence.txt', 'r') as file:
    numbers = [int(line.strip()) for line in file.readlines()]

preamble_length = 25  # Für die Beispieldaten sind es 5, für die echten Daten 25
invalid_number = find_first_invalid_number(numbers, preamble_length)
print("Erste ungültige Zahl:", invalid_number)



#Aufgabenteil 2

def count_bags_inside(color, bag_rules):
    if color not in bag_rules:
        return 0

    total = 0
    for bag_color, count in bag_rules[color]:
        total += count + count * count_bags_inside(bag_color, bag_rules)

    return total

def parse_bag_rules(filename):
    bag_rules = {}
    with open(filename, 'r') as file:
        for line in file:
            parts = line.strip().split(" bags contain ")
            container = parts[0]
            contents = parts[1].split(", ")
            bag_rules[container] = []
            for content in contents:
                if content == "no other bags.":
                    continue
                count, *color_parts = content.split()
                color = " ".join(color_parts[:-1])
                bag_rules[container].append((color, int(count)))
    return bag_rules

# Lesen der Eingabe aus der Datei
bag_rules = parse_bag_rules('data/input_bags.txt')

shiny_gold_bag = "shiny gold"
bags_inside = count_bags_inside(shiny_gold_bag, bag_rules)
print("Anzahl der Taschen im inneren der glänzenden goldenen Tasche:", bags_inside)

