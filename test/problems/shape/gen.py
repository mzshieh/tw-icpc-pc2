#!/usr/bin/env python3

from random import randint as ri
from math import pi

for _ in range(25):
    x1, y1, x2, y2 = [ri(-100,100) for i in range(4)]
    if ri(0,4)<2:
        A = (0.5)*((x1-x2)**2 + (y1-y2)**2)
    elif ri(0,2)<2:
        A = (pi/4)*((x1-x2)**2 + (y1-y2)**2)
    else:
        A = (ri(200,314)/400)*((x1-x2)**2 + (y1-y2)**2)
    print('{:.20f}'.format(A),x1,y1,x2,y2)
