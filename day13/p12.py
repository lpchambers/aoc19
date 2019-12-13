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
    line = f.read()

int_cmds = [int(x) for x in line.strip().split(',')]

c = OpcodeComputer(int_cmds)
c.run_until_stop()
out = c.pop_outputs()

game = {}

for idx in range(0, len(out), 3):
    game[(out[idx], out[idx+1])] = out[idx+2]


blocks = [pos for pos, tile in game.items() if tile == 2]
print("Part 1", len(blocks))


# Part 2
with open('input') as f:
    line = f.read()

int_cmds = [int(x) for x in line.strip().split(',')]
import time
QUICK = False
sleeptime = 0.04

class Game:
    def __init__(self, c):
        self.c = c
        self.tiles = {}
        self.score = None

    def update_screen(self, out):
        for idx in range(0, len(out), 3):
            if (out[idx], out[idx+1]) == (-1, 0):
                self.score = out[idx+2]
            else:
                self.tiles[(out[idx], out[idx+1])] = out[idx+2]

    def print_game(self):
        if not self.tiles:
            self.c.add_inputs([0])
            return
        minx = min(self.tiles.keys(), key=lambda x: x[0])[0]
        maxx = max(self.tiles.keys(), key=lambda x: x[0])[0]
        miny = min(self.tiles.keys(), key=lambda x: x[1])[1]
        maxy = max(self.tiles.keys(), key=lambda x: x[1])[1]
        xlen = maxx - minx + 1
        ylen = maxy - miny + 1
        blank = ["0" * xlen] * ylen
        for pos, tile in self.tiles.items():
            x, y = pos
            l = blank[y]
            nl = l[:x] + str(tile) + l[x+1:]
            blank[y] = nl
        gamescreen = "\n".join(blank)
        gprint = gamescreen.replace("0", " ").replace("1", "#").replace("2", "*").replace("3", "_").replace("4", "o")
        print(gprint)
        print("Score:", self.score)

    def get_move(self):
        ball_x = [pos for pos, tile in self.tiles.items() if tile == 4][0][0]
        padd_x = [pos for pos, tile in self.tiles.items() if tile == 3][0][0]
        return int(padd_x < ball_x) - int(ball_x < padd_x)


    def run_until_input(self):
        while not self.c.run_until_stop():
            self.update_screen(self.c.pop_outputs())
            if not QUICK:
                self.print_game()
            i = self.get_move()
            self.c.add_inputs([i])
            if not QUICK:
                time.sleep(sleeptime)
        self.update_screen(self.c.pop_outputs())
        if not QUICK:
            self.print_game()

# add 2 quarters
int_cmds[0] = 2
c = OpcodeComputer(int_cmds)
g = Game(c)
g.run_until_input()

print("Part 2", g.score)
