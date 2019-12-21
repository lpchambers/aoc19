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

n = 0
beam = []
computer = OpcodeComputer(int_cmds)
for x in range(50):
    for y in range(50):
        computer = OpcodeComputer(int_cmds.copy())
        computer.add_inputs([x, y])
        computer.run_until_stop()
        if computer.pop_outputs() == [1]:
            beam.append((x, y))
            n += 1
print("Part 1", n)

lines = ["." * 50] * 50
for x, y in beam:
    l = lines[y]
    l = l[:x] + "#" + l[x+1:]
    lines[y] = l

print("\n".join(lines))

def test_valid(x, y):
    computer = OpcodeComputer(int_cmds.copy())
    computer.add_inputs([x, y])
    computer.run_until_stop()
    return computer.pop_outputs() == [1]

def fits_box(x, y):
    return test_valid(x+99, y+99) and test_valid(x, y+99) and test_valid(x+99,y)

should_break = False
prev_x_start = 0
for y in range(99, 10000):
    prev = False
    xstart = 0
    for x in range(prev_x_start, 10000):
        print(x, y)
        if test_valid(x, y):
            prev = True
            if xstart == 0:
                xstart = x
            if fits_box(x, y):
                print("x", x, "y", y)
                X = x
                Y = y
                should_break = True
                break
        else:
            if prev:
                break
    prev_x_start = xstart
    if should_break:
        break
print(x * 10000 + y)
