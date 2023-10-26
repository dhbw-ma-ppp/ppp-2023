# PART 1:
# Write a class for a French deck of cards (2-Ace of diamonds, hearts, spades, clubs).
# The deck of cards should behave like a sequence.
# When initialized the cards should all be in a well-defined order (2-Ace of each suite, suites in the order above
# I should be able to index into the deck to retrieve one card.
# I should be able to iterate over all cards in the deck.
# Printing a cards string representation should give me a nice, 
# readable description of that card.
import select

#print("\nTask 1\n")

class Card:
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit

    def __repr__(self):
        return f"{self.value} of {self.suit}"


class FrenchDeck:
    def __init__(self):
        self.cards = []
        self.suits = ["diamonds", "hearts", "spades", "clubs"]
        self.values = ["2", "3", "4", "5", "6", "7", "8", "9", "10",
                       "Jack", "Queen", "King", "Ace"]
        for suits in self.suits:
            for values in self.values:
                self.cards.append(Card(values, suits))

    def __getitem__(self, position):
        return self.cards[position]



class ScatDeck(FrenchDeck):
    def __init__(self):
        super().__init__()
        self.cards = [card for card in self.cards if card.value in [
            "7", "8", "9", "10", "Jack", "Queen", "King", "Ace"]]


frenchdeck = FrenchDeck()
scatdeck = ScatDeck()


# Write some code to test the functionality of both kinds of decks. (You can use `assert` to make sure your classes behave the way you expect them to.)

def test_frenchdeck():
    assert len(frenchdeck.cards) == 52
    assert frenchdeck.cards[0] == Card("2", "diamonds")
    assert frenchdeck.cards[51] == Card("Ace", "clubs")
    assert frenchdeck.cards[12] == Card("Ace", "diamonds")
    assert frenchdeck.cards[13] == Card("2", "hearts")
    assert frenchdeck.cards[25] == Card("Jack", "spades")
    assert frenchdeck.cards[38] == Card("Queen", "clubs")
    assert frenchdeck.cards[51] == Card("Ace", "clubs")


def test_scatdeck():
    assert len(scatdeck.cards) == 32
    assert scatdeck.cards[0] == Card("7", "diamonds")
    assert scatdeck.cards[31] == Card("Ace", "clubs")
    assert scatdeck.cards[12] == Card("Ace", "diamonds")
    assert scatdeck.cards[13] == Card("7", "hearts")
    assert scatdeck.cards[25] == Card("Jack", "spades")




#print(frenchdeck.cards)
#print(scatdeck.cards)





# PART 2:
# Create a second class that represents a deck of cards usable for Skat -- it should only contain cards from 7 upwards.
# It should offer all the same functionality of the first class.


# Write some code to test the functionality of both kinds of decks. (You can use `assert` to make sure your classes behave the way you expect them to.)





#print("\nTask 2\n")









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

#print("\nTask 3\n")

def count_valid_numbers(lower_bound, upper_bound):
    count = 0
    for num in range(lower_bound, upper_bound):
        num_str = str(num)
        has_adjacent = False
        increasing = True

        for i in range(len(num_str) - 1):
            if num_str[i] > num_str[i + 1]:
                increasing = False
                break
            if num_str[i] == num_str[i + 1] and (i == 0 or num_str[i - 1] != num_str[i]) and (i + 2 == len(num_str) or num_str[i + 2] != num_str[i]):
                has_adjacent = True

        if increasing and has_adjacent:
            count += 1

    return count

print(count_valid_numbers(134564, 585159))

