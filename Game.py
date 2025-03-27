# Game.py
import numpy as np

from Card import BeloteCard24, BeloteCard12
from Utils import one_hot, hash

class BeloteGame(object):
    def __init__(self, players, attack_tricks=None, defense_tricks=None, cards_on_table=None):
        self.players = players
        self.attack_tricks = attack_tricks if attack_tricks else []
        self.defense_tricks = defense_tricks if defense_tricks else []
        self.cards_on_table = cards_on_table if cards_on_table else []
        self.n_cards = 12
        self.n_players = len(self.players)
        self.n_tricks = self.n_cards // self.n_players
        self.n_cards_per_trick = self.n_cards // self.n_tricks
        self.table_color = None
        if cards_on_table:
            self.table_color = cards_on_table[0].color

    def get_next_to_play_idx(self):
        i_start = next(k for k, player in enumerate(self.players) if player.first_to_play)
        player_idx = (i_start + len(self.cards_on_table))%self.n_players
        return player_idx

    def get_state(self):
        hand_0 = one_hot(
            input_list=[c.id for c in self.players[0].hand],
            length = self.n_cards
        )
        hand_1 = one_hot(
            input_list=[c.id for c in self.players[1].hand],
            length = self.n_cards
        )
        a_tricks = one_hot(
            input_list=[c.id for c in self.attack_tricks],
            length = self.n_cards
        )
        d_tricks = one_hot(
            input_list=[c.id for c in self.defense_tricks],
            length = self.n_cards
        )

        first_to_play = np.array([i for i,p in enumerate(self.players) if p.first_to_play == True][0]).reshape(1,)
        
        
        if self.n_players == 2:
            if len(self.cards_on_table) == 0:
                table_0 = np.zeros((self.n_cards), dtype=np.int64)

            elif len(self.cards_on_table) == 1:
                table_0 = one_hot(
                    input_list=[c.id for c in self.cards_on_table],
                    length = self.n_cards
                )           

            state = np.concat((hand_0,hand_1, a_tricks, d_tricks, table_0, first_to_play), dtype=np.int64)

        elif self.n_players ==3:

            hand_2 = one_hot(
                input_list=[c.id for c in self.players[2].hand],
                length = self.n_cards
            )

            if len(self.cards_on_table) == 0:
                table_0 = np.zeros((self.n_cards), dtype=np.int64)
                table_1 = np.zeros((self.n_cards), dtype=np.int64)
            elif len(self.cards_on_table) == 1:
                table_0 = one_hot(
                    input_list=[c.id for c in self.cards_on_table],
                    length = self.n_cards
                )
                table_1 = np.zeros((self.n_cards), dtype=np.int64)
            elif len(self.cards_on_table) == 2:
                table_0 = one_hot(
                    input_list=[c.id for c in self.cards_on_table[:1]],
                    length = self.n_cards
                )
                table_1 = one_hot(
                    input_list=[c.id for c in self.cards_on_table[1:]],
                    length = self.n_cards
                )

            state = np.concat((hand_0, hand_1, hand_2, a_tricks, d_tricks, table_0, table_1, first_to_play), dtype=np.int64)
        
        elif self.n_players==4:

            hand_2 = one_hot(
                input_list=[c.id for c in self.players[2].hand],
                length = self.n_cards
            )
            hand_3 = one_hot(
                input_list=[c.id for c in self.players[3].hand],
                length = self.n_cards
            )
            if len(self.cards_on_table) == 0:
                table_0 = np.zeros((self.n_cards), dtype=np.int64)
                table_1 = np.zeros((self.n_cards), dtype=np.int64)
                table_2 = np.zeros((self.n_cards), dtype=np.int64)
            elif len(self.cards_on_table) ==1:
                table_0 = one_hot(
                    input_list=[c.id for c in self.cards_on_table],
                    length=self.n_cards
                )
                table_1 = np.zeros((self.n_cards), dtype=np.int64)
                table_2 = np.zeros((self.n_cards), dtype=np.int64)
            elif len(self.cards_on_table) ==2:
                table_0 = one_hot(
                    input_list=[c.id for c in self.cards_on_table[:1]],
                    length=self.n_cards
                )
                table_1 = one_hot(
                    input_list=[c.id for c in self.cards_on_table[1:2]],
                    length=self.n_cards
                )
                table_2 = np.zeros((self.n_cards), dtype=np.int64)
            elif len(self.cards_on_table) ==3:
                table_0 = one_hot(
                    input_list=[c.id for c in self.cards_on_table[:1]],
                    length=self.n_cards
                )
                table_1 = one_hot(
                    input_list=[c.id for c in self.cards_on_table[1:2]],
                    length=self.n_cards
                )
                table_2 = one_hot(
                    input_list=[c.id for c in self.cards_on_table[2:]],
                    length=self.n_cards
                )

            state = np.concat((hand_0, hand_1, hand_2, hand_3, a_tricks, d_tricks, table_0, table_1, table_2, first_to_play), dtype=np.int64)
        
        return hash(state)

    def reset_game(self):
        self.attack_tricks = []
        self.defense_tricks = []

    def distribute_cards(self):
        cards_ids = [id for id in range(self.n_cards)]
        np.random.shuffle(cards_ids)
        #cards = [BeloteCard24(id) for id in cards_ids]
        cards = [BeloteCard12(id) for id in cards_ids]
        for i, player in enumerate(self.players):
            player.hand = cards[i*self.n_tricks : i*self.n_tricks + self.n_tricks]
        candidates = [player for player in self.players]
        taker = candidates[0]
        taker.team = 'attack'
        taker.first_to_play = True
        if self.n_players < 4:
            for player in [p for p in self.players if p != taker]:
                player.team = 'defense'
        elif self.n_players ==4:
            candidates[1].team = 'defense'
            candidates[2].team = 'attack'
            candidates[3].team = 'defense'

    def give_trick_to_win_team(self):
        for i, player in enumerate(self.players):
            if player.first_to_play == True:
                k = i
        # print(f"table color : {self.table_color}")
        if 'pique' in [card.color for card in self.cards_on_table]:
            win_card_idx = np.argmax([card.value if card.color == 'pique' else 0 for card in self.cards_on_table])
        else:
            win_card_idx = np.argmax([card.value if card.color == self.table_color else 0 for card in self.cards_on_table])
        win_player = self.players[(k + win_card_idx)%self.n_players]
        win_team = win_player.team
        win_team_tricks_att = f'{win_team}_tricks'

        self.__getattribute__(win_team_tricks_att).extend(self.cards_on_table)

        for player in self.players:
            if player == win_player:
                player.first_to_play = True
            else:
                player.first_to_play = False
        # print(f"player {win_player.id} wins the trick.")
        # trick_reward = sum(card.value for card in self.cards_on_table)
        # if win_team == 'attack':
        #     print(f"reward for attack : {trick_reward}")
        #     print(f"reward for defense : {-trick_reward}")
        # else:
        #     print(f"reward for attack : {-trick_reward}")
        #     print(f"reward for defense : {trick_reward}")
            
    def reset_table(self):
        self.cards_on_table = []
        self.table_color = None


    def step(self, action):
        player = self.players[self.get_next_to_play_idx()]
        card = next((c for c in player.get_legal_moves(self) if c.id == action))
        player.play_card(card, self)

        if len(self.cards_on_table) == self.n_cards_per_trick:
            self.give_trick_to_win_team() # (updates self.reward)
            self.reset_table() # (updates cards on table)
        # if len(self.attack_tricks) + len(self.defense_tricks) == self.n_cards:
            # print("Game Finished.")


    def random_step(self):
        player = self.players[self.get_next_to_play_idx()]
        player.naive_move(self)

        if len(self.cards_on_table) == self.n_cards_per_trick:
            self.give_trick_to_win_team() # (updates self.reward)
            self.reset_table() # (updates cards on table)

        # if len(self.attack_tricks) + len(self.defense_tricks) == self.n_cards:
            # print("Game Finished.")

    def playout(self):
        while len(self.attack_tricks) + len(self.defense_tricks) != self.n_cards:
            self.random_step()

        return {
            "attack reward": sum([c.value for c in self.attack_tricks]),
            "defense reward" : sum([c.value for c in self.defense_tricks])
            }
    
    def heuristic_playout(self):
        while len(self.attack_tricks) + len(self.defense_tricks) != self.n_cards:
            player = self.players[self.get_next_to_play_idx()]
            action = player.heuristic_action(self)
            self.step(action)
        return {
            "attack reward": sum([c.value for c in self.attack_tricks]),
            "defense reward" : sum([c.value for c in self.defense_tricks])
            }