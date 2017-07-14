from argparse import ArgumentParser
from flask import Flask, Response
from subprocess import run

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024

### Let's pass the name of the contest via arguments!
if __name__ == '__main__':
    parser = ArgumentParser(description='A web-based printer server for programming contest')
    parser.add_argument('name',nargs='*',default='ACM-ICPC',
            help='The name of the contest')
    contest = ' '.join(parser.parse_args().name)
else:
    contest = 'ACM-ICPC'

def a2ps(team,filename,data):
    title = team+': '+filename
    medium = 'A4'
    cmd = ['a2ps','-b'+contest,'--medium='+medium,'--center-title='+title,
            '--line-number=1','-T4',team+'/'+filename]
    run(cmd)

@app.route('/print',methods=['GET'])
def print_get():
    return 'GET: '+contest

@app.route('/print',methods=['POST'])
def print_post():
    return 'OK'

if __name__ == '__main__':
    app.run(port=50003)
