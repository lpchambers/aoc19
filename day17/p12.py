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


MEMPADLEN = 4096

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

SCAFFOLD = "#"
SPACE = "."
NL = "\n"

UP = "^"
DOWN = "v"
LEFT = "<"
RIGHT = ">"

computer = OpcodeComputer(int_cmds)
computer.run_until_stop()
out = computer.pop_outputs()

vis = "".join([chr(c) for c in out])
print(vis)
vl = vis.splitlines()

# Search for
#   .#.  single
#   ###  triple
#   .#.  single
single = set()
triple = set()
SINGLE = ".#."
TRIPLE = "###"

for rix, row in enumerate(vl):
    for cix in range(len(row)):
        si = row.find(SINGLE, cix)
        ti = row.find(TRIPLE, cix)
        if si != -1:
            single.add((rix, si+1))
        if ti != -1:
            triple.add((rix, ti+1))

param = 0
for mid in triple:
    r, c = mid
    if (r-1, c) in single and (r+1, c) in single:
        param += r * c

print("Part 1", param)

# Part 2
with open('input') as f:
    line = f.read()

def int_to_chrs(ints):
    return "".join([chr(c) for c in out])

def chrs_to_ints(chrs):
    return [ord(x) for x in chrs]

def find_robot(lines):
    """
    Returns a pos and a dir
    """
    for rix, row in enumerate(lines):
        for d in [LEFT, RIGHT, UP, DOWN]:
            if d in row:
                return ((rix, row.find(d)), d)

dirs = {
    LEFT: (0, -1),
    RIGHT: (0, 1),
    UP: (-1, 0),
    DOWN: (1, 0),
}

opp_dir = {
    LEFT: RIGHT,
    RIGHT: LEFT,
    UP: DOWN,
    DOWN: UP,
}

def find_next_dir(lines, pos, cur_dir):
    x, y = pos
    opp = opp_dir[cur_dir]
    for name, delta in dirs.items():
        if name == cur_dir or name == opp:
            continue  # Don't repeat same axis
        dx, dy = delta
        try:
            if lines[x+dx][y+dy] == SCAFFOLD:
                return name
        except:
            continue
    return None

def get_turn(cur_dir, next_dir):
    if cur_dir == UP:
        return "L" if next_dir == LEFT else "R"
    elif cur_dir == LEFT:
        return "L" if next_dir == DOWN else "R"
    elif cur_dir == DOWN:
        return "L" if next_dir == RIGHT else "R"
    elif cur_dir == RIGHT:
        return "L" if next_dir == UP else "R"
    else:
        print("Unknown current dir", cur_dir)

def find_dist(lines, pos, cur_dir):
    x, y = pos
    dx, dy = dirs[cur_dir]
    n = 0
    next_brick = SCAFFOLD
    while next_brick == SCAFFOLD:
        n += 1
        x += dx
        y += dy
        try:
            next_brick = lines[x+dx][y+dy]
        except:
            break
    return (n, (x, y))


int_cmds = [int(x) for x in line.strip().split(',')]
int_cmds[0] = 2

computer = OpcodeComputer(int_cmds)
computer.run_until_stop()
out = computer.pop_outputs()

vis = int_to_chrs(out)
print(vis)
vl = vis.splitlines()

pos, cur_dir = find_robot(vl)
print(pos)
print(cur_dir)

moves = []

while True:
    next_dir = find_next_dir(vl, pos, cur_dir)
    if next_dir is None:
        break
    moves.append(get_turn(cur_dir, next_dir))
    cur_dir = next_dir
    distance, pos = find_dist(vl, pos, cur_dir)
    moves.append(distance)

print(moves)
print(len(moves), "Moves")

mstr = ",".join([str(c) for c in moves])

print(mstr)
# Find the longest match

patlen = {}
for x in range(1, 21):
    match_idx = set()
    pat = mstr[0:x]
    for start_idx in range(len(mstr)):
        match_idx.add(mstr.find(pat, start_idx))
    patlen[x] = len(match_idx) - 1

maxlen = max([l for l, n in patlen.items() if n > 1])
print("A Pattern length", maxlen)
APAT = mstr[:maxlen]
print(APAT)

after_a = mstr.replace(APAT, "A")
print("After A", after_a)
BPAT = "L,12,R,10,L,4"
after_b = mstr.replace(APAT, "A").replace(BPAT, "B")
print("After B", after_b)
CPAT = "L,12,L,6,L,4,L,4"

after_c = mstr.replace(APAT, "A").replace(BPAT, "B").replace(CPAT, "C")
print("After C", after_c)

print()
print("APAT", len(APAT), APAT)
print("BPAT", len(BPAT), BPAT)
print("CPAT", len(CPAT), CPAT)
print("ROUTINE", len(after_c), after_c)

aint = chrs_to_ints(APAT + NL)
bint = chrs_to_ints(BPAT + NL)
cint = chrs_to_ints(CPAT + NL)
routine_int = chrs_to_ints(after_c + NL)

# Routine
computer.add_inputs(routine_int)
computer.run_until_stop()
out = computer.pop_outputs()
vis = "".join([chr(c) for c in out])
print("Computer out:", vis)

# Function A
computer.add_inputs(aint)
computer.run_until_stop()
out = computer.pop_outputs()
vis = "".join([chr(c) for c in out])
print("Computer out:", vis)

# Function B
computer.add_inputs(bint)
computer.run_until_stop()
out = computer.pop_outputs()
vis = "".join([chr(c) for c in out])
print("Computer out:", vis)

# Function C
computer.add_inputs(cint)
computer.run_until_stop()
out = computer.pop_outputs()
vis = "".join([chr(c) for c in out])
print("Computer out:", vis)

# Video feed?
FEED = False
if FEED:
    fval = chrs_to_ints("y" + NL)
else:
    fval = chrs_to_ints("n" + NL)

computer.add_inputs(fval)
computer.run_until_stop()
out = computer.pop_outputs()
print(out[-1])
vis = "".join([chr(c) for c in out])
print("Computer out:", vis)
