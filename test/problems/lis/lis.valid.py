#!/usr/bin/env python3

def subseq(a,b):
    i = j = 0
    while i < len(a) and j < len(b):
        if a[i] == b[j]:
            i += 1
        j += 1
    return i == len(a)

import sys
input_file =  sys.argv[1]
output_file = sys.argv[2]
answer_file = sys.argv[3]

with open(input_file,'rt') as FILE:
    # skip odd lines
    input_lines = [line.rstrip().split() for line in FILE][1::2]

with open(output_file,'rt') as FILE:
    output_lines = [line.rstrip().split() for line in FILE]

with open(answer_file,'rt') as FILE:
    answer_lines = [line.rstrip().split() for line in FILE]

# reject if output and answer have different numbers of lines
if len(answer_lines) != len(output_lines):
    raise

# reject if numbers of tokens on any pairs of corresponding lines are different
if any(len(a) != len(o) for a, o in zip(answer_lines,output_lines)):
    raise

# reject if output is not a subsequence of the input
if any(not subseq(o,i) for o,i in zip(output_lines,input_lines)):
    raise

# reject if not increasing
if any(any(int(o[i-1])>int(o[i]) for i in range(1,len(o))) for o in output_lines):
    raise
