#!/usr/bin/python3
END = 99
ADD = 1
MUL = 2
INP = 3
OUT = 4
JIT = 5
JIF = 6
LT = 7
EQ = 8
RBO = 9  # Relative base offset

num_vals = {
    ADD: 3,
    MUL: 3,
    INP: 1,
    OUT: 1,
    JIT: 2,
    JIF: 2,
    LT: 3,
    EQ: 3,
    RBO: 1,
}


def get_vals_and_locs(opcode, modes, pointer, commands, rel_base):
    n_vals = num_vals[opcode]
    # Pad leading "0"s and reverse
    modes_str = str(modes).rjust(n_vals, "0")[::-1]
    locs = commands[pointer + 1: pointer + 1 + n_vals]
    vals = []
    adjusted_locs = []
    for l, mode in zip(locs, modes_str):
        if mode == "1":
            vals.append(l)
            adjusted_locs.append(l)
        elif mode == "0":
            vals.append(commands[l])
            adjusted_locs.append(l)
        elif mode == "2":
            vals.append(commands[l + rel_base])
            adjusted_locs.append(l + rel_base)
        else:
            print("Invalid mode", mode)
    pointer += n_vals + 1
    return vals, adjusted_locs, pointer


MEMPADLEN = 2048

class OpcodeComputer:
    def __init__(self, commands, inputs=None, pointer=0):
        # Pad out the memory
        self.commands = commands + [0] * MEMPADLEN
        if inputs is None:
            inputs = []
        self.inputs = inputs
        self.pointer = pointer

        # Relative base offset
        self.rel_base = 0

        # Store the outputs
        self.outputs = []

    def pop_outputs(self):
        """
        Returns the current state of the outputs register and
        resets it to empty
        """
        ret = self.outputs
        self.outputs = []
        return ret

    def add_inputs(self, inputs):
        """
        Adds more inputs to the Opcode computers input register
        """
        self.inputs += inputs

    def run_until_stop(self):
        """
        Runs the opcode computer until a 99 command is hit,
        or additional input required
        @return: True iff 99 hit, False if more inupt required
        """
        while self.commands[self.pointer] != END:
            # Get the cmd
            cmd = self.commands[self.pointer]
            opcode = cmd % 100
            modes = cmd // 100
    
            vals, locs, self.pointer = get_vals_and_locs(opcode, modes, self.pointer, self.commands, self.rel_base)

            if opcode == ADD:
                self.commands[locs[2]] = vals[0] + vals[1]
            elif opcode == MUL:
                self.commands[locs[2]] = vals[0] * vals[1]
            elif opcode == INP:
                if self.inputs:
                    self.commands[locs[0]] = self.inputs.pop(0)
                else:
                    # Put the pointer back, so we run this opcode again
                    self.pointer -= 2
                    return False
            elif opcode == OUT:
                self.outputs.append(vals[0])
            elif opcode == JIT:
                if vals[0] != 0:
                    self.pointer = vals[1]
            elif opcode == JIF:
                if vals[0] == 0:
                    self.pointer = vals[1]
            elif opcode == LT:
                self.commands[locs[2]] = 1 if vals[0] < vals[1] else 0
            elif opcode == EQ:
                self.commands[locs[2]] = 1 if vals[0] == vals[1] else 0
            elif opcode == RBO:
                self.rel_base += vals[0]
            else:
                print("FAIL????")

        return True

with open('input') as f:
    lines = f.read()

int_cmds = [int(x) for x in lines.strip().split(',')]

BLACK = 0
WHITE = 1
LEFT = 0
RIGHT = 1

class Painter:
    def __init__(self, cmds, inputs=[]):
        self.computer = OpcodeComputer(cmds, inputs=inputs)
        self.colors = {}

        self.posx = 0
        self.posy = 0

        self.dirx = 0
        self.diry = 1

    def rotate(self, direction):
        if direction == LEFT:
            if self.dirx:
                self.diry = self.dirx
                self.dirx = 0
            else:
                self.dirx = -self.diry
                self.diry = 0
        elif direction == RIGHT:
            if self.dirx:
                self.diry = -self.dirx
                self.dirx = 0
            else:
                self.dirx = self.diry
                self.diry = 0
        else:
            print("Unknown direction", direction)

    def move(self):
        self.posx += self.dirx
        self.posy += self.diry

    def paint_section(self, color):
        p = self.get_pos()
        self.colors[p] = color

    def get_color(self):
        p = self.get_pos()
        return self.colors.get(p, BLACK)

    def get_pos(self):
        return (self.posx, self.posy)

    def get_dir(self):
        return (self.dirx, self.diry)

    def run_painter(self):
        while not self.computer.run_until_stop():
            col, rot = self.computer.pop_outputs()
            self.paint_section(col)
            self.rotate(rot)
            self.move()
            self.computer.add_inputs([self.get_color()])

    def get_paint_job(self):
        minx = min(self.colors.keys(), key=lambda x: x[0])[0]
        miny = min(self.colors.keys(), key=lambda x: x[1])[1]
        maxx = max(self.colors.keys(), key=lambda x: x[0])[0]
        maxy = max(self.colors.keys(), key=lambda x: x[1])[1]
        rows = maxy - miny + 1
        cols = maxx - minx + 1
        strs = [str(BLACK) * cols] * rows

        print(minx, maxx)
        print(cols)
        for p, col in self.colors.items():
            x, y = p
            row = strs[maxy-y]
            xi = x - minx
            new_row = row[:xi] + str(col) + row[xi+1:]
            strs[maxy-y] = new_row

        return "\n".join(strs)

# Part 1
painter = Painter(int_cmds, inputs=[BLACK])
painter.run_painter()
print("Part 1", len(painter.colors))
# Part 2
painter = Painter(int_cmds, inputs=[WHITE])
painter.paint_section(WHITE)
painter.run_painter()
BLK = "█"
paintjob = painter.get_paint_job().replace(str(BLACK), BLK).replace(str(WHITE), " ")
print("Part 2")
print(paintjob)
