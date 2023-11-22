class intComputer:
    def __init__(self,commands,output):
        self.commands = commands
        self.output = output
        self.index = 0
        self.relativeoffset = 0
        self.numopcode = ""
        self.positionlist = [] 
        self.updatelist = []
        self.opcodedict = {
            "01" : (self.add,3),
            "02" : (self.multiply,3),
            "03" : (self.inp,1),
            "04" : (self.outp,1),
            "05" : (self.jump_if_true,2),
            "06" : (self.jump_if_false,2),
            "07" : (self.less_than,3),
            "08" : (self.equals,3),
            "09" : (self.change_offset,1),
        }

    def add(self):
        self.commands[self.positionlist[2]] = self.commands[self.positionlist[0]] + self.commands[self.positionlist[1]]
        self.index += 4

    def multiply(self):
        self.commands[self.positionlist[2]] = self.commands[self.positionlist[0]] * self.commands[self.positionlist[1]]
        self.index += 4

    def inp(self):
        try: self.commands[self.positionlist[0]] = self.output(self.updatelist) 
        except: raise RuntimeError("wrong input")
        self.updatelist = []
        self.index += 2

    def outp(self):
        self.updatelist.append(self.commands[self.positionlist[0]])
        self.index += 2

    def jump_if_true(self):
        if self.commands[self.positionlist[0]] != 0: self.index = self.commands[self.positionlist[1]]
        else: self.index += 3

    def jump_if_false(self):
        if self.commands[self.positionlist[0]] == 0: self.index = self.commands[self.positionlist[1]]
        else: self.index += 3

    def less_than(self):
        if self.commands[self.positionlist[0]] < self.commands[self.positionlist[1]]: self.commands[self.positionlist[2]] = 1
        else: self.commands[self.positionlist[2]] = 0
        self.index += 4
            
    def equals(self):
        if self.commands[self.positionlist[0]] == self.commands[self.positionlist[1]]: self.commands[self.positionlist[2]] = 1
        else: self.commands[self.positionlist[2]] = 0
        self.index += 4
    
    def change_offset(self):
        self.relativeoffset += self.commands[self.positionlist[0]]
        self.index += 2

    def get_postions(self,nofparams,opcode):
        self.positionlist = []
        for i in range (nofparams):
            if opcode[2-i] == "0": self.positionlist.append(self.commands[self.index+i+1])
            elif opcode[2-i] == "1": self.positionlist.append(self.index+i+1)
            elif opcode[2-i] == "2":
                self.z_fill(self.relativeoffset + self.commands[self.index+i+1])
                self.positionlist.append(self.relativeoffset + self.commands[self.index+i+1])
            else: raise ValueError("wrong mode parameter")
    
    def z_fill(self,element):
        while element > len(self.commands)-1: self.commands.append(0)
        if int(element) < 0: raise IndexError("negative index in modelist")
                
    def main(self):
        while True: 
            opcode = str(self.commands[self.index]).zfill(5)
            self.numopcode = opcode[3:]
            if self.numopcode == "99":
                self.output(self.updatelist)
                print("<<<terminated>>>")
                break
            elif self.opcodedict.get(self.numopcode) != None:
                self.get_postions(self.opcodedict[self.numopcode][1],opcode)
                self.opcodedict[self.numopcode][0]()
            else: raise ValueError(f"wrong opcode: {opcode}")