#!/usr/bin/env python3

from random import randint as ri

print(24)
print(*[0]*24)
print(24)
print(*[i for i in range(24,0,-1)])
print(24)
print(*[i for i in range(24)])
for i in range(20):
    print(24)
    print(*[ri(0,99) for x in range(24)])
