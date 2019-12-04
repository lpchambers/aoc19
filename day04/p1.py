#!/usr/bin/python3
start = 165432
end = 707912

def is_valid(num):
    # Check non decreasing
    has_double = False
    for x, y in zip(num[:-1], num[1:]):
        if x > y:
            return False
        has_double |= x == y
    return has_double

valid = [n for n in range(start, end+1) if is_valid(str(n))]
print(len(valid))
