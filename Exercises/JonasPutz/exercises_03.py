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
    """ Placeholder for Card elements.
        A Card is defined by its value (self.value) and its suit (self.suit).

        These values must be specified in the constructor.
    """
    def __init__(self, value, suit):
        """ The constructor returnes a new card with the specified values.

            Parameters
            ----------
            value (str)
                the face value of the card (usually 2 - ace)
            suit (str)
                the suit of the card (usually diamonds, hearts, spades, clubs)
        """
        self.value = value
        self.suit = suit

    def __str__(self) -> str:
        """ Returns a string representation of the card in the form:
            
            "{self.value} of {self.suit}"
            
            e.g: 7 of hearts, Ace of spades, ...
        """
        return f"{self.value} of {self.suit}"
    
class FrenchDeck(UserList):
    """ A french deck

        (using the values: 2 - Ace and suits: diamonds, hearts, spades, clubs)
    """
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
    """ A skat deck

        same as a french deck but just using the values: 7 - Ace
    """
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
    """ Analyse numbers:

        returns all numbers from lower bound (inclusiv) to upper bound (exclusiv) 
        which digits are in ascending order and include at least one digit exactly twice
    """

    numbers = []        #stores all valid numbers
    digitCounter = []   #stores the count of 0's, 1's, ..., 9's
    lastDigit = 0       #stores the last used digit
    isValid = True      #stores if the number is valid

    for number in range(lowerBound, upperBound):
        lastDigit = 0           #resets all used values
        isValid = True
        digitCounter = [0] * 10

        for digit in map(int,str(number)):  #execute for each digit in the number (from left to right)
            if digit < lastDigit:    
                isValid = False             #if the digit is smaller than the last one, set the number to invalid
                break                       #this means, the digits are not ascending order
            lastDigit = digit

            digitCounter[digit] += 1        #increase the digit counter

        isValid &= any(d == 2 for d in digitCounter)    #if the number is valid, test if any digit is included exactly twice

        if isValid:
            numbers.append(number)          #add the number to the list, if it is valid

    return len(numbers)         #returns the number of numbers found

print(f"\n\nThe function found {analyseNumbers(134564, 585159)} valid numbers")


##########################################################################
# The function below is much faster but very complicated. 
# It is not well documented and should be seen as an inspiration of what could have been done.
def analyseNumbersFast(lowerBound, upperBound):
    #calculate the 'real' lower bound (134564 is not a valid number, it will be set to 134566, the first ordered one)
    lowerBoundArray = [int(char) for char in list(str(lowerBound))] #the array containing all digits (e.g:[1,3,4,5,6,6])
    buffer = lowerBoundArray[0]
    for index in range(1, len(lowerBoundArray)):
        buffer = max(buffer, lowerBoundArray[index])
        lowerBoundArray[index] = buffer
    lowerBound = int("".join(map(str,lowerBoundArray)))

    #calculate the 'real' upper bound (585159 will be set to 579999)
    upperBoundArray = [int(char) for char in list(str(upperBound - 1))] #same as before (e.g:[5,7,9,9,9,9])
    buffer = -1
    for index in range(0, len(upperBoundArray) - 1): #finds the index, where the order first breaks (e.g:1 - between 8 and 5)
        if upperBoundArray[index] > upperBoundArray[index + 1]:
            buffer = index
            break
    if buffer >= 0:
        upperBoundArray[buffer] -= 1 #counts the buffer value one down (e.g: 8 -> 7)
        for index in range(buffer + 1, len(upperBoundArray)): #sets all other value to 9
            upperBoundArray[index] = 9
    upperBound = int("".join(map(str,upperBoundArray)))

    for _ in range(len(upperBoundArray) - len(lowerBoundArray)): #fills the lowerBound with leading 0's, if necessary
        lowerBoundArray.insert(0, 0)

    numberCounter = 0 #this value will be used to find the necessary double
    lastDigitIndex = len(upperBoundArray) - 1 #last value being processed by the recursive functions

    #generall Idea:
    #use for a number with n digits n nested for loops with each one starting from the current digit from the last one
    #this will only generate ordered numbers

    #used arguments in the recursive tree:
    #index (int): the current index of the digit being handeled e.g: at the beginning 0 and in the end lastDigitIndex
    #currentNumberCounter (int): this value will follow the following pattern:
    #   >0: first occurence of the given digit              bool(7) = True
    #   =0: second occurence of the given digit             bool(0) = False
    #   <0: third and more occurences of the given digit    bool(-7) = True
    #isNumberInvalid (bool): will contain only false (number is valid) if the double constraint is already matched by digits before
    #   otherwise this will always be true (not yet valid)

    #the start method for the recursiv tree
    #will be executed below with recursiveStarter(0, -1, true)
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
            if upperBoundArray[index] == lowerBoundArray[index]:
                lastRecursiveLoop(index + 1, currentNumberCounter - upperBoundArray[index], isNumberInvalid)
            else:
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
            if lowerBoundArray[index] == lowerBoundArray[index - 1]:
                firstRecursiveLoop(index + 1, currentNumberCounter - lowerBoundArray[index], isNumberInvalid)
            else:
                firstRecursiveLoop(index + 1, lowerBoundArray[index], isNumberInvalid)
            
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

print(f"--------Extra data below--------")
print(f"Function time comparison: (134564 to 585159)")
t1 = timeit(lambda: print(f"Result: {analyseNumbers(134564, 585159)}"), number=1)
print(f"analyseNumbers: {t1}s")
t2 = timeit(lambda: analyseNumbersFast(134564, 585159), number=500) / 500
print(f"Result: {analyseNumbersFast(134564, 585159)}")
print(f"analyseNumbers: {t2}s")
print(f"The fast algorithem is {(t1 / t2 - 1) * 100:.10}% faster")

print(f"\nFunction time comparison: (1345640 to 5851590)")
t3 = timeit(lambda: print(f"Result: {analyseNumbers(1345640, 5851590)}"), number=1)
print(f"analyseNumbers: {t3}s")
t4 = timeit(lambda: analyseNumbersFast(1345640, 5851590), number=100) / 100
print(f"Result: {analyseNumbersFast(1345640, 5851590)}")
print(f"analyseNumbersFast: {t4}s")
print(f"The fast algorithem is {(t3 / t4 - 1) * 100:.10}% faster")

print(f"\nFunction time comparison: (1345640000000000000 to 5851590000000000000)")
print(f"analyseNumbers: to slow to be run on numbers as large")
t5 = timeit(lambda: print(f"Result: {analyseNumbersFast(1345640000000000000, 5851590000000000000)}"), number=1)
print(f"analyseNumbersFast: {t5}s")
print(f"The fast algorithem is {(t1 / t5 - 1) * 100:.10}% faster than analyseNumbers(134564, 585159)")