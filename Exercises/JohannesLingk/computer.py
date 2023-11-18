class State:
    """
    State is passed to the command methods and contains 
    information about the current state of execution like:
        - Commands
        - Head (or Pointer) of execution
        - Mode information for current command
    """
    def __init__(self, computer: "Computer", modes: str) -> None:
        self.commands: list[int] = computer.memory
        self.head: int = computer.pointer
        self.modes = modes
        self.relative_offset = computer.relative_offset

    def _get_mode(self, index: int) -> int:
        return int(self.modes[index]) if len(self.modes) > index else 0
    
    def get_value(self, index: int) -> int:
        """
        For immediate mode: Return value in parameter
        for position mode: Return value at memory address from parameter
        """
        mode = self._get_mode(index)
        if mode == 1: # immediate mode
            return self.get_pointer(index)
        elif mode == 2: # relative mode
            return self.get_memory(self.relative_offset + self.get_pointer(index))
        elif mode == 0: # position mode
            return self.get_memory(self.get_pointer(index))
        
    def get_pointer(self, index: int) -> int:
        """
        Returns the value in paramenter.
        Mostly used for write operation.
        """
        return self.get_memory(self.head + index + 1)
        
    def write_memory(self, index: int, value: int):
        """
        Writes a value into memory position.
        Relative offset is used.
        """
        mode = self._get_mode(index)
        position = self.get_pointer(index) + (self.relative_offset if mode == 2 else 0)
        if len(self.commands) <= position:
            # if list is to small, expand with zeroes
            self.commands.extend([0 for _ in range(position - len(self.commands) + 1)])
        self.commands[position] = value

    def get_memory(self, position: int):
        return self.commands[position] if len(self.commands) > position else 0


class Computer:
    def __init__(self, input_hook, output_hook) -> None:
        self.input_hook = input_hook
        self.output_hook = output_hook

    def command_addition(self, state: State) -> int: # code 1
        number1 = state.get_value(0)
        number2 = state.get_value(1)
        state.write_memory(2, number1 + number2)
        return state.head + 4

    def command_multiplication(self, state: State) -> int: # code 2
        number1 = state.get_value(0)
        number2 = state.get_value(1)
        state.write_memory(2, number1 * number2)
        return state.head + 4

    def command_stop(self, state: State) -> int: # code 99
        return len(state.commands)

    def command_input(self, state: State) -> int: # code 3
        #number = int(input("input digit: "))
        number = self.input_hook()
        state.write_memory(0, number)
        return state.head + 2

    def command_output(self, state: State) -> int: # code 4
        #print(state.get_value(0))
        self.output_hook(state.get_value(0))
        self.output_log.append( state.get_value(0) )
        return state.head + 2

    def command_jump_if_true(self, state: State) -> int: # code 5
        condition = state.get_value(0)
        jump_pos = state.get_value(1)
        if condition != 0:
            return jump_pos
        else:
            return state.head + 3

    def command_jump_if_false(self, state: State) -> int: # code 6
        condition = state.get_value(0)
        jump_pos = state.get_value(1)
        if condition == 0:
            return jump_pos
        else:
            return state.head + 3

    def command_less_than(self, state: State) -> int: # code 7
        number1 = state.get_value(0)
        number2 = state.get_value(1)
        result = 1 if number1 < number2 else 0
        state.write_memory(2, result)
        return state.head + 4

    def command_equals(self, state: State) -> int: # code 8
        number1 = state.get_value(0)
        number2 = state.get_value(1)
        result = 1 if number1 == number2 else 0
        state.write_memory(2, result)
        return state.head + 4
    
    def command_change_offset(self, state: State) -> int: # code 9
        number1 = state.get_value(0)
        new_offset = self.relative_offset + number1
        self.relative_offset = new_offset
        return state.head + 2

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
        9: command_change_offset,
        99: command_stop,
    }

    pointer: int = 0
    memory = []
    relative_offset = 0
    output_log = []

    """
    Main execution loop.
    Runs as long as head is within command bounds.
    For every command read, calls appropriate method and passes State object.
    """
    def run(self, commands: list[int]):
        self.pointer = 0
        self.memory = commands
        self.output_log = []
        self.relative_offset = 0
        while self.pointer < len(self.memory):
            command = str(self.memory[self.pointer])
            # Split command into op_code and mode string
            operation = int(command[-2:])
            modes = command[-3::-1]
            if operation not in self.op_codes.keys():
                raise Exception(f'No operation code: {operation}')
            self.pointer = self.op_codes[operation](self, State(self, modes))
        return self.output_log
        


# COMPLETE INT COMPUTER
# This is only relevant if you decide to extend your own implementation with the necessary features.
# If you decide to use my implementation you can ignore this part.
#
#
# - The computer needs to implement memory much /larger/ than the set of initial commands.
#   Any memory address not part of the initial commands can be assumed to be initialized to 0.
#   (only positive addresses are valid).
# - You need to support a new parameter mode, 'relative mode', denoted as mode 2 in the 'mode' part
#   of the instructions.
#   Relative mode is similar to position mode (the first access mode you implemented). However, 
#   parameters in relative mode count not from 0, but from a value called 'relative offset'. 
#   When the computer is initialized, the relative offset is initialized to 0, and as long as it remains
#   0 relative mode and position mode are identical.
#   In general though parameters in relative mode address the memory location at 'relative offset + parameter value'.
#   EXAMPLE: if the relative offset is 50, the mode is 2, and the value you read from memory is 7 you should 
#     retrieve data from the memory address 57.
#     Equally, if you read -7, you should retrieve data from the memory address 43.
#   This applies to both read- and write operations.
# - You need to implement a new opcode, opcode 9. opcode 9 adjusts the relative offset by the value of its only parameter.
#   the offset increases by the value of the parameter (or decreases if that value is negative).
