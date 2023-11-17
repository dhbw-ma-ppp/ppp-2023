# I should be able to iterate over all cards in the deck.                                                     # Printing a cards string representation should give me a nice,
# readable description of that card.
from functools import lru_cache                        

class Card(object):                                    
    def __init__(self, value, type): # defining the constructor
        self.value = value
        self.type = type

    def __str__(self): # defining the output if the object should be returned as a string
        return f"This is the \"{self.type}-{self.value}\" Card"

class CardDeck(object):
    cardValues = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack","Queen", "King", "Ace"]
    cardTypes = ["Diamond", "Heart", "Spade", "Club"]
    # storing all possible combinations of a french deck of cards

    def __init__(self): # defining the constructor
        self.cards = [] # and creating cards for the deck of cards
        for type in self.cardTypes:
            for value in self.cardValues:
                self.cards.append(Card(value, type))

    def __iter__(self): # defining the iteration of an object CardDeck
        return (card for card in self.cards)

    def __len__(self): # defining the len() function for an object CardDeck
        return len(self.cards)

    def __getitem__(self, index): # defining the behaviour of indexing an object CardDeck
        return self.cards[index]

    def __setitem__(self, index, item): # defining further behaviour of CardDeck as a sequence
        self.cards[index] = item

    def __delitem__(self, index):
        del self.cards[index]

# PART 2:
# Create a second class that represents a deck of cards usable for Skat
#it should only contain cards from 7 upwards.
# It should offer all the same functionality of the first class.
# Write some code to test the functionality of both kinds of decks. (You can use `assert` to make sure your classes behave the way you expect them to.)

class SkatDeck(CardDeck): # inherits the class CardDeck
    cardValues = CardDeck.cardValues[5:] # only referencing the values from 7 to Ace

normalCards = CardDeck() # initialising two objects check if the functions work
skatCards = SkatDeck()

assert(str(normalCards[5]) == str(skatCards[0])) # checks the functionality of indexing
assert(str(normalCards[len(normalCards)-1]) == str(skatCards[len(skatCards)-1])) # checks the funktionality of len()
assert([el for el in normalCards] != []) # checks if the cards can be iterated
assert(str(normalCards[0]) == "This is the \"Diamond-2\" Card") # checks the description string return
normalCards[0] = Card("5", "Diamond")
assert(str(normalCards[0]) == "This is the \"Diamond-5\" Card") # checks if the card can be changed
del normalCards[0]
assert(str(normalCards[0] == "This is the \"Diamond-3\" Card")) # checks if the first element got deleted
assert(issubclass(SkatDeck, CardDeck)) # checks if SkatDeck inherits the methods and therefore can use them

# PART 3:
# write a function that accepts two numbers, a lower bound and an upper bound.
# the function should then return the count of all numbers that meet certain criteria:
# - they are within the (left-inclusive and right-exclusive) bounds passed to the function
# - there is at least one group of exactly two adjacent digits within the number
#   which are the same (like 33 in 123345)
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

def filter_numbers_2(lower_bound, upper_bound, count = 0):
    for str_number in [str(num) for num in range(lower_bound, upper_bound+1)]:
        # storing every number that is contained two times in str_number:
        if([num for num in range(1, 10) if str_number.count(str(num)) == 2]):
            list_num = list(str_number) # splitting str_number into a list of integers
            # storing every number that is greater than the number right next to it:
            if(not [i for i in range(len(list_num)-1) if (list_num[i] > list_num[i+1])]):
                count +=1
    return count

# better version:
@lru_cache(maxsize=None)
def filter_numbers(lb, ub):
    return len([n for n in map(lambda x: str(x), range(lb, ub+1)) if(sorted(l := [*n]) == l and list(filter(lambda x: n.count(str(x)) == 2, range(1,10))))])

assert(filter_numbers(123346,123346) == 1)
assert(filter_numbers(123341,123341) == 0)
assert(filter_numbers(123334,123334) == 0)
assert(filter_numbers(111334,111334) == 1)
assert(filter_numbers(112233,112233) == 1)
assert(filter_numbers(134564, 585159) == 1306)