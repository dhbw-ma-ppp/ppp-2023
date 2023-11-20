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
        self.colors = [(255,255,255),(100,100,100), (0,0,255), (255, 0, 0)]
        self.block_color_interval = [(10,100),(10,200),(10,100)]
        self.frame = 0
        self.block_num = (43,23)
        self.speed = 10
        self.start = False

        self.computer = Computer(commands, self)
        self.setup_canvas()
        pyglet.clock.schedule_interval(self.update_game, 10**(-self.speed))
        pyglet.clock.schedule_interval(self.draw_screen, 0.0125)
        pyglet.app.run()

    def setup_canvas(self):
        self.window = pyglet.window.Window(fullscreen = True)
        window = self.window
        self.window.switch_to()
        self.batch = pyglet.graphics.Batch()
        self.block_width = self.window.width/self.block_num[0]
        self.block_height = self.window.height/self.block_num[1]
        self.window.set_caption("Breakout")
        self.label = pyglet.text.Label('Test',
                          font_name='Times New Roman',
                          font_size=self.window.width/40,
                          x=self.window.width*.85, y=self.window.height*.98,
                          anchor_x='center', anchor_y='center',
                          color=(0,0,0,255),
                          batch=self.batch)
        self.start_label = pyglet.text.Label('Press Space key to start',
                          font_name='Times New Roman',
                          font_size=self.window.width/40,
                          x=self.window.width/2, y=self.window.height/2,
                          anchor_x='center', anchor_y='center',
                          color=(255,255,255,255))
        self.start_label.draw()
        
        @window.event
        def on_key_press(symbol, modifiers):
            if symbol == 32: self.start = True

    def draw_screen(self, dt):
        if not self.start:
            self.window.clear()
            self.start_label.draw()
        else:
            self.window.clear()
            self.batch.draw()
            
    def update_game(self, dt):
        if self.start:
            self.screen_data = []   
            if not(self.computer.terminated):
                self.computer.get_frame()
            self.format_screen_data()
            self.move_paddle()
            self.frame += 1

    def move_paddle(self):
        diff = self.paddle_position[0] - self.ball_position[0]
        if diff > 0: self.paddle_offset = -1
        elif diff < 0: self.paddle_offset = 1
        else: self.paddle_offset = 0
    
    def format_screen_data(self):
        self.new_dict = {}
        for i in range(0,len(self.screen_data),3):
            entity = self.screen_data[i+2]
            position = (self.screen_data[i], self.screen_data[i+1])
            shape = None
            if   entity == 0: shape = self.rectangle(position, self.colors[0])
            elif entity == 1 and not(self.frame): 
                shape = self.rectangle(position, self.colors[1])
            elif entity == 2 and not(self.frame): 
                shape = self.rectangle(position, self.random_color())
            elif entity == 3: 
                self.paddle_position = position
                shape = self.rectangle(position, self.colors[2])
            elif entity == 4: 
                self.ball_position = position
                shape = (self.rectangle(position, self.colors[0]),self.circle(position, self.colors[3]))
            elif entity == -1:
                self.label.text = "Score "+str(entity)
                continue
            if shape:
                self.screen_dict[position] = [entity, shape]

    
    def rectangle(self, position, color):
        return shapes.Rectangle(position[0]*self.block_width, 
                                self.window.height-(position[1]*self.block_height), 
                                self.block_width, self.block_height, color=color, 
                                batch=self.batch) 

    def circle(self, position, color):
        return shapes.Circle(position[0]*self.block_width, 
                             self.window.height-(position[1]*self.block_height), 
                             self.block_width//2, color=color, batch=self.batch)
    
    def random_color(self):
        return (random.randint(*self.block_color_interval[0]),
                random.randint(*self.block_color_interval[1]),
                random.randint(*self.block_color_interval[2]))
    
    
with open("data//breakout_commands.txt") as file:
    commands = [int(line[:-1]) for line in file]
game = Breakout(commands, 2)