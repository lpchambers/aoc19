#!/usr/bin/python3
with open('input') as f:
    input_signal = f.read().strip()

# input_signal = "12345678"
# input_signal = "80871224585914546619083218645595"

base_pat = [0, 1, 0, -1]


def create_scalars(base_pat, pos, l):
    pad_patt = [[x] * (pos + 1) for x in base_pat]
    flat_patt = [item for sublist in pad_patt for item in sublist]
    n_times = (l + 1) // len(flat_patt)
    flat_patt = (n_times + 1) * flat_patt
    return flat_patt[1:l+1]


def dot_product(a, b):
    return sum([x * y for x, y in zip(a, b)])


def do_reduce(x):
    if x < 0:
        return (-1*x) % 10
    return x % 10

def do_fft(input_signal, base_pat):
    in_int = [int(x) for x in input_signal]
    l = len(input_signal)
    out = []
    for idx, x in enumerate(in_int):
        scalars = create_scalars(base_pat, idx, l)
        out.append(str(do_reduce(dot_product(in_int, scalars))))
    return "".join(out)

# Part 1
for _ in range(100):
    input_signal = do_fft(input_signal, base_pat)

print("Part 1", input_signal[:8])
