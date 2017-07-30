from argparse import ArgumentParser
from flask import Flask, Response, redirect, render_template, request, session, url_for
from flask import send_from_directory
from werkzeug.utils import secure_filename
from subprocess import run
from time import strftime, localtime
import json, os, time, mimetypes, sys

### Store the codes to be printed here
UPLOAD_FOLDER = 'upload'
### Only accept C/C++/Java/Python source codes
ALLOWED_EXTENSIONS = set(['c','cpp','java','py'])

### max content length is 1 megabyte
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 128 * 1024 * 1024
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

### Let's pass the name of the contest via arguments!
if __name__ == '__main__':
    parser = ArgumentParser(description='A web-based test server for programming contest')
    parser.add_argument('-p','--port',type=int,default=50003,
            help='Port to listen (default: %(default)d)')
    parser.add_argument('-t','--to-file',type=lambda x: x in ['T','t','True','true'],
            default=True, help='Print to file (default: %(default)s)')
    parser.add_argument('name',nargs='*',default=['ACM-ICPC'],
            help='The name of the contest')
    args = parser.parse_args()
    contest = ' '.join(args.name)

@app.route('/result',methods=['GET'])
def result():
    return send_from_directory(app.config['UPLOAD_FOLDER'],'.SANDBOX_RESULT')

### Code Printer page
@app.route('/prog_tester',methods=['GET'])
def code_printer():
    return render_template('prog_tester.html')

### Post to print
@app.route('/test',methods=['POST'])
def code_test():
    ### Check if filename is OK
    code = request.files.get('code')
    testdata = request.files.get('input')
    if code == None or code.filename == '' or testdata == None or testdata.filename == '':
        return render_template('no_file.html')
    if not any(code.filename.lower().endswith('.'+ext) for ext in ALLOWED_EXTENSIONS):
        return render_template('wrong_type.html')

    ### Save  codes
    filename = secure_filename(code.filename)
    fullname = os.path.join(app.config['UPLOAD_FOLDER'],filename)
    code.save(fullname)
    dataname = os.path.join(app.config['UPLOAD_FOLDER'],'testdata.in')
    testdata.save(dataname)

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
    os.makedirs('log/',exist_ok=True)
    now = time.time()
    logfile = strftime('%H%M%S',localtime(now))+('.%.6f_'%(now%1.0))[2:]+filename
    logfile = request.remote_addr+'_'+logfile
    code.save(os.path.join('log/',logfile))

    if os.fork()==0:
        os.chdir(app.config['UPLOAD_FOLDER'])
        run(['pc2box','-i','0','-d','T','-u','F','g++','-O2','-std=c++11',filename])
        run(['pc2box','-i','1','./a.out'],stdin=open('testdata.in','rt'),stdout=open('ref','wt'))
        os._exit(0)

    return render_template('ok.html')

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'],exist_ok=True)
    app.run(host='0.0.0.0',port=args.port,threaded=True)
