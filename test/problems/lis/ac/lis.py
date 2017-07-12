#!/usr/bin/env python3

while True:
    try:
        n = int(input())
    except:
        break
    a = [int(x) for x in input().split()] + [101]
    l = [0]*(n+1)
    for i in range(n-1,-1,-1):
        l[i] = 1+max(x for x, y in zip(l[i+1:],a[i+1:]) if y > a[i])
    t = max(l)
    o = []
    m = -1
    for i, x in enumerate(a[:-1]):
        if l[i]==t and x > m:
            t -= 1
            o.append(x)
            m = x
    print(*o)
