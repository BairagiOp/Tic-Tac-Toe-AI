# minimax.py

import math


class MinimaxAgent:
    def __init__(self, agent_player):
        """
        agent_player: +1 or -1
        """
        self.agent_player = agent_player
        self.name = "MinimaxAgent"

    def select_move(self, env):
        best_score = -math.inf
        best_move = None

        for move in env.available_actions():
            env_copy = env.clone()
            env_copy.step(move, self.agent_player)
            score = self._minimax(env_copy, maximizing=False)

            if score > best_score:
                best_score = score
                best_move = move

        return best_move

    def _minimax(self, env, maximizing):
        if env.done:
            return self._evaluate(env)

        if maximizing:
            best = -math.inf
            for move in env.available_actions():
                env_copy = env.clone()
                env_copy.step(move, self.agent_player)
                best = max(best, self._minimax(env_copy, False))
            return best
        else:
            best = math.inf
            for move in env.available_actions():
                env_copy = env.clone()
                env_copy.step(move, -self.agent_player)
                best = min(best, self._minimax(env_copy, True))
            return best

    def _evaluate(self, env):
        if env.winner == self.agent_player:
            return 1     # agent win
        elif env.winner == -self.agent_player:
            return -1    # agent loss
        else:
            return 0     # draw