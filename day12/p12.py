#!/usr/bin/python3
class Moon:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.vx = 0
        self.vy = 0
        self.vz = 0

    def __str__(self):
        return f"<pos=(x={self.x}, y={self.y}, z={self.z}), vel=(x={self.vx}, y={self.vy}, z={self.vz})>"

    def __hash__(self):
        return hash(str(self))

    def state(self):
        return (self.x, self.y, self.z, self.vx, self.vy, self.vz)

    def adjust_gravity(self, other):
        self.vx += int(other.x > self.x) - int(self.x > other.x)
        self.vy += int(other.y > self.y) - int(self.y > other.y)
        self.vz += int(other.z > self.z) - int(self.z > other.z)

    def move(self):
        self.x += self.vx
        self.y += self.vy
        self.z += self.vz

    def total_energy(self):
        return self.potential_energy() * self.kinetic_energy()

    def potential_energy(self):
        return abs(self.x) + abs(self.y) + abs(self.z)

    def kinetic_energy(self):
        return abs(self.vx) + abs(self.vy) + abs(self.vz)


import re
import itertools

with open('input') as f:
    lines = f.readlines()

# Tests
# lines = """<x=-1, y=0, z=2>
# <x=2, y=-10, z=-7>
# <x=4, y=-8, z=8>
# <x=3, y=5, z=-1>""".splitlines()

# lines = """<x=-8, y=-10, z=0>
# <x=5, y=5, z=10>
# <x=2, y=-7, z=3>
# <x=9, y=-8, z=-3>""".splitlines()

moons = []
lines2 = lines.copy()
for line in lines:
    m = re.match("<x=([-0-9]*), y=([-0-9]*), z=([-0-9]*)>", line)
    x, y, z = m.groups()
    moon = Moon(int(x), int(y), int(z))
    moons.append(moon)

for _ in range(1000):
    for m1, m2 in itertools.combinations(moons, 2):
        m1.adjust_gravity(m2)
        m2.adjust_gravity(m1)
    for moon in moons:
        moon.move()

print("Part 1:", sum([m.total_energy() for m in moons]))

def get_moon_state_hash(moons):
    return hash("".join([str(moon) for moon in moons]))


class MoonAxis:
    def __init__(self, x):
        self.x = x
        self.v = 0

    def adjust_gravity(self, other):
        self.v += int(other.x > self.x) - int(self.x > other.x)

    def move(self):
        self.x += self.v

    def state(self):
        return (self.x, self.v)

for line in lines2:
    m = re.match("<x=([-0-9]*), y=([-0-9]*), z=([-0-9]*)>", line)
    x, y, z = m.groups()
    moon = Moon(int(x), int(y), int(z))
    moons.append(moon)

xax = []
yax = []
zax = []
for line in lines:
    m = re.match("<x=([-0-9]*), y=([-0-9]*), z=([-0-9]*)>", line)
    x, y, z = m.groups()
    xax.append(MoonAxis(int(x)))
    yax.append(MoonAxis(int(y)))
    zax.append(MoonAxis(int(z)))

def run_axis(axis):
    init_state = [m.state() for m in axis]
    n = 0
    while True:
        n += 1
        for m1, m2 in itertools.combinations(axis, 2):
            m1.adjust_gravity(m2)
            m2.adjust_gravity(m1)
        for m in axis:
            m.move()

        if [m.state() for m in axis] == init_state:
            break

    return(n)

import math
def lcm(a):
    lcm = a[0]
    for i in a[1:]:
        lcm = lcm * i // math.gcd(lcm, i)
    return lcm

xn = run_axis(xax)
yn = run_axis(yax)
zn = run_axis(zax)
print("Part 2", lcm([xn, yn, zn]))
