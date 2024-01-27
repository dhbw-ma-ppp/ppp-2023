# PART 1:
# Write a class for a French deck of cards (2-Ace of diamonds, hearts, spades, clubs).
# The deck of cards should behave like a sequence.
# When initialized the cards should all be in a well-defined order (2-Ace of each suite, suites in the order above
# I should be able to index into the deck to retrieve one card.
# I should be able to iterate over all cards in the deck.
# Printing a cards string representation should give me a nice, 
# readable description of that card.

from collections.abc import Sequence
#definition of class card
class Card:
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit

    def __str__(self):
        return f"{self.value} of {self.suit}"
#definition for frenchdeck 
class FrenchDeck(Sequence):
    values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace1','Ace2']
    suits = ['diamonds', 'hearts', 'spades', 'clubs']

    def __init__(self):
        self.cards = [Card(value, suit) for suit in self.suits for value in self.values]

    def __getitem__(self, position):
        return self.cards[position]

    def __len__(self):
        return len(self.cards)

    def __str__(self):
        return "French Deck of Cards"


# PART 2:
# Create a second class that represents a deck of cards usable for Skat -- it should only contain cards from 7 upwards.
# It should offer all the same functionality of the first class.

from collections.abc import Sequence

class SkatCard(Card):
    def __init__(self, value, suit):
        # Check if the card is 7 or higher before initializing
        if value in ['7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace1','Ace2']:
            super().__init__(value, suit)
        else:
            raise ValueError("Skat cards must be 7 or higher.")

class SkatDeck(Sequence):
    values = ['7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace1','Ace2']
    suits = ['diamonds', 'hearts', 'spades', 'clubs']

    def __init__(self):
        self.cards = [SkatCard(value, suit) for suit in self.suits for value in self.values]

    def __getitem__(self, position):
        return self.cards[position]

    def __len__(self):
        return len(self.cards)

    def __str__(self):
        return "Skat Deck of Cards"


# Write some code to test the functionality of both kinds of decks. (You can use `assert` to make sure your classes behave the way you expect them to.)

# Test FrenchDeck
french_deck = FrenchDeck()

#first and last card
assert str(french_deck[0]) == "2 of diamonds"
assert str(french_deck[-1]) == "Ace2 of clubs"

#length
assert len(french_deck) == 56

# Repetition test French deck
for card in french_deck:
    assert str(card) in [f"{value} of {suit}" for value in FrenchDeck.values for suit in FrenchDeck.suits]

# Test SkatDeck
skat_deck = SkatDeck()

#first and last Skat card
assert str(skat_deck[0]) == "7 of diamonds"
assert str(skat_deck[-1]) == "Ace2 of clubs"

#length Skat deck
assert len(skat_deck) == 36

# Repetiton test Skat deck
for card in skat_deck:
    assert str(card) in [f"{value} of {suit}" for value in SkatDeck.values for suit in SkatDeck.suits]

print("All tests passed!")


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

def count_valid_numbers(lower_bound, upper_bound):
    count = 0

    for number in range(lower_bound, upper_bound):
        num_str = str(number)
        has_adjacent = False
        is_increasing = True

        for i in range(len(num_str) - 1):
            if num_str[i] == num_str[i + 1]:
                has_adjacent = True
            if num_str[i] > num_str[i + 1]:
                is_increasing = False
                break

        if has_adjacent and is_increasing:
            count += 1

    return count

# Test the function with the provided lower and upper bounds
lower_bound = 134564
upper_bound = 585159
result = count_valid_numbers(lower_bound, upper_bound)
print(f"Count of valid numbers between {lower_bound} and {upper_bound}: {result}")

#Count of valid numbers between 134564 and 585159: 1929
  
