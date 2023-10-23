# PART 1:
# Write a class for a French deck of cards (2-Ace of diamonds, hearts, spades, clubs).
# The deck of cards should behave like a sequence.
# When initialized the cards should all be in a well-defined order (2-Ace of each suite, suites in the order above
# I should be able to index into the deck to retrieve one card.
# I should be able to iterate over all cards in the deck.
# Printing a cards string representation should give me a nice, 
# readable description of that card.


import timeit


class FrenchCardDeck:
    def __init__(self):
        ranks = [Rank(str(number), number) for number in range(2, 11)] + \
         [Rank('Jack', 11), Rank('Queen', 12), Rank('King', 13), Rank('Ace', 14)]
        suits = [Suit('Hearts'), Suit('Diamonds'), Suit('Clubs'), Suit('Spades')]
        self.cards = [Card(rank, suit) for suit in suits for rank in ranks]

    def __getitem__(self, position):
        return self.cards[position]

    def __len__(self):
        return len(self.cards)

    def __iter__(self):
        return iter(self.cards)

    def __str__(self):
        return f"{self.rank.name} of {self.suit.symbol}"


class Rank(FrenchCardDeck):
    def __init__(self, name, value):
        self.name = name
        self.value = value


class Suit(FrenchCardDeck):
    def __init__(self, symbol):
        self.symbol = symbol


class Card(FrenchCardDeck):
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit


f_deck = FrenchCardDeck()

print("This is the deck you have:")
for card in f_deck:
    print(card)


print("\nYour 12th card is:")
print(f_deck[11])


# PART 2:
# Create a second class that represents a deck of cards usable for Skat -- it should only contain cards from 7 upwards.
# It should offer all the same functionality of the first class.

class SkatDeck(FrenchCardDeck):
    def __init__(self):
        skat_ranks = [Rank(str(value), value) for value in range(7, 11)] + \
            [Rank('Jack', 11), Rank('Queen', 12), Rank('King', 13), Rank('Ace', 14)]
        skat_suits = [Suit('Hearts'), Suit('Diamonds'), Suit('Clubs'), Suit('Spades')]
        self.cards = [Card(rank, suit) for suit in skat_suits for rank in skat_ranks]


s_deck = SkatDeck()

print("\nThis is the deck you have:")
for card in s_deck:
    print(card)


print("\nYour 7th card is:")
print(s_deck[6])


# Write some code to test the functionality of both kinds of decks. (You can use `assert` to make sure your classes behave the way you expect them to.)


# PART 3:
# write a function that accepts two numbers, a lower bound and an upper bound.
# the function should then return the count of all numbers that meet certain criteria:
# - they are within the (left-inclusive and right-exclusive) bounds passed to the function
# - there is at least one group of exactly two adjacent digits within the number which are the same (like 33 in 123345)
# - digits only increase going from left to right

def valid_number(digit):
    str_num = str(digit)
    has_double = False
    for index in range(len(str_num) - 1):
        if str_num[index] == str_num[index + 1] and \
            (index == 0 or str_num[index] != str_num[index - 1]) and \
           (index == len(str_num) - 2 or str_num[index] != str_num[index + 2]):
            has_double = True
        if str_num[index] > str_num[index + 1]:
            return False
    return has_double


def count_valid_numbers(lower_bound, upper_bound):
    count = 0
    for number in range(lower_bound, upper_bound):
        if valid_number(number):
            count += 1
    return count


lower_bound = 134564
upper_bound = 585159
result = count_valid_numbers(lower_bound, upper_bound)
print("\nCount of valid numbers:", result)

# result is 1306.

#print(timeit.timeit(lambda: count_valid_numbers(lower_bound, upper_bound), number=3)/3)

# Examples:
# - 123345 is a valid number
# - 123341 is not a valid number, as the digits do not increase from left to right
# - 123334 is not a valid number as there is no group of exactly two repeated digits
# - 111334 is a valid number. while there are three 1s, there is also a group of exactly two 3s.
# - 112233 is a valid number. At least one group of two is fulfilled, there is no maximum to the number of such groups.
#
# run your function with the lower bound `134564` and the upper bound `585159`. Note the resulting count
# in your pull request, please.