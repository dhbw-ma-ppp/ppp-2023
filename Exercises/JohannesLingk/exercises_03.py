from enum import Enum
from collections import UserList


class SUITE(Enum):
    CLUBS = "C"
    SPADES = "S"
    HEARTS = "H"
    DIAMONDS = "D"

                                                     #  Jack  Queen  King  Ace
RANKS = {"2", "3", "4", "5", "6", "7", "8", "9", "10", "J",  "Q",   "K",  "A"}


class Card:
    """
    The Card stores basic information about a card in the deck 
    and implements operations like string conversion and equality check
    """
    def __init__(self, suite: SUITE, rank: RANKS) -> None:
        # if invalid rank is passed, throw exception
        if rank not in RANKS:
            raise Exception("Invalid rank.")

        self.suite = suite
        self.rank = rank

    def __str__(self) -> str:
        return self.get_name()
    
    def __eq__(self, __value: object) -> bool:
        return isinstance(__value, Card) and self.rank == __value.rank and self.suite == __value.suite
    
    def get_name(self) -> str:
        """
        Returns a more readable name like "Ace of Spades"
        """
        s = ""
        s += {"2":"Two", "3":"Three", "4":"Four", 
              "5":"Five", "6":"Six", "7":"Seven", 
              "8":"Eight", "9":"Nine", "10":"Ten", 
              "J":"Jack",  "Q":"Queen",   "K":"King",  "A":"Ace"}[self.rank]
        s += " of "
        s += {SUITE.CLUBS: "Clubs", SUITE.SPADES: "Spades", 
              SUITE.HEARTS: "Hearts", SUITE.DIAMONDS: "Diamonds"}[self.suite]
        return s
    
    def get_short_name(self) -> str:
        """
        Returns a short formatted name like "<A-S>"
        """
        return f'<{self.rank}-{self.suite.value}>'

class CardDeck(UserList):
    """
    CardDeck is superclass of FrenchDeck and SkatDeck.
    It stores the cards of the deck and inherits from UserList
    in order to provide the functionality of an iterable.
    """
    def __init__(self, cards = []) -> None:
        super().__init__(cards)

    def __str__(self) -> str:
        """
        Returns the cards in this deck in table format (string).
        """
        output = "Cards in deck:\n"
        cards_per_line = 4
        temp = 0
        for card in self:
            if temp >= cards_per_line: 
                output += "\n"
                temp = 0
            temp += 1
            output += card.get_short_name().rjust(6) + ", "
        return output

# PART 1:
# Write a class for a French deck of cards (2-Ace of diamonds, hearts, spades, clubs).
# The deck of cards should behave like a sequence.
# When initialized the cards should all be in a well-defined order (2-Ace of each suite, suites in the order above
# I should be able to index into the deck to retrieve one card.
# I should be able to iterate over all cards in the deck.
# Printing a cards string representation should give me a nice, 
# readable description of that card.

class FrenchDeck(CardDeck):
    """
    Inherits from CardDeck and adds cards typically present in a french deck on initialization.
    """
    def __init__(self) -> None:
        super().__init__(self._generateDeck())

    def _generateDeck(self) -> list[Card]:
        new_deck = []
        for suite in [SUITE.DIAMONDS, SUITE.HEARTS, SUITE.SPADES, SUITE.CLUBS]:
            for rank in ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]:
                new_deck.append(Card(suite=suite, rank=rank))
        return new_deck


# PART 2:
# Create a second class that represents a deck of cards usable for Skat -- it should only contain cards from 7 upwards.
# It should offer all the same functionality of the first class.


class SkatDeck(CardDeck):
    """
    Inherits from CardDeck and adds cards typically present in a skat deck on initialization.
    """
    def __init__(self) -> None:
        super().__init__(self._generateDeck())

    def _generateDeck(self) -> list[Card]:
        new_deck = []
        for suite in [SUITE.DIAMONDS, SUITE.HEARTS, SUITE.SPADES, SUITE.CLUBS]:
            for rank in ["7", "8", "9", "10", "J", "Q", "K", "A"]:
                new_deck.append(Card(suite=suite, rank=rank))
        return new_deck


# Write some code to test the functionality of both kinds of decks. (You can use `assert` to make sure your classes behave the way you expect them to.)

# initialize decks
french_deck = FrenchDeck()
skat_deck = SkatDeck()

# Print out decks with short card name format
print(F'French Deck:\n {french_deck}\n')
print(F'Skat Deck:\n {skat_deck}')

# get cards at index
assert french_deck[5] == Card(suite=SUITE.DIAMONDS, rank="7")
assert skat_deck[6] == Card(suite=SUITE.DIAMONDS, rank="K")

assert Card(SUITE.DIAMONDS, "7") in skat_deck
assert Card(SUITE.DIAMONDS, "5") not in skat_deck

# iterate and count cards
counter = 0
for c in french_deck:
    counter += 1
assert counter == 52

counter = 0
for c in skat_deck:
    counter += 1
assert counter == 32

# printing cards in readable format
print(f'This is my favorite card: {Card(suite=SUITE.HEARTS, rank="A")}')



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

def _validate_number(number: int) -> bool:
    """
    Checks if a number is valid in terms of the assignment.
    """
    last_char = "-1" 
    eq_chars = 1        # number of equal characters counted in a row
    has_group = False   # stores if a group of two equal numbers has already been found
    # casts number into a string and iterates over every character
    for char in str(number):
        # checks if number only has increasing digits from left to right
        if int(char) < int(last_char):
            return False # the numbers are decreasing so return false
        
        # if current character is equal to last, increase counter
        if last_char == char: eq_chars += 1
        # if current character is not equal, check if there was a group of exactly 2 equal characters
        # before this. If so, set has_group to True. If not, reset counter
        else:
            if eq_chars == 2: has_group = True
            eq_chars = 1

        last_char = char

    # when at end of number, check if last two digits where
    if eq_chars == 2:
        has_group = True
    return has_group
        

def part_3_solution(lowerBound: int, upperBound: int) -> int:
    """
    Given a range of numbers, this function returns the count of numbers within the range, 
    that are valid, in terms of the assignment.
    """
    count = 0
    # for every number within bounds
    for number in range(lowerBound, upperBound):
        if _validate_number(number): count += 1
    return count

# check if solution works (it does)
assert _validate_number(123345) == True
assert _validate_number(123341) == False
assert _validate_number(123334) == False
assert _validate_number(111334) == True
assert _validate_number(112233) == True

# print solution
print(f"Solution to part 3: {part_3_solution(134564, 585159)}")



# ------------------------- INFO -------------------------------
# The following solutions are NOT written with 
# focus on readability and therefore not to be taken too seriously
# although they are working ;)

def part_3_compact(lowerBound: int, upperBound: int) -> int:
    count = 0
    for number in range(lowerBound, upperBound):
        numl = [int(n) for n in str(number)]
        if not all(numl[i] <= numl[i+1] for i in range(len(numl)-1)): continue
        if not 2 in {n:numl.count(n) for n in set(numl)}.values(): continue
        count += 1
    return count

def part_3_oneline(low: int, high: int):
    return len([lnum for lnum in [list(str(num)) for num in range(low, high)] if sorted(lnum) == lnum and (2 in {n:lnum.count(n) for n in set(lnum)}.values())])

assert part_3_compact(134564, 585159) == 1306
assert part_3_oneline(134564, 585159) == 1306