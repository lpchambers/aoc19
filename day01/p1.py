import math
with open('HaxLogs.txt') as f:
	lines = f.readlines()

def fuel_from_mass(mass):
	return math.floor(mass / 3) - 2
s = 0
for line in lines:
	s += fuel_from_mass(int(line))
print(s)
