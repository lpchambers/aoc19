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


def computer(commands):
    pointer = 0
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
            # Input is always 5
            INPUT_VAL = 5
            commands[locs[0]] = INPUT_VAL
        elif opcode == OUT:
            print(f"OUTPUT: {vals[0]}")
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
    return commands

with open('input') as f:
    lines = f.readlines()

for line in lines:
    str_commands = line.strip().split(',')
    int_commands = [int(x) for x in str_commands]
    computer(int_commands)
