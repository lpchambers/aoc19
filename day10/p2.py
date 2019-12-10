#!/usr/bin/python3
import math

with open('input') as f:
    lines = f.readlines()

# lines = """.#..##.###...#######
# ##.############..##.
# .#.######.########.#
# .###.#######.####.#.
# #####.##.#.##.###.##
# ..#####..#.#########
# ####################
# #.####....###.#.#.##
# ##.#################
# #####.##.###..####..
# ..######..##.#######
# ####.##.####...##..#
# .#####..#.######.###
# ##...#.##########...
# #.##########.#######
# .####.#.###.###.#.##
# ....##.##.###..#####
# .#.#.###########.###
# #.#.#.#####.####.###
# ###.##.####.##.#..##""".splitlines()

lines = [x.strip() for x in lines]


ASTEROID = "#"
locs = []

for row, line in enumerate(lines):
    for col, char in enumerate(line):
        if char == ASTEROID:
            locs.append((col, row))


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

def get_all_detects(a1, asteroids):
    detects = []
    for a2 in asteroids:
        if a1 != a2 and can_see(a1, a2, asteroids):
            detects.append(a2)
    return detects

max_ast = None
max_count = 0
for ast in locs:
    n = num_detect(ast, locs)
    if n > max_count:
        max_count = n
        max_ast = ast

print("Max asteroid", max_ast, max_count)

def get_angle(a1, a2):
    dx = a2[0] - a1[0]
    dy = a1[1] - a2[1]
    ang = math.atan2(dy, dx) * 180 / math.pi
    if ang < 0:
        ang += 360

    ang = 90 - ang
    if ang < 0:
        ang += 360

    return ang


detects = get_all_detects(max_ast, locs)

angle_pos = sorted([(get_angle(max_ast, ast), ast) for ast in detects])

ast_200 = angle_pos[199]
print("200th asteroid is", ast_200[1], "at angle", ast_200[0])
print("Answer is", ast_200[1][0] * 100 + ast_200[1][1])
