# PART 1:
# Write a class for a French deck of cards (2-Ace of diamonds, hearts, spades, clubs).
# The deck of cards should behave like a sequence.
# When initialized the cards should all be in a well-defined order (2-Ace of each suite, suites in the order above
# I should be able to index into the deck to retrieve one card.
# I should be able to iterate over all cards in the deck.
# Printing a cards string representation should give me a nice, 
# readable description of that card.
from timeit import timeit
from collections import UserList


class Card:
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit

    def __str__(self) -> str:
        return f"{self.value} of {self.suit}"
    
class FrenchDeck(UserList):
    _values = [
        '2',
        '3',
        '4',
        '5',
        '6',
        '7',
        '8',
        '9',
        '10',
        'Jack',
        'Queen',
        'King',
        'Ace'
    ]
    _suits = [
        'diamonds',
        'hearts',
        'spades',
        'clubs'
    ]

    def __init__(self):
        self.data = [
            Card(value, suit) 
            for suit in self._suits
            for value in self._values
        ]

# PART 2:
# Create a second class that represents a deck of cards usable for Skat -- it should only contain cards from 7 upwards.
# It should offer all the same functionality of the first class.

class SkatDeck(FrenchDeck):
    _values = [
        '7',
        '8',
        '9',
        '10',
        'Jack',
        'Queen',
        'King',
        'Ace'
    ]

# Write some code to test the functionality of both kinds of decks. (You can use `assert` to make sure your classes behave the way you expect them to.)

print("-----French Deck-----")
frenchDeck = FrenchDeck()
for card in frenchDeck:
    print(f"{card}")
print(f"Card at position [1]: {frenchDeck[1]}")

print("-----Skat Deck-----")
skatDeck = SkatDeck()
for card in skatDeck:
    print(f"{card}")
print(f"Card at position [1]: {skatDeck[1]}")

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

def analyseNumbers(lowerBound, upperBound):
    lowerBoundArray = [int(char) for char in list(str(lowerBound))]
    buffer = lowerBoundArray[0]
    for index in range(1, len(lowerBoundArray)):
        buffer = max(buffer, lowerBoundArray[index])
        lowerBoundArray[index] = buffer
    lowerBound = int("".join(map(str,lowerBoundArray)))

    upperBoundArray = [int(char) for char in list(str(upperBound - 1))]
    buffer = -1
    for index in range(0, len(upperBoundArray) - 1):
        if upperBoundArray[index] > upperBoundArray[index + 1]:
            buffer = index
            break
    if buffer >= 0:
        upperBoundArray[buffer] -= 1
        for index in range(buffer + 1, len(upperBoundArray)):
            upperBoundArray[index] = 9
    upperBound = int("".join(map(str,upperBoundArray)))

    for _ in range(len(upperBoundArray) - len(lowerBoundArray)):
        lowerBoundArray.insert(0, 0)

    numberCounter = 0
    lastDigitIndex = len(upperBoundArray) - 1

    def recursiveStarter(index, currentNumberCounter, isNumberInvalid):
        if lowerBoundArray[index] < upperBoundArray[index]:
            if index < lastDigitIndex:
                firstRecursiveLoop(index + 1, currentNumberCounter - lowerBoundArray[index], isNumberInvalid)

                isNumberInvalid &= bool(currentNumberCounter)

                for i in range(lowerBoundArray[index] + 1, upperBoundArray[index]):
                    lowerBoundArray[index + 1] = i
                    recursiveLoop(index + 1, i, isNumberInvalid)

                lowerBoundArray[index + 1] = upperBoundArray[index]
                lastRecursiveLoop(index + 1, upperBoundArray[index], isNumberInvalid)
            else:
                recursiveEnd(isNumberInvalid, currentNumberCounter, lowerBoundArray[index], upperBoundArray[index])
        else:
            if index < lastDigitIndex:
                recursiveStarter(index + 1, lowerBoundArray[index], isNumberInvalid)
            else:
                nonlocal numberCounter
                numberCounter += 0 if isNumberInvalid else 1

    def lastRecursiveLoop(index, currentNumberCounter, isNumberInvalid):
        if index < lastDigitIndex:
            lowerBoundArray[index + 1] = lowerBoundArray[index]
            recursiveLoop(index + 1, currentNumberCounter - lowerBoundArray[index], isNumberInvalid)

            isNumberInvalid &= bool(currentNumberCounter)

            for i in range(lowerBoundArray[index] + 1, upperBoundArray[index]):
                lowerBoundArray[index + 1] = i
                recursiveLoop(index + 1, i, isNumberInvalid)

            lowerBoundArray[index + 1] = upperBoundArray[index]
            lastRecursiveLoop(index + 1, upperBoundArray[index], isNumberInvalid)
        else:
            recursiveEnd(isNumberInvalid, currentNumberCounter, lowerBoundArray[index], upperBoundArray[index])

    def firstRecursiveLoop(index, currentNumberCounter, isNumberInvalid):
        if index < lastDigitIndex:
            firstRecursiveLoop(index + 1, currentNumberCounter - lowerBoundArray[index], isNumberInvalid)
            
            isNumberInvalid &= bool(currentNumberCounter)

            for i in range(lowerBoundArray[index] + 1, 10):
                lowerBoundArray[index + 1] = i
                recursiveLoop(index + 1, i, isNumberInvalid)
        else:
            recursiveEnd(isNumberInvalid, currentNumberCounter, lowerBoundArray[index])

    def recursiveLoop(index, currentNumberCounter, isNumberInvalid):
        if index < lastDigitIndex:
            lowerBoundArray[index + 1] = lowerBoundArray[index]
            recursiveLoop(index + 1, currentNumberCounter - lowerBoundArray[index], isNumberInvalid)

            isNumberInvalid &= bool(currentNumberCounter)

            for i in range(lowerBoundArray[index] + 1, 10):
                lowerBoundArray[index + 1] = i
                recursiveLoop(index + 1, i, isNumberInvalid)
        else:
            recursiveEnd(isNumberInvalid, currentNumberCounter, lowerBoundArray[index])

    def recursiveEnd(isNumberInvalid, currentNumberCounter, lowerBoundValue, upperBoundValue = 9):
        nonlocal numberCounter
        numberCounter += 0 if isNumberInvalid & bool(currentNumberCounter - lowerBoundValue) else 1
        numberCounter += 0 if isNumberInvalid & bool(currentNumberCounter) else upperBoundValue - lowerBoundValue

    recursiveStarter(0, -1, True)

    return numberCounter

print(f"Execution time: {timeit(lambda: analyseNumbers(134564, 585159), number=5000) / 5000}s")
print(analyseNumbers(134564, 585159))