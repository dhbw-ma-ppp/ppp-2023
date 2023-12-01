class IntComputer:
    _memory: dict[int, int]
    _current_pointer: int
    _relative_mode_offset: int

    def __init__(self, input_getter, output_collector):
        def _get_values(params: int, amount_read: int, amount_write: int) -> list[int]:
            locations: list[int] = []
            for i in range(amount_read):
                mode = params % 10

                if mode == 0:
                    locations.append(self._memory.get(self._memory[self._current_pointer + i + 1], 0))
                elif mode == 1:
                    locations.append(self._memory.get(self._current_pointer + i + 1, 0))
                elif mode == 2:
                    locations.append(self._memory.get(self._memory[self._current_pointer + i + 1] + self._relative_mode_offset, 0))
                else:
                    raise ValueError(f"Unknown mode {mode} at {self._current_pointer} ({self._memory[self._current_pointer]})")
                params //= 10
            for i in range(amount_write):
                mode = params % 10

                if mode == 0:
                    locations.append(self._memory[self._current_pointer + i + 1 + amount_read])
                elif mode == 1:
                    raise ValueError(f"Mode {mode} not supported for write operations. At {self._current_pointer} ({self._memory[self._current_pointer]})")
                elif mode == 2:
                    locations.append(self._memory[self._current_pointer + i + 1 + amount_read] + self._relative_mode_offset)
                else:
                    raise ValueError(f"Unknown mode {mode} at {self._current_pointer} ({self._memory[self._current_pointer]})")

                params //= 10
            return locations

        def _command_add(params: int):
            val_1, val_2, write = _get_values(params, 2, 1)

            self._memory[write] = val_1 + val_2
            self._current_pointer += 4

        def _command_multiply(params: int):
            val_1, val_2, write = _get_values(params, 2, 1)
            
            self._memory[write] = val_1 * val_2
            self._current_pointer += 4

        def _command_input(params: int):
            write = _get_values(params, 0, 1)[0]

            self._memory[write] = input_getter()
            self._current_pointer += 2

        def _command_output(params: int):
            value = _get_values(params, 1, 0)[0]

            output_collector(value)
            self._current_pointer += 2

        def _command_jump_if_true(params):
            value, jump_address = _get_values(params, 2, 0)

            if bool(value): self._current_pointer = jump_address
            else: self._current_pointer += 3

        def _command_jump_if_false(params):
            value, jump_address = _get_values(params, 2, 0)

            if bool(value): self._current_pointer += 3
            else: self._current_pointer = jump_address

        def _command_less_than(params):
            val_1, val_2, write = _get_values(params, 2, 1)

            self._memory[write] = int(val_1 < val_2)
            self._current_pointer += 4

        def _command_equals(params):
            val_1, val_2, write = _get_values(params, 2, 1)

            self._memory[write] = int(val_1 == val_2)
            self._current_pointer += 4

        def _command_change_realtive_mode(params):
            val1 = _get_values(params, 1, 0)[0]

            self._relative_mode_offset += val1
            self._current_pointer += 2

        self._opcode_dictionary = {
            1: _command_add,
            2: _command_multiply,
            3: _command_input,
            4: _command_output,
            5: _command_jump_if_true,
            6: _command_jump_if_false,
            7: _command_less_than,
            8: _command_equals,
            9: _command_change_realtive_mode,
        }   
    
    def run(self, data):
        self._memory = {i: v for i, v in enumerate(data)}
        self._current_pointer = 0
        self._relative_mode_offset = 0

        while True:
            params = self._memory[self._current_pointer]
            opcode = params % 100
            params //= 100

            if opcode == 99:
                break

            if opcode in self._opcode_dictionary:
                self._opcode_dictionary[opcode](params)
            else:
                raise LookupError(f"Couldn't read optCode with value {opcode} at position {self._current_pointer}")
        
        print("shutting down...")