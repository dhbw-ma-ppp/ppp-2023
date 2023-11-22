# to solve todays exercise you will need a fully functional int-computer
# a fully functional int-computer has some additional features compared to the 
# last one you implemented.
# you can either use my implementation of an int-computer (see AtrejuTauschinsky/int_computer.py)
# or you can extend your own int-computer with the necessary features. If you want to extend your own
# the features you need to implement will be described at the bottom.
#
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
#
#
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
from int_computer import IntComputer
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import os


class BreakoutGame:
    def __init__(self, commands_path=Path(__file__).parents[2] / 'data' / 'breakout_commands.txt', export_movie=False):
        def input_setter_no_movie():
            self._analyse_frame_update()
            if self._paddle_x < self._ball_x:
                return 1
            if self._paddle_x > self._ball_x:
                return -1
            return 0

        def input_setter_movie():
            return_val = input_setter_no_movie()

            fig, ax = plt.subplots()
            ax.set_axis_off()
            ax.set_title(f'Score: {self._score}', fontsize=15)
            ax.imshow(self._frame)
            plt.savefig(f'img_out/{str(self._frame_counter).zfill(5)}.png', bbox_inches='tight')
            plt.close()
            self._frame_counter += 1

            return return_val

        def output_getter(out_val):
            self._update_data.append(out_val)

        if export_movie:
            self._computer = IntComputer(input_setter_movie, output_getter)
            self._frame_counter = 0
            Path.mkdir(Path.cwd() / 'img_out')
        else:
            self._computer = IntComputer(input_setter_no_movie, output_getter)

        with commands_path.open('r') as commands_in:
            self._commands = [int(command.strip()) for command in commands_in.readlines()]
            self._commands[0] = 2
        self._export_movie = export_movie
        self._update_data = []
        self._frame = np.zeros((23, 43))
        self._paddle_x = None
        self._ball_x = None
        self._score = 0

    def _analyse_frame_update(self):
        for index in range(0, len(self._update_data), 3):
            x, y, data = self._update_data[index], self._update_data[index + 1], self._update_data[index + 2]
            if x < 0:
                self._score = data
            else:
                self._frame[y, x] = data
            if data == 3:
                self._paddle_x = x
            elif data == 4:
                self._ball_x = x
        self._update_data = []

    def run(self):
        self._computer.run(self._commands)
        self._analyse_frame_update()

        if self._export_movie:
            fig, ax = plt.subplots()
            ax.set_axis_off()
            ax.set_title(f'Score: {self._score}', fontsize=15)
            ax.imshow(self._frame)
            for _ in range(120):
                plt.savefig(f'img_out/{str(self._frame_counter).zfill(5)}.png', bbox_inches='tight')
                self._frame_counter += 1
            plt.close()

            os.system(
                'ffmpeg -framerate 60 -pattern_type glob -i "img_out/*.png" -s:v 516x418 -c:v libx264 -crf 17 '
                '-pix_fmt yuv420p breakout_movie.mp4')  # TODO do it with ffmpeg wrapper (if it would just work...)

        print(f'Final score: {self._score}')



