#!/usr/bin/python3
with open('input') as f:
    lines = f.readlines()

r1 = lines[0].strip().split(',')
r2 = lines[1].strip().split(',')

#r1 = "R75,D30,R83,U83,L12,D49,R71,U7,L72".split(',')
#r2 = "U62,R66,U55,R34,D71,R55,D58,R83".split(',')


def get_all_coords(start, direction, n):
    x, y = start
    if direction == 'L':
        return [(x-i, y) for i in range(n+1)]
    elif direction == 'R':
        return [(x+i, y) for i in range(n+1)]
    elif direction == 'U':
        return [(x, y+i) for i in range(n+1)]
    elif direction == 'D':
        return [(x, y-i) for i in range(n+1)]
    else:
        print("UNKNOWN DIR", direction)

def get_route_coords(route):
    coords = set()
    point = (0,0)
    for r in route:
        direction = r[0]
        n = int(r[1:])
        new_coords = get_all_coords(point, direction, n)
        point = new_coords[-1]
        #print(new_coords, point)
        coords = coords.union(set(new_coords))
    return coords

c1 = get_route_coords(r1)
c2 = get_route_coords(r2)

print(c1)

print("\n\n\n")
sizes = [abs(x) + abs(y) for x, y in c1.intersection(c2)]
sizes.remove(0)
ans = min(sizes)
print(ans)
