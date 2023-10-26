# PART 1:
# Write a class for a French deck of cards (2-Ace of diamonds, hearts, spades, clubs).#
# The deck of cards should behave like a sequence.#
# When initialized the cards should all be in a well-defined order (2-Ace of each suite, suites in the order above#
# I should be able to index into the deck to retrieve one card.#
# I should be able to iterate over all cards in the deck.#
# Printing a cards string representation should give me a nice, 
# readable description of that card.###

# PART 2:
# Create a second class that represents a deck of cards usable for Skat -- it should only contain cards from 7 upwards.
# It should offer all the same functionality of the first class.


# Write some code to test the functionality of both kinds of decks. (You can use `assert` to make sure your classes behave the way you expect them to.)

class Karten():
    def __init__(self, tiefste=2):
        """
        Bei der Erstellung der Klasse Karten wird ein Kartendeck von 2 bis Ass mit 4 Farben erstellt.
        Falls das argument 7 mitgegeben wird, wird ein Kartendeck von 7 bis Ass erstellt.
        Die Klasse hat die Attribute farben, werte und einen stapel, in welchem die Karten als strings in einer Liste hinterlegt sind

        args: nichts oder 7
        """
        self.farben = ["Karo","Herz","Pik","Kreuz"]
        self.werte = ["2","3","4","5","6","7","8","9","10","B","D","K","A"]    
        self.stapel = []
        if tiefste == 7:
            self.werte = ["7","8","9","10","B","D","K","A"]
        for farbe in self.farben:
            for wert in self.werte:
                self.stapel.append(farbe + " " + wert)

        
    def get_card(self,position):
        """
        Diese Funktion gibt die Karte an der angegebenen Position aus
        
        arg: Position
        returns: Karte als string
        """
        return self.stapel[position]
    

    def iter_cards(self):   
        """
        Diese Funktion printet die stellen im Kartendeck mit den dazugehörigen Kartenbezeichnungen
        """   
        for card in range(0, len(self.stapel)):
            directory = {card : self.stapel[card]}
            print(directory)
    

class French(Karten):
    def __init__(self):
        super().__init__()        


class Skat(Karten):
    def __init__(self):
        super().__init__(7)
        


skat1 = Skat()
assert skat1.stapel == ['Karo 7', 'Karo 8', 'Karo 9', 'Karo 10', 'Karo B', 'Karo D', 'Karo K', 'Karo A',
                         'Herz 7', 'Herz 8', 'Herz 9', 'Herz 10', 'Herz B', 'Herz D', 'Herz K', 'Herz A',
                         'Pik 7', 'Pik 8', 'Pik 9', 'Pik 10', 'Pik B', 'Pik D', 'Pik K', 'Pik A',
                         'Kreuz 7', 'Kreuz 8', 'Kreuz 9', 'Kreuz 10', 'Kreuz B', 'Kreuz D', 'Kreuz K', 'Kreuz A']
assert skat1.get_card(12) == 'Herz B'

french1 = French()
assert french1.stapel == ['Karo 2', 'Karo 3', 'Karo 4', 'Karo 5', 'Karo 6', 'Karo 7', 'Karo 8', 'Karo 9', 'Karo 10', 'Karo B', 'Karo D', 'Karo K', 'Karo A',
                           'Herz 2', 'Herz 3', 'Herz 4', 'Herz 5', 'Herz 6', 'Herz 7', 'Herz 8', 'Herz 9', 'Herz 10', 'Herz B', 'Herz D', 'Herz K', 'Herz A',
                           'Pik 2', 'Pik 3', 'Pik 4', 'Pik 5', 'Pik 6', 'Pik 7', 'Pik 8', 'Pik 9', 'Pik 10', 'Pik B', 'Pik D', 'Pik K', 'Pik A',
                           'Kreuz 2', 'Kreuz 3', 'Kreuz 4', 'Kreuz 5', 'Kreuz 6', 'Kreuz 7', 'Kreuz 8', 'Kreuz 9', 'Kreuz 10', 'Kreuz B', 'Kreuz D', 'Kreuz K', 'Kreuz A']
assert french1.get_card(12) == 'Karo A'

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

def count_for(lower_bound, upper_bound):
    """
    Diese Funktion zählt, wie viele Zahlen zwischen zwei Grenzen liegen, die folgende Kriterien erfüllen:
    1: die Ziffern der Zahl werden größer von links nach rechts
    2: es gibt mindestens ein Zahlenpaar mit genau 2 gleichen Ziffern
    
    args: untere Grenze, obere Grenze
    return: Anzahl der passenden Zahlen
    
    """
    anzahl = 0
    if upper_bound < lower_bound:
        print("obere Grenze kleiner als untere")
    else:
        for zahl in range(lower_bound, upper_bound):
            ls_zahl = list(str(zahl))
            if check_increase(ls_zahl) and check_doppelt(ls_zahl):
                anzahl += 1
    return anzahl
               

def check_increase(ls_zahl):
    """
    Diese Funktion überprüft das Kriterium 1: die Ziffern der Zahl werden größer von links nach rechts
    
    arg: liste mit ziffern als character
    return: True, wenn Kriterium zutrifft bzw. False, wenn Kriterium nicht zutrifft
    """
    for ziffer in range(1,len(ls_zahl)):
        if int(ls_zahl[ziffer]) < int(ls_zahl[ziffer-1]):
            return False
    return True


def check_doppelt(ls_zahl):
    """
    Diese Funktion überprüft das Kriterium 2: es gibt mindestens ein Zahlenpaar mit genau 2 gleichen Ziffern
    Außerdem werden hier führende Nullen ausgeschlossen
    
    arg: liste mit ziffern als character
    return: True, wenn Kriterium zutrifft bzw. False, wenn Kriterium nicht zutrifft
    """
    for ziffer in set(ls_zahl):
        if ls_zahl.count(ziffer) == 2 and ziffer != 0:
            return True
    return False


print("Anzahl zutreffender Zahlen: ", count_for(134564,585159))