#!/usr/bin/python3
import string
with open('input') as f:
    lines = f.readlines()



MARKER = "@"
WALL = "#"
FREE = "."

UP = 0
DOWN = 1
LEFT = 2
RIGHT = 3

DIRS = {
    UP: (-1, 0),
    DOWN: (1, 0),
    LEFT: (0, -1),
    RIGHT: (0, 1),
}

can_walk = string.ascii_lowercase + FREE

class Vault:
    def __init__(self, lines, steps=0, pos=None, keys=None, doors=None, visited=None):
        self.lines = lines
        if pos is None:
            pos = self.find_pos()
        if keys is None:
            keys = self.find_keys()
        if doors is None:
            doors = self.find_doors()
        if visited is None:
            visited = []

        self.steps = steps
        self.pos = pos
        self.keys = keys
        self.doors = doors
        self.visited = visited

        self.rows = len(lines)
        self.cols = len(lines[0])

    def copy(self):
        return Vault(self.lines.copy(), self.steps, self.pos, self.keys, self.doors, self.visited.copy())

    def can_move(self, d):
        dr, dc = DIRS[d]
        r, c = self.pos

        r += dr
        c += dc

        if (r, c) in self.visited:
            return False

        return r >= 0 and r < self.rows and c >= 0 and c < self.cols and self.lines[r][c] in can_walk

    def update_lines(self, pos, value):
        r, c = pos
        l = self.lines[r]
        l = l[:c] + value + l[c+1:]
        self.lines[r] = l

    def move(self, d):
        dr, dc = DIRS[d]
        r, c = self.pos

        self.visited.append((r, c))
        self.update_lines(self.pos, FREE)

        r += dr
        c += dc

        self.pos = (r, c)
        self.update_lines(self.pos, MARKER)
        if self.lines[r][c] in string.ascii_lowercase:
            key = self.lines[r][c]
            door = chr(ord(key) - 32)
            dpos = self.doors[door]
            self.update_lines(dpos, FREE)
            # Finding a key removes the visited constraint
            self.visited = []
        self.steps += 1

    def num_pos(self):
        return "".join(self.lines).count(MARKER)

    def get_pos_row(self):
        return [ix for ix, r in enumerate(self.lines) if MARKER in r]

    def print_map(self):
        print("\n".join(self.lines))

    def find_pos(self):
        for rix, row in enumerate(self.lines):
            if MARKER in row:
                return (rix, row.find(MARKER))
        print("Could not find pos")

    def find_keys(self):
        keys = {}
        for rix, row in enumerate(self.lines):
            for cix, col in enumerate(row):
                if col in string.ascii_lowercase:
                    keys[col] = (rix, cix)
        return keys

    def find_doors(self):
        doors = {}
        for rix, row in enumerate(self.lines):
            for cix, col in enumerate(row):
                if col in string.ascii_uppercase:
                    doors[col] = (rix, cix)
        return doors

    def min_solve(self):
        min_path = None
        if len(self.find_keys()) == 0:
            return self.steps
        for d in DIRS.keys():
            if self.can_move(d):
                cop = self.copy()
                cop.move(d)
                # cop.print_map()
                path = cop.min_solve()
                if min_path is None or path < min_path:
                    min_path = path
#         if min_path is None:
#             self.print_map()
#             import pdb
#             pdb.set_trace()
        return min_path


vault = Vault([line.strip() for line in lines])

print(vault.pos)
print(len(vault.keys))
print(len(vault.doors))
vault.print_map()

sol = vault.min_solve()
print(sol)

