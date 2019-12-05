#!/usr/bin/python3
END = 99
ADD = 1
MUL = 2
INP = 3
OUT = 4

num_vals = {
    ADD: 3,
    MUL: 3,
    INP: 1,
    OUT: 1,
}

def mode_to_int(mode, code, commands):
    if mode == "0":
        return int(commands[int(code)])
    return int(code)

def computer(commands):
    pointer = 0
    while commands[pointer] != END:
        # Get the cmd
        cmd = commands[pointer]
        opcode = int(cmd[-2:])
        if opcode == END:
            break
        n_vals = num_vals[opcode]
        vals = commands[pointer+1:pointer+1+n_vals]

        # Get the modes
        modes = str(cmd)[:-2].rjust(len(vals), "0")

        if opcode == ADD:
            #import pdb
            #pdb.set_trace()
            in1 = mode_to_int(modes[-1], vals[0], commands)
            in2 = mode_to_int(modes[-2], vals[1], commands)
            commands[int(vals[2])] = str(in1 + in2)
        elif opcode == MUL:
            in1 = mode_to_int(modes[-1], vals[0], commands)
            in2 = mode_to_int(modes[-2], vals[1], commands)
            commands[int(vals[2])] = str(in1 * in2)
        elif opcode == INP:
            # Input is always 1
            INPUT_VAL = "1"
            commands[int(vals[0])] = INPUT_VAL
        elif opcode == OUT:
            print(f"OUTPUT: {commands[int(vals[0])]}")
        else:
            print("FAIL????")
        pointer += 1 + n_vals
    return commands

with open('input') as f:
    lines = f.readlines()

for line in lines:
    str_commands = line.strip().split(',')
    computer(str_commands)
