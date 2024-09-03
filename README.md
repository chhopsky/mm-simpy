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

how it works:
- builds a normal distribution of players around 1350 elo as the mean
- puts you and your friend in a lobby
- attempts to match you with 6 other players randomly
- if sbmm is enabled, it will reject players that don't fit the parameters
- the default parameters set a maximum distance from the average elo of the team. play with these
- if team balancing is enabled, it will use the sbmm rating to balance teams while keeping you and your friend on the same team
- rates how many of the games are one-sided
- calculates how bad your friend got ruined
- tracks how many of their games had significantly higher rated players in it
