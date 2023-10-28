
class Computer:
    commands = []
    intruction_pointer = 0

    def __init__(self, commands):
        self.commands = commands
        return self

    def write_value_to(self, value, address):
        self.commands[address] = value

    def add_write(self, first_reference, second_reference, write_to_pos, **_):
        result = self.commands[first_reference] + self.commands[second_reference]
        self.write_value_to(value=result, address=write_to_pos)
        self.instruction_pointer += 4

    def multiply_write(self, first_reference, second_reference, write_to_pos, **_):
        result = self.commands[first_reference] * self.commands[second_reference]
        self.write_value_to(value=result, address=write_to_pos)
        self.instruction_pointer += 4

    def input_and_write(self, write_to_pos, **_):
        user_input = input("Please input an integer value:")
        try:
            result = int(user_input)
            self.write_value_to(value=result, address=write_to_pos)
        except ValueError:
            print("Please input a valid value next time.")
        self.instruction_pointer += 2

    def output(self, address, **_):
        print(self.commands[address])
        self.instruction_pointer += 1

    def jump_if_true(self, reference, **_):
        if self.commands[reference]:
            self.instruction_pointer += 1

    def jump_if_false(self, reference, **_):
        if not self.commands[reference]:
            self.instruction_pointer += 1

    def less_than(self, first_reference, second_reference, write_to_pos, **_):
        if self.commands[first_reference] < self.commands[second_reference]:
            self.write_value_to(1, write_to_pos)

        else:
            self.write_value_to(0, write_to_pos)
        self.instruction_pointer += 4

    def equals(self, first_reference, second_reference, write_to_pos, **_):
        if self.commands[first_reference] == self.commands[second_reference]:
            self.write_value_to(1, write_to_pos)
        else:
            self.write_value_to(0, write_to_pos)
        self.instruction_pointer += 4

    def terminate(function_pointer):
        function_pointer == None

    opcode_map: {
        1: add_write,
        2: multiply_write,
        3: input_and_write,
        4: output,
        5: jump_if_true,
        6: jump_if_false,
        7: less_than,
        8: equals,
        99: terminate,
    }


def evaluate_opcode(opcode):
    opcode_arr = [int(x) for x in str(opcode)]
    operation_to_perform = int(opcode_arr[-2:])
    Computer.opcode_map[operation_to_perform](first_reference=first_reference)
    


if __name__ == "main.py":

    def main():
        pass
