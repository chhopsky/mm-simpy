import numpy as np
from pprint import pprint
from copy import deepcopy
from itertools import permutations
import random

# running parameters
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

# SBMM accept or reject
def evaluate_player_for_match(player, params):
    if player_pool[player] - sum_team(players) / len(players) + 1 < params["max_skill_difference"]:
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
            # print(f"new best match found:")
            # print(f"team 1: {sum_team(combination_list[0:4])}: {combination_list[0:4]}")
            # print(f"team 2: {sum_team(combination_list[4:8])}: {combination_list[4:8]}")
            # print(f"difference: {best_team_differential}")

    # if playerlist != output_players:
    #     print("team was rebalanced during queuing")

    return output_players

# helper function for adding teams because this data is in numpy and it fights with python's
# built in sum() function
def sum_team(team):
    teamsum = 0
    for player in team:
        teamsum += player
    
    return teamsum 

## ALRIGHT NOW THE ACTUAL CODE
## initialize a random number generator off a normal distribution
## standard deviation 1/3rd, average 50, 10k records

print(f"generating {player_pool_size} players for matchmaking simulation\n")
rng = np.random.default_rng()
generated_players = 1350 + 1350 * rng.normal(0, 1/3 , player_pool_size)

sum = 0
lowest = 0
highest = 0

print(f"team balancing is {'on' if enable_team_balancing else 'off'}")
print(f"sbmm is {'on' if enable_simple_sbmm else 'off'}")

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

    # add up our values to get the average so we can validate that it worked
    sum += number

# just some visual validation
if (debug):
    print(f"\naverage elo: {round(sum / len(generated_players))}")
    print(f"highest elo: {round(highest)}")
    print(f"lowest elo: {lowest}\n")

    # go through the entire set and add them to their brackets
    outputs = np.histogram(generated_players, bins=10)

    i=0
    for number in outputs[0]:
        print(f"{i + 1}0th percentile bracket: {number}")
        i += 1

# make a copy of our results so we can remove players as they're matched
player_pool = list(generated_players)

print(f"\nyour elo: {your_elo}")
print(f"your friends elo: {your_friends_elo}")

if show_example_match:
    print("\nexample match results:\n")
    # no SBMM section
    # pick six random players to match with
    players = [your_friends_elo, your_elo]

    while len(players) < 8:
        # select a player, add it to the selection, remove it from the pool
        selected_player = random.randint(0, len(player_pool) - 1)
        if (enable_simple_sbmm):
            if evaluate_player_for_match(selected_player, sbmm_parameters): 
                players.append(float(player_pool[selected_player]))
                player_pool.pop(selected_player)
        else:
            players.append(float(player_pool[selected_player]))
            player_pool.pop(selected_player)

    your_team_total = 0
    enemy_team_total = 0

    if (enable_team_balancing):
        players = balance_teams_complex(players, team_restriction=[0,1])

    print("your team:")

    for i, k in enumerate(range(4)):
        print(f"teammate {k + 1}: {round(players[k])}")
        your_team_total += players[k]

    print(f"your team total: {round(your_team_total)}")
    print(f"your team average: {round(your_team_total / 4)}\n")

    print("enemy team:")
    for i, k in enumerate(range(4, 8)):
        print(f"opponent {k - 3}: {round(players[k])}")
        enemy_team_total += players[k]

    print(f"enemy team total: {round(enemy_team_total)}")
    print(f"enemy team average: {round(enemy_team_total / 4)}\n")

    if (abs(enemy_team_total - your_team_total) < acceptable_difference):
        print("match was balanced")
    else:
        if (enemy_team_total > your_team_total):
            print(f"match expectation: you lose")
        else:
            print(f"match expectation: you win")
        print(f"match was unbalanced by {round(abs(enemy_team_total - your_team_total))}")

## reset and run the simulation 50 times

rejected_players = 0
high_elo_presence_your_team = 0
high_elo_presence_enemy_team = 0
wins = 0
fair_matches = 0
losses = 0

print(f"\nRunning {simulations_to_run} simulated matches:\n")

total_elo_matches = 0

for i in range(simulations_to_run):
    player_pool = list(generated_players)
    players = [your_friends_elo, your_elo]
    match_count_to_test = 50

    while len(players) < 8:
        # select a player, add it to the selection, remove it from the pool
        selected_player = random.randint(0, len(player_pool) - 1)
        if (enable_simple_sbmm):
            if evaluate_player_for_match(selected_player, sbmm_parameters): 
                players.append(float(player_pool[selected_player]))
                player_pool.pop(selected_player)
            else:
                rejected_players += 1
        else:
            players.append(float(player_pool[selected_player]))
            player_pool.pop(selected_player)

    assert(len(players) == 8)

    your_team_total = 0
    enemy_team_total = 0

    if (enable_team_balancing):
        players = balance_teams_complex(players, team_restriction=[0,1])
    
    assert(len(players) == 8)

    for i, k in enumerate(range(4)):
        your_team_total += players[k]

    for i, k in enumerate(range(4, 8)):
        enemy_team_total += players[k]

    if max(players[0:4]) > your_elo + high_elo_difference:
        high_elo_presence_your_team += 1

    if max(players[4:8]) > your_elo + high_elo_difference:
        high_elo_presence_enemy_team += 1

    if abs(enemy_team_total - your_team_total) < acceptable_difference:
        fair_matches += 1
    else:
        if enemy_team_total > your_team_total:
            losses += 1
        else:
            wins += 1

    total_elo_matches += (enemy_team_total + your_team_total) / 8

print("friend suffering:")
print(f"average match elo: {round(total_elo_matches / simulations_to_run)}")
print(f"amount worse than match average: {round(total_elo_matches / simulations_to_run - your_friends_elo)}")
print(f"\npredicted results:")
print(f"balanced teams: {fair_matches}")
print(f"wins: {wins}")
print(f"losses: {losses}")

if (enable_simple_sbmm):
    print(f"players rejected from matchmaking for too high elo: {rejected_players}")
else:
    print(f"high elo presence, your team: {high_elo_presence_your_team}")
    print(f"high elo presence, enemy team: {high_elo_presence_enemy_team}")
