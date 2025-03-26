# Main.py
import matplotlib.pyplot as plt

from Player import BelotePlayer
from Game import BeloteGame
from UCT import *
from Card import * # for test/visu

# Next step !! Do heuristic playouts instead of random.
# Also compare vs.random

steps_values = [100, 500, 1000, 1500, 2000]
att_scores = []
def_scores = []
n_samples = 10

for max_steps in steps_values:
    att_score = 0
    def_score = 0

    for _ in range(n_samples):
        players = [BelotePlayer(0), BelotePlayer(1), BelotePlayer(2)]

        game = BeloteGame(players)
        game.reset_game()
        game.distribute_cards()

        while len(game.defense_tricks) + len(game.attack_tricks) < game.n_cards:
            player = game.players[game.get_next_to_play_idx()]
            if player.id == 0:
                action = uct_search(game, max_steps=max_steps)
            else:
                action = player.random_action(game)
            game.step(action)
        att_score += sum([c.value for c in game.attack_tricks])
        def_score += sum([c.value for c in game.defense_tricks])
    
    att_scores.append(att_score/n_samples)
    def_scores.append(def_score/n_samples)

plt.figure()
plt.plot(steps_values, att_scores, label="Heuristic")
plt.plot(steps_values, def_scores, label="Random")
plt.xlabel("Number of steps")
plt.ylabel("Final score")
plt.legend()
plt.show()