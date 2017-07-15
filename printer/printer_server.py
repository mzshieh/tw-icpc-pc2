from argparse import ArgumentParser
from flask import Flask, Response, redirect, render_template, request, session, url_for
from werkzeug.utils import secure_filename
from subprocess import run
from time import strftime, localtime
import json, os, time

UPLOAD_FOLDER = 'codes'
ALLOWED_EXTENSIONS = set(['c','cpp','java','py'])

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

### Load account information
with open('config/password.json','rt') as FILE:
    password = json.load(FILE)

### Let's pass the name of the contest via arguments!
if __name__ == '__main__':
    parser = ArgumentParser(description='A web-based printer server for programming contest')
    parser.add_argument('name',nargs='*',default=['ACM-ICPC'],
            help='The name of the contest')
    contest = ' '.join(parser.parse_args().name)

def a2ps(team,filename):
    title = ': '.join(filename.split('_',1))
    medium = 'A4'
    cmd = ['a2ps','-b'+contest,'--medium='+medium,'--center-title='+title,
            '--chars-per-line=80','--line-number=1','-T4',
            os.path.join(app.config['UPLOAD_FOLDER'],filename)]
    cmd+=['--output=ps/{}.ps'.format(filename)]
    run(cmd)

@app.route('/code_printer',methods=['GET'])
def code_printer():
    return render_template('code_printer.html')

@app.route('/print',methods=['POST'])
def print_post():
    for key, value in request.form.items():
        print('{}: {}'.format(key,value))
    team = request.form.get('team')
    if team not in password or password[team]!=request.form.get('password'):
        return render_template('login_failed.html')
    code = request.files.get('code')
    if code == None or code.filename == '':
        return render_template('no_file.html')
    if not any(code.filename.lower().endswith('.'+ext) for ext in ALLOWED_EXTENSIONS):
        return render_template('wrong_type.html')
    filename = secure_filename(team+'_'+code.filename)
    code.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
    os.makedirs('log/'+team,exist_ok=True)
    now = time.time()
    logfile = strftime('%H%M%S',localtime(now))+('%.2f_'%(now%1.0))[2:]+filename
    code.save(os.path.join('log/'+team,logfile))
    a2ps(team,filename)
    return render_template('ok.html')

if __name__ == '__main__':
    app.run(port=50003)
