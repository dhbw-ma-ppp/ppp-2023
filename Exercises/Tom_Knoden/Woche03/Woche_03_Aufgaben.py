#Part 1
suits = ["diamonds", "hearts", "spades", "clubs"]

class card:
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit

    def __str__(self):
        return (f"{self.value} of {self.suit}, ")

class french_card_deck:
    def __init__(self):
        values = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "jack", "queen", "king", "ace"]
        self.deck = []
        for suit in suits:
            for value in values:
                self.deck.append(card(value, suit))

    def __getitem__(self, index):
        if index >= 0 and index < len(self.deck):
            return self.deck[index]
        else:
            raise IndexError("Index out of bound")

    def __iter__(self):
        return (element for element in self.deck)

    def __str__(self):
        storage = ""
        for counter in range(len(self.deck)):
            storage += str(self.deck[counter])
        return storage


#Part 2
class skat_deck:
    def __init__(self):
        values = ["7", "8", "9", "10", "jack", "queen", "king", "ace"]
        self.deck = []
        for suit in suits:
            for value in values:
                self.deck.append(card(value, suit))

    def __getitem__(self, index):
        if index >= 0 and index < len(self.deck):
            return self.deck[index]
        else:
            raise IndexError("Index out of bound")

    def __iter__(self):
        return (element for element in self.deck)

    def __str__(self):
        storage = ""
        for counter in range(len(self.deck)):
            storage += str(self.deck[counter])
        return storage

#Part 3

def count_valid_numbers(lower_bound, upper_bound):
    count = 0
    for number in range(lower_bound, upper_bound):
        num_str = str(number)
        has_adjacent_duplicates = False
        is_increasing = True

        for i in range(len(num_str) - 1):
            if num_str[i] == num_str[i + 1]:
                has_adjacent_duplicates = True
            if num_str[i] > num_str[i + 1]:
                is_increasing = False

        if has_adjacent_duplicates and is_increasing:
            count += 1

    return count

lower_bound = 134564
upper_bound = 585159
result = count_valid_numbers(lower_bound, upper_bound)
print("The count of valid numbers is:", result)

