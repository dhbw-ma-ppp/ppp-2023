# to solve todays exercise you will need a fully functional int-computer
# a fully functional int-computer has some additional features compared to the 
# last one you implemented.
# you can either use my implementation of an int-computer (see AtrejuTauschinsky/int_computer.py)
# or you can extend your own int-computer with the necessary features. If you want to extend your own
# the features you need to implement will be described at the bottom.
#

#________________________________________________________IMPORTS_____________________________________________________________________________________

import operator
from matplotlib import pyplot as plt
import pathlib
import numpy as np

#________________________________________________________COMPUTER___________________________________________________________________________________

class IntComputer:
    """Copied from Atreju Tauschinsky"""
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
                break

            # calculate function arguments
            opcode_function = self.function_map[opcode]
            opcode_function(modes)

        print('shutting down...')

#
# We will run 'breakout' -- the arcade game -- on our simulated computer. 
# (https://en.wikipedia.org/wiki/Breakout_(video_game))
# The code for the computer will be provided under data/breakout_commands.txt
# the code will produce outputs in triplets. every triplet that is output
# specifies (x-position, y-position, tile_type).
# tiles can be of the following types:
# 0: empty tile
# 1: wall. walls are indestructible
# 2: block. blocks can be destroyed by the ball
# 3: paddle. the paddle is indestructible
# 4: ball. the ball moves diagonally and bounces off objects
# 
# EXAMPLE:
# a sequence of output values like 1, 2, 3, 6, 5, 4 would
#  - draw a paddle (type 3) at x=1, y=2
#  - draw the ball (type 4) at x=6, y=5
#
#
# PART 1:
# run the game until it exits. Analyse the output produced during the run, and create
# a visual representation (matplotlib or ascii-art are possibilities here...) of the screen display.
# mark the different tile types as different colors or symbols. Upload the picture with your PR.
#
# PART 2:
# The game didn't actually run in part 1, it just drew a single static screen.
# Change the first instruction of the commands from 1 to 2. Now the game will actually run.
# when the game actually runs you need to provide inputs to steer the paddle. whenever the computer
# requests you to provide an input, you can chose to provide
# -  0: the paddle remains in position
# - -1: move the paddle to the left
# - +1: move the paddle to the right
#
# the game also outputs a score. when an output triplet is in position (-1, 0) the third value of
# the triplet is not a tile type, but your current score.
# You need to beat the game by breaking all tiles without ever letting the ball cross the bottom 
# edge of the screen. What is your high-score at the end of the game? provide the score as part of your PR.
#
# BONUS: (no extra points, just for fun)
# make a movie of playing the game :)


#________________________________________________________GLOBALS___________________________________________________________________________________

output_list = []                #every int, outputted by the computer, written into one list (without format)
matrix = np.zeros([23,43])      #format the output_list into triplets (2dim array)
ball_position = 0               #the x-position of the ball which is always up to date for the paddle to navigate later on
paddle_position = 0             #the x-position of the paddle (horizontal)
score = 0                       #global counter containing the current score of the game
first_frame = True              #True while current frame is the first, False while not. Needed to only open a new window at first frame.

#________________________________________________________EXERCISES___________________________________________________________________________________

def insert_into_list(value: int):
    """writes the given argument-Integer into the output_list"""

    output_list.append(value)


def insert_into_matrix(matrix_input: list):
    """Takes the zero-format-list and adds it's elements into the matrix (2dim Array) formatted"""

    global ball_position
    global paddle_position
    for index in range(0,len(matrix_input),3):  #one step -> +3
        x,y,entity = matrix_input[index], matrix_input[index+1], matrix_input[index+2]
        if entity == 4:
            ball_position = x
        elif entity == 3:
            paddle_position = x
        elif x == -1:
            global score
            score = entity
            continue
        matrix[y,x] = entity


def control_paddle():
    """Returns the command for the paddle for it to always follow the ball"""

    global first_frame
    insert_into_matrix(output_list)
    plt.imshow(matrix, cmap="rainbow")
    if first_frame:
        plt.show(block  = False)
        first_frame = False
    else:
        plt.draw()
    plt.pause(0.000001)
    
    if ball_position < paddle_position:
        return -1
    elif ball_position > paddle_position:
        return 1
    else:
        return 0

#________________________________________________________FOR MAKING MICHI HAPPY___________________________________________________________________________________

root_dir = pathlib.Path(__file__).parent.parent.parent
command_file = root_dir / "data" / "breakout_commands.txt"

with open(command_file) as input_file:
    data_input_list = list()
    for line in input_file.readlines():
        line.strip()    #removing the \n at the end of the line
        data_input_list.append(int(line))
    data_input_list[0] = 2

#________________________________________________________JUST FOR MY FILE SYSTEM___________________________________________________________________________________

"""with open("./data/breakout_commands.txt", "r") as input_file:
    data_input_list = list()
    for line in input_file.readlines():
        line.strip()
        data_input_list.append(int(line))
    data_input_list[0] = 2"""

#________________________________________________________CONTINUE EXERCISE___________________________________________________________________________________
computer_test = IntComputer(control_paddle, insert_into_list)

computer_test.run(data_input_list)
insert_into_matrix(output_list)
print(score)