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

from computer import Computer
import curses
from time import sleep
import pygame
from random import randint

# game speed increases over time
SLEEP_BETWEEN_FRAMES = 0.1
SLEEP_MULT_PER_FRAME = 0.99


def read_input_file():
    with open("./data/breakout_commands.txt", "r") as file:
        return [int(c) for c in file.readlines()]
    
commands = read_input_file()
commands[0] = 2 # interactive mode


class KI:
    ball_x = 0
    pedal_x = 0

    def update(self, ball_x, pedal_x):
        self.ball_x = ball_x
        self.pedal_x = pedal_x

    def get_next_move(self):
        if self.ball_x > self.pedal_x:
            return 1
        elif self.ball_x < self.pedal_x:
            return -1
        else:
            return 0

class Terminal:
    def __init__(self, commands) -> None:
        self.commands = commands
        self.output = []
        self.ki = KI()
        curses.wrapper(self.main)

    def main(self, screen):
        self.screen = screen
        screen.clear()

        # init curses
        curses.curs_set(0)

        curses.start_color()
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_RED, curses.COLOR_BLACK)

        computer = Computer(self.input_callback, self.output_callback)
        computer.run(commands)
        screen.refresh()

    # called when int-computer requests input
    def input_callback(self):
        global SLEEP_INCREASE_PER_FRAME, SLEEP_BETWEEN_FRAMES
        self.screen.refresh()
        SLEEP_BETWEEN_FRAMES *= SLEEP_MULT_PER_FRAME
        sleep(SLEEP_BETWEEN_FRAMES)

        for i in range(0, len(self.output), 3):
            x, y, t = self.output[i:i+3]
            
            if (x == -1):
                self.score = t
                print(f"Score: {self.score}")
                continue

            if (t == 3): self.ki.pedal_x = x
            if (t == 4): self.ki.ball_x = x
            # wall, block, pedal, ball
            self.screen.addstr(y, x, [" ", "▓", "█", "▂", "▅"][t], curses.color_pair(t))

        self.output.clear()
        return  self.ki.get_next_move()
    
    # called when int-computer provides output
    def output_callback(self, value):
        self.output.append(value)

class Graphical:
    def __init__(self, commands) -> None:
        self.framerate = 20
        self.cell_scale = 15
        self.block_colors = ["#85c86f", "#67b1f2", "#8489e2", "#ba82ea", "#fd6669", "#f7aa67"]
        self.extra_lines_bottom = 5

        self.ki = KI()
        pygame.init()
        pygame.font.init()
        self.font = pygame.font.SysFont('Consolas', self.cell_scale)
        self.screen = pygame.display.set_mode((43*self.cell_scale, (23+self.extra_lines_bottom)*self.cell_scale))
        self.clock = pygame.time.Clock()
        self.running = True
        self.dimensions = self.screen.get_size()
        self.grid_dimensions = [43, 23]
        self.computer_output = []
        self.score = 0
        self.gameover = False
        self.paused = True
        self.screen.fill("white")
        Computer(self.update, self.output_callback).run(commands)
        self.gameover = True
        while self.running:
            self.update()

    def output_callback(self, value):
        self.computer_output.append(value)


    def update(self):
        screen = self.screen
        clock = self.clock
        while True: # should get stuck in loop while paused
            if self.running:
                for i in range(0, len(self.computer_output), 3):
                    x, y, t = self.computer_output[i:i+3]
                
                    if (x == -1):
                        self.score = t
                        pygame.display.set_caption(f"Score: {t}")
                        continue

                    if (t == 3): self.ki.pedal_x = x
                    if (t == 4): self.ki.ball_x = x
                    xd = self.dimensions[0] / self.grid_dimensions[0]
                    yd = (self.dimensions[1]-self.extra_lines_bottom*self.cell_scale) / self.grid_dimensions[1]

                    if t == 0: # empty
                        pygame.draw.rect(screen, "white", (xd*x, yd*y, xd, yd))
                    elif t == 1: # wall
                        pygame.draw.rect(screen, "black", (xd*x, yd*y, xd, yd))
                    elif t == 2: # block
                        color = self.block_colors[randint(0, len(self.block_colors)-1)]
                        #color = self.block_colors[y%len(self.block_colors)]
                        pygame.draw.rect(screen, color, (xd*x, yd*y, xd, yd))
                    elif t == 3: # pedal
                        pygame.draw.rect(screen, "black", (xd*x, yd*y, xd, yd*0.5))
                    elif t == 4: # ball
                        pygame.draw.circle(screen, "gray", (int(xd*x+xd*0.5), int(yd*y+yd*0.5)), int(xd*0.5))

                
                self.computer_output.clear()
                # text
                pygame.draw.rect(screen, "black", (0, self.cell_scale*23, 43*self.cell_scale, self.cell_scale*self.extra_lines_bottom))
                pygame.draw.rect(screen, "white", (self.cell_scale, self.cell_scale*23, self.cell_scale*41, self.cell_scale*self.extra_lines_bottom))

                if self.paused:     state = '<PAUSED>  '
                elif self.gameover: state = "<GAMEOVER>"
                else:               state = "<RUNNING> "
                text_lines = [f"{state}{' '*5}FRAMERATE: {self.framerate}{' '*5}SCORE: {self.score}",
                        "", f"[SPACE]: Pause/Resume     [UP]: Speed Up     [DOWN]: Speed Down",
                    "INFO:  Pedal can be controlled manually in PAUSE mode. (Arrow Keys)"]
                
                for i in range(len(text_lines)):
                    text_render = self.font.render(text_lines[i], False, "black")
                    screen.blit(text_render, (self.cell_scale*2, self.cell_scale*(23+i)))
                    

                pygame.display.flip()
                clock.tick(self.framerate) 
                
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                    elif event.type == pygame.KEYDOWN:
                        pressed = pygame.key.get_pressed()
                        if pressed[pygame.K_SPACE]:
                            self.paused = not self.paused
                        if self.paused:
                            if pressed[pygame.K_LEFT]:
                                self.computer_output.clear()
                                return -1
                            if pressed[pygame.K_RIGHT]:
                                return 1
                            if pressed[pygame.K_UP] or pressed[pygame.K_DOWN]:
                                return 0
                        else:
                            if pressed[pygame.K_UP]:
                                self.framerate += 5
                            if pressed[pygame.K_DOWN]:
                                self.framerate -= 5
                                if self.framerate < 1: self.framerate = 1
                        
                        
            else: 
                pygame.quit()

            if not self.paused or not self.running: break

        return self.ki.get_next_move()




if __name__ == "__main__":
    Graphical(commands)

# Highscore: 17086