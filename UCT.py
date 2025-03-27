# UCT.py
import numpy as np
from Node import Node
from Game import BeloteGame
import copy

def best_child(node, game, c):
    values = [((child.total_reward)/(child.n_visits)) + c*np.sqrt((2*np.log(node.n_visits))/(child.n_visits)) for child in node.children]
    best_child = node.children[np.argmax(values)]
    game.step(best_child.inc_action)
    return best_child

def expand(node, game):
    player = game.players[game.get_next_to_play_idx()]
    actions = [c.id for c in player.get_legal_moves(game)]
    new_action = next((a for a in actions if a not in node.actions_tried))
    game.step(new_action)
    new_child = Node(game.get_state(), player.team, new_action) # the "team" of the node is the team of the player making the incoming action
    node.children.append(new_child)
    node.actions_tried.append(new_action)
    return new_child

def is_expandable(node, game):
    player = game.players[game.get_next_to_play_idx()]
    actions = [c.id for c in player.get_legal_moves(game)]
    new_actions = [a for a in actions if a not in node.actions_tried]
    if new_actions:
        return True
    else:
        return False
    
def tree_policy(node, game, search_list, cp=1/np.sqrt(2)):
    terminal = False
    while not terminal:
        if is_expandable(node, game):
            node = expand(node, game)
            search_list.append(node)
            node.n_visits += 1
            return node
        else:
            node = best_child(node, game, cp)
            search_list.append(node)
            node.n_visits += 1
        if len(game.attack_tricks) + len(game.defense_tricks) == game.n_cards:
            terminal = True
    return node

def default_policy(game):
    return game.playout() # should work even if s is terminal

def backup(playout, search_list):
    for node in search_list:
        if node.team == "attack":
            node.total_reward += playout["attack reward"]
        elif node.team == "defense":
            node.total_reward += playout["defense reward"]

def uct_search(game, max_steps = 5):
    root = Node(game.get_state())
    # maybe I need to reset the game (but why are the original players modified ?)
    for i in range(max_steps):
        # print(f"Iteration {i} :")
        root.n_visits += 1
        players = copy.deepcopy(game.players)
        attack_tricks = copy.deepcopy(game.attack_tricks)
        defense_tricks = copy.deepcopy(game.defense_tricks)
        cards_on_table = copy.deepcopy(game.cards_on_table)
        simu_game = BeloteGame(
            players=players,
            attack_tricks=attack_tricks,
            defense_tricks=defense_tricks,
            cards_on_table=cards_on_table
        )
        
        search_list = []
        node = tree_policy(root, simu_game, search_list)
        playout = default_policy(simu_game)
        backup(playout, search_list)
    
    # Copy needed to avoid moving the game one step (not very efficient, could be improved)
    players = copy.deepcopy(game.players)
    attack_tricks = copy.deepcopy(game.attack_tricks)
    defense_tricks = copy.deepcopy(game.defense_tricks)
    cards_on_table = copy.deepcopy(game.cards_on_table)
    simu_game = BeloteGame(
        players=players,
        attack_tricks=attack_tricks,
        defense_tricks=defense_tricks,
        cards_on_table=cards_on_table
    )
    return (best_child(root, simu_game, c=0)).inc_action