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

class DeckOfCards:
    def __init__(self, number):
        self.cards = [] # Initializing empty list
        # Choses specific rank determined by "number"
        ranks = ["7", "8", "9", "10", "J", "Q", "K", "A"] if number == 7 else ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"] 
        for suit in ["♦", "♥", "♠", "♣"]: # Creating all possible cards and using .append to add to list
            for rank in ranks:
                self.cards.append(rank + suit)

    def __getitem__(self, retr): 
        return self.cards[retr]    # Be able to retrieve a card
    
    def __iter__ (self):
        return iter(self.cards)     # Be able to iterate over all cards
    
    def __str__ (self):
        return "\n".join(self.cards) # new line for readable description
        

class FrenchDeckOfCards(DeckOfCards):
    def __init__(self):
        super().__init__(2)
        
class SkatDeck(DeckOfCards):
    def __init__(self):
        super().__init__(7)
        

# Write some code to test the functionality of both kinds of decks. (You can use `assert` to make sure your classes behave the way you expect them to.)

french_deck = FrenchDeckOfCards()
assert french_deck.cards == ['2♦', '3♦', '4♦', '5♦', '6♦', '7♦', '8♦', '9♦', '10♦', 'J♦', 'Q♦', 'K♦', 'A♦', '2♥', '3♥', '4♥', '5♥', '6♥', '7♥', '8♥', '9♥', '10♥', 'J♥', 'Q♥', 'K♥', 'A♥', '2♠', '3♠', '4♠', '5♠', '6♠', '7♠', '8♠', '9♠', '10♠', 'J♠', 'Q♠', 'K♠', 'A♠', '2♣', '3♣', '4♣', '5♣', '6♣', '7♣', '8♣', '9♣', '10♣', 'J♣', 'Q♣', 'K♣', 'A♣']

skat_deck = SkatDeck()
assert skat_deck.cards == ['7♦', '8♦', '9♦', '10♦', 'J♦', 'Q♦', 'K♦', 'A♦', '7♥', '8♥', '9♥', '10♥', 'J♥', 'Q♥', 'K♥', 'A♥', '7♠', '8♠', '9♠', '10♠', 'J♠', 'Q♠', 'K♠', 'A♠', '7♣', '8♣', '9♣', '10♣', 'J♣', 'Q♣', 'K♣', 'A♣']

print("Testing getitem method works:\n")
print(skat_deck.cards[5])
print(french_deck.cards[1])


print("\nTesting If iter method works:\n")
test_iterate = iter(french_deck)
for cards in test_iterate:
    print(cards)


# PART 3:
# write a function that accepts two numbers, a lower bound and an upper bound.
# the function should then return the count of all numbers that meet certain criteria:
# - they are within the (left-inclusive and right-exclusive) bounds passed to the function
# - there is at least one group of exactly two adjacent digits within the number which are the same (like 33 in 123345)
# - digits only increase going from left to right

# Function that checks if there are adjacent numbers in the var
def adjacent_digits_check(number):
    digits = str(number) # Converting number to string
    two_adjacent = 0 # Initializing a counter for the number of adjacent digits
    for i in range(len(digits)-1): # Iterating over each digit in string -1 since the last digit already gets checked with "digits [i+1]"
        if digits [i] == digits [i+1]: # If two adjacent digits are the same, increase "two_adjacent" counter
            two_adjacent += 1
        else:
            if two_adjacent == 1: # if there is exactly two adjacent digits, it returns true
                return True
            two_adjacent = 0 # reset counter to 0
    return two_adjacent == 1 # at the end of the loop checks if counter is 1, if so it returns true. Otherwise returns false.

 
# Function that checks if given number is ascending        
def left_right_ascending(number):
    digits = str(number)
    for i in range(len(digits)-1):  # Iterates over a range of values, starting from 0 to end -1 since "digits [i+1]" already checks last value
        if digits [i] > digits [i+1]: # Checking if front digit is bigger than the next one
            return False # Returns False if front digit is bigger
    return True # If its in an ascending order, it returns true


def number_filter(lowerbound, upperbound):
    count = 0 # creating a counting var
    for number in range(lowerbound, upperbound): # goes through the given range
        if adjacent_digits_check(number) and left_right_ascending(number): # checking if both functions return true
            count += 1 # adds +1 to the count if both functions are true

    return count


# Examples:
# - 123345 is a valid number
# - 123341 is not a valid number, as the digits do not increase from left to right
# - 123334 is not a valid number as there is no group of exactly two repeated digits
# - 111334 is a valid number. while there are three 1s, there is also a group of exactly two 3s.
# - 112233 is a valid number. At least one group of two is fulfilled, there is no maximum to the number of such groups.
#
# run your function with the lower bound `134564` and the upper bound `585159`. Note the resulting count
# in your pull request, please.

print(number_filter(134564, 585159))

