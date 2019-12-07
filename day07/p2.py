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


def computer(commands, inputs, pointer=0):
    outputs = []
    early_break = False
    while commands[pointer] != END:
        # Get the cmd
        cmd = commands[pointer]
        opcode = cmd % 100
        modes = cmd // 100

        if opcode == END:
            break

        vals, locs, pointer = get_vals_and_locs(opcode, modes, pointer, commands)

        if opcode == ADD:
            commands[locs[2]] = vals[0] + vals[1]
        elif opcode == MUL:
            commands[locs[2]] = vals[0] * vals[1]
        elif opcode == INP:
            commands[locs[0]] = inputs.pop(0)
        elif opcode == OUT:
            outputs.append(vals[0])
            early_break = True
            break
        elif opcode == JIT:
            if vals[0] != 0:
                pointer = vals[1]
        elif opcode == JIF:
            if vals[0] == 0:
                pointer = vals[1]
        elif opcode == LT:
            commands[locs[2]] = 1 if vals[0] < vals[1] else 0
        elif opcode == EQ:
            commands[locs[2]] = 1 if vals[0] == vals[1] else 0
        else:
            print("FAIL????")
    return commands, outputs, inputs, pointer, early_break

with open('input') as f:
    lines = f.read()

int_cmds = [int(x) for x in lines.strip().split(',')]

# int_cmds = [3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5]


import itertools
## PART 2
max_output = 0
for combo in itertools.permutations([5,6,7,8,9]):
    p1, p2, p3, p4, p5 = combo
    # Computer 1 - 5: cmds, intputs, pointer
    c1 = ([p1], int_cmds.copy(), 0)
    c2 = ([p2], int_cmds.copy(), 0)
    c3 = ([p3], int_cmds.copy(), 0)
    c4 = ([p4], int_cmds.copy(), 0)
    c5 = ([p5], int_cmds.copy(), 0)
    comps = [c1, c2, c3, c4, c5]
    outputs = [0]
    while comps:
        inputs, cmds, pointer = comps.pop(0)
        new_inputs = inputs + outputs
        cmds, outputs, inputs, pointer, eb = computer(cmds, new_inputs, pointer)
        if eb:
            comps.append((inputs, cmds, pointer))
        else:
            outputs = new_inputs
            break
    if outputs[0] > max_output:
        max_output = outputs[0]
print("part 2 output:", max_output)
