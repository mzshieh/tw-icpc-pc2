# PC^2 scripts for ICPC-style contest in Taiwan

### Prerequisites
+ [`isolate`](https://github.com/ioi/isolate/) sandbox
+ [PC^2^ 9.4.1](http://pc2.ecs.csus.edu/secret.941-0124.html)

### `sandbox` directory

Fitting `isolate` into PC^2 system. Run `sudo ./install.sh` to install.

### `desktop` directory

Create executable icons on the desktop. Just copy what you need to `~/Desktop/`.

### `validator` directory

`valid.py` is a script compatible with PC^2 system. It provide token-based
comparison between the answer and the team's output. It supports strictly
pattern match (`diff` mode) and error tolerate modes (`abs`, `rel` and 
`abs_rel` modes).

### `testcode` directory

Some codes are provided for testing the judge system

### `yaml` directory

Some useful configuration file(s) for PC^2 system
