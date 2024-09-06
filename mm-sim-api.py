import json
import uvicorn
import numpy as np

from fastapi import FastAPI, Request, Response, status
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from itertools import permutations

class ResourceNotFound(Exception):
    def __init__(self, type, id):
        self.id = id
        self.type = type

    def __str__(self):
        return f"{self.type.capitalize()} not found: {self.id}"

webservice = FastAPI()

@webservice.exception_handler(ResourceNotFound)
async def validation_exception_handler(request, exc):
    return JSONResponse({"message": str(exc)}, status_code=404)

@webservice.get("/generate_players")
def gen_players_base():
    return json.dumps(generate_players())

@webservice.get("/generate_players/{number_of_players}")
async def gen_players_num(number_of_players):
    return json.dumps(generate_players(number_of_players))

@webservice.get("/generate_players/{number_of_players}/{average_elo}")
async def gen_players_num(number_of_players, average_elo):
    return json.dumps(generate_players(number_of_players, average_elo))

def generate_players(count=10000, average_elo=1350):
    rng = np.random.default_rng()
    generated_players = average_elo + average_elo * rng.normal(0, 1/3 , count)

    lowest = 0
    highest = 0

    # normal distribution can technically be less than zero with this generation
    # method so bump anyone below zero back to 1. this should be only a handful of
    # players
    for i, number in enumerate(generated_players):

        if (number < 1):
            generated_players[i] = np.float64(1)

        # track highest and lowest
        if number > highest:
            highest = generated_players[i]
        if number < lowest:
            lowest = generated_players[i]
    return generated_players

@webservice.get("/", response_class=HTMLResponse)
def web_home(request: Request):
    return templates.TemplateResponse("web_controller.html", {"request": request, "status": broadcast.get_current_match_data_json()})

def evaluate_player_for_match(player_pool, players, new_player, params):
    if player_pool[new_player] - sum_team(players) / len(players) + 1 < params["max_skill_difference"]:
        # print(f"player {player_pool[player]} + match avg {sum_team(players) / len(players) + 1} < {params['max_skill_difference']}")
        return True
    else:
        # print(f"rejecting player with elo {player_pool[player]}")
        return False

# more sensible balancing of teams that tries to get a match within parameters then finds the optimal
# way to distribute those players across teams
def balance_teams_complex(playerlist, team_restriction = []):
    fixed_team = []
    best_team_differential = 10000 # this is just a random high number
    output_players = []

    if len(team_restriction):
        for teammate in team_restriction:
            fixed_team.append(playerlist[teammate])

        for teammate in reversed(team_restriction):
            playerlist.pop(teammate)
    
    # brute force this, im lazy and its a holiday
    for i, combination in enumerate(permutations(playerlist)):
        combination_list = fixed_team + list(combination)

        if abs(sum_team(combination_list[0:4]) - sum_team(combination_list[4:8])) < best_team_differential:
            best_team_differential = abs(sum_team(combination_list[0:4]) - sum_team(combination_list[4:8]))
            output_players = combination_list

    return output_players

# helper function for adding teams because this data is in numpy and it fights with python's
# built in sum() function
def sum_team(team):
    teamsum = 0
    for player in team:
        teamsum += player
    
    return teamsum 

def do_matchmaking(player_pool, params):
    show_example_match = False
    enable_team_balancing = True
    enable_simple_sbmm = False
    player_pool_size = 10000
    debug = False

    # simulation match parameters
    simulations_to_run = 100

    # player parameters 
    your_elo = 1350
    your_friends_elo = 500
    your_friends_skill_elo = 500

    # distance from match average in which we will accept a new matching player
    sbmm_parameters = {
        "max_skill_difference": 300
    }

    # how much elo difference for the team constitutes an imbalance
    acceptable_difference = 100

    # and how far above you we consider a player to be high elo
    high_elo_difference = 300

if __name__ == "__main__":
    webservice.mount("/static", StaticFiles(directory="/static"), name="static")
    uvicorn.run(webservice, host="0.0.0.0", port=8000, access_log=True)