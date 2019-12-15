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

    def copy(self):
        """
        Returns a copy of the computer
        """
        op = OpcodeComputer(self.commands, pointer=self.pointer)
        return op

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

N = 1
S = 2
W = 3
E = 4
DIRS = (N, S, E, W)

dname = {N: "N", S: "S", E: "E", W: "W"}

WALL = 0
MOVE = 1
OXYGEN = 2

class Map:
    def __init__(self):
        self.walls = set()
        self.path = {(0, 0)}

    def has_pos(self, pos):
        return pos in self.walls or pos in self.path

    def print_map(self, droidx, droidy):
        xmin = min(self.walls.union(self.path).union({(droidx, droidy)}), key=lambda x: x[0])[0]
        xmax = max(self.walls.union(self.path).union({(droidx, droidy)}), key=lambda x: x[0])[0]
        ymin = min(self.walls.union(self.path).union({(droidx, droidy)}), key=lambda x: x[1])[1]
        ymax = max(self.walls.union(self.path).union({(droidx, droidy)}), key=lambda x: x[1])[1]

        dx = xmax - xmin + 1
        dy = ymax - ymin + 1
        lines = [" " * dx] * dy
        for x, y in self.walls:
            x -= xmin
            y -= ymin
            l = lines[y]
            lines[y] = l[:x] + "#" + l[x+1:]
        for x, y in self.path:
            x -= xmin
            y -= ymin
            l = lines[y]
            lines[y] = l[:x] + "." + l[x+1:]

        x = droidx
        y = droidy
        x -= xmin
        y -= ymin
        l = lines[y]
        lines[y] = l[:x] + "D" + l[x+1:]

        print("\n".join(lines))

class Droid:
    def __init__(self, computer, shipmap, x=0, y=0):
        self.computer = computer
        self.shipmap = shipmap
        self.x = x
        self.y = y

    def move(self, x, y, m):
        if m == N:
            y -= 1
        elif m == S:
            y += 1
        elif m == E:
            x += 1
        elif m == W:
            x -= 1
        return (x, y)

    def get_next_explore(self):
        for d in DIRS:
            nextpos = self.move(self.x, self.y, d)
            if nextpos not in self.shipmap.walls and nextpos not in self.shipmap.path:
                return d

        # No unexplored paths, pick 1 we know will work
        print(self.x, self.y)
        for d in DIRS:
            nextpos = self.move(self.x, self.y, d)
            if nextpos not in self.shipmap.walls:
                return d

        # Should not get here (surounded by walls)
        print("SURROUNDED BY WALLLSSS!!!!")
        return N

    def do_move(self, d):
        self.computer.add_inputs([d])
        self.computer.run_until_stop()

        out = self.computer.pop_outputs()
        ret = out[0]

        if ret == WALL:
            self.shipmap.walls.add(self.move(self.x, self.y, d))
            return False
        elif ret == MOVE:
            self.x, self.y = self.move(self.x, self.y, d)
            self.shipmap.path.add((self.x, self.y))
            return True
        elif ret == OXYGEN:
            self.x, self.y = self.move(self.x, self.y, d)
            print("Found Oxygen", self.x, self.y)
            return True
        else:
            print("Unknown return", ret)
            return False

    def copy(self):
        return Droid(self.computer.copy(), self.shipmap, self.x, self.y)

    def explore(self):
        for d in DIRS:
            nextpos = self.move(self.x, self.y, d)
            if not self.shipmap.has_pos(nextpos):
                new_droid = self.copy()
                if new_droid.do_move(d):
                    new_droid.explore()

    def run(self):
        ret = MOVE
        while ret != OXYGEN:
            d = self.get_next_explore()
            print("Moving", d, dname[d])
            self.computer.add_inputs([d])

            self.computer.run_until_stop()

            out = self.computer.pop_outputs()
            ret = out[0]

            if ret == WALL:
                self.shipmap.walls.add(self.move(self.x, self.y, d))
            elif ret == MOVE:
                self.x, self.y = self.move(self.x, self.y, d)
                self.shipmap.path.add((self.x, self.y))
            elif ret == OXYGEN:
                self.x, self.y = self.move(self.x, self.y, d)
                print("Found Oxygen", self.x, self.y)
            else:
                print("Unknown return", ret)

            self.print_map()

        # Out of loop
        self.oxygen = (self.x, self.y)


c = OpcodeComputer(int_cmds)
shipmap = Map()
droid = Droid(c, shipmap)
droid.explore()
shipmap.print_map(droid.x, droid.y)
