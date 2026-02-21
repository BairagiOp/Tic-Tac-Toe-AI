# play.py

from env import TicTacToeEnv
from minimax import MinimaxAgent


def human_vs_agent():
    env = TicTacToeEnv()
    env.reset()

    # Explicit roles
    HUMAN = -1   # X
    AGENT = 1    # O

    agent = MinimaxAgent(agent_player=AGENT)

    print("You are X")
    print("Agent is O")
    print("Board positions:")
    print("0 1 2")
    print("3 4 5")
    print("6 7 8\n")

    env.render()

    player = HUMAN  # YOU start

    while not env.done:
        available_actions = env.available_actions()

        if player == HUMAN:
            # ---------- HUMAN MOVE ----------
            while True:
                try:
                    action = int(input("Your move (0-8): "))
                    if action in available_actions:
                        break
                    print("Invalid move. Try again.")
                except ValueError:
                    print("Please enter a number between 0 and 8.")
        else:
            # ---------- AGENT MOVE ----------
            action = agent.select_move(env)
            print(f"Agent plays: {action}")

        env.step(action, player)
        env.render()
        player = -player

    # ---------- GAME OVER ----------
    if env.winner == HUMAN:
        print("You win 🎉 (this should not happen 😄)")
    elif env.winner == AGENT:
        print("Agent wins 😈")
    else:
        print("It's a draw 🤝")


if __name__ == "__main__":
    human_vs_agent()