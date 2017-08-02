from argparse import ArgumentParser
from flask import Flask, Response, redirect, render_template, request, session, url_for, send_from_directory
from werkzeug.utils import secure_filename
from subprocess import run
from time import strftime, localtime
import json, os, time, mimetypes

### Store the codes to be printed here
UPLOAD_FOLDER = 'codes'
### Only accept C/C++/Java/Python source codes
ALLOWED_EXTENSIONS = set(['c','cpp','java','py'])

### max content length is 1 megabyte
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

### Load account information
### json format
### with open('config/password.json','rt') as FILE:
###     password = json.load(FILE)
### PC^2 tsv format
password = {}
with open('config/account.tsv','rt') as FILE:
    for line in FILE:
        line = line.split('\t')
        if len(line) < 4 or not line[1].startswith('team'): continue
        password[line[1]] = line[3]

### Let's pass the name of the contest via arguments!
if __name__ == '__main__':
    parser = ArgumentParser(description='A web-based printer server for programming contest')
    parser.add_argument('-p','--port',type=int,default=50003,
            help='Port to listen (default: %(default)d)')
    parser.add_argument('-t','--to-file',type=lambda x: x in ['T','t','True','true'],
            default=True, help='Print to file (default: %(default)s)')
    parser.add_argument('name',nargs='*',default=['ACM-ICPC'],
            help='The name of the contest')
    args = parser.parse_args()
    contest = ' '.join(args.name)

### Use a2ps to print codes
def a2ps(team,filename,logfile):
    title = ': '.join(filename.split('_',1))
    medium = 'A4'
    chars_per_line = 80
    tabsize = 4
    cmd = ['a2ps','-b'+contest,'--medium='+medium,'--center-title='+title,
            '--chars-per-line={}'.format(chars_per_line),'--line-number=1',
            '--tabsize={}'.format(tabsize),
            os.path.join(app.config['UPLOAD_FOLDER'],filename)]
    if args.to_file:
        cmd+=['--output=ps/{}.ps'.format(logfile)]
    run(cmd)

### Code Printer page
@app.route('/code_printer',methods=['GET'])
def code_printer():
    return render_template('code_printer.html')

### Post to print
@app.route('/print',methods=['POST'])
def print_post():
    ### Check if team and password are matched
    team = request.form.get('team')
    if team not in password or password[team]!=request.form.get('password'):
        return render_template('login_failed.html')

    ### Check if filename is OK
    code = request.files.get('code')
    if code == None or code.filename == '':
        return render_template('no_file.html')
    if not any(code.filename.lower().endswith('.'+ext) for ext in ALLOWED_EXTENSIONS):
        return render_template('wrong_type.html')

    ### Save  codes
    filename = secure_filename(team+'_'+code.filename)
    fullname = os.path.join(app.config['UPLOAD_FOLDER'],filename)
    code.save(fullname)

    ### Check if the file is text
    try:
        with open(fullname,'rt') as FILE:
            num_lines = len(FILE.readlines())
    except:
        return render_template('wrong_type.html')

    ### Check the file is short enough
    if os.stat(fullname).st_size > 128*1024 or num_lines>4096:
        return render_template('too_long.html')

    ### Copy the file to log with IP and timestamp
    os.makedirs('log/'+team,exist_ok=True)
    now = time.time()
    logfile = strftime('%H%M%S',localtime(now))+('.%.6f_'%(now%1.0))[2:]+filename
    logfile = request.remote_addr+'_'+logfile
    code.save(os.path.join('log/'+team,logfile))

    ### Ready to print
    a2ps(team,filename,logfile)
    return render_template('ok.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory('icon/','favicon.ico')

if __name__ == '__main__':
    if args.to_file:
        os.makedirs('ps',exist_ok=True)
    os.makedirs(app.config['UPLOAD_FOLDER'],exist_ok=True)
    app.run(host='0.0.0.0',port=args.port,threaded=True)
