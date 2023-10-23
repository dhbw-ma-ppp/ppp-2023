# PART 1:
# Write a class for a French deck of cards (2-Ace of diamonds, hearts, spades, clubs).
# The deck of cards should behave like a sequence.
# When initialized the cards should all be in a well-defined order (2-Ace of each suite, suites in the order above
# I should be able to index into the deck to retrieve one card.
# I should be able to iterate over all cards in the deck.
# Printing a cards string representation should give me a nice,
# readable description of that card.


from collections import UserList


class Card:
    def __init__(self, suit, value):
        """Intitializes an object of type card.

        Args:
            suit (string): The suit of the card (e.g. Hearts)
            value (string): The value of the card (e.g. 2, Ace, ...)
        """
        self.suit = suit
        self.value = value

    def __str__(self):
        return f"{self.value} of {self.suit}s"


class FrenchDeck(UserList):
    """A type of list containing the standard card of a french deck."""

    suits = ["Diamond", "Heart", "Spade", "Club"]
    values = [
        "2",
        "3",
        "4",
        "5",
        "6",
        "7",
        "8",
        "9",
        "10",
        "Jack",
        "Queen",
        "King",
        "Ace",
    ]

    def __init__(self):
        self.data = [
            Card(suit, value)
            for suit in self.__class__.suits
            for value in self.__class__.values
        ]


french_deck = FrenchDeck()


# PART 2:
# Create a second class that represents a deck of cards usable for Skat -- it should only contain cards from 7 upwards.
# It should offer all the same functionality of the first class.
class SkatDeck(FrenchDeck):
    """A French deck without the cards 2-6"""

    _values = FrenchDeck.values[5:]


skat_deck = SkatDeck()


# Write some code to test the functionality of both kinds of decks. (You can use `assert` to make sure your classes behave the way you expect them to.)


# this proves that the deck behaves like a sequence,
# that iterating is also implemented
# and that a card can be displayed with a 'nice' string
print("\nFrench Deck:\n", *(x for x in french_deck), sep="\n")

# this proves that you can index a card in the deck
print("\nFrench Deck indexing:\n", french_deck[42])


# this proves that the same functionality of a french deck works
# for a skat deck as well

print("\nSkat Deck:\n", *(x for x in skat_deck), sep="\n")
print("\nSkat Deck indexing:\n", skat_deck[42 - 21])

# PART 3:
# write a function that accepts two numbers, a lower bound and an upper bound.
# the function should then return the count of all numbers that meet certain criteria:
# - they are within the (left-inclusive and right-exclusive) bounds passed to the function
# - there is at least one group of exactly two adjacent digits within the number which are the same (like 33 in 123345)
# - digits only increase going from left to right
#
# Examples:
# - 123345 is a valid number
# - 123341 is not a valid number, as the digits do not increase from left to right
# - 123334 is not a valid number as there is no group of exactly two repeated digits
# - 111334 is a valid number. while there are three 1s, there is also a group of exactly two 3s.
# - 112233 is a valid number. At least one group of two is fulfilled, there is no maximum to the number of such groups.
#
# run your function with the lower bound `134564` and the upper bound `585159`. Note the resulting count
# in your pull request, please.


import timeit


def find_nums(lower_bound, upper_bound):
    # found_numbers = []
    count = 0
    for num in range(lower_bound, upper_bound):
        # convert int to int array to use indexing
        arr = [int(x) for x in str(num)]

        # check if array has ascending numbers
        if arr != sorted(arr.copy()):
            continue

        # check if two same digits follow eachother
        for index, digit in enumerate(arr):
            if index < len(arr) - 1:
                if check_upper_digit(arr, digit, index) and arr.count(digit) == 2:
                    count += 1
                    break

    return count


def check_upper_digit(arr, digit, index):
    return True if (digit == arr[index + 1]) else False


## for testing ##
# def is_valid(arr):
#     result = False
#     for index, digit in enumerate(arr):
#         # if index == 0:

#         if index < len(arr) - 2:
#             if (
#                 check_upper_digit(arr, digit, index)
#                 and not check_upper_digit(arr, digit, index + 1)
#                 and not check_lower_digit(arr, digit, index)
#             ):
#                 result = True
#                 break
#     return result

# print(timeit.timeit(lambda: find_nums(134564, 585159), number=3) / 3)
print(find_nums(134564, 585159))
