#!/usr/bin/python3
END = 99
ADD = 1
MUL = 2

def computer(commands):
    pointer = 0
    while commands[pointer] != END:
        cmd, ix1, ix2, ix3 = commands[pointer:pointer+4]
        if cmd == ADD:
            commands[ix3] = commands[ix1] + commands[ix2]
        elif cmd == MUL:
            commands[ix3] = commands[ix1] * commands[ix2]
        else:
            print("FAIL????")
        pointer += 4
        print(commands)

with open('input') as f:
    l = f.readline()

str_commands = l.strip().split(',')
int_commands = [int(x) for x in str_commands]

print(int_commands)
int_commands[1] = 12
int_commands[2] = 2
print(int_commands)
print("START")
computer(int_commands)
