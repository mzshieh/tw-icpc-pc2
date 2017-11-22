#!/usr/bin/env python3
import sys, os, argparse, re, json
import time
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

os.makedirs('printed',exist_ok=True)

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
                print('failed to parse old log:',line.strip(),file=sys.stderr)

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
            # Supposed to be printed here
            if (teamID,probID) not in delivered:
                filename = 'printed/T{}_P{}_R{}'.format(teamID,probID,runID)
                with open(filename,'wt') as FILE:
                    print('''

   Balloon Delivery Sheet





  Team {} solved Problem {}
  Run {} at {} minutes





      Delivered by:
'''.format(teamID,probID,runID,penalty),file=FILE)
                run(['lp','-o','lpi=1.9','-o','cpi=3.5',filename])
                with open(args.log,'at') as FILE:
                    print(teamID,probID,runID,penalty,file=FILE)
                delivered[(teamID,probID)]={'run': runID, 'time': penalty}
                time.sleep(1)
        line_buf = []

print('The connection to the event feeder is closed.')
