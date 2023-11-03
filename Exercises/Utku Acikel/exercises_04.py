commands = [3,225,1,225,6,6,1100,1,238,225,104,0,1101,40,71,224,1001,224,-111,224,4,224,1002,223,8,223,101,7,224,224,1,224,223,
            223,1102,66,6,225,1102,22,54,225,1,65,35,224,1001,224,-86,224,4,224,102,8,223,223,101,6,224,224,1,224,223,223,1102,20,
            80,225,101,92,148,224,101,-162,224,224,4,224,1002,223,8,223,101,5,224,224,1,224,223,223,1102,63,60,225,1101,32,48,225,
            2,173,95,224,1001,224,-448,224,4,224,102,8,223,223,1001,224,4,224,1,224,223,223,1001,91,16,224,101,-79,224,224,4,224,1002,
            223,8,223,101,3,224,224,1,224,223,223,1101,13,29,225,1101,71,70,225,1002,39,56,224,1001,224,-1232,224,4,224,102,8,223,
            223,101,4,224,224,1,223,224,223,1101,14,59,225,102,38,143,224,1001,224,-494,224,4,224,102,8,223,223,101,3,224,224,1,
            224,223,223,1102,30,28,224,1001,224,-840,224,4,224,1002,223,8,223,101,4,224,224,1,223,224,223,4,223,99,0,0,0,677,0,0,
            0,0,0,0,0,0,0,0,0,1105,0,99999,1105,227,247,1105,1,99999,1005,227,99999,1005,0,256,1105,1,99999,1106,227,99999,1106,0,
            265,1105,1,99999,1006,0,99999,1006,227,274,1105,1,99999,1105,1,280,1105,1,99999,1,225,225,225,1101,294,0,0,105,1,0,
            1105,1,99999,1106,0,300,1105,1,99999,1,225,225,225,1101,314,0,0,106,0,0,1105,1,99999,107,677,226,224,1002,223,2,223,
            1005,224,329,1001,223,1,223,8,226,226,224,102,2,223,223,1006,224,344,101,1,223,223,7,226,677,224,1002,223,2,223,1005,
            224,359,101,1,223,223,1007,677,226,224,1002,223,2,223,1005,224,374,1001,223,1,223,1007,677,677,224,1002,223,2,223,
            1006,224,389,101,1,223,223,1008,226,226,224,1002,223,2,223,1005,224,404,1001,223,1,223,108,677,226,224,1002,223,2,
            223,1006,224,419,1001,223,1,223,1108,677,226,224,102,2,223,223,1006,224,434,1001,223,1,223,108,226,226,224,1002,223,
            2,223,1005,224,449,101,1,223,223,7,677,677,224,1002,223,2,223,1006,224,464,1001,223,1,223,8,226,677,224,1002,223,2,
            223,1005,224,479,1001,223,1,223,107,226,226,224,102,2,223,223,1006,224,494,101,1,223,223,1007,226,226,224,1002,223,
            2,223,1005,224,509,1001,223,1,223,1107,226,677,224,102,2,223,223,1005,224,524,1001,223,1,223,108,677,677,224,1002,
            223,2,223,1005,224,539,101,1,223,223,1107,677,226,224,102,2,223,223,1005,224,554,1001,223,1,223,107,677,677,224,
            1002,223,2,223,1005,224,569,101,1,223,223,8,677,226,224,102,2,223,223,1005,224,584,1001,223,1,223,7,677,226,224,102,
            2,223,223,1006,224,599,101,1,223,223,1008,677,677,224,1002,223,2,223,1005,224,614,101,1,223,223,1008,677,226,224,102,
            2,223,223,1006,224,629,1001,223,1,223,1108,677,677,224,102,2,223,223,1006,224,644,101,1,223,223,1108,226,677,224,1002,
            223,2,223,1005,224,659,1001,223,1,223,1107,226,226,224,102,2,223,223,1006,224,674,1001,223,1,223,4,223,99,226]
 
 
    
def get_value(storage, index, mode):
    return storage[index] if mode else storage[storage[index]]

"""
def get_value:

This function returns if the mode is in immediate or position mode, so if the mode is 1
(1 means the true), it returns "storage[index"]" and if its false it returns "storage[storage[index]]"
"""

def addition(storage, index, modes):
    param1 = get_value(storage, index+1, modes[0])
    param2 = get_value(storage, index+2, modes[1])
    storage[storage[index+3]] = param1 + param2
    return index + 4
    
    
def multiply(storage, index, modes):
    param1 = get_value(storage, index+1, modes[0])
    param2 = get_value(storage, index+2, modes[1])
    storage[storage[index+3]] = param1 * param2
    return index + 4
    
def read_and_save(storage, index, _):
    try:
        storage[storage[index+1]] = int(input("Enter a number: "))
    except:
        print("Error, given input is not a number")
    return index + 2

def output_value(storage, index, modes):
    output_value = get_value(storage, index+1, modes[0])
    print(output_value)
    return index + 2
    
def jump_if_true(storage, index, modes):
    if get_value(storage, index+1, modes[0]) != 0:
        return get_value(storage, index+2, modes[1])
    else:
        return index + 3

def jump_if_false(storage, index, modes):
    if get_value(storage, index+1, modes[0]) == 0:
        return get_value(storage, index+2, modes[1])
    else:
        return index + 3

def less_than(storage, index, modes):
    param1 = get_value(storage, index+1, modes[0])
    param2 = get_value(storage, index+2, modes[1])
    storage[storage[index+3]] = 1 if param1 < param2 else 0
    return index + 4

def equals(storage, index, modes):
    param1 = get_value(storage, index+1, modes[0])
    param2 = get_value(storage, index+2, modes[1])
    storage[storage[index+3]] = 1 if param1 == param2 else 0
    return index + 4

def halt(*args):
    print("Number 99 occured, halting the program")
    return None  # Exits main loop

opcode_dict = {
    1: addition,
    2: multiply,
    3: read_and_save,
    4: output_value,
    5: jump_if_true,
    6: jump_if_false,
    7: less_than,
    8: equals,
    99: halt 
}

"""
opcode_dict is a dictionary where each value is a function and can be called like used under this

That means when the current index number is 8, the opcode_dict will use that to call the equals function,
then it will be used with the given arguments: storage, index and modes
"""

def sim_computer(storage):
    index = 0
    while index is not None:
        instruction = storage[index]
        opcode = instruction % 100
        modes = [(instruction // 100) % 10, (instruction // 1000) % 10, (instruction // 10000) % 10]
        index = opcode_dict[opcode](storage, index, modes)

"""
def sim_computer(storage):

initializing index to 0

Using a while loop to continue as long index is not none, index will get set to none as soon as the halt
function gets called (When number 99 appears)

instruction = storage[index]: setting the instruction to the current element in the list "storage"

opcode = instruction % 100: using modulus operator to get the remainder by dividing instruction by 100
for example when the instruction is at 1105, the remainder will be 05. This is done since the 2 right-most
digits is the actual opcode

modes = (instruction // 100) % 10, and the other ones are used to specify what parameter mode it has,
so dividing by //100 (// returning largest operator) would show first parameter, second division by 1000
would give the second parameter and the division by 10000 would give the third parameter mode.

index = opcode_dict[opcode](storage, index, modes), basically to call a function from the opcode_dict,
while having 3 arguments, storage, index and modes. Storage being the list, index the current position and modes
for the current parameter mode its in
"""

# Running through commands
sim_computer(commands)
