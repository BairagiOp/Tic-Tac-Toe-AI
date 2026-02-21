# Tic-Tac-Toe-AI

A Tic Tac Toe game implemented with two AI approaches:
	•	Minimax (perfect-play, deterministic)
	•	Q-Learning (reinforcement learning)

The project allows a human to play against the AI and demonstrates the difference between search-based AI and learning-based AI on a simple game.
---

## Features
	•	Terminal-based Tic Tac Toe game
	•	Human vs AI gameplay
	•	Minimax agent (plays perfectly, never loses)
	•	Q-Learning agent (learns by self-play)
	•	Simple, modular codebase
	•	No heavy libraries required

  ---

  ## Project Structure
  ```
Tic-Tac-Toe-AI/
├── env.py          # Game environment and rules
├── agent.py        # Q-Learning agent
├── train.py        # Training loop for Q-Learning
├── minimax.py      # Minimax agent (perfect play)
├── play.py         # Human vs AI gameplay
├── evaluate.py     # Evaluation utilities
├── .gitignore
└── README.md
```
## How It Works
1. Environment (env.py)
	•	Manages the board state
	•	Validates moves
	•	Detects wins, draws, and terminal states

2. Minimax Agent (minimax.py)
	•	Explores all possible future moves
	•	Assumes optimal opponent play
	•	Guarantees win or draw
	•	No training required

3. Q-Learning Agent (agent.py, train.py)
	•	Learns state–action values using rewards
	•	Improves by playing many games
	•	Performance depends on training quality
---

Example Gameplay
```
You are X
Agent is O

X | O | X
---------
O | X | .
---------
. | . | O
```
