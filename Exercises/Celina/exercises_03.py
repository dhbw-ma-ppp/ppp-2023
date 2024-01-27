# PART 1:
# Write a class for a French deck of cards (2-Ace of diamonds, hearts, spades, clubs).
# The deck of cards should behave like a sequence.
# When initialized the cards should all be in a well-defined order (2-Ace of each suite, suites in the order above
# I should be able to index into the deck to retrieve one card.
# I should be able to iterate over all cards in the deck.
# Printing a cards string representation should give me a nice, 
# readable description of that card.

class Card(object):
    def __init__(self,shape,number):
        self.shape= shape
        self.number= number
    
    def __str__(self):
        return f"{self.number} {self.shape}"


class Card_deck(object):
    def __init__(self):
        self.cards= []
    
    def add(self,card):
        self.cards.append(card)
    
    def show_cards(self):
        for elements in self.cards:
            print(elements)


class French_deck(Card_deck):
    def __init__(self):
        self.deck = Card_deck()

    def make_french_deck(self):
        #deck = Card_deck()
        shape=["diamonds","hearts","spades","clubs"]
        number=[2,3,4,5,6,7,8,9,10,"J","Q","K","A"]
        for type in shape:
            for elements in number:
                self.deck.add(Card(number=elements,shape=type))

    def show_cards(self):
        self.deck.show_cards()
    

# PART 2:
# Create a second class that represents a deck of cards usable for Skat -- it should only contain cards from 7 upwards.
# It should offer all the same functionality of the first class.

class Skat_deck(Card_deck):
    def __init__(self):
        self.deck = Card_deck()

    def make_skat_deck(self):
        #deck = Card_deck()
        shape=["diamonds","hearts","spades","clubs"]
        number=[7,8,9,10,"J","Q","K","A"]
        for type in shape:
            for elements in number:
                self.deck.add(Card(number=elements,shape=type))

    def show_cards(self):
        self.deck.show_cards()


# Write some code to test the functionality of both kinds of decks. (You can use `assert` to make sure your classes behave the way you expect them to.)

game=French_deck()
game.make_french_deck()
game.show_cards()

game_2 =Skat_deck()
game_2.make_skat_deck()
game_2.show_cards()

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

def number_sorted(number):
    if "".join(sorted(number)) == number:
        return True
    return False

def number_sets(number):
    for elements in set(number):
        if number.count(elements) == 2:
            return True
    return False

def number_counter(first_num,second_num):
    counter=0
    for numbers in range(first_num,second_num):
        if number_sorted(str(numbers)) == True:
            if number_sets(str(numbers)) == True:
                counter+=1
    return counter

print(number_counter(134564,585159))