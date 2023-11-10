# PART 1:
# Write a class for a French deck of cards (2-Ace of diamonds, hearts, spades, clubs).
# The deck of cards should behave like a sequence.
# When initialized the cards should all be in a well-defined order (2-Ace of each suite, suites in the order above
# I should be able to index into the deck to retrieve one card.
# I should be able to iterate over all cards in the deck.
# Printing a cards string representation should give me a nice, 
# readable description of that card.

import unittest
import math



class Card:
    """Card - Represent a Card by it's suite and value

    Attributes:
    --------------
    self.suits(str):                    the Card's suite
    self.type(str):                     Card type
    """
    def __init__(self, suit:str, card_type:str):
        self.suit = suit#define Card suits (hearts, spades etc.)
        self.card_type = card_type#define Card value (2,7,king, ace)

    def __repr__(self) -> str:
        return f"Card({self.suit}, {self.card_type})"
    
    def __str__(self) -> str:#string representation
        return f"{self.card_type} of {self.suit}"




class CardDeck:
    """CardDeck - A deck of Cards represented by a list of Card objects
    
    Attributes:
    --------------
    self.cards(list):                   list of Card objects
    """
    def __init__(self, cards:list):
        self.cards = cards

    def __iter__(self):
        return (elements for elements in self.cards)

    def __str__(self) -> str:#string representation
        return ", ".join([str(card) for card in self.cards])


    def __repr__(self) -> str:
        return f"CardDeck({self.cards})"

    def __getitem__(self,index: int):
        if 0 <= index < len(self.cards):
            return self.cards[index]
        else:
            raise IndexError(f"Index out of range ({index})")








class FrenchCardDeck(CardDeck):
    """Deck of French Cards
    
    """

    def __init__(self):
        cards = []
        card_suits = ["diamonds", "hearts", "spades","clubs"]
        card_types = ["2","3","4","5","6","7","8","9","jack","queen","king","ace"]
        for suits in card_suits:
            for types in card_types:
                cards.append(Card(suit=suits, card_type=types))

        super().__init__(cards=cards)


# PART 2:
# Create a second class that represents a deck of cards usable for Skat -- it should only contain cards from 7 upwards.
# It should offer all the same functionality of the first class.



class SkatDeck(CardDeck):
    """Deck of Cards for Skat
    
    """

    def __init__(self):
        cards = []
        card_suits = ["diamonds", "hearts", "spades","clubs"]
        card_types = ["7","8","9","jack","queen","king","ace"]
        for suits in card_suits:
            for types in card_types:
                cards.append(Card(suit=suits, card_type=types))

        super().__init__(cards=cards)




# Write some code to test the functionality of both kinds of decks. (You can use `assert` to make sure your classes behave the way you expect them to.)




class card_game_test(unittest.TestCase):
    """
    Test class for the card games
    """

    def test_Card_object(self):
        TestCard = Card(suit="diamonds",card_type="ace")#create Test Card
        #test string representation
        test_str_representation_expected = "ace of diamonds"
        test_str_representation_actual = str(TestCard)
        self.assertEqual(test_str_representation_expected,test_str_representation_actual)

        #test attributes (assert they are public)
        test_attr_type_public_expected = "ace"
        test_attr_type_public_actual = TestCard.card_type
        self.assertEqual(test_attr_type_public_expected,test_attr_type_public_actual)


    def test_indexing(self):
        TestFrenchCardDeck = FrenchCardDeck()
        TestSkatDeck = SkatDeck()

        ExampleCardFrench = TestFrenchCardDeck[0]
        ExampleCardSkat = TestSkatDeck[0]
        self.assertIsInstance(ExampleCardFrench,Card)
        self.assertIsInstance(ExampleCardSkat,Card)


    def test_iterating(self):
        TestFrenchCardDeck = FrenchCardDeck()
        TestSkatDeck = SkatDeck()

        for cards in TestFrenchCardDeck:#test iterating through the FrenchCardDeck
            self.assertIsInstance(cards, Card)
            self.assertIsInstance(str(cards), str)

        for cards in TestSkatDeck:#test iterating through the SkatDeck
            self.assertIsInstance(cards, Card)
            self.assertIsInstance(str(cards), str)

    def test_str_representation(self):
        TestFrenchCardDeck = FrenchCardDeck()
        TestSkatDeck = SkatDeck()
        #FrenchDeck representation as string
        FrenchDeck_str_expected = "2 of diamonds, 3 of diamonds, 4 of diamonds, 5 of diamonds, 6 of diamonds, 7 of diamonds, 8 of diamonds, 9 of diamonds, jack of diamonds, queen of diamonds, king of diamonds, ace of diamonds, 2 of hearts, 3 of hearts, 4 of hearts, 5 of hearts, 6 of hearts, 7 of hearts, 8 of hearts, 9 of hearts, jack of hearts, queen of hearts, king of hearts, ace of hearts, 2 of spades, 3 of spades, 4 of spades, 5 of spades, 6 of spades, 7 of spades, 8 of spades, 9 of spades, jack of spades, queen of spades, king of spades, ace of spades, 2 of clubs, 3 of clubs, 4 of clubs, 5 of clubs, 6 of clubs, 7 of clubs, 8 of clubs, 9 of clubs, jack of clubs, queen of clubs, king of clubs, ace of clubs"
        FrenchDeck_str_actual = str(TestFrenchCardDeck)
        self.assertEqual(FrenchDeck_str_expected,FrenchDeck_str_actual)
        
        #SkatDeck representation as string
        SkatDeck_str_expected = "7 of diamonds, 8 of diamonds, 9 of diamonds, jack of diamonds, queen of diamonds, king of diamonds, ace of diamonds, 7 of hearts, 8 of hearts, 9 of hearts, jack of hearts, queen of hearts, king of hearts, ace of hearts, 7 of spades, 8 of spades, 9 of spades, jack of spades, queen of spades, king of spades, ace of spades, 7 of clubs, 8 of clubs, 9 of clubs, jack of clubs, queen of clubs, king of clubs, ace of clubs"
        SkatDeck_str_actual = str(TestSkatDeck)
        self.assertEqual(SkatDeck_str_expected,SkatDeck_str_actual)



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



def double_finder(lower_bound:int, upper_bound:int) -> int:
    """Solution for Exercise 3

    Parameters:
    --------------
    lower_bound(int):                   lower bound of the loop(inclusive)
    upper_bound(int):                   upper bound of the loop(exclusive)
    
    Return Values:
    --------------
    int:                                count of numbers that fulfill the requirements:

    - they are within the (left-inclusive and right-exclusive) bounds passed to the function
    - there is at least one group of exactly two adjacent digits within the number which are the same (like 33 in 123345)
    - digits only increase going from left to right

    Code Optimizations to reach high efficiency:
    minor improvments:
    1. Avoiding strings and using array / tuple(previously) of ints instead
    2. converting the current number to the array via bytes and ascii
    3. Skip follow-up valid numbers (Example: 123345 - skips: 123346, 123347, 123348, 123349)

    major improvments (responsible for O(logn) complexity):
    Skip invalid numbers: Skips numbers that are certainly invalid.
    Example: i = 123934 - is invalid because out of order (possibly more causes)
    - will stay invalid up to at least 12399, hence, numbers from 1239934 up to 12399 do not have to be checked -> 65 numbers will be skipped

    If you are interested in what exactly happens in the code, consider un-commenting lines 244, 262, 269 to see debugging information
    """


    hit_count = 0#count valid numbers (='hits')
    skip_count = 0#DEBUG: counts how many numbers have been skipped
    iskip_count = 0#DEBUG: count individual skips
    pos_skip_count = 0#DEBUG: positive skip count
    pos_iskip_count = 0#DEBUG: positive individual skip count

    i = lower_bound
    while i < upper_bound:
        ascii0 = b'0'[0]
        digit_tuple = [d-ascii0 for d in b'%d'%i]#split digits into a array
        digit_len = len(digit_tuple)#length of current number
        adj_pos = digit_len#adjacent digit position -> required for positive skip calculation

        elem_counter = 1#element counter
        ordered = True#set ordered as True
        adj_elements = False#set adjacent values as False
        for idx,elements in enumerate(digit_tuple):#enumerate over the digits
            if idx == 0: continue#go to next iteration if looking at the first value
            if  elements < digit_tuple[idx-1]:#check if list is in order
                ordered = False
                #calculate skips
                curr_skips = 0
                for j in range(idx-1,digit_len):#loop from previous index to end of list
                    if digit_tuple[j] < digit_tuple[idx-1]:
                        curr_skips += (digit_tuple[idx-1] - digit_tuple[j])*10**((digit_len)- j -1)
                #print(f"NSkip found - i: {i}, stopped at: {elements}[{idx}], digits read as: {digit_tuple} ,skips: {curr_skips}, new_i: {i+curr_skips}")#Debug statement
                i += curr_skips - 1
                skip_count += curr_skips - 1#Debug info
                iskip_count += 1#Debug info
            elif elements == digit_tuple[idx-1]:#check if digit is same as previous digit
                elem_counter += 1
            else:
                if elem_counter == 2:#found single adjacent double (because current value differs from previous)
                    adj_elements = True
                    adj_pos = idx
                elem_counter = 1
        if elem_counter == 2:
            adj_elements = True
        
        if ordered and adj_elements:#found adjacent double
            hit_count += 1
            if digit_tuple[digit_len-1] < 9 and adj_pos < digit_len -2:#only calculate skips if the double was not found near end
                pos_skips = 9 - digit_tuple[digit_len-1]#calculate 'positive' skips -> how many numbers are certainly valid
                #print(f"\tPSkip found - i: {i}, stopped at: {elements}[{idx}], digits read as: {digit_tuple} ,skips: {pos_skips}, new_i: {i+pos_skips}")#Debug statement (one tab to be easier to read)
                i += pos_skips
                hit_count += pos_skips
                pos_skip_count += pos_skips#Debug info
                pos_iskip_count+= 1#Debug info

        i += 1
    #print(f"Skip_count: {skip_count}; iskips: {iskip_count}; average iskip-width: {round(skip_count/iskip_count,2)}| pos_skips: {pos_skip_count}; pos_iskips: {pos_iskip_count}; average iskip width: {round(pos_skip_count/pos_iskip_count,2)}")
    return hit_count




from timeit import timeit
#print(double_finder(134564, 585159))

#print(timeit(lambda: double_finder(134564, 585159), number=1000)/1000)# on average: 0.005s on personal hardware, time complexity: O(log(n)) and space: O(k) (n: range of numbers, k: digit length) 



class double_finder_test(unittest.TestCase):

    def test_response_given(self):
        lower_bound = 134564
        upper_bound = 585159
        response_expected = 1306
        response_actual = double_finder(lower_bound=lower_bound,upper_bound=upper_bound)
        self.assertEqual(response_expected, response_actual)

    def test_performance_regular_data(self):
        avg_time = timeit(lambda: double_finder(134564, 585159), number=50)/50
        self.assertTrue(avg_time < 1)#assume the script should be faster than 1 second on any hardware(on my hardware: 0.005s)
        print(f"average time Task 3: {round(avg_time,5)}")



if __name__ == '__main__':#unittest test runner
    unittest.main()


