# agent.py

import random
from collections import defaultdict
from env import TicTacToeEnv


class QLearningAgent:
    """
    Tabular Q-learning agent for Tic-Tac-Toe.
    """

    def __init__(
        self,
        alpha: float = 0.5,     # learning rate
        gamma: float = 0.9,     # discount factor
        epsilon: float = 0.1    # exploration rate
    ):
        # Q[state][action] = value
        self.Q = defaultdict(lambda: defaultdict(float))

        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon

    # ── Action selection ──────────────────────────────────────────────────

    def choose_action(self, state, available_actions):
        """
        ε-greedy action selection.
        """
        # Explore
        if random.random() < self.epsilon:
            return random.choice(available_actions)

        # Exploit (pick best known action)
        q_values = self.Q[state]
        max_q = float("-inf")
        best_actions = []

        for action in available_actions:
            value = q_values[action]
            if value > max_q:
                max_q = value
                best_actions = [action]
            elif value == max_q:
                best_actions.append(action)

        return random.choice(best_actions)

    # ── Learning ──────────────────────────────────────────────────────────

    def update(self, state, action, reward, next_state, next_available_actions):
        """
        Apply the Q-learning update rule.
        """

        current_q = self.Q[state][action]

        # If no next actions, it's a terminal state
        if not next_available_actions:
            target = reward
        else:
            next_max_q = max(self.Q[next_state][a] for a in next_available_actions)
            target = reward + self.gamma * next_max_q

        # Bellman update
        self.Q[state][action] = current_q + self.alpha * (target - current_q)