#!/usr/bin/env python3

from random import randint as ri

print(-10**18,10**18)
print(-10**18,-10**18)
print(10**18,10**18)
for i in range(20):
    print(ri(-10**18,10**18),ri(-10**18,10**18))
