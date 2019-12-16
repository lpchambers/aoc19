#!/usr/bin/python3
with open('input') as f:
    input_signal = f.read().strip()

# input_signal = "03036732577212944063491565474664"
# input_signal = "12345678"


def do_reduce(x):
    if x < 0:
        return (-1*x) % 10
    return x % 10

input_signal = input_signal * 10000

offset = int(input_signal[:7])
print(offset)
print(len(input_signal))

input_signal = input_signal[offset:]
input_signal = [int(x) for x in input_signal]
l = len(input_signal)
print("LEN", l)

last = input_signal[-1]

# Part 2
for _ in range(100):
    new_input = [0] * l
    new_input[-1] = last
    for idx in range(l-2, -1, -1):
        new_input[idx] = do_reduce(input_signal[idx] + new_input[idx+1])
    input_signal = new_input
    print(_)

print(input_signal[:8])
print("".join(input_signal[:8]))
