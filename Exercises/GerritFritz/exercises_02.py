#Gerrit Fritz
#15.10.2023


# Aufgabe 1

testCase1 = [1, 0, 0, 0, 99]
testCase2 = [1, 1, 1, 4, 99, 5, 6, 0, 99]
testCase3 = [1, 12, 2, 3, 1, 1, 2, 3, 1, 3, 4, 3, 1, 5, 0, 3, 2, 1, 9, 19, 1, 5, 19, 23, 1, 6, 23, 27, 1, 27, 10, 31, 1, 31, 5, 35, 2, 10, 35, 39, 1, 9, 39, 43, 1, 43, 5, 47, 1, 47, 6, 51, 2, 51, 6, 55, 1, 13, 55, 59, 2, 6, 59, 63, 1, 63, 5, 67, 2, 10, 67, 71, 1, 9, 71, 75, 1, 75, 13, 79, 1, 10, 79, 83, 2, 83, 13, 87, 1, 87, 6, 91, 1, 5, 91, 95, 2, 95, 9, 99, 1, 5, 99, 103, 1, 103, 6, 107, 2, 107, 13, 111, 1, 111, 10, 115, 2, 10, 115, 119, 1, 9, 119, 123, 1, 123, 9, 127, 1, 13, 127, 131, 2, 10, 131, 135, 1, 135, 5, 139, 1, 2, 139, 143, 1, 143, 5, 0, 99, 2, 0, 14, 0]

def calculate(opcode, num1, num2):
    match opcode:
        case 1: return num1+num2
        case 2: return num1*num2
        case _: raise RuntimeError('Wrong opcode')

def getOutput(commands):
    for i, element in enumerate(commands):
        if i%4 != 0:
            continue
        if element == 99:
            break
        index1 = commands[i+1]
        index2 = commands[i+2]
        commands[commands[i+3]] = calculate(element, commands[index1], commands[index2])
    return commands[0]

for i in range(3):
    print(f"Output for testcase {i+1}: {getOutput(eval('testCase' + str(i+1)))}")


# Aufgabe 2

testArgs1 = ("test", "hi", "a","-1","123", "hey456")
testArgs2 = ("a","bc","123325g3","1,2","1.5","4")
testArgs3 = ("a1233","b","123325g3","1-0","-2","99..9999")

def getArgLists(*args):
    numberList = []
    singleList = []
    for element in args:
        if len(element)==1:
            singleList.append(element)
        num = str("".join([char for char in element if char in "-.1234567890"]))
        if num == element and element.count(".")<=1 and element.count("-")<=1:
            if "-" in element and element.index("-")>=1:
                continue
            numberList.append(element)
    return numberList,singleList

for i in range(3):
    args = eval('testArgs' + str(i+1))
    print(f"Output for args {args}: \n{getArgLists(*args)}")