#!/usr/bin/env python3
import sys, os, argparse, re
from math import fabs

### Setup argument parser
parser = argparse.ArgumentParser(description="MZ's PC^2 Validator")
parser.add_argument('-i','--input',
                    help='Test input file')
parser.add_argument('-o','--output',
                    help='Team\'s output file')
parser.add_argument('-a','--answer',
                    help='Judge\'s answer file')
parser.add_argument('-v','--verdict',
                    help='Validator\'s verdict file')
parser.add_argument('-m','--mode',default='diff',
                    choices=['diff','abs','rel','abs_rel'],
                    help='Mode (default: %(default)s)')
parser.add_argument('-e','--error',type=float,default=5*0.0000001,
                    help='Tolerance error (default: %(default)g)')
parser.add_argument('-t','--time-limit',type=float,default=10.0,
                    help='Time limit (default: %(default)g seconds)')

args = parser.parse_args()

TIME_LIMIT = args.time_limit

verdict = '<?xml version="1.0"?><result outcome="%s" security="'
verdict += args.verdict
verdict +='"> %s </result>'

def bad(ans,out):
    if args.mode == 'diff':
        return ans != out
    elif args.mode == 'abs':
        return fabs(float(ans)-float(out)) > args.error
    elif args.mode == 'rel':
        return float(ans)==0 or fabs((float(ans)-float(out))/float(ans)) > args.error
    elif args.mode == 'abs_rel':
        if fabs(float(ans)-float(out)) <= args.error: return False
        return float(ans)==0 or fabs((float(ans)-float(out))/float(ans)) > args.error
    return True

def raiseIfInvalid(IN, OUT, ANS):
    if len(ANS) != len(OUT): ## must have same number of lines
        raise
    if any(bad(ans,out) for ans, out in zip(ANS,OUT)):
        ## NOT OK
        raise

def isAC():
    try:
        ## Line-based checking while ignore leading and trailing white spaces
        ## rstrip() removes ' ', '\n', '\r' on the right end
        with open(args.input,'rt') as FILE: 
            IN = [line.rstrip() for line in FILE]
        with open(args.answer,'rt') as FILE:
            ANS = [line.rstrip() for line in FILE]
        with open(args.output,'rt') as FILE:
            OUT = [line.rstrip() for line in FILE]
        raiseIfInvalid(IN,ANS,OUT)
    except:
        return False
    return True

def isOCS():
    if os.path.exists('EXITCODE.TXT'):
        with open('EXITCODE.TXT','rt') as FILE:
            return FILE.readline().rstrip() != '0x1'
    return False

def isTLE():
    with open('SANDBOX_VERDICT','rt') as FILE:
        line = FILE.readline().strip()
        if line.startswith('Time'):
            return True
        if line.startswith('OK'):
            return float(line.replace('(',' ').split()[1]) > args.time_limit
    return False

def isRE():
    return os.path.exists('EXITCODE.TXT')

if isOCS():
    verdict %= ('No - Other - Contact Staff',)*2
elif isTLE():
    verdict %= ('No - Time Limit Exceeded',)*2
elif isRE():
    verdict %= ('No - Run-time Error',)*2
elif isAC():
    verdict %= ('accepted', 'Yes')
else:
    verdict %= ('No - Wrong Answer',)*2

with open(args.verdict,'wt') as result:
    print(verdict,file=result)

print(verdict[:-1].split('>')[-1].split('<')[0].strip())
with open('SANDBOX_RESULT','rt') as FILE:
    for line in FILE:
        print(line.strip())
