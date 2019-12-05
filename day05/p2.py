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
            in1 = mode_to_int(modes[-1], vals[0], commands)
            in2 = mode_to_int(modes[-2], vals[1], commands)
            commands[int(vals[2])] = str(in1 + in2)
        elif opcode == MUL:
            in1 = mode_to_int(modes[-1], vals[0], commands)
            in2 = mode_to_int(modes[-2], vals[1], commands)
            commands[int(vals[2])] = str(in1 * in2)
        elif opcode == INP:
            # Input is always 1
            INPUT_VAL = "5"
            commands[int(vals[0])] = INPUT_VAL
        elif opcode == OUT:
            print(f"OUTPUT: {commands[int(vals[0])]}")
        elif opcode == JIT:
            in1 = mode_to_int(modes[-1], vals[0], commands)
            in2 = mode_to_int(modes[-2], vals[1], commands)
            if in1 != 0:
                pointer = in2
                continue
        elif opcode == JIF:
            in1 = mode_to_int(modes[-1], vals[0], commands)
            in2 = mode_to_int(modes[-2], vals[1], commands)
            if in1 == 0:
                pointer = in2
                continue
        elif opcode == LT:
            in1 = mode_to_int(modes[-1], vals[0], commands)
            in2 = mode_to_int(modes[-2], vals[1], commands)
            val = "1" if in1 < in2 else "0"
            commands[int(vals[2])] = val
        elif opcode == EQ:
            in1 = mode_to_int(modes[-1], vals[0], commands)
            in2 = mode_to_int(modes[-2], vals[1], commands)
            val = "1" if in1 == in2 else "0"
            commands[int(vals[2])] = val
        else:
            print("FAIL????")
        pointer += 1 + n_vals
    return commands

with open('input') as f:
    lines = f.readlines()

for line in lines:
    str_commands = line.strip().split(',')
    computer(str_commands)
