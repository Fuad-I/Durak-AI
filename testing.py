import copy
from Durak_18_vs_18 import Durak
from MCTS_for_Durak_18_vs_18 import MCTS
import random
from tqdm import tqdm
import time

ARGS = {
    'C': 1.41,
    'num_searches': 1000
}

HEARTS = "♥"
DIAMONDS = "♦"
CLUBS = "♣"
SPADES = "♠"

SUITS = [HEARTS, DIAMONDS, CLUBS, SPADES]


def repr_card(card):
    return '{}{}'.format(card[0], SUITS[card[1]])


def simulate_ai_vs_random(num_games, args):
    durak = Durak()
    mcts = MCTS(durak, args)

    results = {'AI Wins': 0, 'Random Wins': 0}

    for _ in tqdm(range(num_games), desc="Playing Games"):
        state = durak.get_initial_state()
        player = state['current_player']

        while True:
            # Get valid moves
            valid_moves = durak.get_valid_moves(state)
            new_state = copy.deepcopy(state)
            if player == 0:
                # AI player
                action, mcts_probs = mcts.search(new_state)
            else:
                action = random.choice(valid_moves)

            # Apply the move to the state
            state = durak.get_next_state(state, action)

            # Check if the game has ended
            value, is_terminal = durak.get_value_and_terminated(state)
            if is_terminal:
                if player == 0:
                    results['AI Wins'] += 1
                    print('AI Wins')
                else:
                    results['Random Wins'] += 1
                    print('Random Wins')
                break

            # Switch players
            player = state['current_player']

    print(results)


def play_vs_ai(args):
    durak = Durak()
    mcts = MCTS(durak, args)

    state = durak.get_initial_state()
    player = state['current_player']

    print(state['trump_suit'])
    print('Player cards ', sorted(state['player_hands'][1]))
    # print('AI cards ', state['player_hands'][0])

    while True:
        # Get valid moves
        valid_moves = durak.get_valid_moves(state)
        new_state = copy.deepcopy(state)
        if player == 0:
            # AI player
            print('Plays AI')
            action, mcts_probs = mcts.search(new_state)
            print('AI played ', action)
        else:
            print('Your turn', '\n')
            input_action = input()
            if input_action == 'end':
                action = 'end_attack'
            elif input_action == 'take':
                action = 'take_cards'
            else:
                action = tuple(int(x) for x in input_action.split())
            print('You played ', action)

        # Apply the move to the state
        state = durak.get_next_state(state, action)

        print('Table ', state['table'])

        print('Player cards ', sorted(state['player_hands'][1]))

        # Check if the game has ended
        value, is_terminal = durak.get_value_and_terminated(state)
        if is_terminal:
            if player == 0:
                print('AI Wins')
            else:
                print('You Win')
            break

        # Switch players
        player = state['current_player']


if __name__ == "__main__":
    # n_games = int(input('Number of games: '))
    # simulate_ai_vs_random(n_games, ARGS)
    play_vs_ai(ARGS)
