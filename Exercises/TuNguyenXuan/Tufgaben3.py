# PART 1:
# Write a class for a French deck of cards (2-Ace of diamonds, hearts, spades, clubs).
# The deck of cards should behave like a sequence.
# When initialized the cards should all be in a well-defined order (2-Ace of each suite, suites in the order above
# I should be able to index into the deck to retrieve one card.
# I should be able to iterate over all cards in the deck.
# Printing a cards string representation should give me a nice,
# readable description of that card.

class Card:

    deck = []

    def __init__(self, suit, val):
        self.suit = suit
        self.val = val

    def __str__(self):
        return f"{self.suit} of {self.val}"

class FrenchCardDeck:
    suit = ["Spades", "Clubs", "Diamond", "Hearts"]
    val = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King", "Ace"]

    def __init__(self, value = 0):
        self.cards = []
        for suit in self.suit:
            for val in self.val[value:]:
                self.cards.append(Card(val, suit))

    def __str__(self):
        return f", ".join([str(card) for card in self.cards])

    def __iter__(self):
        return(card for card in (self.cards))

    def __get__(self, i):
        return self.cards[i]


# PART 2:
# Create a second class that represents a deck of cards usable for Skat -- it should only contain cards from 7 upwards.
# It should offer all the same functionality of the first class.
class SkatCardDeck(FrenchCardDeck):
    def __init__(self):
        super().__init__(7)


# Write some code to test the functionality of both kinds of decks. (You can use `assert` to make sure your classes behave the way you expect them to.)

french_card_deck = FrenchCardDeck()

print(french_card_deck)
for card in french_card_deck.cards:
    print(card)

print(french_card_deck.__get__(10))

skat_card_deck = SkatCardDeck()

print(skat_card_deck)
for card in skat_card_deck.cards:
    print(card)

print(skat_card_deck.__get__(10))
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


def number_filter(lowerbound, upperbound):
    count = 0
    numbers = [*range(lowerbound, upperbound)]
    arr = [str(x) for x in numbers]
    for i in range(len(arr)):
        valid_number = None
        for j in range(len(arr[i])):
            if j == len(arr[i])-1:
                break
            else:
                if arr[i][j] < arr[i][j+1]:
                    valid_number = True
                    if arr[i][j] == arr[i][j+1]:
                        if arr[i][j] != arr[i][j+2]:
                            valid_number = True
                else:
                    valid_number = False

        if valid_number:
            print(arr[i])
            count = count + 1

    return count


print(number_filter(134564, 585159))

