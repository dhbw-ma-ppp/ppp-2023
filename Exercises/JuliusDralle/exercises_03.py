# PART 1:
# Write a class for a French deck of cards (2-Ace of diamonds, hearts, spades, clubs).
# The deck of cards should behave like a sequence.
# When initialized the cards should all be in a well-defined order (2-Ace of each suite, suites in the order above
# I should be able to index into the deck to retrieve one card.
# I should be able to iterate over all cards in the deck.
# Printing a cards string representation should give me a nice, 
# readable description of that card.

cardtype_dict = {
    "01" : "Ace",
    "02" : "2",
    "03" : "3",
    "04" : "4",
    "05" : "5",
    "06" : "6",
    "07" : "7",
    "08" : "8",
    "09" : "9",
    "10" : "10",
    "11" : "Jack",
    "12" : "Queen",
    "12" : "King"
}
suits_dict = {
    "01" : "2-Ace of Diamonds",
    "02" : "Hearts",
    "03" : "Spades",
    "04" : "Clubs"
}

class DeckOfCards:
    list_of_cards = []
    def __init__(self):
        for iterator_through_suits in suits_dict:
            for iterator_through_cardstype in cardtype_dict:
                self.list_of_cards.append(Card(iterator_through_suits, iterator_through_cardstype))

    def __getitem__(self, index):
        return(self.list_of_cards[index])

    def __iter__(self):
        return(i for i in self.list_of_cards)


    def print_cards(self):
        for iterator_through_cards in self.list_of_cards:
            iterator_through_cards.print_value()
        return 0






class Card:  
    def __init__(self, card_suite_id, card_type_id):
        self.card_suite = card_suite_id
        self.card_type = card_type_id

    def print_value(self):
        print(f"This card is a \t{cardtype_dict[self.card_type]} \tin this suite: {suits_dict[self.card_suite]}")

    def get_value(self):
        return(cardtype_dict[self.card_type], suits_dict[self.card_suite])
    

meinKartendeck = DeckOfCards()
print(meinKartendeck[2].get_value())
 


# PART 2:
# Create a second class that represents a deck of cards usable for Skat -- it should only contain cards from 7 upwards.
# It should offer all the same functionality of the first class.


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
#
# run your function with the lower bound `134564` and the upper bound `585159`. Note the resulting count
# in your pull request, please.