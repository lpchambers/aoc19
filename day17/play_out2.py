#!/usr/bin/python3
import time
with open('out2') as f:
    lines = f.readlines()

NLINES = 48

f1 = lines[0:NLINES]

print("".join(f1))
ix = 124
while True:
    frame = lines[ix+1:ix+NLINES - 2]
    print("".join(frame), end="")
    ix += NLINES
    time.sleep(0.1)
