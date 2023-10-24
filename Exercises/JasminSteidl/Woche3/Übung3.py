# PART 1:
# Write a class for a French deck of cards (2-Ace of diamonds, hearts, spades, clubs).
# The deck of cards should behave like a sequence.
# When initialized the cards should all be in a well-defined order (2-Ace of each suite, suites in the order above
# I should be able to index into the deck to retrieve one card.
# I should be able to iterate over all cards in the deck.
# Printing a cards string representation should give me a nice, 
# readable description of that card.

# PART 2:
# Create a second class that represents a deck of cards usable for Skat -- it should only contain cards from 7 upwards.
# It should offer all the same functionality of the first class.

# Write some code to test the functionality of both kinds of decks. (You can use `assert` to make sure your classes behave the way you expect them to.)

#import timeit

class CardDeck:
    def __init__(self, ranks, suits):
        self.cards = [{'rank': rank, 'suit': suit} for suit in suits for rank in ranks]

    def __len__(self):
        return len(self.cards)

    def __getitem__(self, position):
        if 0 <= position < len(self.cards):
            return self.cards[position]
        else:
            raise IndexError("Index out of range")

    def __iter__(self):
        return iter(self.cards)

    def __str__(self):
        return f"\nYou have a {self.__class__.__name__} with {len(self)} cards"

    def card_description(self, card):
        return f"{card['rank']} of {card['suit']}"


class FrenchDeck(CardDeck):
    def __init__(self):
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
        suits = ['Diamonds', 'Hearts', 'Spades', 'Clubs']
        super().__init__(ranks, suits)


class SkatDeck(CardDeck):
    def __init__(self):
        ranks = ['7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
        suits = ['Diamonds', 'Hearts', 'Spades', 'Clubs']
        super().__init__(ranks, suits)


french_deck = FrenchDeck()

# For FrenchDeck:

# Accessing cards by index
print("This is your first card:")
card_index = 0
specific_card = french_deck[card_index]
print(french_deck.card_description(specific_card))

# Showing all cards
print("\nThis is the deck you have:")
for card in french_deck:
    print(french_deck.card_description(card))

# Printing number of cards
print(french_deck)

skat_deck = SkatDeck()

# For SkatDeck:

print("\nThis is your first card:")
card_index = 0 
specific_card = skat_deck[card_index]
print(skat_deck.card_description(specific_card))


print("\nThis is the deck you have:")
for card in skat_deck:
    print(skat_deck.card_description(card))

print(skat_deck)

# PART 3:
# write a function that accepts two numbers, a lower bound and an upper bound.
# the function should then return the count of all numbers that meet certain criteria:
# - they are within the (left-inclusive and right-exclusive) bounds passed to the function
# - there is at least one group of exactly two adjacent digits within the number which are the same (like 33 in 123345)
# - digits only increase going from left to right


def ascending(digit):
    str_num = str(digit)
    for index in range(len(str_num) - 1):
        if str_num[index] > str_num[index + 1]:
            return False
    return True


def double(digit):
    str_num = str(digit)
    for index in set(str_num):
        if str_num.count(index) == 2:
            return True
    return False


def count_valid_numbers(lower_bound, upper_bound):
    count = 0
    for digit in range(lower_bound, upper_bound):
        if ascending(digit) and double(digit):
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

