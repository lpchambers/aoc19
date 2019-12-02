#!/usr/bin/python3
END = 99
ADD = 1
MUL = 2

TARGET = 19690720

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
    return commands

with open('input') as f:
    l = f.readline()

str_commands = l.strip().split(',')
int_commands = [int(x) for x in str_commands]

print(int_commands)

for noun in range(100):
    for verb in range(100):
        test_cmd = int_commands.copy()
        test_cmd[1] = noun
        test_cmd[2] = verb
        
        res = computer(test_cmd)
        if res[0] == TARGET:
            print(f"noun={noun}, verb={verb}, ans={100 * noun + verb}")
            import sys
            sys.exit()

