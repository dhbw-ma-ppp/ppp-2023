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



#!IMPORTANT: if you want to use the terminal interface of this code, please download the dependencies




from int_computer import IntComputer
import pathlib
import asciimatics
import time
from asciimatics.screen import Screen
from asciimatics.effects import Cycle, Stars
from asciimatics.renderers import FigletText
from asciimatics.scene import Scene


here = pathlib.Path(__file__).parent
exercise_dir = here.parent
data_dir = exercise_dir.parent / "data"



#get the commands
with open(data_dir / "breakout_commands.txt","r") as file:
    data = file.readlines()

commands =[int(char.rstrip("\n"))for char in data]



COLOUR_BLACK = 0
COLOUR_RED = 1
COLOUR_GREEN = 2
COLOUR_YELLOW = 3
COLOUR_BLUE = 4
COLOUR_MAGENTA = 5
COLOUR_CYAN = 6
COLOUR_WHITE = 7


A_BOLD = 1
A_NORMAL = 2
A_REVERSE = 3
A_UNDERLINE = 4



FPS = 2


class Game:
    pixel_encoding = {
        0: ("",COLOUR_WHITE),
        1: ("#", COLOUR_WHITE),
        2: ("=", COLOUR_BLUE),
        3: ("-", COLOUR_GREEN),
        4: ("O", COLOUR_RED)
    }
    def __init__(self):
        self.usr_inputs = 0
        self.score = 0
        self.triplet_arr = []
        self.pixel_dict = {}
        self.screen = None


    def score_display(self, screen):
        score_str = f"YOUR  SCORE   IS  : {self.score}"
        effects = [
            Cycle(
                screen,
                FigletText("Breakout", font='big'),
                int(screen.height / 2 - 8)),
            Cycle(
                screen,
                FigletText(score_str, font='big'),
                int(screen.height / 2 + 3)),
            Stars(screen, 200)
        ]
        screen.play([Scene(effects, 500)])




    def render(self,screen:Screen):
        self.screen = screen
        for key, item in self.pixel_dict.items():
            xy_pos = key.split("_")
            #Print Pixel: 1st argument: char to print, 2nd argument: x position, 3rd argument: y position, 4th argument: color
            screen.print_at(item[0],int(xy_pos[0]),int(xy_pos[1]),item[1])#print the pixel

        screen.refresh()
        time.sleep(1/FPS)#sleep for 



    def split_triplets(self, inpt:int):
        self.triplet_arr.append(inpt)
        if len(self.triplet_arr) == 3:
            #full triplet -> draw screen

            if self.triplet_arr[0] == -1:#score update
                self.score += self.triplet_arr[2]#update the score
            else:

                #check if a pixel with the same index0 and 1 is already present
                
                dict_key = str(self.triplet_arr[0]) + "_" + str(self.triplet_arr[1])

                self.pixel_dict[dict_key] = Game.pixel_encoding[self.triplet_arr[2]]

            self.triplet_arr = []



    def input_getter(self):
        self.usr_inputs += 1
        #get input, draw new screen
        
        Screen.wrapper(self.render)
        key = self.screen.get_event()
        if not key:
            return 0
        key = key.key_code
        print(key)
        if key == 97:#A pressed -> move left
            return -1
        elif key == 100:#D pressed -> move right
            return 1
        else:#don't move the padle if no valid key was pressed
            return 0
        






def task1():
    #only print the game without starting it
    game = Game()

    computer = IntComputer(game.input_getter, game.split_triplets)
    response = computer.run(commands)
    Screen.wrapper(game.score_display)



def task2():
    """
    Start game in playable mode (Controls: A for left, D for right, no key pressed -> don't move peedle)
    """
    game = Game()

    computer = IntComputer(game.input_getter, game.split_triplets)
    commands[0] = 2
    response = computer.run(commands)
    Screen.wrapper(game.score_display)






if __name__ == "__main__":
    task1()#first executre task 1
    task2()#start interactive game