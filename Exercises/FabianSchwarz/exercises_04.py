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



def split_digits(n:int, base=10):
    """Generator to split number into digits

    Parameters:
    --------------
    n(int):                             integer to split into digits
    base(int)=10                        base to split integer to

    Return Values:
    --------------
    list/set/tuple of digits

    #! the digits this returns are in descending order !
    """
    if n == 0:
        yield 0
    while n:
        n, d = divmod(n, base)
        yield d



class processor:
    """
    Class for the 'processor' / turing machine
    """

    def __init__(self, memory:list):
        self.__memory = memory#store the memory

    def write_data(self,tasks:list):
        """
        Write tuples of both data and destination to the computer's memory

        Parameters:
        --------------
        tasks(list of tuples of ints):      list of tuples of ints that provide both data and adress (DATA,ADRESS_INDEX)

        Return Values:
        --------------
        None
        """
        for task_tuple in tasks:
            try:
                self.__memory[task_tuple[1]] = task_tuple[0]
            except IndexError:
                print(f"Your code ran into an unexpected Issue: WriteError, Write Instruction: {tasks}")
                return None


    def read_data(self,tasks:list):
        """
        Read data at indexes given by the input list

        Parameters:
        --------------
        tasks(list of ints):                list of ints that indicate indexes which should be read

        Return Values:
        --------------
        data_list(list):                    list of requested values
        """
        data_list = []
        for indexes in tasks:
            try:
                data_list.append(self.__memory[indexes])
            except IndexError:
                print(f"Your code ran into an unexpected Issue: ReadError, Read Instruction: {indexes}")
                return None
        
        return data_list


    def opcode_add(self, current_position:int ,param1_idx:int, param2_idx: int, destination_idx: int):
        """
        Add two values (given by index) and write the result to a given target index(via the write function)

        Parameters:
        --------------
        current_position(int):              current position in memory
        param1_idx(int):                    index where the first value can be found
        param2_idx(int):                    index where the second value can be found
        destination_idx(int):               index where the result should be written to

        Return Values:
        --------------
        current_positon(int):               new current position for the computer 
        """
        values = self.read_data([param1_idx, param2_idx])
        value_1 = values[0]
        value_2 = values[1]
        self.write_data([(value_1+value_2,destination_idx)])#write data
        return current_position + 4 


    def opcode_multiply(self, current_position:int,param1_idx:int, param2_idx: int, destination_idx:int):
        """
        Multiply two values (given by index) and write the result to a given target index(via the write function)

        Parameters:
        --------------
        current_position(int):              current position in memory
        param1_idx(int):                    index where the first value can be found
        param2_idx(int):                    index where the second value can be found
        destination_idx(int):               index where the result should be written to

        Return Values:
        --------------
        current_positon(int):               new current position for the computer 
        """
        values = self.read_data([param1_idx, param2_idx])
        value_1 = values[0]
        value_2 = values[1]
        self.write_data([(value_1*value_2,destination_idx)])#write data
        return current_position + 4


    def opcode_get_input(self, current_position:int, destination_idx:int):
        """
        Read value and save it to index given(via the write function)

        Parameters:
        --------------
        current_position(int):              current position in memory
        destination_idx(int):               index where the data should be written to

        Return Values:
        --------------
        current_positon(int):               new current position for the computer 
        """
        usr_input = input("Input: ")
        digit_set = {'0','1','2','3','4','5','6','7','8','9'}
        for chars in usr_input:
            if chars not in digit_set:
                print("Input invalid")
        self.write_data([(int(usr_input),destination_idx)])
        return current_position + 2


    def opcode_output(self, current_position:int, requested_idx:int):
        """
        Read value(given by index) and write it to the standard output

        Parameters:
        --------------
        current_position(int):              current position in memory
        requested_idx(int):                 idx of data that should be read
        
        Return Values:
        --------------
        current_positon(int):               new current position for the computer 
        """
        print(int(self.read_data([requested_idx])[0]))
        return current_position + 2


    def opcode_jump_if_true(self, current_position:int ,bool_idx:int, destination_idx:int):
        """
        Check if the first parameter is 0, if no, jump to instruction indicated by the second index

        Parameters:
        --------------
        current_position(int):              current position in memory
        bool_idx(int):                      index where the number that should be evaluated is located
        destination_idx(int):               index where the data should be written to

        Return Values:
        --------------
        current_positon(int):               new current position for the computer 
        """
        bool_value = self.read_data([bool_idx])[0]
        if bool_value != 0:
            return self.read_data([destination_idx])[0]
        else:
            return current_position + 3


    def opcode_jump_if_false(self, current_position:int ,bool_idx:int, destination_idx:int):
        """
        Check if the first parameter is 0, if yes, jump to instruction indicated by the second index

        Parameters:
        --------------
        current_position(int):              current position in memory
        bool_idx(int):                      index where the number that should be evaluated is located
        destination_idx(int):               index where the data should be written to

        Return Values:
        --------------
        current_positon(int):               new current position for the computer 
        """
        bool_value = self.read_data([bool_idx])[0]
        if bool_value == 0:
            return self.read_data([destination_idx])[0]
        else:
            return current_position + 3

    def opcode_less_than(self, current_position:int ,param1_idx:int, param2_idx: int, destination_idx: int):
        """
        write 1 to the destination if the first value is less than the second value, otherwise it writes 0

        Parameters:
        --------------
        current_position(int):              current position in memory
        param1_idx(int):                    index where the first value can be found
        param2_idx(int):                    index where the second value can be found
        destination_idx(int):               index where the data should be written to

        Return Values:
        --------------
        current_positon(int):               new current position for the computer 
        """
        if self.read_data([param1_idx])[0] < self.read_data([param2_idx])[0]:
            self.write_data([(1,destination_idx)])
        else:
            self.write_data([(0,destination_idx)])
        return current_position + 4


    def opcode_equals(self, current_position:int, param1_idx:int, param2_idx: int, destination_idx:int):
        """
        Write 1 to destination index if given input params are the same, otherwise write value 0

        Parameters:
        --------------
        current_position(int):              current position in memory
        param1_idx(int):                    index where the first value can be found
        param2_idx(int):                    index where the second value can be found
        destination(int):                   index where the result should be written to

        Return Values:
        --------------
        current_positon(int):               new current position for the computer 
        """
        if self.read_data([param1_idx]) == self.read_data([param2_idx]):
            self.write_data([(1,destination_idx)])
        else: 
            self.write_data([(0,destination_idx)])
        return current_position + 4









def compute(memory):
    """
    run the program
    """
    compute_instance = processor(memory)


    opcode_dict = {#save opcode function and number of parameters
        1: (compute_instance.opcode_add, 3),
        2: (compute_instance.opcode_multiply,3),
        3: (compute_instance.opcode_get_input, 1),
        4: (compute_instance.opcode_output,1),
        5: (compute_instance.opcode_jump_if_true,2),
        6: (compute_instance.opcode_jump_if_false, 2),
        7: (compute_instance.opcode_less_than, 3),
        8: (compute_instance.opcode_equals, 3),
        99: (None, 0)
    }


    running = True
    curr_pos = 0
    while running:
        #get opcode from current_position
        try:
            curr_command = memory[curr_pos]
        except IndexError:
            print("an index error has occured while running your code")
            return None
        
    
        opcode = curr_command % 100
        if opcode not in opcode_dict.keys():
            print("Your opcode could not be found")
            quit()
        if opcode == 99:
            #halt program
            running = False
            break

        param_digits = list(split_digits(curr_command))[2:]

        opcode_arg_count = opcode_dict[opcode][1]#get the amount of arguments the function wants
        opcode_function = opcode_dict[opcode][0]#get the opcode's function
        #perform action
        if len(param_digits) == 0:#generate array of default modes if none are given
            mode_arr = [0 for i in range(opcode_arg_count)]
        elif len(param_digits) == opcode_arg_count:#no need to generate defaults if all paramters are given
            mode_arr = param_digits
        else:
            mode_arr = param_digits
            for i in range(opcode_arg_count - len(param_digits)):
                mode_arr.append(0)

        #get an array if indixes for the values to give to the functions
        idx_arr = []
        for idx,elements in enumerate(mode_arr):
            if elements == 1:#immediate mode
                idx_arr.append(curr_pos+idx+1)
            else:
                idx_arr.append(memory[curr_pos+idx+1])
        #executing the opcode
        curr_pos = opcode_function(curr_pos, *idx_arr)


compute(commands)