import math
with open('HaxLogs.txt') as f:
	lines = f.readlines()

def fuel_from_mass(mass):
	fuel = math.floor(mass / 3) - 2
	if fuel <= 0:
		return 0
	return fuel + fuel_from_mass(fuel)

s = 0
for line in lines:
	s += fuel_from_mass(int(line))
print(s)
