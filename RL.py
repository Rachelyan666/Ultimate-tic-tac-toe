import numpy as np
import random
from collections import defaultdict

class UltimateTicTacToeRL:
    def __init__(self, alpha=0.1, gamma=0.9, epsilon=0.1):
        # Learning rate
        self.alpha = alpha
        # Discount factor
        self.gamma = gamma
        # Exploration rate
        self.epsilon = epsilon
        # Q table
        self.q_table = defaultdict(lambda: np.zeros(81))
        # State history for the episode
        self.state_history = []

    def choose_action(self, state, valid_actions):
        """
        Epsilon selection
        """
        if random.uniform(0, 1) < self.epsilon:
            # Exploration: choose a random valid action
            return random.choice(valid_actions)
        else:
            state_key = self.state_to_key(state)
            q_values = self.q_table[state_key]
            valid_q_values = [(action, q_values[action[0] * 9 + action[1]]) for action in valid_actions]
            return max(valid_q_values, key=lambda x: x[1])[0]

    def update_q_table(self, reward):
        """Update Q-table based on the episode's history."""
        for i in reversed(range(len(self.state_history) - 1)):
            state, action = self.state_history[i]
            next_state, _ = self.state_history[i + 1]

            state_key = self.state_to_key(state)
            next_state_key = self.state_to_key(next_state)

            action_index = action[0] * 9 + action[1]
            best_next_action = max(self.q_table[next_state_key])

            # Update Q-value using Bellman equation
            self.q_table[state_key][action_index] += self.alpha * (
                reward + self.gamma * best_next_action - self.q_table[state_key][action_index]
            )

            # Set reward to 0 after the first step (reward is already added)
            reward = 0


    def get_valid_moves(self, game_state, active_box):
        """
        Returns all available moves as tuples within the active box.
        """
        if active_box is not None:
            box_row, box_col = active_box
            valid_moves = [
                (box_row * 3 + i, box_col * 3 + j)
                for i in range(3) for j in range(3)
                if game_state[box_row * 3 + i][box_col * 3 + j] == ' '
            ]
            if valid_moves:
                return valid_moves
        return [(i, j) for i in range(9) for j in range(9) if game_state[i][j] == ' ']
    
    def play(self, big_board, player, state):
       pass
       #unimplemented, not sure if we have time for this