import numpy as np
import math
import random

class Node:
    def __init__(self, game, args, state, parent=None, action_taken=None):
        self.game = game
        self.args = args
        self.state = state
        self.parent = parent
        self.action_taken = action_taken

        self.children = []
        self.expandable_moves = game.get_valid_moves(state)

        self.visit_count = 0
        self.value_sum = 0

    def is_fully_expanded(self):
        return not self.expandable_moves and len(self.children) > 0

    def select(self):
        best_child = None
        best_ucb = -np.inf

        for child in self.children:
            ucb = self.get_ucb(child)
            if ucb > best_ucb:
                best_child = child
                best_ucb = ucb

        return best_child

    def get_ucb(self, child):
        q_value = 1 - ((child.value_sum / child.visit_count) + 1) / 2
        return q_value + self.args['C'] * math.sqrt(math.log(self.visit_count) / child.visit_count)

    def expand(self):
        # action = self.expandable_moves[random.randint(0, len(self.expandable_moves) - 1)]
        action = random.choice(self.expandable_moves)
        self.expandable_moves.remove(action)

        child_state = self.state.copy()
        child_state = self.game.get_next_state(child_state, action)

        child = Node(self.game, self.args, child_state, self, action)
        self.children.append(child)
        return child

    def simulate(self):
        value, is_terminal = self.game.get_value_and_terminated(self.state)

        if is_terminal:
            return -value

        rollout_state = self.state.copy()
        rollout_player = self.state['current_player']
        while True:
            valid_moves = self.game.get_valid_moves(rollout_state)
            action = random.choice(valid_moves)
            rollout_state = self.game.get_next_state(rollout_state, action)
            value, is_terminal = self.game.get_value_and_terminated(rollout_state)
            if is_terminal:
                if rollout_player == rollout_state['current_player']:
                    return - self.game.get_value_and_terminated(rollout_state)[0]
                return self.game.get_value_and_terminated(rollout_state)[0]

    def backpropagate(self, value):
        self.value_sum += value
        self.visit_count += 1

        value = - value
        if self.parent is not None:
            self.parent.backpropagate(value)


class MCTS:
    def __init__(self, game, args):
        self.game = game
        self.args = args

    def search(self, state):
        temp_state = state.copy()
        root = Node(self.game, self.args, state)

        for search in range(self.args['num_searches']):
            node = root

            while node.is_fully_expanded():
                node = node.select()

            value, is_terminal = self.game.get_value_and_terminated(node.state)
            value = - value

            if not is_terminal:
                node = node.expand()
                value = node.simulate()

            node.backpropagate(value)

        action_probs = {}
        for child in root.children:
            action_probs[child.action_taken] = child.visit_count
        total_visits = sum(action_probs.values())
        if total_visits > 0:
            action_probs = {action: count / total_visits for action, count in action_probs.items()}
        best_action = max(action_probs, key=action_probs.get)
        return best_action, action_probs

