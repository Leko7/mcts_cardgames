# Node.py
class Node(object):
    def __init__(self, state, team = None, inc_action = None):
        self.state = state # integer
        self.total_reward = 0
        self.n_visits = 0
        self.children = [] # list of integers
        self.actions_tried = []
        self.team = team
        self.inc_action = inc_action