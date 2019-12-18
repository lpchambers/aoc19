#!/usr/bin/python3
import string
with open('input') as f:
    lines = f.readlines()

# lines = """#########
# #b.A.@.a#
# #########""".splitlines()
lines = """########################
#f.D.E.e.C.b.A.@.a.B.c.#
######################.#
#d.....................#
########################""".splitlines()
lines = """#################
#i.G..c...e..H.p#
########.########
#j.A..b...f..D.o#
########@########
#k.E..a...g..B.n#
########.########
#l.F..d...h..C.m#
#################""".splitlines()


INF = 999999999999999

class VaultSearch:
    def __init__(self, vault, pos=None, steps=0, keys=None, open_doors=None):
        self.vault = vault
        if pos is None:
            pos = self.vault.find_pos()
        if open_doors is None:
            open_doors = []
        if keys is None:
            keys = []
        self.pos = pos
        self.steps = steps
        self.open_doors = open_doors
        self.keys = keys

    def can_move(self, pos, d):
        dr, dc = DIRS[d]
        r, c = pos
        r += dr
        c += dc
        if (r, c) in self.open_doors:
            return (True, (r, c))
        return (self.vault.can_walk((r, c)), (r, c))

    def get_value(self):
        r, c = self.pos
        return self.vault.lines[r][c]

    def search_out(self):
        """
        Starting from self.pos, find all paths
        """
        costs = {self.pos: 0}
        unchecked = [self.pos]
        while unchecked:
            pos = unchecked.pop(0)
            for d in DIRS:
                can_move, new_pos = self.can_move(pos, d)
                if not can_move:
                    continue
                new_cost = costs[pos] + 1
                if new_pos not in costs:
                    costs[new_pos] = new_cost
                    unchecked.append(new_pos)
                elif new_cost < costs[new_pos]:
                    costs[new_pos] = new_costs

        start = self.get_value()
        keys = []
        for key, pos in self.vault.keys.items():
            if pos in costs:
                self.vault.costs[start][key] = costs[pos]
                self.vault.costs[key][start] = costs[pos]
                keys.append(key)
        return keys

    def solve(self):
        if len(self.keys) == len(self.vault.keys):
            return self.steps
        keys = self.search_out()
        searches = []
        for key in keys:
            if key in self.keys:
                continue
            pos = self.vault.keys[key]
            steps = self.steps + self.vault.costs[self.get_value()][key]
            found_keys = self.keys + [key]
            door = key.upper()
            if door in self.vault.doors:
                open_doors = self.open_doors + [self.vault.doors[door]]
            else:
                open_doors = self.open_doors.copy()
            new_search = VaultSearch(self.vault, pos, steps, found_keys, open_doors)
            searches.append(new_search)
        if searches:
            print(self.keys)
            return min([s.solve() for s in searches])
        else:
            print(len(self.keys))
            import pdb
            pdb.set_trace()
            return INF


class Vault:
    def __init__(self, lines, keys=None, doors=None):
        self.lines = lines
        if keys is None:
            keys = self.find_keys()
        if doors is None:
            doors = self.find_doors()

        self.keys = keys
        self.doors = doors

        self.costs = {key: {} for key in self.keys.keys()}
        self.costs[MARKER] = {}

        self.rows = len(lines)
        self.cols = len(lines[0])

    def copy(self):
        return Vault(self.lines.copy(), self.keys, self.doors)

    def can_walk(self, pos):
        r, c = pos
        if self.lines[r][c] == MARKER:
            return True
        return r >= 0 and r < self.rows and c >= 0 and c < self.cols and self.lines[r][c] in can_walk

    def update_lines(self, pos, value):
        r, c = pos
        l = self.lines[r]
        l = l[:c] + value + l[c+1:]
        self.lines[r] = l

    def move(self, d):
        dr, dc = DIRS[d]
        r, c = self.pos

        self.update_lines(self.pos, FREE)

        r += dr
        c += dc

        self.pos = (r, c)
        if self.lines[r][c] in string.ascii_lowercase:
            key = self.lines[r][c]
            # Remove the door
            door = chr(ord(key) - 32)
            if door in self.doors:
                dpos = self.doors[door]
                self.update_lines(dpos, FREE)
        self.update_lines(self.pos, MARKER)
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
                if path is None:
                    continue
                if min_path is None or path < min_path:
                    min_path = path
        return min_path


#vault = Vault([line.strip() for line in lines])
#
#print(len(vault.keys))
#print(len(vault.doors))
#vault.print_map()

#p0 = VaultSearch(vault)
#p0.solve()


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

lines = [line.strip() for line in lines]

# Get keys
keys = {}
for rix, row in enumerate(lines):
    for cix, col in enumerate(row):
        if col in string.ascii_lowercase:
            keys[col] = (rix, cix)

for rix, row in enumerate(lines):
    if MARKER in row:
        keys[MARKER] = (rix, row.find(MARKER))

# Get doors
doors = {}
for rix, row in enumerate(lines):
    for cix, col in enumerate(row):
        if col in string.ascii_uppercase:
            doors[col] = (rix, cix)

WALKABLE = string.ascii_lowercase + FREE + MARKER
rows = len(lines)
cols = len(lines[0])

# Cost for each pair
# {key --> (cost, [keys_needed])}
pair_costs = {key: {} for key in keys}
for start_key in keys:
    key_pos = keys[start_key]
    costs = {key_pos: (0, [])}
    unchecked = [key_pos]
    while unchecked:
        pos = unchecked.pop(0)
        for d in DIRS:
            dr, dc = DIRS[d]
            r, c = pos
            r += dr
            c += dc
            new_pos = (r, c)

            # check bounds
            if r < 0 or r >= rows or c < 0 or c >= cols:
                continue

            if lines[r][c] in WALKABLE:
                # Explicitly walkable
                new_doors = []
            elif lines[r][c] in string.ascii_uppercase:
                # Gone through door
                new_doors = [lines[r][c]]
            else:
                # wall
                continue
            old_cost, old_doors = costs[pos]
            new_cost = old_cost + 1
            new_doors = old_doors + new_doors

            # Check if adding or comparing
            if new_pos not in costs:
                costs[new_pos] = (new_cost, new_doors)
                unchecked.append(new_pos)
            elif new_cost < costs[new_pos][0]:
                costs[new_pos] = (new_cost, new_doors)

    for end_key, pos in keys.items():
        if pos in costs:
            pair_costs[start_key][end_key] = costs[pos]

import pprint
pprint.pprint(pair_costs)

# Calculate lower bound of graph
s = 0
min_edge_cost = {}
for v, c in pair_costs.items():
    nums = [x[0] for x in c.values()]
    s_nums = sorted(nums)
    # Cost to self is included, so get #1 and #2
    s += s_nums[1] + s_nums[2]
    min_edge_cost[v] = s_nums[1]


lower_bound = s // 2

lb_start = MARKER
lb_visit = [MARKER]
lower_bound_edge = {}
while len(lb_visit) != len(keys):
    lbc = sorted(pair_costs[lb_start].items(), key=lambda x: x[1][0])
    for lbk, lbv in lbc:
        if lbk in lb_visit:
            continue
        lower_bound_edge[lb_start] = lbv[0]
        lb_visit.append(lbk)
        lb_start = lbk
        break

lower_bound_edge[lb_start] = pair_costs[lb_start][MARKER][0]
lower_bound = sum(lower_bound_edge.values())
print(lower_bound)

# List of (position, cost, open_doors, collected_keys, lower_bound)
unchecked = [(MARKER, 0, [], [MARKER], lower_bound)]
shortest_cost = None
shortest_path = None
while unchecked:
    pos, cost, open_doors, collected_keys, lower_bound = unchecked.pop(0)
    print(shortest_cost, lower_bound, collected_keys)
    # Exit condition
    if len(collected_keys) == len(keys):
        print(collected_keys)
        if shortest_cost is None:
            shortest_cost = cost
            shortest_path = collected_keys
        elif cost < shortest_cost:
            shortest_cost = cost
            shortest_path = collected_keys
        print(shortest_cost)
        continue

    for key, val in pair_costs[pos].items():
        # If we already have the key, ignore it
        if key in collected_keys:
            continue
        cost_to_key, doors_in_way = val
        # If the path to the key is open, try it
        if all(door in open_doors for door in doors_in_way):
            # Computer a new lower bound - if it is already greater than
            # the current loewst cost, ignore this branch entirely
            new_lower = lower_bound - lower_bound_edge[pos] + cost_to_key
            if shortest_cost and new_lower > shortest_cost:
                # print("Prune branch")
                continue

            check = (key, cost+cost_to_key, open_doors + [key.upper()], collected_keys + [key], new_lower)
            unchecked.insert(0, check)

print(shortest_cost)
print(shortest_path)
