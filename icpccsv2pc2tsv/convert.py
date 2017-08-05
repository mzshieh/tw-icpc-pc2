#!/usr/bin/env python3
import sys, os, argparse, re
from random import randint as ri
from subprocess import run


def rand_alpha(n):
    return ''.join([chr(ord('A')+ri(0,25)) for _ in range(n)])

### Setup argument parser
parser = argparse.ArgumentParser(description="MZ's PC^2 Validator")
parser.add_argument('-a','--admin',default=1,type=int,
                    help='#Administrators (default: %(default)g)')
parser.add_argument('-t','--team',default=0,type=int,
                    help='#Backup_Teams (default: %(default)g)')
parser.add_argument('-j','--judge',default=12, type=int,
                    help='#Judges (default: %(default)d)')
parser.add_argument('-s','--scoreboard',default=1,type=int,
                    help='#Scoreboard (default: %(default)d)')
parser.add_argument('-f','--feeder',default=1,type=int,
                    help='#Feeders (default: %(default)d)')
parser.add_argument('-r','--random-password',default=True,
                    type=lambda x: x in ['T','t','True','true'],
                    help='Use random password (default: %(default)s)')

args = parser.parse_args()

tsv_header = ['site', 'account', 'displayname', 'password', 'group', 'permdisplay', 'permlogin', 'externalid', 'alias', 'permpassword', 'longschoolname', 'shortschoolname', 'countrycode']
csv_header = ["Site","Team","","Institution","Coach","Created","Status","Ineligibilityprediction","Paid","Extended <br/>status"]

print(*tsv_header,sep='\t')

for i in range(1,1+args.admin):
    row = ['1']
    row += ['administrator{}'.format(i)]*2
    row += ['administrator{}'.format(i)] if not args.random_password else [rand_alpha(8)]
    row += ['', 'false', 'true', str(1000+i), '', 'true', '', '', 'TWN']
    print(*row,sep='\t')

for i in range(1,1+args.judge):
    row = ['1']
    row += ['judge{}'.format(i)]*2
    row += ['judge{}'.format(i)] if not args.random_password else [rand_alpha(8)]
    row += ['', 'false', 'true', str(1000+i), '', 'true', '', '', 'TWN']
    print(*row,sep='\t')

for i in range(1,1+args.scoreboard):
    row = ['1']
    row += ['scoreboard{}'.format(i)]*2
    row += ['scoreboard{}'.format(i)] if not args.random_password else [rand_alpha(8)]
    row += ['', 'false', 'true', str(1000+i), '', 'true', '', '', 'TWN']
    print(*row,sep='\t')

for i in range(1,1+args.feeder):
    row = ['1']
    row += ['feeder{}'.format(i)]*2
    row += ['feeder{}'.format(i)] if not args.random_password else [rand_alpha(8)]
    row += ['', 'false', 'true', str(1000+i), '', 'true', '', '', 'TWN']
    print(*row,sep='\t')

num_team = 0
it = iter(sys.stdin)
next(it)
for line in it:
    tokens = line.rstrip('\n').strip('"').split('","')
    if tokens[6] != 'Accepted':
        continue
    num_team += 1
    i = num_team
    row = ['1']
    row += ['team{}'.format(i)]
    row += [tokens[1]]
    row += ['team{}'.format(i)] if not args.random_password else [rand_alpha(8)]
    row += ['','true','true',str(1000+i),'','false',tokens[2],'','TWN']
    print(*row,sep='\t')

for i in range(1,1+args.team):
    i += num_team
    row = ['1']
    row += ['team{}'.format(i)]*2
    row += ['team{}'.format(i)] if not args.random_password else [rand_alpha(8)]
    row += ['', 'false', 'true', str(1000+i), '', 'false', '', '', 'TWN']
    print(*row,sep='\t')
