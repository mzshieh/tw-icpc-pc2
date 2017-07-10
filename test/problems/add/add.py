#!/usr/bin/env python3

import sys

for line in sys.stdin:
    print(sum([int(x) for x in line.split()]))
