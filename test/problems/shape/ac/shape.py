#!/usr/bin/env python3

from math import pi
from sys import stdin

for line in stdin:
    A, x1, y1, x2, y2 = [float(x) for x in line.split()]
    r2 = (0.25)*((x1-x2)**2 + (y1-y2)**2)
    if abs(A-2*r2)<=1e-5:
        print('Square',(32*r2)**0.5)
    elif abs(A-pi*r2)<=1e-5:
        print('Circle',2*pi*(r2**0.5))
    else:
        print('MZ is a liar!')
