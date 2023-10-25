commands = [1, 12, 2, 3, 1, 1, 2, 3, 1, 3, 4, 3, 1, 5, 0, 3, 2, 1, 9, 19, 1, 5, 19, 23, 1, 6, 23, 27, 1, 27, 10, 31, 1, 31, 5, 35, 2, 10, 35, 39, 1, 9, 39, 43, 1, 43, 5, 47, 1, 47, 6, 51, 2, 51, 6, 55, 1, 13, 55, 59, 2, 6, 59, 63, 1, 63, 5, 67, 2, 10, 67, 71, 1, 9, 71, 75, 1, 75, 13, 79, 1, 10, 79, 83, 2, 83, 13, 87, 1, 87, 6, 91, 1, 5, 91, 95, 2, 95, 9, 99, 1, 5, 99, 103, 1, 103, 6, 107, 2, 107, 13, 111, 1, 111, 10, 115, 2, 10, 115, 119, 1, 9, 119, 123, 1, 123, 9, 127, 1, 13, 127, 131, 2, 10, 131, 135, 1, 135, 5, 139, 1, 2, 139, 143, 1, 143, 5, 0, 99, 2, 0, 14, 0]
      
def listRechnung(arr):
    for i in range(0,len(arr),4):
        if arr[i] == 1:
            arr[arr[i+3]] = arr[i+1] + arr[i+2]
        elif arr[i] == 2:
            arr[arr[i+3]] = arr[i+1] * arr[i+2]
        elif arr[i] == 99:
            break
        else: 
            print("Fehler an Stelle ", i)
            break
    return arr[0]

print(listRechnung(commands))


liste1 = ["7", "g", "67", "fuenf", "hh"]
liste2 = ["h", "j", "88", "5677777", "2"]
liste3 = []
liste4 = ["pferd", "1", "lotto", "a", "7"]
liste5 = ["2", "+", "2,78", "h", "H", "k"]
# Ich habe "number" als integer interpretiert und Nummern sind nicht in der char Liste

def listSort(*args):
    zahlen = []
    character = []
    for i in range(0,len(args)):
        try:
            int(args[i])
            zahlen.append(int(args[i]))
        except(ValueError):      
            if len(args[i]) == 1:
                character.append(args[i])
      
    return zahlen, character


print(listSort(*liste1))
print(listSort(*liste2))
print(listSort(*liste3))
print(listSort(*liste4))
print(listSort(*liste5))
