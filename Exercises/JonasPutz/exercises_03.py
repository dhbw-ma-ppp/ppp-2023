# PART 1:
# Write a class for a French deck of cards (2-Ace of diamonds, hearts, spades, clubs).
# The deck of cards should behave like a sequence.
# When initialized the cards should all be in a well-defined order (2-Ace of each suite, suites in the order above
# I should be able to index into the deck to retrieve one card.
# I should be able to iterate over all cards in the deck.
# Printing a cards string representation should give me a nice, 
# readable description of that card.
from timeit import timeit
from collections import UserList


class Card:
    """ Placeholder for Card elements.
        A Card is defined by its value (self.value) and its suit (self.suit).

        These values must be specified in the constructor.
    """
    def __init__(self, value, suit):
        """ The constructor returnes a new card with the specified values.

            Parameters
            ----------
            value (str)
                the face value of the card (usually 2 - ace)
            suit (str)
                the suit of the card (usually diamonds, hearts, spades, clubs)
        """
        self.value = value
        self.suit = suit

    def __str__(self) -> str:
        """ Returns a string representation of the card in the form:
            
            "{self.value} of {self.suit}"
            
            e.g: 7 of hearts, Ace of spades, ...
        """
        return f"{self.value} of {self.suit}"
    
class French_Deck(UserList):
    """ A french deck

        (using the values: 2 - Ace and suits: diamonds, hearts, spades, clubs)
    """
    _values = [
        '2',
        '3',
        '4',
        '5',
        '6',
        '7',
        '8',
        '9',
        '10',
        'Jack',
        'Queen',
        'King',
        'Ace'
    ]
    _suits = [
        'diamonds',
        'hearts',
        'spades',
        'clubs'
    ]

    def __init__(self):
        self.data = [
            Card(value, suit) 
            for suit in self._suits
            for value in self._values
        ]

# PART 2:
# Create a second class that represents a deck of cards usable for Skat -- it should only contain cards from 7 upwards.
# It should offer all the same functionality of the first class.

class Skat_Deck(French_Deck):
    """ A skat deck

        same as a french deck but just using the values: 7 - Ace
    """
    _values = [
        '7',
        '8',
        '9',
        '10',
        'Jack',
        'Queen',
        'King',
        'Ace'
    ]

# Write some code to test the functionality of both kinds of decks. (You can use `assert` to make sure your classes behave the way you expect them to.)

print("-----French Deck-----")
french_deck = French_Deck()
for card in french_deck:
    print(f"{card}")
print(f"Card at position [1]: {french_deck[1]}")

print("-----Skat Deck-----")
skat_deck = Skat_Deck()
for card in skat_deck:
    print(f"{card}")
print(f"Card at position [1]: {skat_deck[1]}")

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

def analyse_numbers(lower_bound, upper_bound):
    """ Analyse numbers:

        returns all numbers from lower bound (inclusiv) to upper bound (exclusiv) 
        which digits are in ascending order and include at least one digit exactly twice
    """

    numbers = []        #stores all valid numbers
    digit_counter = []   #stores the count of 0's, 1's, ..., 9's
    last_digit = 0       #stores the last used digit
    is_valid = True      #stores if the number is valid

    for number in range(lower_bound, upper_bound):
        last_digit = 0           #resets all used values
        is_valid = True
        digit_counter = [0] * 10

        for digit in map(int,str(number)):  #execute for each digit in the number (from left to right)
            if digit < last_digit:    
                is_valid = False             #if the digit is smaller than the last one, set the number to invalid
                break                       #this means, the digits are not ascending order
            last_digit = digit

            digit_counter[digit] += 1        #increase the digit counter

        is_valid &= any(d == 2 for d in digit_counter)    #if the number is valid, test if any digit is included exactly twice

        if is_valid:
            numbers.append(number)          #add the number to the list, if it is valid

    return len(numbers)         #returns the number of numbers found

print(f"\n\nThe function found {analyse_numbers(134564, 585159)} valid numbers")


##########################################################################
# The function below is much faster but very complicated. 
# It is not well documented and should be seen as an inspiration of what could have been done.
def analyse_numbers_fast(lower_bound, upper_bound):
    #calculate the 'real' lower bound (134564 is not a valid number, it will be set to 134566, the first ordered one)
    lower_bound_array = [int(char) for char in list(str(lower_bound))] #the array containing all digits (e.g:[1,3,4,5,6,6])
    buffer = lower_bound_array[0]
    for index in range(1, len(lower_bound_array)):
        buffer = max(buffer, lower_bound_array[index])
        lower_bound_array[index] = buffer
    lower_bound = int("".join(map(str,lower_bound_array)))

    #calculate the 'real' upper bound (585159 will be set to 579999)
    upper_bound_array = [int(char) for char in list(str(upper_bound - 1))] #same as before (e.g:[5,7,9,9,9,9])
    buffer = -1
    for index in range(0, len(upper_bound_array) - 1): #finds the index, where the order first breaks (e.g:1 - between 8 and 5)
        if upper_bound_array[index] > upper_bound_array[index + 1]:
            buffer = index
            break
    if buffer >= 0:
        upper_bound_array[buffer] -= 1 #counts the buffer value one down (e.g: 8 -> 7)
        for index in range(buffer + 1, len(upper_bound_array)): #sets all other value to 9
            upper_bound_array[index] = 9
    upper_bound = int("".join(map(str,upper_bound_array)))

    for _ in range(len(upper_bound_array) - len(lower_bound_array)): #fills the lower_bound with leading 0's, if necessary
        lower_bound_array.insert(0, 0)

    number_counter = 0 #this value will be used to find the necessary double
    last_digit_index = len(upper_bound_array) - 1 #last value being processed by the recursive functions

    #generall Idea:
    #use for a number with n digits n nested for loops with each one starting from the current digit from the last one
    #this will only generate ordered numbers

    #used arguments in the recursive tree:
    #index (int): the current index of the digit being handeled e.g: at the beginning 0 and in the end last_digit_index
    #current_number_counter (int): this value will follow the following pattern:
    #   >0: first occurence of the given digit              bool(7) = True
    #   =0: second occurence of the given digit             bool(0) = False
    #   <0: third and more occurences of the given digit    bool(-7) = True
    #is_number_invalid (bool): will contain only false (number is valid) if the double constraint is already matched by digits before
    #   otherwise this will always be true (not yet valid)

    #the start method for the recursiv tree
    #will be executed below with recursive_starter(0, -1, true)
    def recursive_starter(index, current_number_counter, is_number_invalid):
        #this function will represent the for loop from the lower_bound_array[index] to upperBoundIndex[index]

        if lower_bound_array[index] < upper_bound_array[index]:
            #for loop required, the digit isnt clearly determined by the bounds (e.g lower_bound:2, upper_bound:7)

            if index < last_digit_index:
                #recursion will continue for the next index

                #will loop over the next digit from lower_bound_array[index + 1] to 9
                if lower_bound_array[index] == lower_bound_array[index + 1]: #count current_number_counter down if the digit is a double digit
                    first_recursive_loop(index + 1, current_number_counter - lower_bound_array[index], is_number_invalid)
                else:
                    first_recursive_loop(index + 1, lower_bound_array[index], is_number_invalid)

                #set is_number_invalid to false (number is now valid) if a doubleDigit is found.
                #in the future, only digits will be evaluated, that are larger -> no chance for the double to change to a triple
                is_number_invalid &= bool(current_number_counter)

                #loop from lower_bound_array[index] + 1 to upper_bound_array[index]: lower_bound_array[index] is already handled before!
                for i in range(lower_bound_array[index] + 1, upper_bound_array[index]):
                    lower_bound_array[index + 1] = i #set the nex numbers lower bound to be this digit
                    #continue with the next digit: current_number_counter will be reset (to i), 
                    #as i is now different from the last handeled digit
                    recursive_loop(index + 1, i, is_number_invalid) 

                #the last digit will be handeled seperatly by the "last_recursive_loop",
                #as the loop in this function will only count to the upper_bound
                lower_bound_array[index + 1] = upper_bound_array[index]
                last_recursive_loop(index + 1, upper_bound_array[index], is_number_invalid)
            else:
                #end the recursive loop and lets the end method count the valid numbers
                recursive_end(is_number_invalid, current_number_counter, lower_bound_array[index], upper_bound_array[index])
        else:
            #for loop not required, the digit is clearly determined by the bounds (e.g lower_bound:4, upper_bound:4)

            if index < last_digit_index:
                #start again with the next digit in the array
                recursive_starter(index + 1, lower_bound_array[index], is_number_invalid)
            else:
                #adds a valid number to the count, if the recursive loop should be exited and the current number is valid
                nonlocal number_counter
                number_counter += 0 if is_number_invalid else 1

    def last_recursive_loop(index, current_number_counter, is_number_invalid):
        #this function will count from 0 to upper_bound_array[index]

        if index < last_digit_index:
            #recursive loop

            if upper_bound_array[index] == lower_bound_array[index]:
                #number is determined by the bounds, continue with next number
                #as the lower bound is set by the function before to be the lowest possible digit (same as last one),
                #the current_number_counter will count down
                last_recursive_loop(index + 1, current_number_counter - upper_bound_array[index], is_number_invalid)
            else:
                #go to the next digit with this digit one being the digit before -> current_number_counter will count down
                lower_bound_array[index + 1] = lower_bound_array[index]
                recursive_loop(index + 1, current_number_counter - lower_bound_array[index], is_number_invalid)

                #the digit finally changed -> check if the number is now valid (is_number_invalid will be false)
                is_number_invalid &= bool(current_number_counter)

                #run through the loop from lower_bound_array[index] + 1 to upper_bound_array[index]
                for i in range(lower_bound_array[index] + 1, upper_bound_array[index]):
                    lower_bound_array[index + 1] = i
                    recursive_loop(index + 1, i, is_number_invalid) #continue with the next digit (current_number_counter is reset)

                #the last digit will be handeled by a last recursive loop again (respecting the upper bound)
                lower_bound_array[index + 1] = upper_bound_array[index]
                last_recursive_loop(index + 1, upper_bound_array[index], is_number_invalid)
        else:
            #stop of recursive loop
            recursive_end(is_number_invalid, current_number_counter, lower_bound_array[index], upper_bound_array[index])

    def first_recursive_loop(index, current_number_counter, is_number_invalid):
        #this function will count from lower_bound_array[index] to 9
        
        if index < last_digit_index:
            #recursive loop

            #run the next recursive step again with a first loop (respecting the preset lowerBounds)
            if lower_bound_array[index] == lower_bound_array[index - 1]:
                #digit is same as last one, decreasing current_number_counter
                first_recursive_loop(index + 1, current_number_counter - lower_bound_array[index], is_number_invalid)
            else:
                #digit is not the same, reset current_number_counter and set the number to valid if necessary
                is_number_invalid &= bool(current_number_counter)
                first_recursive_loop(index + 1, lower_bound_array[index], is_number_invalid)
            
            #set the number to valid if necessary
            is_number_invalid &= bool(current_number_counter)

            #run through the loop from lower_bound_array[index] + 1 (inclusive) to 10 (exclusive)
            for i in range(lower_bound_array[index] + 1, 10):
                #set the next lower_bound to be the current digit
                lower_bound_array[index + 1] = i
                #continue with next digit (currnetNumberCounter reset, digit is not the same as the last one)
                recursive_loop(index + 1, i, is_number_invalid)
        else:
            #stop the recursive loop
            recursive_end(is_number_invalid, current_number_counter, lower_bound_array[index])

    def recursive_loop(index, current_number_counter, is_number_invalid):
        #this function will count from a new (non preset by the pre recursiv) lower Bound to 9

        if index < last_digit_index:
            #recursive loop

            #the digit is the same as the last one -> current_number_counter decrease
            lower_bound_array[index + 1] = lower_bound_array[index]
            recursive_loop(index + 1, current_number_counter - lower_bound_array[index], is_number_invalid)

            #update is_number_invalid (digit has now changed)
            is_number_invalid &= bool(current_number_counter)

            #execute next recursive step (current_number_counter reset, digit has changed)
            for i in range(lower_bound_array[index] + 1, 10):
                lower_bound_array[index + 1] = i
                recursive_loop(index + 1, i, is_number_invalid)
        else:
            #stop the recursive function
            recursive_end(is_number_invalid, current_number_counter, lower_bound_array[index])


    def recursive_end(is_number_invalid, current_number_counter, lowerBoundValue, upperBoundValue = 9):
        nonlocal number_counter
        #add one number to the counter (this number has the format _______xx), if the current_number_counter reaches 0 after one more subtraction
        number_counter += 0 if is_number_invalid & bool(current_number_counter - lowerBoundValue) else 1

        #add remaining numbers to the counter (these numbers have the format _______xy), if the current_number_counter was 0 before -> ______xxy
        number_counter += 0 if is_number_invalid & bool(current_number_counter) else upperBoundValue - lowerBoundValue


    #start the recursive loop
    recursive_starter(0, -1, True)
    #and return the count after the loop finished
    return number_counter

print(f"--------Extra data below--------")
print(f"Function time comparison: (134564 to 585159)")
t1 = timeit(lambda: print(f"Result: {analyse_numbers(134564, 585159)}"), number=1)
print(f"analyse_numbers: {t1}s")
t2 = timeit(lambda: analyse_numbers_fast(134564, 585159), number=500) / 500
print(f"Result: {analyse_numbers_fast(134564, 585159)}")
print(f"analyse_numbers_fast: {t2}s")
print(f"The fast algorithem is {(t1 / t2 - 1) * 100:.10}% faster")

print(f"\nFunction time comparison: (1345640 to 5851590)")
t3 = timeit(lambda: print(f"Result: {analyse_numbers(1345640, 5851590)}"), number=1)
print(f"analyse_numbers: {t3}s")
t4 = timeit(lambda: analyse_numbers_fast(1345640, 5851590), number=100) / 100
print(f"Result: {analyse_numbers_fast(1345640, 5851590)}")
print(f"analyse_numbers_fast: {t4}s")
print(f"The fast algorithem is {(t3 / t4 - 1) * 100:.10}% faster")

print(f"\nFunction time comparison: (1345640000000000000 to 5851590000000000000)")
print(f"analyse_numbers: to slow to be run on numbers as large")
t5 = timeit(lambda: print(f"Result: {analyse_numbers_fast(1345640000000000000, 5851590000000000000)}"), number=1)
print(f"analyse_numbers_fast: {t5}s")
print(f"The fast algorithem is {(t1 / t5 - 1) * 100:.10}% faster than analyse_numbers(134564, 585159)")