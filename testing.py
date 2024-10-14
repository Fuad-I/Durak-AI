import copy

from Durak_18_vs_18 import Durak
from MCTS_for_Durak_18_vs_18 import MCTS
import random
from tqdm import tqdm
import time

ARGS = {
    'C': 1.41,
    'num_searches': 10
}

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
                    print()
                    print('AI Wins')
                else:
                    results['Random Wins'] += 1
                    print()
                    print('Random Wins')
                break

            # Switch players
            player = state['current_player']
    print(results)

def simulate_ai_vs_ai(num_games, n_searches1, n_searches2):
    durak = Durak()
    args1 = {
        'C': 1.41,
        'num_searches': n_searches1
    }
    args2 = {
        'C': 1.41,
        'num_searches': n_searches2
    }
    mcts10 = MCTS(durak, args1)
    mcts100 = MCTS(durak, args2)

    results = {'AI10 Wins': 0, 'AI100 Wins': 0}

    for _ in tqdm(range(num_games), desc="Playing Games"):
        state = durak.get_initial_state()
        player = state['current_player']

        while True:
            new_state = copy.deepcopy(state)
            if player == 0:
                # AI player
                action, mcts_probs = mcts10.search(new_state)
            else:
                action, mcts_probs = mcts100.search(new_state)

            # Apply the move to the state
            state = durak.get_next_state(state, action)

            # Check if the game has ended
            value, is_terminal = durak.get_value_and_terminated(state)
            if is_terminal:
                if player == 0:
                    results['AI1 Wins'] += 1
                    print()
                    print('AI1 Wins')
                else:
                    results['AI2 Wins'] += 1
                    print()
                    print('AI2 Wins')
                break

            # Switch players
            player = state['current_player']
    print(results)

if __name__ == "__main__":
    n_games = int(input('Number of games: '))
    n_searches1 = int(input('Number of searches AI1: '))
    n_searches2 = int(input('Number of searches AI2: '))
    #simulate_ai_vs_random(n_games, ARGS10)
    simulate_ai_vs_ai(n_games, n_searches1, n_searches2)


