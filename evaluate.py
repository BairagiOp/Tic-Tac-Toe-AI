# evaluate.py

import random
from env import TicTacToeEnv
from agent import QLearningAgent


def play_vs_random(agent: QLearningAgent, games: int = 1_000):
    env = TicTacToeEnv()

    results = {"win": 0, "loss": 0, "draw": 0}

    for _ in range(games):
        state = env.reset()
        done = False
        player = 1  # agent is X

        while not done:
            available_actions = env.available_actions()

            if player == 1:
                # Agent move (pure exploitation — no exploration)
                action = max(
                    available_actions,
                    key=lambda a: agent.Q[state][a]
                )
            else:
                # Random opponent
                action = random.choice(available_actions)

            state, reward, done, _ = env.step(action, player)
            player = -player

        # Record result (from agent perspective)
        if env.winner == 1:
            results["win"] += 1
        elif env.winner == -1:
            results["loss"] += 1
        else:
            results["draw"] += 1

    return results


if __name__ == "__main__":
    # Train first
    from train import train

    agent, _ = train(episodes=50_000)

    # Evaluate
    results = play_vs_random(agent, games=1_000)

    total = sum(results.values())
    print("Evaluation vs Random Opponent")
    print(f"Wins:  {results['win']} ({results['win']/total:.2%})")
    print(f"Losses:{results['loss']} ({results['loss']/total:.2%})")
    print(f"Draws: {results['draw']} ({results['draw']/total:.2%})")