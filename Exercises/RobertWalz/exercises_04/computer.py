import util


class Computer:
    def __init__(self, commands):
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

    def write_value_to(self, value, amount_of_params):
        """Writes a value to the location of the instruction pointer + the respective save_pos_from_pointer

        Args:
            value (int): the value to write
            save_pos_from_pointer (int): position to add from instruction_pointer
        """
        self.commands[self.instruction_pointer + amount_of_params + 1] = value

    def add_write(self):
        amount_of_params = 2
        first_reference, second_reference = util.get_refs(
            self.commands, self.instruction_pointer, params_to_get=amount_of_params
        )
        result = self.commands[first_reference] + self.commands[second_reference]
        self.write_value_to(value=result, amount_of_params=amount_of_params)
        self.instruction_pointer += 4

    def multiply_write(self):
        amount_of_params = 2
        first_reference, second_reference = util.get_refs(
            self.commands, self.instruction_pointer, params_to_get=amount_of_params
        )
        result = self.commands[first_reference] * self.commands[second_reference]
        self.write_value_to(value=result, amount_of_params=amount_of_params)
        self.instruction_pointer += 4

    def input_and_write(self):
        user_input = input("Please input an integer value:")
        try:
            result = int(user_input)
            self.write_value_to(value=result, amount_of_params=0)
        except ValueError:
            print("Please input a valid value next time.")
        self.instruction_pointer += 2

    def output(self):
        amount_of_params = 1
        address = util.get_refs(
            self.commands, self.instruction_pointer, params_to_get=amount_of_params
        )
        print(self.commands[address])
        self.instruction_pointer += 1

    def jump_if_true(self):
        amount_of_params = 1
        address = util.get_refs(
            self.commands, self.instruction_pointer, params_to_get=amount_of_params
        )
        if self.commands[address]:
            self.instruction_pointer += 1

    def jump_if_false(self):
        amount_of_params = 1
        address = util.get_refs(
            self.commands, self.instruction_pointer, params_to_get=amount_of_params
        )
        if not self.commands[address]:
            self.instruction_pointer += 1

    def less_than(self):
        amount_of_params = 2
        first_reference, second_reference = util.get_refs(
            self.commands, self.instruction_pointer, params_to_get=amount_of_params
        )
        if self.commands[first_reference] < self.commands[second_reference]:
            self.write_value_to(1, amount_of_params=amount_of_params)

        else:
            self.write_value_to(0, amount_of_params=amount_of_params)
        self.instruction_pointer += 4

    def equals(self):
        amount_of_params = 2
        first_reference, second_reference = util.get_refs(
            self.commands, self.instruction_pointer, params_to_get=amount_of_params
        )
        if self.commands[first_reference] == self.commands[second_reference]:
            self.write_value_to(1, amount_of_params=amount_of_params)
        else:
            self.write_value_to(0, amount_of_params=amount_of_params)
        self.instruction_pointer += 4

    def terminate(self, **_):
        self.function_pointer = None

    


if __name__ == "__main__":

    def main():
        pass
