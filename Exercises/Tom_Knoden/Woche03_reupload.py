# Part 1
suits = ["diamonds", "hearts", "spades", "clubs"]

class Card:
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit

    def __str__(self):
        return f"{self.value} of {self.suit}"

class FrenchCardDeck:
    def __init__(self):
        values = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "jack", "queen", "king", "ace"]
        self.deck = [Card(value, suit) for suit in suits for value in values]

    def __getitem__(self, index):
        return self.deck[index]

    def __str__(self):
        return ", ".join(str(card) for card in self.deck)

# Part 2
class SkatDeck:
    def __init__(self):
        values = ["7", "8", "9", "10", "jack", "queen", "king", "ace"]
        self.deck = [Card(value, suit) for suit in suits for value in values]

    def __getitem__(self, index):
        return self.deck[index]

    def __str__(self):
        return ", ".join(str(card) for card in self.deck)

# Part 3
def count_valid_numbers(lower_bound, upper_bound):
    count = 0
    for number in range(lower_bound, upper_bound):
        num_str = str(number)
        has_adjacent_duplicates = any(num_str[i] == num_str[i + 1] for i in range(len(num_str) - 1))
        is_increasing = all(num_str[i] <= num_str[i + 1] for i in range(len(num_str) - 1))

        if has_adjacent_duplicates and is_increasing:
            count += 1

    return count

lower_bound = 134564
upper_bound = 585159
result = count_valid_numbers(lower_bound, upper_bound)
print("The count of valid numbers is:", result)
