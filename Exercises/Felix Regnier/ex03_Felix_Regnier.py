# PART 1:
# Write a class for a French deck of cards (2-Ace of diamonds, hearts, spades, clubs).
# The deck of cards should behave like a sequence.
# When initialized the cards should all be in a well-defined order (2-Ace of each suite, suites in the order above
# I should be able to index into the deck to retrieve one card.
# I should be able to iterate over all cards in the deck.
# Printing a cards string representation should give me a nice, 
# readable description of that card.


#######################################################################################
#instanzen werden die kartendecks, welche der klasse french oder skat angehören. beide sind jeweils eine Liste, die die Karten in gegebener Reihenfolge angibt.
#Diese Reihenfolge wird im constructor erstellt. Die übergeordnete Gruppe wird Cards. Hier wird die Liste erstellt. Die Subklassen geben nur den Bereich der Karten an.

class Karten():
  def __init__(self, tiefste=2):
    self.farben = ["Karo","Herz","Pik","Kreuz"]
    self.werte = ["2","3","4","5","6","7","8","9","10","B","D","K","A"]    
    stapel = []
    if tiefste == 7:
      werte = ["7","8","9","10","B","D","K","A"]
    for wert in werte:
      for farbe in farben:
        stapel.append(farbe + " " + wert)

class French(Karten):
    def __init__(self):
        Karten()

class Skat(Karten):
    def __init__(self):
        Karten(7)
            
#######################################################################################

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