#!/usr/bin/env python3
import argparse, os, sys, re
from random import randint as ri
from subprocess import run
from shlex import quote
from shutil import copy
from math import ceil

### Setup argument parser
parser = argparse.ArgumentParser(description='Run a program in an isolate sandbox.')
parser.add_argument('-i','--id',type=int,default=ri(0,999),
                    help='Run in box ID [0,999] (default: random)')
parser.add_argument('-m','--mem',type=float,default=512.0,
                    help='Memory limit in megabytes (default: %(default)s)')
parser.add_argument('-t','--time',type=float,default=10.0,
                    help='Time limit in seconds (default: %(default)s)')
parser.add_argument('-s','--size',type=float,default=1.0,
                    help='Output size limit in megabytes (default: %(default)s)')
parser.add_argument('-d','--dump',type=lambda x: x in ['T','t','True','true'],
                    default=False, help='Dump all files out (default: %(default)s)')
parser.add_argument('-u','--use-stdin',type=lambda x: x in ['T','t','True','true'],
                    default=True, 
                    help='The program uses stdin (default: %(default)s)')
parser.add_argument('cmd',help='Command to execute the program')
parser.add_argument('arguments',nargs=argparse.REMAINDER,help='Arguments')

### Parsing the arguments
res = parser.parse_args()
box_id = res.id
mem_limit = ceil(res.mem*1024)   # isolate uses kilobytes
time_limit = res.time
size_limit = ceil(res.size*1024) # isolate uses kilobytes
cmd = res.cmd
arg = res.arguments
dump = res.dump
use_stdin = res.use_stdin

### Setup the default file names
RESULT = 'SANDBOX_RESULT'
INIT = 'SANDBOX_INIT'
PATH = 'SANDBOX_PATH'
VERDICT = 'SANDBOX_VERDICT'
OUTPUT = 'SANDBOX_OUTPUT_%016X'%ri(0,2**64-1)
ERROR = 'SANDBOX_ERROR_%016X'%ri(0,2**64-1)
INPUT = 'SANDBOX_INPUT_%016X'%ri(0,2**64-1)

### Setup the arguments for invoking isolate
isolate = ['isolate','--box={}'.format(box_id),'--cg']
io = ['--stdin='+INPUT,'--stdout='+OUTPUT,'--stderr='+ERROR,'--meta='+RESULT]
run_env = ['-e','--run','/usr/bin/env','--']
limit = ['-p','--fsize={}'.format(size_limit),'--time={}'.format(time_limit)]
limit+= ['--wall-time={}'.format(2*time_limit),'--extra-time=2']
if cmd == 'java':
    # Potentially buggy
    arg = [tok for tok in arg if not re.match('-Xmx.*|-Xms.*|-Xss.*',tok)]
    arg = '-Xmx{}k -Xms{}k -Xss{}k'.format(*((mem_limit,)*3)).split() + arg
else:
    limit+= ['--cg-mem={}'.format(mem_limit),'--mem={}'.format(mem_limit)]
execute = isolate + io + limit + run_env + [cmd] + arg
### Print debug
# print(' '.join(isolate))

### Clean up quietly
with open('/dev/null','w') as dev_null:
    cleanup = isolate + ['--cleanup']
    run(cleanup,stderr=dev_null)

### Init
with open(INIT,'wt') as init_log:
    with open(PATH,'wt') as box_path:
        init_proc = run(isolate+['--init'],stdout=box_path)
        print('init return code: {}'.format(init_proc.returncode),file=init_log)

### Execute cmd in the isolate sandbox
# sucessful finished: exit code 0
# fail to finish: exit code 1
# sandbox internal err: exit code 2
# fail to initialize: exit code 255 
with open(VERDICT,'wt') as verdict:
    exitcode = 255
    if init_proc.returncode:
        print('Initialization failed',file=verdict)
    else:
        ### Copy necessary files to the sandbox
        for box_path in open(PATH,'rt'): pass
        box_path = box_path[:-1] + '/box' # removing newline
        if cmd == 'java':
            for name in filter(lambda x: x.endswith('.class'), os.listdir()):
                copy(name,box_path)
        else:
            # Potentially buggy
            for name in filter(lambda x: x in arg, os.listdir()):
                copy(name,box_path)
            if os.path.isfile(cmd):
                copy(cmd,box_path)
        ### Consume the input
        with open(box_path+'/'+INPUT,'wt') as stdin:
            if use_stdin:
                for line in sys.stdin:
                    print(line.rstrip(),file=stdin)
        ### Run and get exitcode
        exitcode = run(execute,stderr=verdict).returncode
        if exitcode > 1:
            print('Sandbox internal error',file=sys.stderr)
        else:
            ### Dump the output to stdout
            run(['/usr/bin/env','head','--bytes={}'.format(size_limit*1024),box_path+'/'+OUTPUT])
            ### Dump the error to stderr
            with open(box_path+'/'+ERROR,'rt') as err:
                for line in err:
                    print(line.rstrip(),file=sys.stderr)
            ### Dump the files from the sandbox to current directory
            if dump:
                os.system('cp -rn {}/* .'.format(box_path))

### Clean up
with open('/dev/null','wt'):
    run(isolate+['--cleanup'])

sys.exit(exitcode)
