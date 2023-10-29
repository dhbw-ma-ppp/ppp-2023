class Computer:
    """
    The computer only uses referenced values and therfore converts explicit values to references.
    Therefore a 'value' in this doc in reality means 'commands[reference_to_that_value]'
    """

    def __init__(self, commands):
        """Initializes a computer with the given commands.

        Args:
            commands (list_of_int): A list of the
        """
        self.commands = commands
        self.instruction_pointer = 0
        self.opcode_map = {
            1: self.add_write,
            2: self.multiply_write,
            3: self.input_and_write,
            4: self.output,
            5: self.jump_if_true,
            6: self.jump_if_false,
            7: self.less_than,
            8: self.equals,
            99: self.terminate,
        }

    def add_write(self):
        """
        Adds the first and second value after the instructio_pointer and stores it in third position.
        Finally it moves the instruction pointer 4 steps forwards.
        """
        amount_of_params = 2
        first_reference, second_reference = self.get_refs(
            params_to_get=amount_of_params
        )
        result = self.commands[first_reference] + self.commands[second_reference]
        self.write_value_to(value=result, amount_of_params=amount_of_params)
        self.instruction_pointer += amount_of_params + 2  # 2: opcode + savepos

    def multiply_write(self):
        """
        Multiplies the first and second value after the instructio_pointer and stores it in third position.
        Finally it moves the instruction pointer 4 steps forwards.
        """
        amount_of_params = 2
        first_reference, second_reference = self.get_refs(
            params_to_get=amount_of_params
        )
        result = self.commands[first_reference] * self.commands[second_reference]
        self.write_value_to(value=result, amount_of_params=amount_of_params)
        self.instruction_pointer += amount_of_params + 2  # 2: opcode + savepos

    def input_and_write(self):
        """
        Reads a number user input and saves it at the first value after the opcode.
        If the input is not valid, the computer will terminate.
        """
        user_input = input("Please input an integer value: ")
        try:
            result = int(user_input)
            self.write_value_to(value=result, amount_of_params=0)
        except ValueError:
            print("Please input a valid value next time.")
            self.terminate()
        self.instruction_pointer += 2  # opcode + write_pos

    def output(self):
        """
        Outputs the first value after the instruction poiunter and moves the instruction_pointer one step forwards.
        """
        amount_of_params = 1
        (address,) = self.get_refs(params_to_get=amount_of_params)
        print(self.commands[address])
        self.instruction_pointer += amount_of_params + 1  # 1: opcode

    def jump_if_true(self):
        """
        Jumps to position referenced by the second position from the instruction pointer, if the first value is true (!=0).
        Otherwise it moves the instruction_pointer 3 steps forwards.
        """
        amount_of_params = 2
        value_ref, jump_location_ref = self.get_refs(params_to_get=amount_of_params)
        if self.commands[value_ref]:
            self.instruction_pointer = self.commands[jump_location_ref]
        else:
            self.instruction_pointer += amount_of_params + 1  # 1: opcode

    def jump_if_false(self):
        """
        Jumps to position referenced by the second position from the instruction pointer, if the first value is false (=0).
        Otherwise it moves the instruction_pointer 3 steps forward.
        """
        amount_of_params = 2
        value_ref, jump_location_ref = self.get_refs(params_to_get=amount_of_params)
        if not self.commands[value_ref]:
            self.instruction_pointer = self.commands[jump_location_ref]
        else:
            self.instruction_pointer += amount_of_params + 1  # 1: opcode

    def less_than(self):
        """
        Writes 1 to third position from instruction_pointer, if the first value is less than the second value from the instruction pointer .
        Otherwise it sets the value to 0
        """
        amount_of_params = 2
        first_reference, second_reference = self.get_refs(
            params_to_get=amount_of_params
        )
        if self.commands[first_reference] < self.commands[second_reference]:
            self.write_value_to(1, amount_of_params=amount_of_params)

        else:
            self.write_value_to(0, amount_of_params=amount_of_params)
        self.instruction_pointer += amount_of_params + 2  # 2: opcode + savepos

    def equals(self):
        """
        Writes 1 to third position from instruction_pointer, if the first to values are equal.
        Otherwise it sets the value to 0
        """
        amount_of_params = 2
        first_reference, second_reference = self.get_refs(
            params_to_get=amount_of_params
        )
        if self.commands[first_reference] == self.commands[second_reference]:
            self.write_value_to(1, amount_of_params=amount_of_params)
        else:
            self.write_value_to(0, amount_of_params=amount_of_params)
        self.instruction_pointer += amount_of_params + 2  # 2: opcode + savepos

    def terminate(self):
        """sets the instruction_pointer to None"""
        self.instruction_pointer = None

    def calculate_step(self):
        """calculates the next operation based on the position of the instruction_pointer"""
        opcode = self.commands[self.instruction_pointer]
        operation_to_perform = opcode % 100
        self.opcode_map[operation_to_perform]()

    def write_value_to(self, value, amount_of_params):
        """Writes a value to the location of the instruction pointer + the respective save_pos_from_pointer

        Args:
            value (int): the value to write
            save_pos_from_pointer (int): position to add from instruction_pointer
        """
        save_ref = self.commands[
            self.instruction_pointer + amount_of_params + 1
        ]  # 1 for the opcode
        self.commands[save_ref] = value

    def get_refs(self, params_to_get):
        """gets references to a set number of params

        Args:
            params_to_get (number): amount of arg refs to get


        Returns:
            tuple: (first_ref, second_ref, third_ref, ...)
        """

        params = self.commands[self.instruction_pointer] // 100

        refs = []
        for index in range(0, params_to_get):
            if params % 10:
                refs.append(self.instruction_pointer + 1 + index)
            else:
                # postion
                refs.append(self.commands[self.instruction_pointer + 1 + index])
            params //= 10

        return tuple(refs)


if __name__ == "__main__":

    def main():
        pass
