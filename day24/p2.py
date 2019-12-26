#!/usr/bin/python3
with open('input') as f:
    lines = f.readlines()

lines = [l.strip() for l in lines]
NTIMES = 200
# NTIMES = 10
# lines = """....#
# #..#.
# #..##
# ..#..
# #....""".splitlines()

H = len(lines)
W = len(lines[0])

# Space is now (row, col, layer)
space = {}
for rix, line in enumerate(lines):
    for cix, c in enumerate(line):
        space[(rix, cix, 0)] = True if c=="#" else False

# Remove the middle tile
del space[(2, 2, 0)]

# After 2 mins, a bug can spread out to other layers
# Looking for 200 mins, so do +/- 100 layers
for layer in range(-100, 101):
    if layer == 0:
        continue
    for rix in range(H):
        for cix in range(W):
            if rix == 2 and cix == 2:
                continue
            space[(rix, cix, layer)] = False

peers = {}
for rix, cix, layer in space:
    plist = []

    # Layer plus
    lp = layer + 1
    # Go up
    if (rix-1, cix) == (2, 2):
        plist.extend([(4,0,lp), (4,1,lp), (4,2,lp), (4,3,lp), (4,4,lp)])
    elif rix-1 >= 0:
        plist.append((rix-1, cix, layer))
    else:
        plist.append((1, 2, layer - 1))

    # Go down
    if (rix+1, cix) == (2, 2):
        plist.extend([(0,0,lp), (0,1,lp), (0,2,lp), (0,3,lp), (0,4,lp)])
    elif rix+1 <= W-1:
        plist.append((rix+1, cix, layer))
    else:
        plist.append((3, 2, layer - 1))

    # Go left
    if (rix, cix-1) == (2, 2):
        plist.extend([(0,4,lp), (1,4,lp), (2,4,lp), (3,4,lp), (4,4,lp)])
    elif cix-1 >= 0:
        plist.append((rix, cix-1, layer))
    else:
        plist.append((2, 1, layer - 1))

    # Go right
    if (rix, cix+1) == (2, 2):
        plist.extend([(0,0,lp), (1,0,lp), (2,0,lp), (3,0,lp), (4,0,lp)])
    elif cix+1 <= H-1:
        plist.append((rix, cix+1, layer))
    else:
        plist.append((2, 3, layer - 1))

    peers[(rix, cix, layer)] = plist

for t in range(NTIMES):
    new_space = {}
    for pos, bug in space.items():
        nadj = len([peerpos for peerpos in peers[pos] if space.get(peerpos, False)])
        if bug:
            new_space[pos] = nadj == 1
        else:
            new_space[pos] = nadj in [1, 2]

    space = new_space

print("Part 2", len([pos for pos, bug in space.items() if bug]))
