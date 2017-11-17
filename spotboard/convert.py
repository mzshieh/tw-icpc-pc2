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


# Compute the scores

scores = {}

# Collect Accepted Time
for sub in runs:
    if sub['result']=='No': continue
    scores.setdefault(sub['team'],{})
    scores[sub['team']].setdefault(sub['problem'],(sub['id'],sub['submissionTime']))
    scores[sub['team']][sub['problem']] = min(scores[sub['team']][sub['problem']], (sub['id'],sub['submissionTime']))

# Compute penalty

# Collect accepted runs
for score in scores.values():
    penalty = sum(y for x, y in score.values())
    lastID = max(x for x, y in score.values())
    solved = len(score)
    score['solved'], score['penalty'], score['lastID'] = solved, penalty, lastID

# Compute penalty for rejected runs
for sub in runs:
    if sub['result']=='Yes': continue 
    if None == scores.get(sub['team']): continue
    if None == scores[sub['team']].get(sub['problem']): continue
    if scores[sub['team']][sub['problem']] < (sub['id'],sub['submissionTime']): continue
    scores[sub['team']]['penalty'] += 20

# Compute standings

rank = sorted(((-v['solved'],v['penalty'],v['lastID']),k) for k, v in scores.items())

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
# balloons = ['darkgreen', 'violet', 'gold', 'gray', 'white', 'purple', 
#     'yellow', 'lightblue', 'turquoise', 'pink', 'blue', 'lime', 'brown', 
#     'darkorange', 'red', 'orange', 'deeppink', 'skyblue', 'ivory']
balloons = ['yellow','lightblue','white','orange','darkgreen','purple',
    'ivory','blue','red','lime','gold','pink','violet']
contest = {"systemName": "PC^2", "systemVersion": "9.4.1", "teams":[],"problems":[]}
prob_cnt = 0
teams = {}
with open(args.input) as FILE:
    for child in etree.parse(FILE).getroot():
        if child.tag == 'contest_information':
            contest['title'] = child.get('title')
        elif child.tag == 'account' and child.get('type')=='TEAM':
            contest['teams'].append({
                'id':int(child.get('number')),
                'name':child.get('name')+' ({})'.format(univ.get(child.get('name'),'Unofficial'))})
            teams[int(child.get('number'))] = {}
            teams[int(child.get('number'))]['name'] = child.get('name')
            teams[int(child.get('number'))]['univ'] = univ.get(child.get('name'),'Unofficial')
        elif child.tag == 'problem' and child.get('active')=='true':
            prob_cnt += 1
contest['problems'] = [{'id':i,'name':chr(ord('A')+i),'title':chr(ord('A')+i),'color':balloons[i]}
    for i in range(prob_cnt)]

# Create contest.json
with open(args.contest,'wt') as FILE:
    print(json.dumps(contest),file=FILE)

for (solved,penalty,lastID), teamID in rank:
    print(teams[teamID]['name'],-solved,penalty)
