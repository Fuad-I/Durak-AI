from Durak_18_vs_18 import Durak
from MCTS_for_Durak_18_vs_18 import MCTS
import random
from tqdm import tqdm
import time

ARGS = {
    'C': 1.41,
    'num_searches': 2
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
            new_state = state.copy()
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


if __name__ == "__main__":
    n_games = int(input('Number of games: '))
    simulate_ai_vs_random(n_games, ARGS)

