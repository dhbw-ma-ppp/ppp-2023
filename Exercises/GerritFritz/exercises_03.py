#Gerrit Fritz
#22.10.2023

class Card():
    def __init__(self, symbol, number):
        self.symbol = symbol
        if number < 2: raise ValueError(f"Card number {number} not in range(2,15)")
        elif number <= 10:
            self.number = str(number)
        elif number <= 14:
            match number:
                case 11: self.number = "Jack"
                case 12: self.number = "Queen"
                case 13: self.number = "King"
                case 14: self.number = "Ace"
        else: raise ValueError(f"Card number {number} not in range(2,15)")

    def __str__(self):
        return (f"{self.number} of {self.symbol}")


class BasicDeck():
    def __init__(self, start, end):
        self.cards =  [Card(symbol, number) for symbol in ["Diamonds","Hearts","Spades","Clubs"] for number in range(start, end+1)]

    def __iter__(self):
        return (card for card in self.cards)
    
    def __str__(self):
        return ", ".join([str(card) for card in self.cards])
    
    def __getitem__(self, index):
        card_range = range(len(self.cards))
        if index in card_range:
            return self.cards[index]
        else: raise IndexError(f"Index {index} not in {card_range}")


class FrenchDeck(BasicDeck):
    def __init__(self): super().__init__(2, 14)
        

class SkatDeck(BasicDeck):
    def __init__(self): super().__init__(7, 14)


fr_deck = FrenchDeck()
sk_deck = SkatDeck()

assert str(fr_deck) == "2 of Diamonds, 3 of Diamonds, 4 of Diamonds, 5 of Diamonds, 6 of Diamonds, 7 of Diamonds, 8 of Diamonds, 9 of Diamonds, 10 of Diamonds, Jack of Diamonds, Queen of Diamonds, King of Diamonds, Ace of Diamonds, 2 of Hearts, 3 of Hearts, 4 of Hearts, 5 of Hearts, 6 of Hearts, 7 of Hearts, 8 of Hearts, 9 of Hearts, 10 of Hearts, Jack of Hearts, Queen of Hearts, King of Hearts, Ace of Hearts, 2 of Spades, 3 of Spades, 4 of Spades, 5 of Spades, 6 of Spades, 7 of Spades, 8 of Spades, 9 of Spades, 10 of Spades, Jack of Spades, Queen of Spades, King of Spades, Ace of Spades, 2 of Clubs, 3 of Clubs, 4 of Clubs, 5 of Clubs, 6 of Clubs, 7 of Clubs, 8 of Clubs, 9 of Clubs, 10 of Clubs, Jack of Clubs, Queen of Clubs, King of Clubs, Ace of Clubs"
assert str(sk_deck) == "7 of Diamonds, 8 of Diamonds, 9 of Diamonds, 10 of Diamonds, Jack of Diamonds, Queen of Diamonds, King of Diamonds, Ace of Diamonds, 7 of Hearts, 8 of Hearts, 9 of Hearts, 10 of Hearts, Jack of Hearts, Queen of Hearts, King of Hearts, Ace of Hearts, 7 of Spades, 8 of Spades, 9 of Spades, 10 of Spades, Jack of Spades, Queen of Spades, King of Spades, Ace of Spades, 7 of Clubs, 8 of Clubs, 9 of Clubs, 10 of Clubs, Jack of Clubs, Queen of Clubs, King of Clubs, Ace of Clubs"
assert str(fr_deck[51]) == "Ace of Clubs"
assert str(sk_deck[31]) == "Ace of Clubs"
assert str([str(card) for card in fr_deck]) == "['2 of Diamonds', '3 of Diamonds', '4 of Diamonds', '5 of Diamonds', '6 of Diamonds', '7 of Diamonds', '8 of Diamonds', '9 of Diamonds', '10 of Diamonds', 'Jack of Diamonds', 'Queen of Diamonds', 'King of Diamonds', 'Ace of Diamonds', '2 of Hearts', '3 of Hearts', '4 of Hearts', '5 of Hearts', '6 of Hearts', '7 of Hearts', '8 of Hearts', '9 of Hearts', '10 of Hearts', 'Jack of Hearts', 'Queen of Hearts', 'King of Hearts', 'Ace of Hearts', '2 of Spades', '3 of Spades', '4 of Spades', '5 of Spades', '6 of Spades', '7 of Spades', '8 of Spades', '9 of Spades', '10 of Spades', 'Jack of Spades', 'Queen of Spades', 'King of Spades', 'Ace of Spades', '2 of Clubs', '3 of Clubs', '4 of Clubs', '5 of Clubs', '6 of Clubs', '7 of Clubs', '8 of Clubs', '9 of Clubs', '10 of Clubs', 'Jack of Clubs', 'Queen of Clubs', 'King of Clubs', 'Ace of Clubs']"
assert str([str(card) for card in sk_deck]) == "['7 of Diamonds', '8 of Diamonds', '9 of Diamonds', '10 of Diamonds', 'Jack of Diamonds', 'Queen of Diamonds', 'King of Diamonds', 'Ace of Diamonds', '7 of Hearts', '8 of Hearts', '9 of Hearts', '10 of Hearts', 'Jack of Hearts', 'Queen of Hearts', 'King of Hearts', 'Ace of Hearts', '7 of Spades', '8 of Spades', '9 of Spades', '10 of Spades', 'Jack of Spades', 'Queen of Spades', 'King of Spades', 'Ace of Spades', '7 of Clubs', '8 of Clubs', '9 of Clubs', '10 of Clubs', 'Jack of Clubs', 'Queen of Clubs', 'King of Clubs', 'Ace of Clubs']"


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
