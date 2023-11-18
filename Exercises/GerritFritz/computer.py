class Computer:
    def __init__(self, commands, UI):
        self.commands = commands
        self.UI = UI
        self.offset = 0
        self.memory_pointer = 0
        self.opcode = 0
        self.positions = []
        self.mode = "000"
        self.terminated = False

        self.opcodes = {
        1: self.add,
        2: self.mul,
        3: self.inp,
        4: self.out,
        5: self.jump_True,
        6: self.jump_False,
        7: self.less,
        8: self.equals,
        9: self.offset_increment,
        }

    def add(self):
        self.commands[self.positions[2]] = self.commands[self.positions[0]] + self.commands[self.positions[1]]
        self.memory_pointer += 4
        
    def mul(self):
        self.commands[self.positions[2]] = self.commands[self.positions[0]] * self.commands[self.positions[1]]
        self.memory_pointer += 4

    def inp(self):
        try: self.commands[self.positions[0]] = self.UI.paddle_offset
        except: raise RuntimeError("invalid input")
        self.memory_pointer += 2

    def out(self):
        self.UI.screen_data.append(self.commands[self.positions[0]])
        self.memory_pointer += 2

    def jump_True(self):
        if self.commands[self.positions[0]] != 0:  self.memory_pointer = self.commands[self.positions[1]]
        else: self.memory_pointer += 3

    def jump_False(self):
        if self.commands[self.positions[0]] == 0: self.memory_pointer = self.commands[self.positions[1]]
        else: self.memory_pointer += 3

    def less(self):
        if self.commands[self.positions[0]] < self.commands[self.positions[1]]: self.commands[self.positions[2]] = 1
        else: self.commands[self.positions[2]] = 0
        self.memory_pointer += 4
        
    def equals(self):
        if self.commands[self.positions[0]] == self.commands[self.positions[1]]: 
            self.commands[self.positions[2]] = 1
        else: 
            self.commands[self.positions[2]] = 0
        self.memory_pointer += 4

    def offset_increment(self):
        self.offset += self.commands[self.positions[0]]
        self.memory_pointer += 2

    def mode_to_index(self):
        self.positions  = []
        for i in range(0,len(self.mode)):
            if len(self.commands)>self.memory_pointer+i+1:
                local_mode = self.mode[i]
                match local_mode:
                    case "0": self.positions.append(self.commands[self.memory_pointer+i+1])
                    case "1": self.positions.append(self.memory_pointer+i+1)
                    case "2": self.positions.append(self.offset+self.commands[self.memory_pointer+i+1])
                    case _: raise KeyError(f"Wrong mode {self.mode}")
            else:
                raise IndexError(f"out of range")
                    
        for i, position in enumerate(self.positions):
            if position>len(self.commands)-1:
                self.commands += [0]*(position-(len(self.commands)-1))
        
    def get_commands(self):
        command_tuple = divmod(self.commands[self.memory_pointer],100)
        self.opcode = command_tuple[1]
        self.mode = f"{command_tuple[0]:03d}"[::-1]

    def get_frame(self):
        while self.commands[self.memory_pointer] != 99:
            if self.commands[self.memory_pointer] == 3 and len(self.UI.screen_data):
                break
            self.get_commands()
            if self.opcode in self.opcodes.keys():
                self.mode_to_index()
                self.opcodes[self.opcode]()
            else: raise KeyError(f"Wrong opcode {self.opcode}")
        if self.commands[self.memory_pointer] == 99:
            print("terminated")
            self.terminated = True