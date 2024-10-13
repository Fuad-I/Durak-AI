import numpy as np
import random

suits = [1, 2, 3, 4]
ranks = list(range(6, 15))  # 6 to Ace represented by numbers 6-14


def init_deck():
    deck = [(rank, suit) for suit in suits for rank in ranks]
    random.shuffle(deck)
    return deck


class Durak:
    def __init__(self):
        self.deck = init_deck()
        self.players_hands = [[], []]
        self.trump_card = self.deck[-1]  # Last card in the deck is the trump card
        self.trump_suit = self.trump_card[1]
        self.table = []
        self.deal_cards()

    def deal_cards(self):
        self.players_hands[0], self.players_hands[1] = self.deck[:18], self.deck[18:]

    def set_turn(self):
        if (6, self.trump_suit) in self.players_hands[0]:
            return 0
        return 1

    def get_initial_state(self):
        return {
            'player_hands': self.players_hands,
            'table': [],
            'trump_suit': self.trump_suit,
            'current_player': self.set_turn(),
            'attacker': self.set_turn(),
            'defender': self.get_opponent(self.set_turn())
        }

    def get_valid_moves(self, state):
        valid_moves = []
        player = state['current_player']
        if player == state['attacker']:
            if len(state['table']) == 12:
                return ['end_attack']
            if state['table']:
                valid_moves = [card for card in state['player_hands'][player] if card[0]
                               in [dcard[0] for dcard in state['table']]] + ['end_attack']
            else:
                valid_moves = state['player_hands'][player]
        else:
            if state['table']:
                valid_moves = [card for card in state['player_hands'][player] if
                               self.is_valid_defense(card, state['table'][-1])]
                valid_moves.append("take_cards")

        return valid_moves

    def is_valid_defense(self, defend_card, attack_card):
        if defend_card[1] == attack_card[1] and defend_card[0] > attack_card[0]:
            return True
        if defend_card[1] == self.trump_suit and attack_card[1] != self.trump_suit:
            return True
        return False

    def get_next_state(self, state, action):
        if action == "end_attack":
            state['attacker'], state['defender'] = state['defender'], state['attacker']
            state['current_player'] = self.get_opponent(state['current_player'])
            state['table'] = []
            return state
        elif action == "take_cards":
            # Defender takes all cards from the table
            state['player_hands'][state['current_player']].extend(state['table'])
            state['table'] = []
            state['current_player'] = self.get_opponent(state['current_player'])
            return state
        else:
            # Regular card play
            state['table'].append(action)
            if action not in state['player_hands'][state['current_player']]:
                print(state['player_hands'][state['current_player']], state['current_player'], action)
            state['player_hands'][state['current_player']].remove(action)
            state['current_player'] = self.get_opponent(state['current_player'])

        return state

    def get_value_and_terminated(self, state):
        if not state['player_hands'][0] or not state['player_hands'][1]:
            return 1, True
        return 0, False

    def get_opponent(self, player):
        return (player + 1) % 2

    def change_perspective(self, state):
        state['current_player'] = self.get_opponent(state['current_player'])
        state['attacker'], state['defender'] = state['defender'], state['attacker']
