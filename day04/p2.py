#!/usr/bin/python3
start = 165432
end = 707912

def is_valid(num):
    # Check non decreasing
    has_only_double = False
    n_in_a_row = 1
    for x, y in zip(num[:-1], num[1:]):
        if x > y:
            return False
        if x == y:
            n_in_a_row += 1
        else:
            # End of seq - check if only 2 in a row
            if n_in_a_row == 2:
                has_only_double = True
            else:
                n_in_a_row = 1

    if n_in_a_row == 2:
        return True

    return has_only_double

valid = [n for n in range(start, end+1) if is_valid(str(n))]
print(len(valid))
