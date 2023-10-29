# Extend the simulated computer from the second week:
# You will need to support a number of additional opcodes:
# - 3: read a single integer as input and save it to the position given
#      by its only parameter. the command 3,19 would read an input
#      and store the result at address 19
# - 4: output the value of the single parameter for this opcode.
#      for example 4,19 would output the value stored at address 19
# - 5: jump-if-true: if the first parameter is non-zero, it sets the instruction pointer to the value from the second parameter. Otherwise, it does nothing.
#      Self made example: 1, 3 sets the instruction pointer to 3 | 0, 3 does nothing
# - 6: jump-if-false: if the first parameter is zero, it sets the instruction pointer to the value from the second parameter. Otherwise, it does nothing.
#      Self made example: 0, 3 sets the instruction pointer to 3 | 1, 3 does nothing
# - 7: less than: if the first parameter is less than the second parameter, it stores 1 in the position given by the third parameter. Otherwise, it stores 0.
#      Self made example: 1, 3 stores 1 in the position given by the third parameter | 3, 1 stores 0 in the position given by the third paramter
# - 8: equals: if the first parameter is equal to the second parameter, it stores 1 in the position given by the third parameter. Otherwise, it stores 0.
#      Self made example: 3, 3 stores 1 in the position given by the third parameter | 1, 3 stores 0 in the position given by the third paramter
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

def execute():
    """Main method of the mini computer. Reads in the commands, takes the values from the command array and calls the opcodes.

        First, this method gets the command that is located at the location of the instruction pointer. This command has already been split up into the read modes and the opcode (see split_command())
        Than it takes the values and arrays that are needed for the specific opcode of the command.
        At last it calls the operation that matches the opcode.
        This method is in an endless loop since the only way to halt the computer is to execute opcode 99 (sadly not 66)
    """

    global instruction_pointer
    while True:
        splitted_command = split_command()
        instruction_pointer += 1
        operation = splitted_command[2]

        #initialize variables to prevent UnboundLocalError when calling an operation with these values.
        read_value = None
        read_value_1 = None
        read_value_2 = None
        write_location = None

        #stores the values at the locations for simplicity of the further code. Not possible for write_location since the location is actually needed there
        if operation in [1, 2, 7, 8]:
            read_value_1 = commands[get_location(splitted_command[0])]
            read_value_2 = commands[get_location(splitted_command[1])]
            write_location = get_location()
        elif operation == 3:
            write_location = get_location()
        elif operation == 4:
            read_value = commands[get_location(splitted_command[0])]
        elif operation in [5, 6]:
            read_value_1 = commands[get_location(splitted_command[0])]
            read_value_2 = commands[get_location(splitted_command[1])]
        
        #has every argument thats needed by at least one of the operations. the operations throw unnecessary arguments away by using *__
        operation_dictionary[operation](read_value = read_value, read_value_1 = read_value_1, read_value_2 = read_value_2, write_location = write_location)

def split_command():
    """Splits the given command.

        Expects a four digit long command and splits it into the read modes for location one and two and the operation code, which is two digits long.
        if the command is shorter than four digits it is filled up with zeros. All values are converted to integers so if the opcode is 02 it will return 2.

        Example
        -------
        The command 1002 is split up into the read mode locations and the opcode. The result is:
        read_mode_location_1 = 1
        read_mode_location_2 = 0
        opcode = 2
    """

    command_str = str(commands[instruction_pointer])
    len_command = len(command_str)
    
    if len_command > 1:
        opcode = command_str[len_command-2] + command_str[len_command-1]
    #required because the command could be one digit long
    else:
        opcode = command_str[0]

    match len_command:
        case 4:
            read_mode_location_1 = command_str[len_command-3]
            read_mode_location_2 = command_str[len_command-4]
        case 3:
            read_mode_location_1 = command_str[len_command-3]
            read_mode_location_2 = 0
        case 2:
            read_mode_location_1 = 0
            read_mode_location_2 = 0
        case 1:
            read_mode_location_1 = 0
            read_mode_location_2 = 0

    return [int(read_mode_location_1), int(read_mode_location_2), int(opcode)]


def get_location(read_mode = 0):
    """returns the location of a value in the command array.

        This function is used to differentiate between the position mode and the immediate mode by converting both of them to the actual position the sought value is stored at.

    """
    global instruction_pointer
    match read_mode:
        case 0:
            location = commands[instruction_pointer]
        case 1:
            location = instruction_pointer
        case _:
            raise Exception("number does not match read mode")
    instruction_pointer += 1
    return location

def operation_add(read_value_1, read_value_2, write_location, **_):
    commands[write_location] = read_value_1 + read_value_2

def operation_multiply(read_value_1, read_value_2, write_location, **_):
    commands[write_location] = read_value_1 * read_value_2

def operation_read_integer(write_location, **_):
    user_input = input("Please enter a number: ")
    try:
        commands[write_location] = int(user_input)
    except ValueError:
        print("You have to input something that can be converted into an integer")
        operation_read_integer(write_location)

def operation_output_integer(read_value, **_):
    print(read_value)

def operation_jmp_if_true(read_value_1, read_value_2, **_):
    global instruction_pointer
    if read_value_1 != 0:
        instruction_pointer = read_value_2

def operation_jmp_if_false(read_value_1, read_value_2, **_):
    global instruction_pointer
    if read_value_1 == 0:
        instruction_pointer = read_value_2

def operation_less_than(read_value_1, read_value_2, write_location, **_):
    if read_value_1 < read_value_2:
        commands[write_location] = 1
    else:
        commands[write_location] = 0

def operation_equals(read_value_1, read_value_2, write_location, **_):
    if read_value_1 == read_value_2:
        commands[write_location] = 1
    else:
        commands[write_location] = 0

def operation_halt(**_):
    exit(0)
    
operation_dictionary = {
    1: operation_add,
    2: operation_multiply,
    3: operation_read_integer,
    4: operation_output_integer,
    5: operation_jmp_if_true,
    6: operation_jmp_if_false,
    7: operation_less_than,
    8: operation_equals,
    99: operation_halt
}

instruction_pointer = 0
commands = [3,225,1,225,6,6,1100,1,238,225,104,0,1101,40,71,224,1001,224,-111,224,4,224,1002,223,8,223,101,7,224,224,1,224,223,223,1102,66,6,225,1102,22,54,225,1,65,35,224,1001,224,-86,224,4,224,102,8,223,223,101,6,224,224,1,224,223,223,1102,20,80,225,101,92,148,224,101,-162,224,224,4,224,1002,223,8,223,101,5,224,224,1,224,223,223,1102,63,60,225,1101,32,48,225,2,173,95,224,1001,224,-448,224,4,224,102,8,223,223,1001,224,4,224,1,224,223,223,1001,91,16,224,101,-79,224,224,4,224,1002,223,8,223,101,3,224,224,1,224,223,223,1101,13,29,225,1101,71,70,225,1002,39,56,224,1001,224,-1232,224,4,224,102,8,223,223,101,4,224,224,1,223,224,223,1101,14,59,225,102,38,143,224,1001,224,-494,224,4,224,102,8,223,223,101,3,224,224,1,224,223,223,1102,30,28,224,1001,224,-840,224,4,224,1002,223,8,223,101,4,224,224,1,223,224,223,4,223,99,0,0,0,677,0,0,0,0,0,0,0,0,0,0,0,1105,0,99999,1105,227,247,1105,1,99999,1005,227,99999,1005,0,256,1105,1,99999,1106,227,99999,1106,0,265,1105,1,99999,1006,0,99999,1006,227,274,1105,1,99999,1105,1,280,1105,1,99999,1,225,225,225,1101,294,0,0,105,1,0,1105,1,99999,1106,0,300,1105,1,99999,1,225,225,225,1101,314,0,0,106,0,0,1105,1,99999,107,677,226,224,1002,223,2,223,1005,224,329,1001,223,1,223,8,226,226,224,102,2,223,223,1006,224,344,101,1,223,223,7,226,677,224,1002,223,2,223,1005,224,359,101,1,223,223,1007,677,226,224,1002,223,2,223,1005,224,374,1001,223,1,223,1007,677,677,224,1002,223,2,223,1006,224,389,101,1,223,223,1008,226,226,224,1002,223,2,223,1005,224,404,1001,223,1,223,108,677,226,224,1002,223,2,223,1006,224,419,1001,223,1,223,1108,677,226,224,102,2,223,223,1006,224,434,1001,223,1,223,108,226,226,224,1002,223,2,223,1005,224,449,101,1,223,223,7,677,677,224,1002,223,2,223,1006,224,464,1001,223,1,223,8,226,677,224,1002,223,2,223,1005,224,479,1001,223,1,223,107,226,226,224,102,2,223,223,1006,224,494,101,1,223,223,1007,226,226,224,1002,223,2,223,1005,224,509,1001,223,1,223,1107,226,677,224,102,2,223,223,1005,224,524,1001,223,1,223,108,677,677,224,1002,223,2,223,1005,224,539,101,1,223,223,1107,677,226,224,102,2,223,223,1005,224,554,1001,223,1,223,107,677,677,224,1002,223,2,223,1005,224,569,101,1,223,223,8,677,226,224,102,2,223,223,1005,224,584,1001,223,1,223,7,677,226,224,102,2,223,223,1006,224,599,101,1,223,223,1008,677,677,224,1002,223,2,223,1005,224,614,101,1,223,223,1008,677,226,224,102,2,223,223,1006,224,629,1001,223,1,223,1108,677,677,224,102,2,223,223,1006,224,644,101,1,223,223,1108,226,677,224,1002,223,2,223,1005,224,659,1001,223,1,223,1107,226,226,224,102,2,223,223,1006,224,674,1001,223,1,223,4,223,99,226]
execute()
