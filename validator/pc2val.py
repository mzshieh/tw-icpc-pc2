#!/usr/bin/env python3
import sys, os, argparse, re
from math import fabs, isnan, isinf
from subprocess import run

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
                    choices=['diff','abs','rel','abs_rel','ext'],
                    help='Mode (default: %(default)s)')
parser.add_argument('-e','--error',type=float,default=5*0.0000001,
                    help='Tolerance error (default: %(default)g)')
parser.add_argument('-x','--external',
                    help='External validator script')
parser.add_argument('-t','--time-limit',type=float,default=10.0,
                    help='Time limit (default: %(default)g seconds)')

args = parser.parse_args()

TIME_LIMIT = args.time_limit

verdict = '<?xml version="1.0"?><result outcome="%s" security="'
verdict += args.verdict
verdict +='"> %s </result>'

def invalidToken(ans,out):
    # If two tokens are the same, then the output is valid.
    if ans == out: return False
    if args.mode == 'diff': return True

    # Floating point mode
    # Cast str to float. If failed, then the output is invalid. Raise an exception.
    # Note: The validator still work for format including strings, since identical
    #       two tokens should pass the previous lines.
    a, o = float(ans), float(out)
    if isnan(o) or isinf(o):
        return True

    if args.mode == 'abs':
        return fabs(a-o) > args.error
    elif args.mode == 'rel':
        if a == o: return False
        return a==0 or fabs((a-o)/a) > args.error
    elif args.mode == 'abs_rel':
        if fabs(a-o) <= args.error: return False
        return a==0 or fabs((a-o)/a) > args.error
    return True

def invalidLine(ans,out):
    if args.mode == 'diff':
        # Purely line-based: currently, only diff is.
        return ans != out
    # Token-based validator for each line
    # abs, rel, abs_rel
    ans, out = ans.split(), out.split()
    return len(ans)!=len(out) or any(invalidToken(a,o) for a, o in zip(ans,out))

def raiseIfInvalid(IN, ANS, OUT):
    if len(ANS) != len(OUT): ## must have same number of lines
        raise
    if any(invalidLine(ans,out) for ans, out in zip(ANS,OUT)):
        ## NOT OK
        raise

def isAC():
    try:
        ## External validator
        ## Run it with arguments input, team_outut, judge answers
        ## If yes, it returns 0. Otherwise, it return non-zero.
        if args.mode == 'ext':
            if run([args.external,args.input,args.output,args.answer]).returncode:
                raise
            else:
                return True
        ## Line-based checking while ignore leading and trailing white spaces
        ## rstrip() removes ' ', '\n', '\r' on the right end
        with open(args.input,'rt') as FILE: 
            IN = [line.rstrip() for line in FILE]
        with open(args.answer,'rt') as FILE:
            ANS = [line.rstrip() for line in FILE]
            # remove trailing blank lines
            while len(ANS) and ANS[-1]=='':
                ANS.pop()
        with open(args.output,'rt') as FILE:
            OUT = [line.rstrip() for line in FILE]
            # remove trailing blank lines
            while len(OUT) and OUT[-1]=='':
                OUT.pop()
        raiseIfInvalid(IN,ANS,OUT)
    except:
        return False
    return True

def isOCS():
    # pc2box should exit with 0 or 1
    if os.path.exists('EXITCODE.TXT'):
        with open('EXITCODE.TXT','rt') as FILE:
            return FILE.readline().rstrip() != '0x1'
    # Mode is external but there is no external validator
    return args.mode != 'ext' and args.external

def isTLE():
    with open('.SANDBOX_VERDICT','rt') as FILE:
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
with open('.SANDBOX_RESULT','rt') as FILE:
    for line in FILE:
        print(line.strip())
