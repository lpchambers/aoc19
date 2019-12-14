#!/usr/bin/python3
with open('input') as f:
    lines = f.readlines()

# lines = """10 ORE => 10 A
# 1 ORE => 1 B
# 7 A, 1 B => 1 C
# 7 A, 1 C => 1 D
# 7 A, 1 D => 1 E
# 7 A, 1 E => 1 FUEL""".splitlines()

class Chemical:
    def __init__(self, chemical, amount, reaction=None):
        self.chemical = chemical 
        self.amount = amount
        if reaction is None:
            reaction = {}
        # Dict mapping chemical name to amount needed
        self.reaction = reaction

        self.req = None
        self.steps = None

    def max_n_steps(self):
        if self.chemical == "ORE":
            return 0
        if self.steps is not None:
            return self.steps
        rec_n_steps = [chemicals_map[chem].max_n_steps() for chem in self.reaction]
        self.steps = max(rec_n_steps) + 1
        return self.steps

    def get_requires(self):
        if self.chemical == "ORE":
            return set()
        if self.req is not None:
            return self.req

        self.req = set()
        for ing in self.reaction:
            self.req = self.req.union(chemicals_map[ing].get_requires())
            self.req.add(ing)
        return self.req

# Maps Name to chemical
chemicals_map = {}
for l in lines:
    consume, produce = l.strip().split('=>')
    am_prod, name = produce.strip().split()

    recipe = {}

    for c in consume.split(","):
        amount, ing = c.strip().split()
        recipe[ing] = int(amount)

    chemicals_map[name] = Chemical(name, int(am_prod), recipe)

# Add ORE
chemicals_map["ORE"] = Chemical("ORE", 1)

import collections

def resolve_need():
    while need:
        # Find the thing we need with the greatest number of steps
        # to ORE
        #print("NEED", need)
        #print("Have", have)
        #need_set = set(need.keys())
        #req_sets = [chemicals_map[x].get_requires() for x in need]
        #all_chain = set.union(*req_sets)
    
        #max_need = need_set.difference(all_chain)
        #max_ing = list(max_need)[0]
        # print("Getting", max_ing)
    
    
        max_ing = max(need, key=lambda x: chemicals_map[x].max_n_steps())
        if max_ing == "ORE":
            return
    
        c = chemicals_map[max_ing]
        amt_needed = need[max_ing]
        scale = amt_needed // c.amount + (amt_needed % c.amount != 0)
        have[max_ing] += scale * c.amount
        need[max_ing] -= scale * c.amount
        if need[max_ing] <= 0:
            need.pop(max_ing)
    
        recipe = c.reaction
        # print("It needs", recipe)
        # Get the things we need
        for ing_need, amt_need in recipe.items():
            amt_have = have[ing_need]
            amt_need = amt_need * scale
            if amt_have >= amt_need:
                have[ing_need] -= amt_need
            else:
                # use all we have, and need some
                more_need = amt_need - amt_have
                have[ing_need] = 0
                need[ing_need] += more_need

need = collections.defaultdict(lambda: 0)
need['FUEL'] = 1
have = collections.defaultdict(lambda: 0)
INITIAL_ORE = 1000000000000
have['ORE']  = INITIAL_ORE

resolve_need()
p1_sol = INITIAL_ORE - have["ORE"]
print("Part 1", p1_sol)


# Part 2
under_f = have["ORE"] // p1_sol
over_f = None
guess = under_f

while True:
    need = collections.defaultdict(lambda: 0)
    need['FUEL'] = guess
    have = collections.defaultdict(lambda: 0)
    INITIAL_ORE = 1000000000000
    have['ORE']  = INITIAL_ORE
    resolve_need()

    print("Trying", guess)

    if need["ORE"] > 0:
        over_f = guess
        print("Needs more ore", need["ORE"])
    else:
        under_f = guess
        print("Left over")

    old_g = guess
    if over_f:
        guess = (under_f + over_f) // 2
    else:
        guess = guess * 2

    if old_g == guess:
        break

print("Part 2", guess)
