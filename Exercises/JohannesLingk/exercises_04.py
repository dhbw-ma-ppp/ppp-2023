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



###########################################
# Write a function that takes an arbitrary number of unnamed arguments
# All inputs will be of type string.
# the function should return two lists:
#   The first list should contain all arguments which can be interpreted
#   as a number.
#   The second list should contain all strings which contain just one character.
# Think of some good inputs to test this functionality, write down at least three
# examples and verify that the output for these examples is correct.



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
commands = [3,225,1,225,6,6,1100,1,238,225,104,0,1101,40,71,224,1001,224,-111,224,4,224,1002,223,8,223,101,7,224,224,1,224,223,223,1102,66,6,225,1102,22,54,225,1,65,35,224,1001,224,-86,224,4,224,102,8,223,223,101,6,224,224,1,224,223,223,1102,20,80,225,101,92,148,224,101,-162,224,224,4,224,1002,223,8,223,101,5,224,224,1,224,223,223,1102,63,60,225,1101,32,48,225,2,173,95,224,1001,224,-448,224,4,224,102,8,223,223,1001,224,4,224,1,224,223,223,1001,91,16,224,101,-79,224,224,4,224,1002,223,8,223,101,3,224,224,1,224,223,223,1101,13,29,225,1101,71,70,225,1002,39,56,224,1001,224,-1232,224,4,224,102,8,223,223,101,4,224,224,1,223,224,223,1101,14,59,225,102,38,143,224,1001,224,-494,224,4,224,102,8,223,223,101,3,224,224,1,224,223,223,1102,30,28,224,1001,224,-840,224,4,224,1002,223,8,223,101,4,224,224,1,223,224,223,4,223,99,0,0,0,677,0,0,0,0,0,0,0,0,0,0,0,1105,0,99999,1105,227,247,1105,1,99999,1005,227,99999,1005,0,256,1105,1,99999,1106,227,99999,1106,0,265,1105,1,99999,1006,0,99999,1006,227,274,1105,1,99999,1105,1,280,1105,1,99999,1,225,225,225,1101,294,0,0,105,1,0,1105,1,99999,1106,0,300,1105,1,99999,1,225,225,225,1101,314,0,0,106,0,0,1105,1,99999,107,677,226,224,1002,223,2,223,1005,224,329,1001,223,1,223,8,226,226,224,102,2,223,223,1006,224,344,101,1,223,223,7,226,677,224,1002,223,2,223,1005,224,359,101,1,223,223,1007,677,226,224,1002,223,2,223,1005,224,374,1001,223,1,223,1007,677,677,224,1002,223,2,223,1006,224,389,101,1,223,223,1008,226,226,224,1002,223,2,223,1005,224,404,1001,223,1,223,108,677,226,224,1002,223,2,223,1006,224,419,1001,223,1,223,1108,677,226,224,102,2,223,223,1006,224,434,1001,223,1,223,108,226,226,224,1002,223,2,223,1005,224,449,101,1,223,223,7,677,677,224,1002,223,2,223,1006,224,464,1001,223,1,223,8,226,677,224,1002,223,2,223,1005,224,479,1001,223,1,223,107,226,226,224,102,2,223,223,1006,224,494,101,1,223,223,1007,226,226,224,1002,223,2,223,1005,224,509,1001,223,1,223,1107,226,677,224,102,2,223,223,1005,224,524,1001,223,1,223,108,677,677,224,1002,223,2,223,1005,224,539,101,1,223,223,1107,677,226,224,102,2,223,223,1005,224,554,1001,223,1,223,107,677,677,224,1002,223,2,223,1005,224,569,101,1,223,223,8,677,226,224,102,2,223,223,1005,224,584,1001,223,1,223,7,677,226,224,102,2,223,223,1006,224,599,101,1,223,223,1008,677,677,224,1002,223,2,223,1005,224,614,101,1,223,223,1008,677,226,224,102,2,223,223,1006,224,629,1001,223,1,223,1108,677,677,224,102,2,223,223,1006,224,644,101,1,223,223,1108,226,677,224,1002,223,2,223,1005,224,659,1001,223,1,223,1107,226,226,224,102,2,223,223,1006,224,674,1001,223,1,223,4,223,99,226]


class State:
    """
    State is passed to the command methods and contains 
    information about the current state of execution like:
        - Commands
        - Head (or Pointer) of execution
        - Mode information for current command
    """
    def __init__(self, commands: list[int], head: int, modes: str) -> None:
        self.commands = commands
        self.head = head
        self.modes = modes

    def _get_mode(self, index: int) -> int:
        return int(self.modes[index]) if len(self.modes) > index else 0
    
    def get_value(self, index: int) -> int:
        """
        For immediate mode: Return value in parameter
        for position mode: Return value at memory address from parameter
        """
        mode = self._get_mode(index)
        if mode == 1: # immediate mode
            return self.commands[self.head + index + 1]
        elif mode == 0: # position mode
            return self.commands[self.commands[self.head + index + 1]]
        
    def get_pointer(self, index: int) -> int:
        """
        Returns the value in paramenter.
        Mostly used for write operation.
        """
        return self.commands[self.head + index + 1]
        
    def write_memory(self, position: int, value: int):
        """
        Writes a value into memory position.
        """
        self.commands[position] = value


def command_addition(state: State) -> int: # code 1
    number1 = state.get_value(0)
    number2 = state.get_value(1)
    state.write_memory(state.get_pointer(2), number1 + number2)
    return state.head + 4

def command_multiplication(state: State) -> int: # code 2
    number1 = state.get_value(0)
    number2 = state.get_value(1)
    state.write_memory(state.get_pointer(2), number1 * number2)
    return state.head + 4

def command_stop(state: State) -> int: # code 99
    return len(state.commands)

def command_input(state: State) -> int: # code 3
    number = int(input("input digit: "))
    state.write_memory(state.get_pointer(0), number)
    return state.head + 2

def command_output(state: State) -> int: # code 4
    print(state.get_value(0))
    return state.head + 2

def command_jump_if_true(state: State) -> int: # code 5
    condition = state.get_value(0)
    jump_pos = state.get_value(1)
    if condition != 0:
        return jump_pos
    else:
        return state.head + 3

def command_jump_if_false(state: State) -> int: # code 6
    condition = state.get_value(0)
    jump_pos = state.get_value(1)
    if condition == 0:
        return jump_pos
    else:
        return state.head + 3

def command_less_than(state: State) -> int: # code 7
    number1 = state.get_value(0)
    number2 = state.get_value(1)
    result = 1 if number1 < number2 else 0
    state.write_memory(state.get_pointer(2), result)
    return state.head + 4

def command_equals(state: State) -> int: # code 8
    number1 = state.get_value(0)
    number2 = state.get_value(1)
    result = 1 if number1 == number2 else 0
    state.write_memory(state.get_pointer(2), result)
    return state.head + 4

"""
This matches every known op_code to an implemented method
"""
op_codes = {
    1: command_addition,
    2: command_multiplication,
    3: command_input,
    4: command_output,
    5: command_jump_if_true,
    6: command_jump_if_false,
    7: command_less_than,
    8: command_equals,
    99: command_stop,
}

"""
Main execution loop.
Runs as long as head is within command bounds.
For every command read, calls appropriate method and passes State object.
"""
def run(commands: list[int]):
    head = 0
    while head < len(commands):
        command = str(commands[head])
        # Split command into op_code and mode string
        operation = int(command[-2:])
        modes = command[-3::-1]
        if operation not in op_codes.keys():
            raise Exception(f'No operation code: {operation}')
        head = op_codes[operation](State(commands, head, modes))
    
    print("Done!")
    

run(commands)
# For input "5" returns 16694270