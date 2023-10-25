# PART 1:
# Write a class for a French deck of cards (2-Ace of diamonds, hearts, spades, clubs).
# The deck of cards should behave like a sequence.
# When initialized the cards should all be in a well-defined order (2-Ace of each suite, suites in the order above
# I should be able to index into the deck to retrieve one card.
# I should be able to iterate over all cards in the deck.
# Printing a cards string representation should give me a nice, 
# readable description of that card.

suits = ["diamonds", "hearts", "spades", "clubs"]

class card:
    """The class card needs a value und a suit to be constructed"""
    
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit
    
    def __str__(self):
        return (f"{self.value} of {self.suit}, ")


class french_card_deck:
    """initializes a list of card-objects as a whole french card deck (2 to ace),
    which can be used to get one item out of it or to iterate. This classes
    contructor doens't need any arguments."""
    
    def __init__(self): #contructor
        values = ["2","3","4","5","6","7","8","9","10","jack","queen","king","ace"]
        self.deck = []
        for suit in suits:  #create a list of cards as the deck. Each card is a string
            for value in values:
                self.deck.append(card(value, suit))
    
    def __getitem__(self, index):
        if index >= 0 and index < len(self.deck):   #to prevent an index-out-of-bound Error
            return self.deck[index] #using __str__ of the object?
        else:
            raise IndexError("Index out of bound")
        
    def __iter__(self): #returning every card in the deck
        return (element for element in self.deck)
    
    def __str__(self):
        storage = ""
        for counter in range(len(self.deck)):
            storage += str(self.deck[counter])
        return storage

# PART 2:
# Create a second class that represents a deck of cards usable for Skat -- it should only contain cards from 7 upwards.
# It should offer all the same functionality of the first class.

class skat_deck:
    """initializes a list of card-objects as a whole skat card deck (7 to ace),
    which can be used to get one item out of it or to iterate. This classes
    contructor doens't need any arguments."""
    
    def __init__(self): #contructor
        values = ["7","8","9","10","jack","queen","king","ace"]
        self.deck = []
        for suit in suits:  #create a list of cards as the deck. Each card is a string
            for value in values:
                self.deck.append(card(value, suit))
    
    def __getitem__(self, index):
        if index >= 0 and index < len(self.deck):   #to prevent an index-out-of-bound Error
            return self.deck[index] #using the __str__ of the class card?
        else:
            raise IndexError("Index out of bound")
        
    def __iter__(self): #returning every card in the deck
        return (element for element in self.deck)
    
    def __str__(self):
        storage = ""
        for counter in range(len(self.deck)):
            storage += str(self.deck[counter])
        return storage

# Write some code to test the functionality of both kinds of decks. (You can use `assert` to make sure your classes behave the way you expect them to.)

deck1 = french_card_deck()
deck2 = skat_deck()

assert str(deck1) == "2 of diamonds, 3 of diamonds, 4 of diamonds, 5 of diamonds, 6 of diamonds, 7 of diamonds, 8 of diamonds, 9 of diamonds, 10 of diamonds, jack of diamonds, queen of diamonds, king of diamonds, ace of diamonds, 2 of hearts, 3 of hearts, 4 of hearts, 5 of hearts, 6 of hearts, 7 of hearts, 8 of hearts, 9 of hearts, 10 of hearts, jack of hearts, queen of hearts, king of hearts, ace of hearts, 2 of spades, 3 of spades, 4 of spades, 5 of spades, 6 of spades, 7 of spades, 8 of spades, 9 of spades, 10 of spades, jack of spades, queen of spades, king of spades, ace of spades, 2 of clubs, 3 of clubs, 4 of clubs, 5 of clubs, 6 of clubs, 7 of clubs, 8 of clubs, 9 of clubs, 10 of clubs, jack of clubs, queen of clubs, king of clubs, ace of clubs, "
print("french card deck:\n", str(deck1))

assert str(deck2) == "7 of diamonds, 8 of diamonds, 9 of diamonds, 10 of diamonds, jack of diamonds, queen of diamonds, king of diamonds, ace of diamonds, 7 of hearts, 8 of hearts, 9 of hearts, 10 of hearts, jack of hearts, queen of hearts, king of hearts, ace of hearts, 7 of spades, 8 of spades, 9 of spades, 10 of spades, jack of spades, queen of spades, king of spades, ace of spades, 7 of clubs, 8 of clubs, 9 of clubs, 10 of clubs, jack of clubs, queen of clubs, king of clubs, ace of clubs, "
print("skat deck:\n", str(deck2))

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

def num_counter(min, max):
    """returns the number of integers, that are between the
    min and max bounds and meet the given criteria"""
    counter = 0
    for i in range(min, max):   # includes min, excludes max
        temp = str(i)
        num = []
        for j in range(10): # creating a list that saves every number's count
            j_as_str = str(j)
            num.append(temp.count(j_as_str))
        if num.count(2) != 0:
            counter += 1
    return counter


print(str(num_counter(min = 134564, max = 585159))) # finds 331261 numbers