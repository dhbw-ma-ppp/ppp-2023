import numpy as np
from matplotlib import pyplot as plt
from pathlib import Path
from computer import intComputer

class breakout:
    def __init__(self):
        self.filepath = Path(".") /'data' / 'breakout_commands.txt'
        self.colour = "gist_stern"
        self.pausetimer = 0.0001
        self.computeroutput = []
        self.commands = []
        self.paddle_x = 0
        self.ball_x = 0
        self.highscore = 0
        self.arr = np.zeros((23, 43), dtype=int)

    def get_commands(self):     
        with open(self.filepath, 'r') as file: 
            return [int(line.replace('\n', '')) for line in file]
        
    def tripletinator(self):
        for i in range(0, len(self.computeroutput), 3): 
            yield self.computeroutput[i:i + 3] 

    def update_screen(self, output):
        self.computeroutput = output
        for element in self.tripletinator():
            if element[0] == -1: self.highscore = element[2] 
            else:
                self.arr[element[1], element[0]] = element[2]
                if element[2] == 3: self.paddle_x = element[0]
                elif element[2] == 4: self.ball_x = element[0]
        plt.cla()
        plt.imshow(self.arr,cmap = self.colour)
        plt.title(f"highscore: {self.highscore}") 
        plt.show(block=False)   #*Note: for part 1 remove block False and change first number in breakout commands from 2 to 1
        plt.pause(self.pausetimer) 
        return self.AI()

    def AI(self):
        if self.paddle_x < self.ball_x: return +1
        elif self.paddle_x > self.ball_x: return -1
        else: return 0
        
    def main(self):
        self.commands = self.get_commands()
        plt.imshow(self.arr,cmap = self.colour)
        intcomp = intComputer(self.commands, self.update_screen)
        plt.title(f"highscore: {self.highscore}") 
        plt.show(block=False)
        intcomp.main()  

run = breakout()
run.main()