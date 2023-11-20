class Computer:
    """
    The computer only uses referenced values and therfore converts explicit values to references.
    Therefore a 'value' in this doc in reality means 'commands[reference_to_that_value]'
    """

    def __init__(self, memory: dict[int, int], output_stream):
        """Initializes a computer with the given commands.

        Args:
            commands (list_of_int): A list of the
        """
        self._memory = memory
        self._instruction_pointer = 0
        self._relative_offset = 0
        self._output_stream = output_stream
        self.opcode_map = {
            1: self._add_write,
            2: self._multiply_write,
            3: self._input_and_write,
            4: self._output,
            5: self._jump_if_true,
            6: self._jump_if_false,
            7: self._less_than,
            8: self._equals,
            9: self._adjust_relative_offset,
            99: self.terminate,
        }

    def _read_value(self, position: int):
        value = self._memory.get(position, 0)
        return value

    def _add_write(self):
        """
        Adds the first and second value after the instructio_pointer and stores it in third position.
        Finally it moves the instruction pointer 4 steps forwards.
        """

        amount_of_params = 3
        first_reference, second_reference, save_ref = self._get_refs(
            params_to_get=amount_of_params
        )
        result = self._read_value(first_reference) + self._read_value(second_reference)
        self._write_value_to(value=result, save_pos=save_ref)
        self._instruction_pointer += amount_of_params + 1  # opcode

    def _multiply_write(self):
        """
        Multiplies the first and second value after the instructio_pointer and stores it in third position.
        Finally it moves the instruction pointer 4 steps forwards.
        """
        amount_of_params = 3
        first_reference, second_reference, save_ref = self._get_refs(
            params_to_get=amount_of_params
        )
        result = self._read_value(first_reference) * self._read_value(second_reference)
        self._write_value_to(value=result, save_pos=save_ref)
        self._instruction_pointer += amount_of_params + 1  # opcode

    def _input_and_write(self):
        """
        Reads a number user input and saves it at the first value after the opcode.
        If the input is not valid, the computer will terminate.
        """
        user_input = input("Please input an integer value: ")
        amount_of_params = 1
        try:
            result = int(user_input)
            (save_ref,) = self._get_refs(params_to_get=amount_of_params)
            self._write_value_to(result, save_ref)
        except ValueError:
            print("Please input a valid value next time.")
            self.terminate()
        self._instruction_pointer += amount_of_params + 1  # opcode + write_pos

    def _output(self):
        """
        Outputs the first value after the instruction poiunter and moves the instruction_pointer one step forwards.
        """
        amount_of_params = 1
        (address,) = self._get_refs(params_to_get=amount_of_params)
        self._output_stream.append(self._read_value(address))
        self._instruction_pointer += amount_of_params + 1  # 1: opcode

    def _jump_if_true(self):
        """
        Jumps to position referenced by the second position from the instruction pointer, if the first value is true (!=0).
        Otherwise it moves the instruction_pointer 3 steps forwards.
        """
        amount_of_params = 2
        value_ref, jump_location_ref = self._get_refs(params_to_get=amount_of_params)
        if self._read_value(value_ref):
            self._instruction_pointer = self._read_value(jump_location_ref)
        else:
            self._instruction_pointer += amount_of_params + 1  # 1: opcode

    def _jump_if_false(self):
        """
        Jumps to position referenced by the second position from the instruction pointer, if the first value is false (=0).
        Otherwise it moves the instruction_pointer 3 steps forward.
        """
        amount_of_params = 2
        value_ref, jump_location_ref = self._get_refs(params_to_get=amount_of_params)
        if not self._read_value(value_ref):
            self._instruction_pointer = self._read_value(jump_location_ref)
        else:
            self._instruction_pointer += amount_of_params + 1  # 1: opcode

    def _less_than(self):
        """
        Writes 1 to third position from instruction_pointer, if the first value is less than the second value from the instruction pointer .
        Otherwise it sets the value to 0
        """
        amount_of_params = 3
        first_reference, second_reference, save_ref = self._get_refs(
            params_to_get=amount_of_params
        )
        if self._read_value(first_reference) < self._read_value(second_reference):
            self._write_value_to(1, save_ref)

        else:
            self._write_value_to(0, save_ref)
        self._instruction_pointer += amount_of_params + 1  # opcode

    def _equals(self):
        """
        Writes 1 to third position from instruction_pointer, if the first to values are equal.
        Otherwise it sets the value to 0
        """
        amount_of_params = 3
        first_reference, second_reference, save_ref = self._get_refs(
            params_to_get=amount_of_params
        )
        if self._read_value(first_reference) == self._read_value(second_reference):
            self._write_value_to(1, save_ref)
        else:
            self._write_value_to(0, save_ref)
        self._instruction_pointer += amount_of_params + 1  # opcode

    def _adjust_relative_offset(self):
        amount_of_params = 1
        (ref,) = self._get_refs(amount_of_params)
        self._relative_offset += self._read_value(ref)
        self._instruction_pointer += amount_of_params + 1

    def _write_value_to(self, value, save_pos):
        """Writes a value to the location of the instruction pointer + the respective save_pos_from_pointer

        Args:
            value (int): the value to write
            save_pos_from_pointer (int): position to add from instruction_pointer
        """

        # this value could be written in offset mode
        self._memory[save_pos] = value

    def _get_refs(self, params_to_get):
        """gets references to a set number of params

        Args:
            params_to_get (number): amount of arg refs to get


        Returns:
            tuple: (first_ref, second_ref, third_ref, ...)
        """

        params = self._read_value(self._instruction_pointer) // 100

        refs = []
        for index in range(0, params_to_get):
            mode = params % 10
            match mode:
                case 0:
                    # absolute
                    refs.append(self._read_value(self._instruction_pointer + 1 + index))
                case 1:
                    # position
                    refs.append(self._instruction_pointer + 1 + index)
                case 2:
                    # relative
                    refs.append(
                        self._read_value(self._instruction_pointer + 1 + index)
                        + self._relative_offset
                    )
            params //= 10

        return tuple(refs)

    def terminate(self):
        """sets the instruction_pointer to None"""
        self._instruction_pointer = None

    def calculate_step(self):
        """calculates the next operation based on the position of the instruction_pointer"""
        opcode = self._read_value(self._instruction_pointer)
        operation_to_perform = opcode % 100
        self.opcode_map[operation_to_perform]()

    def run(self):
        while self._instruction_pointer is not None and self._instruction_pointer < len(
            self._memory
        ):
            self.calculate_step()

        return 0
