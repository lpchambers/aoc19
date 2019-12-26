#!/usr/bin/python3
with open('input') as f:
    lines = f.readlines()

lines = [l.strip() for l in lines]

H = len(lines)
W = len(lines[0])

space = {}
for rix, line in enumerate(lines):
    for cix, c in enumerate(line):
        space[(rix, cix)] = True if c=="#" else False

peers = {}
for rix, cix in space:
    plist = []
    if rix-1 >= 0:
        plist.append((rix-1, cix))
    if rix+1 <= W-1:
        plist.append((rix+1, cix))
    if cix-1 >= 0:
        plist.append((rix, cix-1))
    if cix+1 <= H-1:
        plist.append((rix, cix+1))

    peers[(rix, cix)] = plist

seen = set()
while True:
    bio = sum([2**(5*rix+cix) for (rix, cix), bug in space.items() if bug])
    if bio in seen:
        break
    seen.add(bio)

    new_space = {}
    for pos, bug in space.items():
        nadj = len([peerpos for peerpos in peers[pos] if space[peerpos]])
        if bug:
            new_space[pos] = nadj == 1
        else:
            new_space[pos] = nadj in [1, 2]

    space = new_space

print("Part 1", bio)
