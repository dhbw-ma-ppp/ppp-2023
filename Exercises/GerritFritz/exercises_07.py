from computer import Computer
import pyglet
from pyglet import shapes
import random

class Breakout():
    def __init__(self, commands, mode):
        commands[0] = mode
        self.mode = mode
        self.screen_data = []
        self.screen_dict = {}
        self.speed = 1
        self.frame = 0
        self.computer = Computer(commands, self)
        self.setup_canvas()
        pyglet.app.run()

    def setup_canvas(self):
        window = pyglet.window.Window(800, 500)
        self.batch = pyglet.graphics.Batch()
        value = window.get_size()
        self.screen_width = value[0]
        self.screen_height = value[1]
        block_num = (43,23)
        self.block_width = self.screen_width/block_num[0]
        self.block_height = self.screen_height/block_num[1]
        
        @window.event
        def on_draw():
            self.screen_data = []
            self.computer.get_frame()
            self.format_screen_data()
            self.move_paddle()
            if not (self.frame%self.speed):
                self.draw_screen()
            
            window.clear()
            self.batch.draw()
            self.frame += 1
    
    def move_paddle(self):
        diff = self.paddle_position[0] - self.ball_position[0]
        if diff > 0: self.paddle_offset = -1
        elif diff < 0: self.paddle_offset = 1
        else: self.paddle_offset = 0
    
    def format_screen_data(self):
        self.new_dict = {}
        for i in range(0,len(self.screen_data),3):
            block_x = self.screen_data[i]
            block_y = self.screen_data[i+1]
            entity = self.screen_data[i+2]
            if self.screen_data[i+2] == 3:
                self.paddle_position = (block_x,block_y)
            elif self.screen_data[i+2] == 4:
                self.ball_position = (block_x,block_y)
            elif block_x == -1:
                pass
                continue
        
            self.new_dict[(block_x,block_y)] = [entity]
        self.screen_dict.update(self.new_dict)
    
    def draw_screen(self):
        for position in self.screen_dict.keys():
            match self.screen_dict[position][0]:
                case 1: shape = self.rectangle(position, (100,100,100))
                case 2: shape = self.rectangle(position, (random.randint(0,255),random.randint(0,255),random.randint(0,255))) if not self.frame else self.screen_dict[position]
                case 3: shape = self.rectangle(position, (0,255,0))
                case 4: shape = shapes.Circle(position[0]*self.block_width, self.screen_height-(position[1]*self.block_height), self.block_width//2, color=(255, 255, 255), batch=self.batch)
            self.screen_dict[position] = [self.screen_dict[position][0], shape]
    
    def rectangle(self, position, color):
        return shapes.Rectangle(position[0]*self.block_width, self.screen_height-(position[1]*self.block_height), self.block_width, self.block_height, color=color, batch=self.batch) 

with open("data//breakout_commands.txt") as file:
    commands = [int(line[:-1]) for line in file]
game = Breakout(commands, 2)