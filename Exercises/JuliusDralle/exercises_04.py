# Extend the simulated computer from the second week:
# You will need to support a number of additional opcodes:
# - 3: read a single integer as input and save it to the position given
#      by its only parameter. the command 3,19 would read an input
#      and store the result at address 19
# - 4: output the value of the single parameter for this opcode.
#      for example 4,19 would output the value stored at address 19
# - 5: jump-if-true: if the first parameter is non-zero, it sets the instruction pointer to the value from the second parameter. Otherwise, it does nothing.
# - 6: jump-if-false: if the first parameter is zero, it sets the instruction pointer to the value from the second parameter. Otherwise, it does nothing.
# - 7: less than: if the first parameter is less than the second parameter, it stores 1 in the position given by the third parameter. Otherwise, it stores 0.
# - 8: equals: if the first parameter is equal to the second parameter, it stores 1 in the position given by the third parameter. Otherwise, it stores 0.
#
# caution: since these opcodes expect a variable number of parameters the instruction pointer after executing an instruction should no longer always
# increase by four. Instead, it should increase  according to the number of parameters that instruction expects.
# caution: numbers in your storage, as well as inputs can be negative!
# If, however, the opcode directly manipulates the instruction pointer (5 and 6) there should be no additional modification of the instruction pointer.
# The next instruction to execute is stored directly at the location indicated by the parameter to these opcodes.
#
# Additionally, you need to support two different parameter modes: position mode (mode 0), and immediate mode (mode 1).
# Position mode: Opcode arguments are memory addresses. If an argument has the value 18 you fetch the 'calculation value'
#   from the memory at address 18. This is the mode you already know from last time.
# Immediate mode: In immediate mode a parameter is directly interpreted as a value. If the first argument to the 'sum' opcode is 8
#   then the first summand in your calculation is 8.
#
# Parameter modes are specified per-parameter as part of the opcode by extending the opcodes.
# When reading a number that specifies an opcode
#   - the two right-most digits contain the actual opcode
#   - any further digits contain the parameter mode of the parameters, reading digits from right-to-left
#     and parameters in-order from left to right. Any unspecified digits default to 0 (position mode).
#     NOTE: parameters for the target address of a write operation (e.g. the third parameter of the 'sum' or 'multiply' opcode)
#           are never given in immediate mode.
#
# Here's an example:
#   consider the sequence of instructions `1002,4,3,4,33`.
#   The two right-most digits of the first entry ('02') indicate the opcode: multiplication
#   Then, from right to left the next digit is '0', indicating that the first parameter is in position mode.
#   The next digit is '1' indicating the second parameter is in immediate mode.
#   The next digit is not present, defaulting to '0' so the third parameter is again in position mode.
#   No further parameter modes need to be determined as the multiply instruction accepts 3 parameters.
#   Reading the first parameter in position mode is the value at address '4' -- 33.
#   Reading the second parameter in immediate mode is the value '3'.
#   Executing the multiplication instruction gives us the result 33*3=99
#   The third parameter (4) in position mode assigns this value to the memory in location 4 (the location that used
#   to have value 33 is now 99).
#   Now moving the instruction pointer forward brings us to position 4 with opcode 99, halting the program.
#
# And here's some test cases:
#   3,9,8,9,10,9,4,9,99,-1,8 -- test whether the input is equal to 8 (using position mode)
#   3,3,1107,-1,8,3,4,3,99 -- test whether the input is less than 8 (using immediate mode)
#   3,3,1105,-1,9,1101,0,0,12,4,12,99,1 -- test whether the input is 0 using jump instructions
#
# Finally, run you code for the following instructions; when asked for input provide the number '5'. The program should print a single number when executed.
# Please take note of that number in your PR, so I don't need to run all the files myself :)
commands = [3, 225, 1, 225, 6, 6, 1100, 1, 238, 225, 104, 0, 1101, 40, 71, 224, 1001, 224, -111, 224, 4, 224, 1002, 223, 8, 223, 101, 7, 224, 224, 1, 224, 223, 223, 1102, 66, 6, 225, 1102, 22, 54, 225, 1, 65, 35, 224, 1001, 224, -86, 224, 4, 224, 102, 8, 223, 223, 101, 6, 224, 224, 1, 224, 223, 223, 1102, 20, 80, 225, 101, 92, 148, 224, 101, -162, 224, 224, 4, 224, 1002, 223, 8, 223, 101, 5, 224, 224, 1, 224, 223, 223, 1102, 63, 60, 225, 1101, 32, 48, 225, 2, 173, 95, 224, 1001, 224, -448, 224, 4, 224, 102, 8, 223, 223, 1001, 224, 4, 224, 1, 224, 223, 223, 1001, 91, 16, 224, 101, -79, 224, 224, 4, 224, 1002, 223, 8, 223, 101, 3, 224, 224, 1, 224, 223, 223, 1101, 13, 29, 225, 1101, 71, 70, 225, 1002, 39, 56, 224, 1001, 224, -1232, 224, 4, 224, 102, 8, 223, 223, 101, 4, 224, 224, 1, 223, 224, 223, 1101, 14, 59, 225, 102, 38, 143, 224, 1001, 224, -494, 224, 4, 224, 102, 8, 223, 223, 101, 3, 224, 224, 1, 224, 223, 223, 1102, 30, 28, 224, 1001, 224, -840, 224, 4, 224, 1002, 223, 8, 223, 101, 4, 224, 224, 1, 223, 224, 223, 4, 223, 99, 0, 0, 0, 677, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1105, 0, 99999, 1105, 227, 247, 1105, 1, 99999, 1005, 227, 99999, 1005, 0, 256, 1105, 1, 99999, 1106, 227, 99999, 1106, 0, 265, 1105, 1, 99999, 1006, 0, 99999, 1006, 227, 274, 1105, 1, 99999, 1105, 1, 280, 1105, 1, 99999, 1, 225, 225, 225, 1101, 294, 0, 0, 105, 1, 0, 1105, 1, 99999, 1106, 0, 300, 1105, 1, 99999, 1, 225, 225, 225, 1101, 314, 0, 0, 106, 0, 0, 1105, 1, 99999, 107, 677, 226, 224, 1002, 223, 2, 223, 1005, 224, 329, 1001, 223, 1, 223, 8, 226, 226, 224, 102, 2, 223, 223, 1006, 224, 344, 101, 1, 223, 223, 7, 226, 677, 224, 1002, 223, 2, 223, 1005, 224, 359, 101, 1, 223, 223, 1007, 677, 226, 224, 1002, 223, 2, 223, 1005, 224, 374, 1001, 223, 1, 223, 1007, 677, 677, 224, 1002, 223, 2, 223, 1006, 224, 389, 101, 1, 223, 223, 1008, 226, 226, 224, 1002, 223, 2, 223, 1005, 224, 404, 1001, 223, 1, 223, 108, 677, 226, 224, 1002, 223, 2, 223, 1006, 224, 419, 1001, 223, 1, 223, 1108, 677, 226, 224, 102, 2, 223, 223, 1006, 224, 434, 1001, 223, 1, 223, 108, 226, 226, 224, 1002, 223, 2, 223, 1005, 224, 449, 101, 1, 223, 223, 7, 677, 677, 224, 1002, 223, 2, 223, 1006, 224, 464, 1001, 223, 1, 223, 8, 226, 677, 224, 1002, 223, 2, 223, 1005, 224, 479, 1001, 223, 1, 223, 107, 226, 226, 224, 102, 2, 223, 223, 1006, 224, 494, 101, 1, 223, 223, 1007, 226, 226, 224, 1002, 223, 2, 223, 1005, 224, 509, 1001, 223, 1, 223, 1107, 226, 677, 224, 102, 2, 223, 223, 1005, 224, 524, 1001, 223, 1, 223, 108, 677, 677, 224, 1002, 223, 2, 223, 1005, 224, 539, 101, 1, 223, 223, 1107, 677, 226, 224, 102, 2, 223, 223, 1005, 224, 554, 1001, 223, 1, 223, 107, 677, 677, 224, 1002, 223, 2, 223, 1005, 224, 569, 101, 1, 223, 223, 8, 677, 226, 224, 102, 2, 223, 223, 1005, 224, 584, 1001, 223, 1, 223, 7, 677, 226, 224, 102, 2, 223, 223, 1006, 224, 599, 101, 1, 223, 223, 1008, 677, 677, 224, 1002, 223, 2, 223, 1005, 224, 614, 101, 1, 223, 223, 1008, 677, 226, 224, 102, 2, 223, 223, 1006, 224, 629, 1001, 223, 1, 223, 1108, 677, 677, 224, 102, 2, 223, 223, 1006, 224, 644, 101, 1, 223, 223, 1108, 226, 677, 224, 1002, 223, 2, 223, 1005, 224, 659, 1001, 223, 1, 223, 1107, 226, 226, 224, 102, 2, 223, 223, 1006, 224, 674, 1001, 223, 1, 223, 4, 223, 99, 226]
running = True


def reveal_parameters_in_opcode(opcode):
    parameters_in_opcode = opcode // 100
    if parameters_in_opcode < 10:
         parameter_one = parameters_in_opcode
         parameter_two = 0
         parameter_three = 0
    elif parameters_in_opcode < 100:
         parameter_one = parameters_in_opcode % 10
         parameter_two = parameters_in_opcode // 10
         parameter_three = 0
    elif parameters_in_opcode < 1000:
         parameter_one = parameters_in_opcode % 10
         parameter_two = parameters_in_opcode % 100 // 10
         parameter_three = parameters_in_opcode // 100
    return parameter_one, parameter_two, parameter_three

def addition(opcode, index, commands):
    parametermode_one, parametermode_two, parametermode_three = reveal_parameters_in_opcode(opcode)
    num_arguments_needed = 3

    if parametermode_one:
         value_one = commands[index+1]
    else:
         value_one = int(commands[commands[index+1]])

    if parametermode_two:
         value_two = commands[index+2]
    else:
         value_two = int(commands[commands[index+2]])
         
    commands[commands[index+3]] = int(value_one + value_two)
    return 0, num_arguments_needed

def multiply(opcode, index, commands):
    try:
        parametermode_one, parametermode_two, parametermode_three = reveal_parameters_in_opcode(opcode)
        num_arguments_needed = 3

        if parametermode_one:
            value_one = commands[index+1]
        else:
            value_one = int(commands[commands[index+1]])

        if parametermode_two:
            value_two = commands[index+2]
        else:
            value_two = int(commands[commands[index+2]])
            
        commands[commands[index+3]] = value_one * value_two
    except KeyError:
        print("Key Error at Index: ", index)
    return 0, num_arguments_needed

def save_at(opcode, index, commands):
    num_arguments_needed = 1
    parametermode_one, parametermode_two, parametermode_three = reveal_parameters_in_opcode(opcode)
    
    parametermode_one = 0

    commands[commands[index+1]] = int(input("Input required: "))

    return 0, num_arguments_needed


def output(opcode, index, commands):
    num_arguments_needed = 1
    parametermode_one, parametermode_two, parametermode_three = reveal_parameters_in_opcode(opcode)
    if parametermode_one == 0:
        print(commands[commands[index+1]])
    
    elif parametermode_one == 1:
        print(commands[index+1])

    return 0, num_arguments_needed


# - 5: jump-if-true: if the first parameter is non-zero, it sets the instruction pointer to the value from the second parameter. Otherwise, it does nothing.
def jump_if_true(opcode, index, commands):
    num_arguments_needed = 2
    parametermode_one, parametermode_two, parametermode_three = reveal_parameters_in_opcode(opcode)

    isTrue = False
    if parametermode_one == 0:
        if commands[commands[index+1]] != 0:
            isTrue = True
        
    elif parametermode_one == 1:
        if commands[index+1] != 0:
            isTrue = True

    if isTrue:
        if parametermode_two == 0:
            newpointer = int(commands[commands[index + 2]])
        elif parametermode_two == 1:
            newpointer = int(commands[index + 2])
    elif isTrue == False:
        newpointer = index + num_arguments_needed + 1

    #return the newpointer because the runner sets the new pointer + 1, therefore the -1 is needed
    return 0, newpointer - index - 1


def jump_if_false(opcode, index, commands):
    num_arguments_needed = 2
    parametermode_one, parametermode_two, parametermode_three = reveal_parameters_in_opcode(opcode)

    isFalse = False
    if parametermode_one == 0:
        if commands[commands[index+1]] == 0:
            isFalse = True
        
    elif parametermode_one == 1:
        if commands[index+1] == 0:
            isFalse = True 

    if isFalse:
        if parametermode_two == 0:
            newpointer = int(commands[commands[index + 2]])
        elif parametermode_two == 1:
            newpointer = commands[index + 2]
    elif isFalse == False:
        newpointer = index + num_arguments_needed + 1

    #return the newpointer because the runner sets the new pointer + 1, therefore the -1 is needed
    return 0, newpointer - index - 1


def less_than(opcode, index, commands):
    num_arguments_needed = 3
    parametermode_one, parametermode_two, parametermode_three = reveal_parameters_in_opcode(opcode)

    if parametermode_one == 0:
        paramOne = int(commands[commands[index+1]])
    elif parametermode_one == 1:
        paramOne = commands[index+1]

    if parametermode_two == 0:
        paramTwo = int(commands[commands[index+2]])
    elif parametermode_two == 1:
        paramTwo = commands[index+2]
        
    paramThree = commands[index + 3]

    if paramOne < paramTwo:
        commands[paramThree] = 1
    else:
        commands[paramThree] = 0

    return 0, num_arguments_needed


def equals(opcode, index, commands):
    num_arguments_needed = 3
    parametermode_one, parametermode_two, parametermode_three = reveal_parameters_in_opcode(opcode)

    if parametermode_one == 0:
        paramOne = int(commands[commands[index+1]])
    elif parametermode_one == 1:
        paramOne = commands[index+1]

    if parametermode_two == 0:
        paramTwo = int(commands[commands[index+2]])
    elif parametermode_two == 1:
        paramTwo = commands[index+2]
        
    paramThree = commands[index + 3]

    if paramOne == paramTwo:
        commands[paramThree] = 1
    else:
        commands[paramThree] = 0

    return 0, num_arguments_needed

def halt(opcode, index, commands):
    global running
    print("halt")
    num_arguments_needed = 0
    parametermode_one, parametermode_two, parametermode_three = reveal_parameters_in_opcode(opcode)

    running = False 

    return 0, num_arguments_needed


opcode_dict = {
    1 : addition,
    2 : multiply,
    3 : save_at,
    4 : output,
    5 : jump_if_true,
    6 : jump_if_false,
    7 : less_than,
    8 : equals,
    99: halt
}

opcode_args_num = {
    addition: 3,
    multiply: 3,
    save_at : 1,                  # save_at
    output : 1,                  # output
    jump_if_true : 2,                  # jump_if_true
    jump_if_false : 2,                  # jump_if_false
    less_than : 3,                  # less_than
    equals : 3                   # equals
}

def read_opcode(opcodenumber):
    correct_operation = halt
    if opcodenumber <= 9:
        try:
            correct_operation = opcode_dict[opcodenumber]
            #print(f"Der Opcode verweist auf folgende Funktion: {correct_operation}")
        except KeyError:
            print(f"Falscher Key wurde entdeckt mit der Abfrage des Opcodes in {opcodenumber}")
    else:
        opcode_operationkey = int(opcodenumber % 100)
        correct_operation = opcode_dict[opcode_operationkey]
    return correct_operation

def runner(commands):
    pointer = 0
    while pointer < len(commands) and running == True:

        correct_operation = read_opcode(commands[pointer])
        
        outputvalue, new_pointer = correct_operation(commands[pointer], pointer ,commands)
        pointer += new_pointer + 1
        #print(outputvalue, pointer)

#runner(commands)

#testcommand = [1,2,2,3]
#addition(1,0,testcommand)
#print(testcommand)
# Result is: [1, 2, 2, 4]

runner(commands)
#print(commands)