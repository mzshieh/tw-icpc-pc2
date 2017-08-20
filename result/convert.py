#!/usr/bin/env python3
import sys, os, argparse, re
from lxml import etree 
from subprocess import run

### Setup argument parser
parser = argparse.ArgumentParser(description="Convert Results (XMLs) to Standings (tsv)")
parser.add_argument('-t','--template',
                    help='ICPC standing template XML')
parser.add_argument('-r','--result',
                    help='PC^2 result')
parser.add_argument('-o','--output',
                    help='Output standing')
parser.add_argument('-g','--gold',type=int,default=8,
                    help='Number of Gold Prizes')
parser.add_argument('-s','--silver',type=int,default=16,
                    help='Number of Silver Prizes')
parser.add_argument('-b','--bronze',type=int,default=24,
                    help='Number of Bronze Prizes')

args = parser.parse_args()

team = {}

with open(args.template) as FILE:
    for child in etree.parse(FILE).getroot():
        teamname = child.get('TeamName')
        if teamname != None:
            team[teamname] = {'TeamID':child.get('TeamID')}

with open(args.result) as FILE:
    for child in etree.parse(FILE).getroot():
        if child.tag != 'teamStanding': continue
        t = team.get(child.get('teamName'))
        if t == None: continue
        for key in ['rank','solved','points','lastSolved']:
            t[key]=child.get(key)

for val in team.values():
    rank = int(val.get('rank'))
    if rank <= args.gold:
        val['medal'] = 'Gold'
    elif rank <= args.gold+args.silver:
        val['medal'] = 'Silver'
    elif rank <= args.gold+args.silver+args.bronze:
        val['medal'] = 'Bronze'
    else:
        val['medal'] = ''

with open(args.output,'wt') as FILE:
    print('file_version\t1',file=FILE)
    for v in team.values():
        print(v['TeamID'],v['rank'],v['medal'],v['solved'],v['points'],v['lastSolved'],'',sep='\t',file=FILE)


