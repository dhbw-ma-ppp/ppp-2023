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
class DeckOfCards:
    def __init__(self,deck):
        self.deck = deck
    def __iter__(self):
        return (i for i in self.deck)
    def __str__(self):
        return str(", ".join(self.deck))
    def __getitem__(self,index):
        if 0 <= index < len(self.deck):
            return self.deck[index]
        else:
            raise IndexError("Index out of range")

class FrenchDeck(DeckOfCards):
    def __init__(self):
        deck = []
        for suits in ["diamonds", "hearts", "spades", "clubs"]:
            for type in ["2","3","4","5","6","7","8","9","10","Jack","Queen","King"]:
                deck.append(type+" of "+suits)
        super().__init__(deck)
                
class SkatDeck(DeckOfCards):
    def __init__(self):
        deck = []
        for suits in ["diamonds", "hearts", "spades", "clubs"]:
            for type in ["7","8","9","10","Jack","Queen","King"]:
                deck.append(type+" of "+suits)
        super().__init__(deck)

french_deck=FrenchDeck()
assert str(french_deck) == "2 of diamonds, 3 of diamonds, 4 of diamonds, 5 of diamonds, 6 of diamonds, 7 of diamonds, 8 of diamonds, 9 of diamonds, 10 of diamonds, Jack of diamonds, Queen of diamonds, King of diamonds, 2 of hearts, 3 of hearts, 4 of hearts, 5 of hearts, 6 of hearts, 7 of hearts, 8 of hearts, 9 of hearts, 10 of hearts, Jack of hearts, Queen of hearts, King of hearts, 2 of spades, 3 of spades, 4 of spades, 5 of spades, 6 of spades, 7 of spades, 8 of spades, 9 of spades, 10 of spades, Jack of spades, Queen of spades, King of spades, 2 of clubs, 3 of clubs, 4 of clubs, 5 of clubs, 6 of clubs, 7 of clubs, 8 of clubs, 9 of clubs, 10 of clubs, Jack of clubs, Queen of clubs, King of clubs"
assert [i for i in french_deck] == ['2 of diamonds', '3 of diamonds', '4 of diamonds', '5 of diamonds', '6 of diamonds', '7 of diamonds', '8 of diamonds', '9 of diamonds', '10 of diamonds', 'Jack of diamonds', 'Queen of diamonds', 'King of diamonds', '2 of hearts', '3 of hearts', '4 of hearts', '5 of hearts', '6 of hearts', '7 of hearts', '8 of hearts', '9 of hearts', '10 of hearts', 'Jack of hearts', 'Queen of hearts', 'King of hearts', '2 of spades', '3 of spades', '4 of spades', '5 of spades', '6 of spades', '7 of spades', '8 of spades', '9 of spades', '10 of spades', 'Jack of spades', 'Queen of spades', 'King of spades', '2 of clubs', '3 of clubs', '4 of clubs', '5 of clubs', '6 of clubs', '7 of clubs', '8 of clubs', '9 of clubs', '10 of clubs', 'Jack of clubs', 'Queen of clubs', 'King of clubs']
assert french_deck[37] == "3 of clubs"


skat_deck=SkatDeck()
assert str(skat_deck) =="7 of diamonds, 8 of diamonds, 9 of diamonds, 10 of diamonds, Jack of diamonds, Queen of diamonds, King of diamonds, 7 of hearts, 8 of hearts, 9 of hearts, 10 of hearts, Jack of hearts, Queen of hearts, King of hearts, 7 of spades, 8 of spades, 9 of spades, 10 of spades, Jack of spades, Queen of spades, King of spades, 7 of clubs, 8 of clubs, 9 of clubs, 10 of clubs, Jack of clubs, Queen of clubs, King of clubs"
assert [i for i in skat_deck] == ['7 of diamonds', '8 of diamonds', '9 of diamonds', '10 of diamonds', 'Jack of diamonds', 'Queen of diamonds', 'King of diamonds', '7 of hearts', '8 of hearts', '9 of hearts', '10 of hearts', 'Jack of hearts', 'Queen of hearts', 'King of hearts', '7 of spades', '8 of spades', '9 of spades', '10 of spades', 'Jack of spades', 'Queen of spades', 'King of spades', '7 of clubs', '8 of clubs', '9 of clubs', '10 of clubs', 'Jack of clubs', 'Queen of clubs', 'King of clubs']
assert skat_deck[4] == "Jack of diamonds"


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

def increase(num):
    for index in range(len(num)-1):
        if num[index]>num[index+1]:
            return False   
    return True

def grouping(num): 
    for index in range(len(num)-1):
        if num[index]==num[index+1] and num.count(num[index])==2: 
            return True
    return False
        
def validator(low,high):
    valid_count = 0
    for number in range(low,high):
        if increase(str(number)) == True and grouping(str(number)) == True:
            valid_count+=1
    return valid_count

print(validator(134564,585159))
#result  1306    


