# CompareUCTvsRandom.py

import numpy as np

from Player import BelotePlayer
from Game import BeloteGame
from UCT import *

# Next step !! Do heuristic playouts instead of random.
# Also compare them vs.random

max_steps = 100
uct_scores = []
random_scores = []
n_samples = 1 #10_000


for s in range(n_samples):
    if s < 5000:
        uct_pair = [0,2]
    else:
        uct_pair = [1,3]
    
    players = [BelotePlayer(0), BelotePlayer(1), BelotePlayer(2), BelotePlayer(3)]
    game = BeloteGame(players)
    game.reset_game()
    game.distribute_cards()

    while len(game.defense_tricks) + len(game.attack_tricks) < game.n_cards:
        player = game.players[game.get_next_to_play_idx()]
        if player.id in uct_pair:
            if len(player.get_legal_moves(game)) > 1:
                action = uct_search(game, max_steps=max_steps)
            else:
                action = player.random_action(game)
        else:
            action = player.random_action(game)
        game.step(action)
    if s < 5000:
        uct_scores.append(sum([c.value for c in game.attack_tricks]))
        random_scores.append(sum([c.value for c in game.defense_tricks]))
    else:
        uct_scores.append(sum([c.value for c in game.defense_tricks]))
        random_scores.append(sum([c.value for c in game.attack_tricks]))

uct_mean = np.mean(uct_scores)
uct_std = np.std(uct_scores, ddof=1)

random_mean = np.mean(random_scores)
random_std = np.std(random_scores, ddof=1)

print(f"UCT ----> Mean : {uct_mean}, STD : {uct_std}")
print(f"RANDOM ----> Mean : {random_mean}, STD : {random_std}")

# plt.figure()
# plt.plot(steps_values, att_scores, label="Random")
# plt.plot(steps_values, def_scores, label="UCT")
# plt.xlabel("Search tree descent budget")
# plt.ylabel(f"Average score over n={n_samples} samples")
# plt.legend()
# plt.show()