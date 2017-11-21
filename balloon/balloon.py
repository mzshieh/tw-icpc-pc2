#!/usr/bin/env python3
import sys, os, argparse, re, json
from lxml import etree
from bs4 import BeautifulSoup as Soup
from subprocess import run

### Setup argument parser
parser = argparse.ArgumentParser(description="Balloon Sheet Printer")
parser.add_argument('-l','--log',default='balloon.log',
                    help='Store delivered balloons (default: balloon.log)')
parser.add_argument('-c','--cont',default=True,type=eval,
                    help='Continue to deliver (default: True)')

args = parser.parse_args()

with open(args.log,'at'):
    pass

delivered = {}
if args.cont:
    with open(args.log) as FILE:
        for line in FILE:
            try:
                teamID, probID, runID, penalty = line.strip().split()
                delivered[(teamID,probID)]={'run': runID, 'time': penalty}
            except:
                print('failed to parse old log',file=sys.stderr)

# Main loop
line_buf = []
for line in sys.stdin:
    line = line.strip()
    # print('ECHO',line,file=sys.stderr)
    # print('LINE_BUF',line_buf,file=sys.stderr)
    if len(line_buf) == 0 and line == '<run>':
        line_buf.append(line)
    elif len(line_buf):
        line_buf.append(line)
    if line_buf and line == '</run>':
        s = Soup('\n'.join(line_buf),'lxml')
        if s.find('judged').text == 'True' and s.find('solved').text == 'true':
            runID = s.find('id').text
            probID = chr(ord('A')-1+int(s.find('problem').text))
            teamID = s.find('team').text
            penalty = int(float(s.find('time').text)/60)
            with open(args.log,'at') as FILE:
                print(teamID,probID,runID,penalty,file=FILE)
            delivered[(teamID,probID)]={'run': runID, 'time': penalty}
            print(teamID,probID,runID,penalty)
        line_buf = []
