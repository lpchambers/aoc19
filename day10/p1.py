#!/usr/bin/python3
import math

with open('input') as f:
    lines = f.readlines()

# lines = """.#..#
# .....
# #####
# ....#
# ...##""".splitlines()

lines = [x.strip() for x in lines]


ASTEROID = "#"
locs = []

for row, line in enumerate(lines):
    for col, char in enumerate(line):
        if char == ASTEROID:
            locs.append((row, col))


def can_see(a1, a2, asteroids):
    dr = a2[0] - a1[0]
    dc = a2[1] - a1[1]
    gcd = math.gcd(dr, dc)
    if gcd == 1:
        return True

    step_r = dr // gcd
    step_c = dc // gcd
    if dr != 0:
        steps = dr // step_r
    else:
        steps = dc // step_c

    for x in range(1, steps):
        if (a1[0] + x*step_r, a1[1] + x*step_c) in asteroids:
            return False
    return True

def num_detect(a1, asteroids):
    n = 0
    for a2 in asteroids:
        if a1 != a2 and can_see(a1, a2, asteroids):
            n += 1
    return n

max_ast = None
max_count = 0
for ast in locs:
    n = num_detect(ast, locs)
    print(ast, n)
    if n > max_count:
        max_count = n
        max_ast = ast

print("Max asteroid", max_ast, max_count)
