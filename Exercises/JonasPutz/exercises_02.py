# Write a function that takes as input a list of integers and returns a single integer number.
# the numbers passed as argument form the working memory of a simulated computer.
# this computer will start by looking at the first value in the list passed to the function.
# this value will contain an `opcode`. Valid opcodes are 1, 2 or 99.
# Encountering any other value when you expect an opcode indicates an error in your coding.
# Meaning of opcodes:
#  1 indicates addition. If you encounter the opcode 1 you should read values from two positions 
#    of your working memory, add them, and store the result in a third position of your working memory.
#    The three numbers immediately after your opcode indicate the memory locations to read (first two values)
#    and write (third value) respectively. 
#    After executing the addition you should move to the next opcode by stepping forward 4 positions.
#  2 indicates multiplication. Otherwise the same rules apply as for opcode 1.
# 99 indicates halt. the program should stop after encountering the opcode 99.
# After the program stops, the function should return the value in the first location (address 0) 
# of your working memory.

# As an example, if the list of integers passed to your function is 
# [1, 0, 0, 0, 99] the 1 in the first position indicates you should read the values
# at position given by the second and third entries. Both of these indicate position 0, so you should read the value
# at position 0 twice. That value is 1. Adding 1 and 1 gives you two. You then look at the value in the fourth
# position, which is again 0, so you write the result to position 0. You then step forward by 4 steps, arriving at 99
# and ending the program. The final memory looks like [2, 0, 0, 0, 99]. Your function should return 2.

# Here's another testcase:
# [1, 1, 1, 4, 99, 5, 6, 0, 99] should become [30, 1, 1, 4, 2, 5, 6, 0, 99]
# Your function should return 30.


# print out which value is returned by your function for the following list:
commands = [1, 12, 2, 3, 1, 1, 2, 3, 1, 3, 4, 3, 1, 5, 0, 3, 2, 1, 9, 19, 1, 5, 19, 23, 1, 6, 23, 27, 1, 27, 10, 31, 1, 31, 5, 35, 2, 10, 35, 39, 1, 9, 39, 43, 1, 43, 5, 47, 1, 47, 6, 51, 2, 51, 6, 55, 1, 13, 55, 59, 2, 6, 59, 63, 1, 63, 5, 67, 2, 10, 67, 71, 1, 9, 71, 75, 1, 75, 13, 79, 1, 10, 79, 83, 2, 83, 13, 87, 1, 87, 6, 91, 1, 5, 91, 95, 2, 95, 9, 99, 1, 5, 99, 103, 1, 103, 6, 107, 2, 107, 13, 111, 1, 111, 10, 115, 2, 10, 115, 119, 1, 9, 119, 123, 1, 123, 9, 127, 1, 13, 127, 131, 2, 10, 131, 135, 1, 135, 5, 139, 1, 2, 139, 143, 1, 143, 5, 0, 99, 2, 0, 14, 0]

def commandAdd(currentIndex, memoryStream):
    """
        Command add:
            This function adds the values at positions specified at currentIndex + 1 and currnetIndex + 2 and saves the value in the slot at currentIndex + 3
        
        Input:
            currentIndex: The current position of the computer in the memory stream\n
            memoryStream: The memory stream the computer is running on\n
        
        Output:
            A tuple of:
                [0] the new position of the computer (int)
                
                [1] the modified memory stream (int[])    
    """
    memoryStream[memoryStream[currentIndex + 3]] = memoryStream[memoryStream[currentIndex + 1]] + memoryStream[memoryStream[currentIndex + 2]]
    return currentIndex + 4, memoryStream

def commandMultiply(currentIndex, memoryStream):
    """
        Command multiply:
            This function multiplies the values at positions specified at currentIndex + 1 and currnetIndex + 2 and saves the value in the slot at currentIndex + 3
        
        Input:
            currentIndex: The current position of the computer in the memory stream\n
            memoryStream: The memory stream the computer is running on\n
        
        Output:
            A tuple of:
                [0] the new position of the computer (int)
                
                [1] the modified memory stream (int[])
    """    
    memoryStream[memoryStream[currentIndex + 3]] = memoryStream[memoryStream[currentIndex + 1]] * memoryStream[memoryStream[currentIndex + 2]]
    return currentIndex + 4, memoryStream

def commandHalt(currentIndex, memoryStream):
    """
        Command Halt:
            Stops the execution of the computer
        
        Input:
            currentIndex: The current position of the computer in the memory stream
            memoryStream: The memory stream the computer is running on
        Output:
            A tuple of:
                [0] the new position of the computer -1, telling the program that the computer finished successfully (int)
            
                [1] the memoryStream inputet via the input (int[])
    """
    return -1, memoryStream

commandDictionary = {
    1: commandAdd,
    2: commandMultiply,
    99: commandHalt
}

def miniComputer(memoryStream):
    currentIndex = 0
    while currentIndex >= 0:
        if memoryStream[currentIndex] in commandDictionary:
            currentIndex, memoryStream = commandDictionary[memoryStream[currentIndex]](currentIndex, memoryStream)
        else:
            raise LookupError("Couldn't read command with value", memoryStream[currentIndex], "at position", currentIndex)
    
    if currentIndex == -1:
        print("mini computer finished execution succesfully")
    else:
        print(f"mini computer finished execution with error code: {currentIndex}")
    
    return memoryStream[0]

returnValue = miniComputer(commands)
print(f"mini computer returned the value {returnValue}")

#output:
#mini computer finished execution succesfully
#mini computer returned the value 3562672

###########################################
# Write a function that takes an arbitrary number of unnamed arguments
# All inputs will be of type string.
# the function should return two lists:
#   The first list should contain all arguments which can be interpreted
#   as a number.
#   The second list should contain all strings which contain just one character.
# Think of some good inputs to test this functionality, write down at least three
# examples and verify that the output for these examples is correct.

def inputSplitter(*args):
    """Input Splitter:
        This Method takes an arbitrary amount of unnamed input arguments and returns the numbers and chars found in the arguments in seperate arrays
        
        Input:
            *args: The number of arguments the method will run on
        
        Output:
            A tuple of:
                [0] the array of all numbers found (including complex numbers) in the arguments as complex numbers
                
                [1] the array of all chars found in the arguments
    """
    numbers = []
    chars = []
    for val in args:
        try:
            numbers.append(complex(val))
        except ValueError:
            pass

        if len(val) == 1:
            chars.append(val)

    
    return numbers, chars

test1 = [
    'a',
    'b',
    'c',
    'ab',
    '16',
    '25',
    '4',
    '1.32',
    '.5',
    '-8.3',
    '4.62.1',
    '54e-7',
]
#Output of test1:
#The Test with the input: ['a', 'b', 'c', 'ab', '16', '25', '4', '1.32', '.5', '-8.3', '4.62.1', '54e-7'] returned:
#numbers=[(16+0j), (25+0j), (4+0j), (1.32+0j), (0.5+0j), (-8.3+0j), (5.4e-06+0j)]
#chars=['a', 'b', 'c', '4']

test2 = [
    '1',
    '0',
    '-4',
    '123456789789745451212487845154.24689784546587456456',
    'aaaaaaaa',
    'kkj',
    'x'
]
#output of test2:
#The Test with the input: ['1', '0', '-4', '123456789789745451212487845154.24689784546587456456', 'aaaaaaaa', 'kkj', 'x'] returned:
#numbers=[(1+0j), 0j, (-4+0j), (1.2345678978974545e+29+0j)]
#chars=['1', '0', 'x']

test3 = [
    '5+7j',
    'a',
    'pi',
    '7.2-35.0004j',
    '9',
    '270e+3',
    '5.34e-5-24.5e+27j',
]
#output of test3:
#The Test with the input: ['5+7j', 'a', 'pi', '7.2-35.0004j', '9', '270e+3', '5.34e-5-24.5e+27j'] returned:
#numbers=[(5+7j), (7.2-35.0004j), (9+0j), (270000+0j), (5.34e-05-2.45e+28j)]
#chars=['a', '9']

currentTest = test1
numbers, chars = inputSplitter(*currentTest)
print(f"The Test with the input: {currentTest} returned:\n{numbers=}\n{chars=}")