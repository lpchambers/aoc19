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

H = len(lines)
W = len(lines[0])
BUF = 4

def get_neighbour(pos, d):
    x, y = pos
    dx, dy = DIRS[d]
    return (x+dx, y+dy)

def get_neighbours(pos):
    return [get_neighbour(pos, d) for d in DIRS]

def is_outside(pos):
    """
    Returns whether the position is an inside or an outside
    or maze position
    """
    rix, cix = pos
    if rix < BUF or rix > H-BUF:
        return True
    if cix < BUF or cix > W-BUF:
        return True
    return False

# Maps position to found and unused chars for portals
found_chars = {}
for rix, line in enumerate(lines):
    for cix, c in enumerate(line):
        if c == ".":
            maze.append((rix, cix))
        elif c in string.ascii_uppercase:
            up = get_neighbour((rix, cix), U)
            left = get_neighbour((rix, cix), L)
            delta_level = -1 if is_outside((rix, cix)) else 1
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
                new_portal = (portal_step, map_step, delta_level)
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
                new_portal = (portal_step, map_step, delta_level)
                if pname in portals:
                    portals[pname] = (portals[pname], new_portal)
                else:
                    portals[pname] = new_portal
            else:
                found_chars[(rix, cix)] = c

if found_chars:
    print("Unmatched chars", found_chars)

# Portals key "name", value: (portal_step, map_step, delta_level)

START = (portals['AA'][1][0], portals['AA'][1][1], 0)
END = (portals['ZZ'][1][0], portals['ZZ'][1][1], 0)

print("Start", START)
print("End", END)

# Takes where you would step in 1 portal to where you would come out the other
mapped_portals = {}
for k, v in portals.items():
    if k in ['AA', 'ZZ']:
        continue
    e1, e2 = v
    p1, m1, l1 = e1
    p2, m2, l2 = e2
    mapped_portals[p1] = (m2, l1)
    mapped_portals[p2] = (m1, l2)

def get_real_neighbours(pos):
    real = []
    x, y, l = pos

    for n in get_neighbours((x, y)):
        if n in maze:
            n_level = (n[0], n[1], l)
            real.append(n_level)
        elif n in mapped_portals:
            peer_portal, d_level = mapped_portals[n]
            new_level = l + d_level
            if new_level < 0:
                continue
            real.append((peer_portal[0], peer_portal[1], new_level))
    return real

distances = {START: 0}
seen = set()
while END not in distances:
    _lev, min_cost, min_vert = min((k[2], v, k) for k, v in distances.items() if k not in seen)
    seen.add(min_vert)
    new_cost = min_cost + 1
    if min_vert[2] == 0:
        print(min_vert, min_cost)
    for n in get_real_neighbours(min_vert):
        if n not in distances:
            distances[n] = new_cost
        elif new_cost < distances[n]:
            distances[n] = new_cost

print("Part 2", distances[END])
