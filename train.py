# train.py

import random
from env import TicTacToeEnv
from agent import QLearningAgent


def train(
    episodes: int = 100_000,
    alpha: float = 0.5,
    gamma: float = 0.9,
    epsilon: float = 1.0,
    epsilon_decay: float = 0.99995,
    epsilon_min: float = 0.05,
):
    env = TicTacToeEnv()
    agent = QLearningAgent(alpha=alpha, gamma=gamma, epsilon=epsilon)

    stats = {"win": 0, "loss": 0, "draw": 0}

    for episode in range(episodes):
        state = env.reset()
        done = False

        # Agent is always X
        while not done:
            # ---------- AGENT MOVE (X) ----------
            available_actions = env.available_actions()
            action = agent.choose_action(state, available_actions)

            next_state, reward, done, _ = env.step(action, player=1)
            next_available_actions = env.available_actions() if not done else []

            agent.update(
                state,
                action,
                reward,
                next_state,
                next_available_actions
            )

            state = next_state

            if done:
                break

            # ---------- OPPONENT MOVE (O, random) ----------
            opp_action = random.choice(env.available_actions())
            state, _, done, _ = env.step(opp_action, player=-1)

        # ---------- Stats ----------
        if env.winner == 1:
            stats["win"] += 1
        elif env.winner == -1:
            stats["loss"] += 1
        else:
            stats["draw"] += 1

        # ---------- Epsilon decay ----------
        agent.epsilon = max(epsilon_min, agent.epsilon * epsilon_decay)

        # Optional progress log
        if (episode + 1) % 10_000 == 0:
            print(
                f"Episode {episode+1}/{episodes} | "
                f"W:{stats['win']} L:{stats['loss']} D:{stats['draw']} | "
                f"ε={agent.epsilon:.3f}"
            )

    print("\nTraining finished")
    print("Q-table size:", len(agent.Q))

    return agent, stats


if __name__ == "__main__":
    train()