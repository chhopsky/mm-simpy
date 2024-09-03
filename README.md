A simple matchmaking simulator comparing stochastic matchmaking results (no SBMM) with SBMM results while attempting to play with a friend who is bad

to the surprise of absolutely no-one, the friend has a way better time with SBMM because:
1. the matches are more likely to be balanced
2. the average skill of the participants is lower
   
we are not simulating changing elo on account of that i didn't feel like it

to use:
- install python 3.11 via any means. if you have windows there's an installer: https://www.python.org/ftp/python/3.11.7/python-3.11.7-amd64.exe
- download this repo to your computer somewhere
- pip install pipenv
- install the requirements
- pipenv shell
- `python mm-simpy.py` to run
- adjust the parameters at the top of the file to see various results
