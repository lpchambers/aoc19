#!/usr/bin/python3
import string
with open('input') as f:
    lines = f.readlines()

# Map from portal label 'XX' to tuple of 2 points ((x1,y1),(x2,y2))
portals = {}
# All (row, col) spaces in the maze
maze = []

D = 0
U = 1
R = 2
L = 3

DIRS = {
    0: (1, 0),
    1: (-1, 0),
    2: (0, 1),
    3: (0, -1),
}

def get_neighbour(pos, d):
    x, y = pos
    dx, dy = DIRS[d]
    return (x+dx, y+dy)

def get_neighbours(pos):
    return [get_neighbour(pos, d) for d in DIRS]

# Maps position to found and unused chars for portals
found_chars = {}
for rix, line in enumerate(lines):
    for cix, c in enumerate(line):
        if c == ".":
            maze.append((rix, cix))
        elif c in string.ascii_uppercase:
            up = get_neighbour((rix, cix), U)
            left = get_neighbour((rix, cix), L)
            if up in found_chars:
                pre = found_chars.pop(up)
                pname = pre + c
                # Char above, if 2 up is in maze, bottom portal
                u2 = get_neighbour(up, U)
                if u2 in maze:
                    map_step = u2
                    portal_step = up
                else:
                    map_step = get_neighbour((rix, cix), D)
                    portal_step = (rix, cix)
                new_portal = (portal_step, map_step)
                if pname in portals:
                    portals[pname] = (portals[pname], new_portal)
                else:
                    portals[pname] = new_portal
            elif left in found_chars:
                pre = found_chars.pop(left)
                pname = pre + c
                l2 = get_neighbour(left, L)
                if l2 in maze:
                    map_step = l2
                    portal_step = left
                else:
                    map_step = get_neighbour((rix, cix), R)
                    portal_step = (rix, cix)
                new_portal = (portal_step, map_step)
                if pname in portals:
                    portals[pname] = (portals[pname], new_portal)
                else:
                    portals[pname] = new_portal
            else:
                found_chars[(rix, cix)] = c

if found_chars:
    print("Unmatched chars", found_chars)

# Portals key "name", value: (portal_step, map_step)

START = portals['AA'][1]
END = portals['ZZ'][1]

# Takes where you would step in 1 portal to where you would come out the other
mapped_portals = {}
for k, v in portals.items():
    if k in ['AA', 'ZZ']:
        continue
    e1, e2 = v
    p1, m1 = e1
    p2, m2 = e2
    mapped_portals[p1] = m2
    mapped_portals[p2] = m1

def get_real_neighbours(pos):
    real = []
    for n in get_neighbours(pos):
        if n in maze:
            real.append(n)
        elif n in mapped_portals:
            real.append(mapped_portals[n])
    return real

INF = 99999
distances = {p: INF for p in maze}
distances[START] = 0
seen = set()
while len(seen) != len(maze):
    min_cost, min_vert = min((v, k) for k, v in distances.items() if k not in seen)
    seen.add(min_vert)
    new_cost = min_cost + 1
    for n in get_real_neighbours(min_vert):
        if new_cost < distances[n]:
            distances[n] = new_cost

print("Part 1", distances[END])
