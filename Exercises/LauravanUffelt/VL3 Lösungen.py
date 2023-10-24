# PART 1:
# Write a class for a French deck of cards (2-Ace of diamonds, hearts, spades, clubs).
# The deck of cards should behave like a sequence.
# When initialized the cards should all be in a well-defined order (2-Ace of each suite, suites in the order above
# I should be able to index into the deck to retrieve one card.
# I should be able to iterate over all cards in the deck.
# Printing a cards string representation should give me a nice,
# readable description of that card.

class Cards():
    def __init__(self, number, symbol):
        self.symbol = symbol

        if number >= 2 and number <= 10:
            self.number = str(number)

        elif number >= 11 and number <= 14:
            match number:
                case 11: self.number = "Jack"
                case 12: self.number = "Queen"
                case 13: self.number = "King"
                case 14: self.number = "Ace"
        elif number <= 1 or number >= 15:
            raise ValueError(f"{number} is not in the cards")

    def __str__(self):
        return (f"the {self.number} of {self.symbol}")


class FrenchDeck():
    def __init__(self, begin, end):
        self.cards = [Cards(number, symbol) for symbol in ["Diamonds", "Hearts", "Spades", "Clubs"] for number in range(begin, end+1)]

    def __str__(self):
        return ", ".join([str(card)for card in self.cards])

    def __iter__(self):
        return (card for card in (self.cards))

    def __get__(self, index):
        card_range = range(len(self.cards))
        if index in card_range:
            return self.cards[index]
        else:
            raise IndexError("Index is not in Range")

# PART 2:
# Create a second class that represents a deck of cards usable for Skat -- it should only contain cards from 7 upwards.
# It should offer all the same functionality of the first class.


class SkatDeck(FrenchDeck):
    def __init__(self):
        super().__init__(7, 14)


sk = SkatDeck()
fr = FrenchDeck(2, 14)

# Write some code to test the functionality of both kinds of decks. (You can use `assert` to make sure your classes behave the way you expect them to.)

print(f"your 22nd Card is {sk.__get__(21)}")
print(f"your French Deck contains the following cards:\n {fr}")

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


def count(a, b):
    counter = 0
    # controls if number is in bound
    for number in range(a, b):
        # writes each number in a list
        digits = [int(digit) for digit in str(number)]
        # controls if number increases by comparing to the sorted number
        if digits == sorted(digits.copy()):
            a = digits.count(1)
            b = digits.count(2)
            c = digits.count(3)
            d = digits.count(4)
            e = digits.count(5)
            f = digits.count(6)
            g = digits.count(7)
            h = digits.count(8)
            i = digits.count(9)
            if a == 2 or b == 2 or c == 2 or d == 2 or e == 2 or f == 2 or g == 2 or h == 2 or i == 2:
                print(number)
                counter += 1
        else:
            continue
    print(counter)


count(134564,  585159)
