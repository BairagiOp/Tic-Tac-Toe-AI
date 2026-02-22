# Tic-Tac-Toe-AI
## 🚀 Live Demo
👉 [Play it here](https://tic-tac-toe-ai-jgfo.onrender.com)
> ⏳ First load may take ~30 seconds to wake up (free tier)

A Tic Tac Toe game implemented with two AI approaches: <br>
	•	Minimax (perfect-play, deterministic)<br>
	•	Q-Learning (reinforcement learning)<br>


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
1. Environment (env.py)<br>
	•	Manages the board state<br>
	•	Validates moves<br>
	•	Detects wins, draws, and terminal states<br>

2. Minimax Agent (minimax.py)<br>
	•	Explores all possible future moves<br>
	•	Assumes optimal opponent play<br>
	•	Guarantees win or draw<br>
	•	No training required<br>

3. Q-Learning Agent (agent.py, train.py)<br>
	•	Learns state–action values using rewards<br>
	•	Improves by playing many games<br>
	•	Performance depends on training quality<br>
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
