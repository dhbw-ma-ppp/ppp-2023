import operator
import os
import sys

global three_values, x, y, type, high_score, c_input, buffer 
three_values, x, y, type, buffer = [], [], [], [], []
high_score, c_input = 0, 0
game_type = sys.argv[1] if len(sys.argv) >= 2 else "no arguments"

class IntComputer:
    def __init__(self, input_getter, output_collector):
        def get_input(modes):
            target_mode = modes % 10
            if target_mode == 2:
                target = self.memory.get(self.ip, 0) + self.relative_mode_offset
            else:
                target = self.memory.get(self.ip, 0)
            self.memory[target] = input_getter()
            self.ip += 1

        def write_output(modes):
            x = self.get_function_arguments(modes, 1)[0]
            output_collector(x)

        def set_offset(modes):
            x = self.get_function_arguments(modes, 1)[0]
            self.relative_mode_offset += x

        self.function_map = {
            1: self._make_register_setter(operator.add),
            2: self._make_register_setter(operator.mul),
            3: get_input,
            4: write_output,
            5: self._make_ip_setter(operator.ne, 0),
            6: self._make_ip_setter(operator.eq, 0),
            7: self._make_register_setter(operator.lt),
            8: self._make_register_setter(operator.eq),
            9: set_offset,
        }

    def _make_register_setter(self, func):
        # make generic function that sets a register
        def f(modes):
            x, y = self.get_function_arguments(modes, 2)
            target_mode = (modes // (10**2)) % 10
            if target_mode == 2:
                target = self.memory.get(self.ip, 0) + self.relative_mode_offset
            else:
                target = self.memory.get(self.ip, 0)
            self.memory[target] = int(func(x, y))
            self.ip += 1
        return f

    def _make_ip_setter(self, func, comparison_value):
        # make a generic function that sets the instruction pointer
        def f(modes):
            x, y = self.get_function_arguments(modes, 2)
            if func(x, comparison_value):
                self.ip = y
        return f

    def _resolve_argument_value(self, arg_mode, arg_value):
        if arg_mode == 0:
            return self.memory.get(arg_value, 0)
        if arg_mode == 1:
            return arg_value
        if arg_mode == 2:
            return self.memory.get(arg_value + self.relative_mode_offset, 0)

    def get_function_arguments(self, modes, n_args):
        arg_values = [self.memory[self.ip + x] for x in range(n_args)]
        arg_modes = [(modes // (10**i)) % 10 for i in range(n_args)]
        arguments = [self._resolve_argument_value(mode, value) for mode, value in zip(arg_modes, arg_values)]
        self.ip += n_args
        return arguments

    def split_command_and_modes(self):
        command = self.memory[self.ip]
        self.ip += 1
        return command % 100, command // 100

    def run(self, data):
        self.memory = {i: v for i, v in enumerate(data)}
        self.ip = 0
        self.relative_mode_offset = 0

        while True:
            opcode, modes = self.split_command_and_modes()
            if opcode == 99:
                global high_score
                print(f"\n[Highscore]: {high_score}")
                break
            # calculate function arguments
            opcode_function = self.function_map[opcode]
            opcode_function(modes)


def input_getter():
    graphical_output()
    if("computer" in game_type):
        return c_input
    else:
        value = input()
        return int(value)


def output_collector(output):
    global three_values 
    three_values.append(output)
    if len(three_values) == 3:
        global x,y,type,high_score
        x.append(three_values[0]) 
        y.append(three_values[1])
        if(three_values[0] == -1 and three_values[1] == 0):
            high_score = three_values[2]
        match three_values[2]:
            case 1:
                type.append("#")
            case 2:
                type.append("~")
            case 3:
                type.append("_")
            case 4:
                type.append("x")
            case _:
                type.append(" ")

        three_values = []

def graphical_output():
    global x,y,type,c_input,buffer
    print("\x1b[H\x1b[J")
    if not buffer:
        for i in range(max(y)+1):
            buffer.append(["0" for c in range(max(x)+1)])
    for j in range(len(y)):
        buffer[y[j]][x[j]] = type[j]

    j_buffer = "#" +"\n".join(("".join(line) for line in buffer))
    print(j_buffer)
    j_buffer  = ""
    x_point, x_platform = 0,0
    x,y,type = [],[],[]
    for line in buffer:
        if "x" in line:
            x_point = line.index("x")
        if "_" in line:
            x_platform = line.index("_")    

    if(x_point == x_platform):
        c_input = 0
    elif(x_point > x_platform):
        c_input = 1
    else:
        c_input = -1

ic = IntComputer(input_getter, output_collector)

with open(".."+os.sep+".."+os.sep+"data"+os.sep+"breakout_commands.txt", "r") as file:
    lines = [line.split("\n")[0] for line in file.readlines()]
    [lines.append("0") for num in range(1000)]
    lines[0] = 2
    ic.run([*map(int, lines)])
