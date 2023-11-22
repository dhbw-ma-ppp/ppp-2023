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
import os
from pathlib import Path
import tkinter as tk
from int_computer import IntComputer

import os
from pathlib import Path
import tkinter as tk
from int_computer import IntComputer

class ArcadeGame:
    def __init__(self, master, program):
        self.master = master
        master.title("Advent of Code 2019 - Day 13 Arcade Game")

        # Create a canvas to draw the game
        self.canvas = tk.Canvas(master, width=400, height=400)
        self.canvas.pack()

        # Create a variable to store the output
        self.current_output = None

        # Initialize x and y coordinates
        self.current_x = 0
        self.current_y = 0

        # Set the canvas width (adjust this based on your canvas size)
        self.canvas_width = 10

        # Wrap the update_display method to capture the output
        def output_wrapper(output):
            self.current_output = output
            self.update_display(output)

        # Create an instance of IntComputer with the wrapped output_collector
        self.computer = IntComputer(self.get_input, output_wrapper)
        self.computer.run(program)

    def update_display(self, tile_type):
        # Map tile types to colors (you can customize this mapping)
        color_map = {
            0: "white",  # empty tile
            1: "black",  # wall
            2: "blue",  # block
            3: "green",  # paddle
            4: "red"  # ball
        }

        # Draw a rectangle on the canvas based on the tile type
        tile_size = 20  # You can adjust this based on your preference
        x, y = self.current_x, self.current_y
        x_pixel, y_pixel = x * tile_size, y * tile_size
        x1, y1 = x_pixel, y_pixel
        x2, y2 = x1 + tile_size, y1 + tile_size

        # Use the color corresponding to the tile type
        fill_color = color_map.get(tile_type, "gray")

        # Create or update the rectangle on the canvas
        if hasattr(self, 'tiles') and (x, y) in self.tiles:  # Check if 'tiles' attribute exists
            self.canvas.coords(self.tiles[(x, y)], x1, y1, x2, y2)
            self.canvas.itemconfig(self.tiles[(x, y)], fill=fill_color)
        else:
            if not hasattr(self, 'tiles'):
                self.tiles = {}
            self.tiles[(x, y)] = self.canvas.create_rectangle(x1, y1, x2, y2, fill=fill_color)

        # Update the display
        self.master.update()

        # Update x and y coordinates for the next tile
        self.current_x += 1
        if self.current_x >= self.canvas_width:
            self.current_x = 0
            self.current_y += 1

    def get_input(self):
        # Logic to control the paddle based on the ball's position
        # You need to implement this based on the task description
        return 0  # For now, the paddle remains in position

def main():
    # Read the file
    working_dir = Path(os.getcwd()).parent.absolute().parent.absolute()
    path = Path(str(working_dir) + "/data/breakout_commands.txt")
    with open(path, 'r') as file:
        # Create a list of numbers
        numbers = [int(line) for line in file.readlines()]

    root = tk.Tk()
    game = ArcadeGame(root, numbers)
    root.mainloop()

if __name__ == "__main__":
    main()
