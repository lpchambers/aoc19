#!/usr/bin/python3
import functools

with open('input') as f:
    lines = f.readlines()

lines = [l.strip() for l in lines]

def deal_into_new_stack(deck):
    return list(reversed(deck))

def cut(deck, n):
    return deck[n:] + deck[:n]

def deal_with_increment(deck, n):
    L = len(deck)
    new_deck = [-1] * L
    for idx, card in enumerate(deck):
        new_idx = (n * idx) % L
        new_deck[new_idx] = card
    return new_deck

NCARDS = 10007
deck = list(range(NCARDS))

# test_deck = list(range(10))
# print("Test deck", test_deck)
# print("Deal into new", list(deal_into_new_stack(test_deck)))
# print("Cut 3", cut(test_deck, 3))
# print("Cut -4", cut(test_deck, -4))
# print("Deal with increment 3", deal_with_increment(test_deck, 3))

for line in lines:
    if line.startswith("deal into new stack"):
        deck = deal_into_new_stack(deck)
    elif line.startswith("cut"):
        n = int(line.split()[-1])
        deck = cut(deck, n)
    elif line.startswith("deal with increment"):
        n = int(line.split()[-1])
        deck = deal_with_increment(deck, n)

print("Part 1", deck.index(2019))

NCARDS = 119315717514047
NLOOPS = 101741582076661

def undo_deal_into_new_stack(idx, ncards):
    return ncards - idx

def undo_cut(idx, ncards, n):
    return (idx + n) % ncards

@functools.lru_cache(maxsize=100)
def extended_gcd(aa, bb):
    lastremainder, remainder = abs(aa), abs(bb)
    x, lastx, y, lasty = 0, 1, 1, 0
    while remainder:
        lastremainder, (quotient, remainder) = remainder, divmod(lastremainder, remainder)
        x, lastx = lastx - quotient*x, x
        y, lasty = lasty - quotient*y, y
    return lastremainder, lastx * (-1 if aa < 0 else 1), lasty * (-1 if bb < 0 else 1)

@functools.lru_cache(maxsize=100)
def modinv(a, m):
    g, x, y = extended_gcd(a, m)
    if g != 1:
        raise ValueError
    return x % m

def undo_deal_with_increment(idx, ncards, n):
    return (modinv(n, ncards) * idx) % ncards

def poly_new(a, b, ncards):
    return -a, ncards-b-1

def poly_cut(a, b, n, ncards):
    return a, (b + n)%ncards

def poly_inc(a, b, n, ncards):
    inv = modinv(n, ncards)
    inv = pow(n, ncards - 2, ncards)
    return (a*inv)%ncards, (b*inv)%ncards

a = 1
b = 0
for line in lines[::-1]:
    if line.startswith("deal into new stack"):
        a, b = poly_new(a, b, NCARDS)
    elif line.startswith("cut"):
        n = int(line.split()[-1])
        a, b = poly_cut(a, b, n, NCARDS)
    elif line.startswith("deal with increment"):
        n = int(line.split()[-1])
        a, b = poly_inc(a, b, n, NCARDS)

# (ax + b) ^ p % ncards
def polypow(a, b, p, ncards):
    if p==0:
        return 1, 0
    elif p%2==0:
        return polypow(a*a%ncards, (a*b+b)%ncards, p//2, ncards)
    else:
        c, d = polypow(a, b, p-1, ncards)
        return a*c%ncards, (a*d+b)%ncards

a, b = polypow(a, b, NLOOPS, NCARDS)
end_idx = 2020
print("Part 2", (a*end_idx + b) % NCARDS)
