import numpy as np
from pprint import pprint
from copy import deepcopy
import random

## initialize a random number generator off a normal distribution
## standard deviation 1/3rd, average 50, 10k records
rng = np.random.default_rng()
generated_players = 50 + 50 * rng.normal(0, 1/3, 10000)

sum = 0
lowest = 0
highest = 0

for i, number in enumerate(generated_players):
    # normal distribution can extend past our boundaries, cap them.
    # this does not favor high or low end
    if (number > 99):
        generated_players[i] = 99
    if (number < 1):
        generated_players[i] = 1

    # track highest and lowest
    if number > highest:
        highest = generated_players[i]
    if number < lowest:
        lowest = generated_players[i]

    # add up our values to get the average so we can validate that it worked
    sum += number

# these are here to validate the 
print(f"average percentile: {sum / len(generated_players)}")
print(f"highest percentile: {highest}")
print(f"lowest percentile: {lowest}\n")

# percentiles in 10s. each value represents a percentile bracket e.g. 1 - 9%, 10 - 19%
outputs = [0,0,0,0,0,0,0,0,0,0]

# go through the entire set and add them to their brackets
for i, number in enumerate(generated_players):
    outputs[int(number) // 10] += 1

for i, number in enumerate(outputs):
    print(f"{i + 1}0th percentile bracket: {number}")

# make a copy of our results so we can remove players as they're matched
player_pool = list(generated_players)

your_percentile = 50
your_friends_percentile = 5
acceptable_difference = 20

print("\nexample match:")

# no SBMM section
# pick six random players to match with
players = []
for i, k in enumerate(range(6)):
    # select a player, add it to the selection, remove it from the pool
    selected_player = random.randint(0, len(player_pool) - 1)
    players.append(player_pool[selected_player])
    player_pool.pop(selected_player)

your_team_total = 0
enemy_team_total = 0
print("\nmatchmaking results:\n")
print("your team:")
your_team_total += your_percentile
your_team_total += your_friends_percentile

print(f"you: {your_percentile}")
print(f"your friend: {your_friends_percentile}")
for i, k in enumerate(range(2)):
    print(f"teammate {i + 1}: {round(players[i], 2)}")
    your_team_total += players[i]

print(f"your team total: {round(your_team_total, 2)}")
print(f"your team average: {round(your_team_total / 4, 2)}")

print("\nenemy team:")
for i, k in enumerate(range(2, 6)):
    print(f"opponent: {k + 1}: {round(players[k], 2)}")
    enemy_team_total += players[k]

print(f"enemy team total: {round(enemy_team_total, 2)}")
print(f"enemy team average: {round(enemy_team_total / 4, 2)}\n")

if (abs(enemy_team_total - your_team_total) < acceptable_difference):
    print("match was balanced")
else:
    if (enemy_team_total > your_team_total):
        print(f"match expectation: you lose")
    else:
        print(f"match expectation: you win")
    print(f"match was unbalanced by {round(abs(enemy_team_total - your_team_total), 2)}")




## reset and run the simulation 50 times

wins = 0
fair_matches = 0
losses = 0
simulations_to_run = 50

print(f"\nRunning {simulations_to_run} simluated matches:\n")


for i in range(simulations_to_run):
    player_pool = list(generated_players)
    players = []
    match_count_to_test = 50
    for i, k in enumerate(range(6)):
        # select a player, add it to the selection, remove it from the pool
        selected_player = random.randint(0, len(player_pool) - 1)
        players.append(player_pool[selected_player])
        player_pool.pop(selected_player)

    your_team_total = 0
    enemy_team_total = 0
    your_team_total += your_percentile
    your_team_total += your_friends_percentile
    for i, k in enumerate(range(2)):
        your_team_total += players[i]

    for i, k in enumerate(range(2, 6)):
        enemy_team_total += players[k]

    if abs(enemy_team_total - your_team_total) < acceptable_difference:
        fair_matches += 1
    else:
        if enemy_team_total > your_team_total:
            losses += 1
        else:
            wins += 1

print(f"predicted results:")
print(f"fair matches: {fair_matches}")
print(f"wins: {wins}")
print(f"losses: {losses}")