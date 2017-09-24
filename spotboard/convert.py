#!/usr/bin/env python3
import sys, os, argparse, re, json
from lxml import etree 
from subprocess import run

### Setup argument parser
parser = argparse.ArgumentParser(description="Convert PC^2 Contest XML to Spotboard JSON")
parser.add_argument('-i','--input',default='contest.xml',
                    help='PC^2 Contest XML')
parser.add_argument('-f','--five-field',default='Run5field',
                    help='PC^2 Run 5 Field')
parser.add_argument('-r','--runs',default='runs.json',
                    help='Spotboard runs.json')
parser.add_argument('-c','--contest',default='contest.json',
                    help='Spotboard contest.json')
parser.add_argument('-u','--univ',default='univ.csv',
                    help='University mapping (csv)')

args = parser.parse_args()

# Load runs from Run 5 field
runs = []
with open(args.five_field) as FILE:
    for line in FILE:
        fields = line.strip().split(',')
        if len(fields)==5 and fields[4] in ['Yes','No']:
            runs.append({'id':int(fields[0]), 
                         'team':int(fields[1]), 
                         'problem': ord(fields[2])-ord('A'),
                         'result': fields[4],
                         'submissionTime': int(fields[3])})
# Create runs.json    
runs = {'runs': runs, 'time':{"contestTime":18000,"noMoreUpdate":False,"timestamp":0}}
with open(args.runs,'wt') as FILE:
    print(json.dumps(runs),file=FILE)

# Load Team -> University mapping
univ = {}
with open(args.univ) as FILE:
    for line in FILE:
        col = eval(line.strip())
        if len(col) < 5: continue
        team, university = col[2],col[4]
        univ[team] = university
# Load contest information from contest.xml
balloons = ['darkgreen', 'violet', 'gold', 'gray', 'white', 'purple', 
    'yellow', 'lightblue', 'turquoise', 'pink', 'blue', 'lime', 'brown', 
    'darkorange', 'red', 'orange', 'deeppink', 'skyblue', 'ivory']
contest = {"systemName": "PC^2", "systemVersion": "9.4.1", "teams":[],"problems":[]}
prob_cnt = 0
with open(args.input) as FILE:
    for child in etree.parse(FILE).getroot():
        if child.tag == 'contest_information':
            contest['title'] = child.get('title')
        elif child.tag == 'account' and child.get('type')=='TEAM':
            contest['teams'].append({
                'id':int(child.get('number')),
                'name':child.get('name')+' ({})'.format(univ.get(child.get('name'),'Unofficial'))})
        elif child.tag == 'problem' and child.get('active')=='true':
            prob_cnt += 1
contest['problems'] = [{'id':i,'name':chr(ord('A')+i),'title':chr(ord('A')+i),'color':balloons[i]}
    for i in range(prob_cnt)]

# Create contest.json
with open(args.contest,'wt') as FILE:
    print(json.dumps(contest),file=FILE)
