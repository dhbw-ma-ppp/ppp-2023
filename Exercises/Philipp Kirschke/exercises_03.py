# PART 1:
# Write a class for a French deck of cards (2-Ace of diamonds, hearts, spades, clubs).
# The deck of cards should behave like a sequence.
# When initialized the cards should all be in a well-defined order (2-Ace of each suite, suites in the order above
# I should be able to index into the deck to retrieve one card.
# I should be able to iterate over all cards in the deck.
# Printing a cards string representation should give me a nice, 
# readable description of that card.


class Card:
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit
        self.name = str(value) + " of " + suit

    def __str__(self):
        return self.name

class Deck:
    def __init__(self):
        self.cards = []
        self.suits = ["diamonds", "hearts", "spades", "clubs"]
        self.values = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack",
        "Queen", "King", "Ace"]
        for suit in self.suits:
            for value in self.values:
                self.cards.append(Card(value, suit))

    def getcard(self, index):
        return self.cards[index]

    def iterate(self):
        return iter(self.cards)



deck = Deck()
cardIndex = input("Enter the index of the card you want to see or press enter to see all cards in the deck: ")
if (cardIndex == ""):
    deck.iterate()
    for card in deck.iterate():
        print(card)
elif (int(cardIndex) > 51):
    print("There are only 52 cards in a deck.")
else:
    print("The card at index " + cardIndex + " is a " + str(deck.getcard(int(cardIndex))))


# PART 2:
# Create a second class that represents a deck of cards usable for Skat -- it should only contain cards from 7 upwards.
# It should offer all the same functionality of the first class.
class skat:
    def __init__(self):
        self.cards = []
        self.suits = ["diamonds", "hearts", "spades", "clubs"]
        self.values = ["7", "8", "9", "10", "Jack",
        "Queen", "King", "Ace"]
        for suit in self.suits:
            for value in self.values:
                self.cards.append(Card(value, suit))

    def getcard(self, index):
        return self.cards[index]

    def iterate(self):
        return iter(self.cards)


# Write some code to test the functionality of both kinds of decks. (You can use `assert` to make sure your classes behave the way you expect them to.)


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

def checkNumber(lowerBound, upperBound):
    numberCount = 0
    for number in range(lowerBound, upperBound):
        if(checkIncrease(number)):
            if(checkDouble(number)):
                numberCount += 1
    print(numberCount)

def checkIncrease(number):
    number = str(number)
    for i in range(len(number)-1):
        if (number[i] > number[i+1]):
            return False
    return True

def checkDouble(number):
    number = str(number)
    for index in range(len(number)-1):
        if (number[index] == number[index+1] and number.count(number[index]) == 2):
            return True
    return False

#
# run your function with the lower bound `134564` and the upper bound `585159`. Note the resulting count
checkNumber(134564, 585159)
# in your pull request, please.
