class Space:
	def __init__(self, name):
		self.name = name
		self.children = []
		self.parent = None

	def set_parent(self, parent):
		self.parent = parent
		self.parent.children.append(self)

	def cost(self):
		if self.name == "COM":
			return 0
		if self.parent is None:
			print(self.name)
		return self.parent.cost() + 1
	
	def chain(self):
		if self.name == "COM":
			return ["COM"]
		return [self.name] + self.parent.chain()
		

	def chainstr(self):
		if self.name == "COM":
			return "COM"
		return self.name + " -> " + self.parent.chain()


with open('input') as f:
	lines = f.readlines()

orbits = {}  # Name to Space
lines_parse = [line.strip().split(')') for line in lines]


for parent, child in lines_parse:
	if parent in orbits:
		po = orbits[parent]
	else:
		po = Space(parent)
		orbits[parent] = po
	if child in orbits:
		co = orbits[child]
	else:
		co = Space(child)
		orbits[child] = co

	co.set_parent(po)

print("P1:", sum(space.cost() for space in orbits.values()))

uchain = orbits["YOU"].chain()
schain = orbits["SAN"].chain()

for par in uchain:
	if par in schain:
		print("First common parent:", par)
		break

print("P2:", orbits["YOU"].cost() + orbits["SAN"].cost() - (2*orbits[par].cost()) - 2)
