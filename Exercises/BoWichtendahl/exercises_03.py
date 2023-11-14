# PART 1:
# Write a class for a French deck of cards (2-Ace of diamonds, hearts, spades, clubs).
# The deck of cards should behave like a sequence.
# When initialized the cards should all be in a well-defined order (2-Ace of each suite, suites in the order above)
# I should be able to index into the deck to retrieve one card.
# I should be able to iterate over all cards in the deck.
# Printing a cards string representation should give me a nice, 
# readable description of that card.

class CardDeck:
    """
    This class represents a deck of cards.

    It can be initialized with a minimum card value. The default is 2.
    This class should not be used directly. This class is used as a base class which provides the basic functionality
    for other card decks.
    """
    def __init__(self, min_card='2'):
        card_colors = ['diamonds', 'hearts', 'spades', 'clubs']
        card_values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'jack', 'queen', 'king', 'ace']
        self.__cards = []
        for color in card_colors:
            for i in range(card_values.index(min_card), len(card_values)):
                self.__cards.append((' of '.join([card_values[i], color])))

    def __len__(self):
        return len(self.__cards)

    def __iter__(self):
        self.__index = 0
        return self

    def __next__(self):
        self.__index += 1
        try:
            return self.__cards[self.__index - 1]
        except IndexError:
            raise StopIteration

    def __getitem__(self, index):
        try:
            return self.__cards[index]
        except IndexError:
            print('Index out of bounds')

    def __str__(self):
        return str(self.__cards)


class FrenchDeck(CardDeck):
    """
    This class represents a French deck of cards. It inherits its functionality from the CardDeck class and has all the
    cards from the 2 to the ace.
    """
    def __init__(self):
        super().__init__()


# PART 2:
# Create a second class that represents a deck of cards usable for Skat -- it should only contain cards from 7 upwards.
# It should offer all the same functionality of the first class.


class SkatDeck(CardDeck):
    """
    This class represents a Skat deck of cards. It inherits its functionality from the CardDeck class and has all the
    cards from the 7 to the ace.
    """
    def __init__(self):
        super().__init__(min_card='7')


# Write some code to test the functionality of both kinds of decks. (You can use `assert` to make sure your classes
# behave the way you expect them to.)

french_deck_1 = FrenchDeck()

assert str(french_deck_1) == ("['2 of diamonds', '3 of diamonds', '4 of diamonds', '5 of diamonds', '6 of diamonds', "
                              "'7 of diamonds', '8 of diamonds', '9 of diamonds', '10 of diamonds', "
                              "'jack of diamonds', 'queen of diamonds', 'king of diamonds', 'ace of diamonds', "
                              "'2 of hearts', '3 of hearts', '4 of hearts', '5 of hearts', '6 of hearts', "
                              "'7 of hearts', '8 of hearts', '9 of hearts', '10 of hearts', 'jack of hearts', "
                              "'queen of hearts', 'king of hearts', 'ace of hearts', '2 of spades', '3 of spades', "
                              "'4 of spades', '5 of spades', '6 of spades', '7 of spades', '8 of spades', "
                              "'9 of spades', '10 of spades', 'jack of spades', 'queen of spades', 'king of spades', "
                              "'ace of spades', '2 of clubs', '3 of clubs', '4 of clubs', '5 of clubs', '6 of clubs', "
                              "'7 of clubs', '8 of clubs', '9 of clubs', '10 of clubs', 'jack of clubs', "
                              "'queen of clubs', 'king of clubs', 'ace of clubs']")
assert french_deck_1[0] == '2 of diamonds'
assert french_deck_1[12] == 'ace of diamonds'
assert french_deck_1[13] == '2 of hearts'
assert french_deck_1[51] == 'ace of clubs'

skat_deck_1 = SkatDeck()

assert str(skat_deck_1) == ("['7 of diamonds', '8 of diamonds', '9 of diamonds', '10 of diamonds', "
                            "'jack of diamonds', 'queen of diamonds', 'king of diamonds', 'ace of diamonds', "
                            "'7 of hearts', '8 of hearts', '9 of hearts', '10 of hearts', 'jack of hearts', "
                            "'queen of hearts', 'king of hearts', 'ace of hearts', '7 of spades', '8 of spades', "
                            "'9 of spades', '10 of spades', 'jack of spades', 'queen of spades', 'king of spades', "
                            "'ace of spades', '7 of clubs', '8 of clubs', '9 of clubs', '10 of clubs', "
                            "'jack of clubs', 'queen of clubs', 'king of clubs', 'ace of clubs']")
assert skat_deck_1[0] == '7 of diamonds'
assert skat_deck_1[31] == 'ace of clubs'
assert skat_deck_1[14] == 'king of hearts'
assert skat_deck_1[20] == 'jack of spades'


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


def in_order(number):
    """
    Evaluates if the digits of the given number are in increasing order.
    :param number:
    :return:
    """
    number_string = str(number)
    for index in range(len(number_string) - 1):
        if number_string[index] > number_string[index + 1]:
            return False
    return True


def pair_checker(number):
    """
    Evaluates if there is a digit that is exactly 2 times in the given number.
    :param number:
    :return:
    """
    number_string = str(number)
    for digit in set(number_string):
        if number_string.count(digit) == 2:
            return True
    return False


def num_checker(lower_bound, upper_bound):
    """
    This function checks how many numbers in a given range meet both of the following criteria.

    1: The digits of the number are in increasing order

    2: There is at least one digit that occurs exactly 2 times in the number
    :param lower_bound:
    :param upper_bound:
    :return:
    """
    valid_count = 0
    for number in range(lower_bound, upper_bound):
        if pair_checker(number) and in_order(number):
            valid_count += 1
    return valid_count


print(f'The resulting count in task 3 is {num_checker(134564, 585159)}')
