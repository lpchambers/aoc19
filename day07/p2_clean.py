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

num_vals = {
    ADD: 3,
    MUL: 3,
    INP: 1,
    OUT: 1,
    JIT: 2,
    JIF: 2,
    LT: 3,
    EQ: 3,
}


def get_vals_and_locs(opcode, modes, pointer, commands):
    n_vals = num_vals[opcode]
    # Pad leading "0"s and reverse
    modes_str = str(modes).rjust(n_vals, "0")[::-1]
    locs = commands[pointer + 1: pointer + 1 + n_vals]
    vals = [l if mode == "1" else commands[l] for l, mode in zip(locs, modes_str)]
    pointer += n_vals + 1
    return vals, locs, pointer


class OpcodeComputer:
    def __init__(self, commands, inputs=None, pointer=0):
        self.commands = commands
        if inputs is None:
            inputs = []
        self.inputs = inputs
        self.pointer = pointer

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
    
            vals, locs, self.pointer = get_vals_and_locs(opcode, modes, self.pointer, self.commands)
    
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
            else:
                print("FAIL????")

        return True

with open('input') as f:
    lines = f.read()

int_cmds = [int(x) for x in lines.strip().split(',')]

# int_cmds = [3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5]


import itertools
## PART 2
max_output = 0
for combo in itertools.permutations([5,6,7,8,9]):
    computers = [OpcodeComputer(int_cmds.copy(), inputs=[phase]) for phase in combo]
    # Set the initial output (ie input value for computer A)
    outputs = [0]
    while computers:
        opcode_comp = computers.pop(0)
        opcode_comp.add_inputs(outputs)
        prog_over = opcode_comp.run_until_stop()

        # Get the next output
        outputs = opcode_comp.pop_outputs()

        # If the program isn't over, add it to the end of the list
        if not prog_over:
            computers.append(opcode_comp)

    # Check if this output is the biggest
    if outputs[0] > max_output:
        max_output = outputs[0]

print("part 2 output:", max_output)
