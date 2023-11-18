import tkinter
import turtle
from computer import Computer


class Breakout():
    def __init__(self, commands, mode):
        commands[0] = mode
        self.mode = mode
        self.highscore = 0
        self.screen_data = []
        self.screen_dict = {}
        self.frame_counter = 0
        self.percentage = 0
        self.timepause = 0
        self.computer = Computer(commands, self)
        self.color_map = ["white", "grey", "green", "blue", "red"]
        self.stopped = True
        self.skipping = False 
        self.setup_canvas()
        self.after_id = self.window.after(self.timepause, lambda:self.game_loop())
        self.window.mainloop()

    def game_loop(self):
        if not self.stopped or not self.frame_counter:
            self.screen_data = []
            self.computer.get_frame()
            self.format_screen_data()
            self.move_paddle()
        self.draw_screen()
        if self.mode == 2:
            self.after_id = self.window.after(self.timepause, lambda:self.game_loop())

    def setup_canvas(self):
        self.window = tkinter.Tk()
        self.window.title("Breakout game")
        
        self.width, self.height = self.window.maxsize()
        self.width*=1
        self.height*=.9

        upper_grid = tkinter.Frame(master= self.window)
        self.canvas = tkinter.Canvas(master= self.window, width= self.width, height= self.height)
        self.highscore_label = tkinter.Label(master= upper_grid, text= self.highscore)
        self.frame_counter_label = tkinter.Label(master= upper_grid, text= self.frame_counter)
        self.percentage_label = tkinter.Label(master= upper_grid, text= self.percentage)
        self.skip_button = tkinter.Button(master= upper_grid, text= "start skip", command= self.skip)
        self.exit_button = tkinter.Button(master= upper_grid, text= "Exit", command= self.window.destroy)
        self.start_button = tkinter.Button(master= upper_grid, text= "Start", command= self.stop)

        for i in range(6):
            tkinter.Grid.columnconfigure(upper_grid, i, weight=1)
            
        upper_grid.pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=True)
        self.start_button.grid (column=0, row=0, sticky=tkinter.NSEW)
        self.skip_button.grid (column=1, row=0, sticky=tkinter.NSEW)
        self.highscore_label.grid(column=2, row=0, sticky=tkinter.NSEW)
        self.frame_counter_label.grid(column=3, row=0, sticky=tkinter.NSEW)
        self.percentage_label.grid(column=4, row=0, sticky=tkinter.NSEW)
        self.exit_button.grid(column=5, row=0, sticky=tkinter.NSEW)
        self.canvas.pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=True)
        
        self.screen = turtle.TurtleScreen(self.canvas)
        self.screen.tracer(0)
        self.pointer = turtle.RawTurtle(self.screen)
        self.pointer.ht()
        self.pointer.up()
        self.pointer.setundobuffer(None)
    
    def stop(self):
        self.stopped = not self.stopped
        self.start_button.configure(text=["stop","start"][self.stopped])
    
    def skip(self):
        self.skipping = not self.skipping
        self.skip_button.configure(text=["stop skip","start skip"][not self.skipping])
        
    def format_screen_data(self):
        self.new_dict = {}
        for i in range(0,len(self.screen_data),3):
            if self.screen_data[i+2] == 3:
                self.paddle_position = (self.screen_data[i],self.screen_data[i+1])
            elif self.screen_data[i+2] == 4:
                self.ball_position = (self.screen_data[i],self.screen_data[i+1])
            elif self.screen_data[i] == -1:
                self.highscore_label.config(text = f"Score: {self.screen_data[i+2]:10}") 
                continue
            self.new_dict[(self.screen_data[i],self.screen_data[i+1])] = self.screen_data[i+2]
        self.screen_dict.update(self.new_dict)
        
   
    def move_paddle(self):
        diff = self.paddle_position[0] - self.ball_position[0]
        if diff > 0: self.paddle_offset = -1
        elif diff < 0: self.paddle_offset = 1
        else: self.paddle_offset = 0
        
    def draw_screen(self):
        if not self.frame_counter:
            self.max_x_square, self.min_x_square = max([x for x,_ in self.screen_dict.keys()]), min([x for x,_ in self.screen_dict.keys()])
            self.max_y_square, self.min_y_square = max([y for _,y in self.screen_dict.keys()]), min([y for _,y in self.screen_dict.keys()])
            self.square_width = self.width/(self.max_x_square - self.min_x_square)
            self.square_height = self.height/(self.max_y_square - self.min_y_square)
            self.max_blocks = len([0 for pos in self.screen_dict.keys() if self.screen_dict[pos] == 2])
            self.current_blocks = 0
            
        self.current_blocks = len([0 for pos in self.screen_dict.keys() if self.screen_dict[pos] == 2])
        self.percentage  = 100-(self.current_blocks*100//self.max_blocks)
        self.percentage_label.config(text = f"Percentage: {self.percentage:10}%") 

        self.frame_counter += 1
        self.frame_counter_label.config(text = f"Frame: {self.frame_counter:10}") 
        
        self.pointer.clear()
        for position in self.screen_dict.keys():
            if not self.skipping:
                entity= self.screen_dict[position]
                if entity in [2,1]: self.draw_shape(position, self.color_map[entity], self.draw_rectangle)
                elif entity == 4: self.draw_shape(position, self.color_map[4], self.draw_ball)
                elif entity == 3: self.draw_shape(position, self.color_map[3], self.draw_paddle)
        self.screen.update()

    def draw_shape(self, position, color, shape):
        x_position = (self.width/2)-position[0]*self.square_width
        y_position = (self.height/2)-position[1]*self.square_height
        self.pointer.goto(x_position,y_position)
        self.pointer.fillcolor(color)
        self.pointer.begin_fill()
        self.pointer.setheading(90)
        shape()
        self.pointer.end_fill()
        
    def draw_rectangle(self):
        self.pointer.fd(self.square_height/2)
        self.pointer.left(90)
        self.pointer.fd(self.square_width/2)
        for i in range(4):
            self.pointer.left(90)
            self.pointer.fd(self.square_height if not i % 2 else self.square_width)
        
    def draw_ball(self):
        offset = min((self.square_width, self.square_height))
        self.pointer.circle(radius=offset/2)
    
    def draw_paddle(self):
        self.pointer.fd(self.square_height/2)
        self.pointer.left(90)
        self.pointer.fd(self.square_width*2)
        for i in range(4):
            self.pointer.left(90)
            self.pointer.fd(self.square_height if not i % 2 else self.square_width*4)


with open("data//breakout_commands.txt") as file:
    commands = [int(line[:-1]) for line in file]

game = Breakout(commands, 2)
