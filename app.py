# app.py — Streamlit Tic-Tac-Toe AI
# Run with: streamlit run app.py

import random
import math
import streamlit as st
from collections import defaultdict

# ──────────────────────────────────────────────────────────────────────────────
# PAGE CONFIG
# ──────────────────────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="Tic-Tac-Toe AI",
    page_icon="🎮",
    layout="centered",
)

# ──────────────────────────────────────────────────────────────────────────────
# CUSTOM CSS
# ──────────────────────────────────────────────────────────────────────────────

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Space+Mono:wght@400;700&display=swap');

/* Base */
html, body, [class*="css"] {
    background-color: #0d0d0d;
    color: #f0ece0;
    font-family: 'Space Mono', monospace;
}

/* Title */
.title-block {
    text-align: center;
    margin-bottom: 2rem;
}
.title-block h1 {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 4rem;
    letter-spacing: 0.15em;
    color: #f0ece0;
    margin: 0;
    line-height: 1;
}
.title-block .subtitle {
    font-family: 'Space Mono', monospace;
    font-size: 0.75rem;
    letter-spacing: 0.3em;
    color: #888;
    text-transform: uppercase;
    margin-top: 0.5rem;
}

/* Status banner */
.status-banner {
    text-align: center;
    padding: 0.75rem 1.5rem;
    margin-bottom: 1.5rem;
    border: 1px solid #333;
    font-family: 'Space Mono', monospace;
    font-size: 0.85rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    background: #161616;
    color: #e0d8c0;
}
.status-banner.win  { border-color: #c8ff00; color: #c8ff00; background: #111a00; }
.status-banner.loss { border-color: #ff3c3c; color: #ff3c3c; background: #1a0000; }
.status-banner.draw { border-color: #888;    color: #ccc;    background: #161616; }

/* Board */
.board-wrap {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 6px;
    max-width: 340px;
    margin: 0 auto 1.5rem;
}

/* Cells */
.cell {
    aspect-ratio: 1;
    display: flex;
    align-items: center;
    justify-content: center;
    font-family: 'Bebas Neue', sans-serif;
    font-size: 3.5rem;
    cursor: pointer;
    background: #1a1a1a;
    border: 1px solid #2e2e2e;
    transition: background 0.1s, border-color 0.1s;
    user-select: none;
    color: #f0ece0;
}
.cell:hover { background: #242424; border-color: #555; }
.cell.x-cell { color: #c8ff00; }
.cell.o-cell { color: #ff6a3d; }
.cell.winning { background: #1e2800; border-color: #c8ff00; }
.cell.empty { color: #2e2e2e; }

/* Score strip */
.score-strip {
    display: flex;
    justify-content: center;
    gap: 2rem;
    margin-bottom: 1.5rem;
}
.score-item {
    text-align: center;
}
.score-item .label {
    font-size: 0.6rem;
    letter-spacing: 0.2em;
    color: #666;
    text-transform: uppercase;
    margin-bottom: 0.2rem;
}
.score-item .value {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 2.5rem;
    line-height: 1;
}
.score-item.wins  .value { color: #c8ff00; }
.score-item.losses .value { color: #ff6a3d; }
.score-item.draws .value  { color: #888; }

/* Divider */
.divider { border: none; border-top: 1px solid #2a2a2a; margin: 1.5rem 0; }

/* Sidebar tweaks */
section[data-testid="stSidebar"] {
    background: #111;
    border-right: 1px solid #2a2a2a;
}

/* Streamlit button overrides */
div.stButton > button {
    font-family: 'Space Mono', monospace;
    font-size: 0.75rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    background: #1a1a1a;
    color: #f0ece0;
    border: 1px solid #444;
    border-radius: 0;
    padding: 0.5rem 1.2rem;
    width: 100%;
    transition: background 0.15s, border-color 0.15s;
}
div.stButton > button:hover {
    background: #2a2a2a;
    border-color: #c8ff00;
    color: #c8ff00;
}
div.stButton > button:focus {
    box-shadow: none;
}

/* Radio & select */
div[data-testid="stRadio"] label, div[data-testid="stSelectbox"] label {
    font-size: 0.7rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #888 !important;
}
div[data-testid="stMarkdownContainer"] p {
    font-size: 0.85rem;
    line-height: 1.6;
}

/* Move log */
.log-entry {
    font-size: 0.7rem;
    color: #666;
    padding: 2px 0;
    border-bottom: 1px solid #1e1e1e;
    letter-spacing: 0.05em;
}
.log-entry span { color: #999; }
</style>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────────────────────
# ENVIRONMENT
# ──────────────────────────────────────────────────────────────────────────────

WINS = [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]

def check_win(board, player):
    return any(board[a]==board[b]==board[c]==player for a,b,c in WINS)

def winning_combo(board, player):
    for combo in WINS:
        a,b,c = combo
        if board[a]==board[b]==board[c]==player:
            return combo
    return None

def check_draw(board):
    return all(v != 0 for v in board)

def available_actions(board):
    return [i for i,v in enumerate(board) if v == 0]

# ──────────────────────────────────────────────────────────────────────────────
# MINIMAX (with alpha-beta pruning)
# ──────────────────────────────────────────────────────────────────────────────

def minimax(board, depth, is_max, agent_player, alpha=-math.inf, beta=math.inf):
    opponent = -agent_player
    if check_win(board, agent_player):
        return 10 - depth
    if check_win(board, opponent):
        return depth - 10
    moves = available_actions(board)
    if not moves:
        return 0

    if is_max:
        best = -math.inf
        for m in moves:
            board[m] = agent_player
            best = max(best, minimax(board, depth+1, False, agent_player, alpha, beta))
            board[m] = 0
            alpha = max(alpha, best)
            if beta <= alpha:
                break
        return best
    else:
        best = math.inf
        for m in moves:
            board[m] = opponent
            best = min(best, minimax(board, depth+1, True, agent_player, alpha, beta))
            board[m] = 0
            beta = min(beta, best)
            if beta <= alpha:
                break
        return best

def minimax_move(board, agent_player):
    best_score = -math.inf
    best_move = None
    for m in available_actions(board):
        board[m] = agent_player
        score = minimax(board, 0, False, agent_player)
        board[m] = 0
        if score > best_score:
            best_score = score
            best_move = m
    return best_move

# ──────────────────────────────────────────────────────────────────────────────
# Q-LEARNING AGENT (train in session)
# ──────────────────────────────────────────────────────────────────────────────

class QLearningAgent:
    def __init__(self, alpha=0.5, gamma=0.9, epsilon=0.0):
        self.Q = defaultdict(lambda: defaultdict(float))
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon

    def choose_action(self, state, actions):
        if random.random() < self.epsilon:
            return random.choice(actions)
        q = self.Q[state]
        best = max(actions, key=lambda a: q[a])
        return best

    def update(self, state, action, reward, next_state, next_actions):
        cur = self.Q[state][action]
        if not next_actions:
            target = reward
        else:
            target = reward + self.gamma * max(self.Q[next_state][a] for a in next_actions)
        self.Q[state][action] = cur + self.alpha * (target - cur)

def train_q_agent(episodes=30_000):
    agent = QLearningAgent(alpha=0.5, gamma=0.9, epsilon=1.0)
    eps_decay = 0.9999
    eps_min = 0.05
    for _ in range(episodes):
        board = [0]*9
        done = False
        state = tuple(board)
        while not done:
            acts = available_actions(board)
            action = agent.choose_action(state, acts)
            board[action] = 1
            if check_win(board, 1):
                agent.update(state, action, 1, tuple(board), [])
                done = True; break
            if check_draw(board):
                agent.update(state, action, 0.5, tuple(board), [])
                done = True; break
            next_state = tuple(board)
            opp_acts = available_actions(board)
            opp = random.choice(opp_acts)
            board[opp] = -1
            if check_win(board, -1):
                agent.update(state, action, -1, tuple(board), [])
                done = True; break
            if check_draw(board):
                agent.update(state, action, 0.5, tuple(board), [])
                done = True; break
            next_state2 = tuple(board)
            agent.update(state, action, 0, next_state2, available_actions(board))
            state = next_state2
        agent.epsilon = max(eps_min, agent.epsilon * eps_decay)
    agent.epsilon = 0.0
    return agent

# ──────────────────────────────────────────────────────────────────────────────
# SESSION STATE INIT
# ──────────────────────────────────────────────────────────────────────────────

def init_state():
    if "board" not in st.session_state:
        st.session_state.board = [0]*9
        st.session_state.done = False
        st.session_state.winner = None
        st.session_state.current_player = 1   # 1=human X, -1=AI O
        st.session_state.score = {"W":0,"L":0,"D":0}
        st.session_state.move_log = []
        st.session_state.q_agent = None
        st.session_state.q_trained = False
        st.session_state.ai_mode = "Minimax"
        st.session_state.human_goes_first = True

init_state()

# ──────────────────────────────────────────────────────────────────────────────
# HELPERS
# ──────────────────────────────────────────────────────────────────────────────

HUMAN = 1
AI = -1

def new_game():
    st.session_state.board = [0]*9
    st.session_state.done = False
    st.session_state.winner = None
    st.session_state.move_log = []
    # Alternate first move or keep setting
    if st.session_state.human_goes_first:
        st.session_state.current_player = HUMAN
    else:
        st.session_state.current_player = AI

def log(msg):
    st.session_state.move_log.insert(0, msg)
    if len(st.session_state.move_log) > 20:
        st.session_state.move_log.pop()

def ai_move():
    board = st.session_state.board
    mode = st.session_state.ai_mode
    if mode == "Minimax":
        action = minimax_move(board[:], AI)
    elif mode == "Q-Learning":
        if st.session_state.q_agent is None:
            action = random.choice(available_actions(board))
        else:
            state = tuple(board)
            acts = available_actions(board)
            action = st.session_state.q_agent.choose_action(state, acts)
    else:  # Random
        action = random.choice(available_actions(board))

    board[action] = AI
    log(f"AI → cell {action}")

    if check_win(board, AI):
        st.session_state.done = True
        st.session_state.winner = AI
        st.session_state.score["L"] += 1
    elif check_draw(board):
        st.session_state.done = True
        st.session_state.winner = 0
        st.session_state.score["D"] += 1
    else:
        st.session_state.current_player = HUMAN

def human_move(idx):
    board = st.session_state.board
    if board[idx] != 0 or st.session_state.done:
        return
    board[idx] = HUMAN
    log(f"You → cell {idx}")
    if check_win(board, HUMAN):
        st.session_state.done = True
        st.session_state.winner = HUMAN
        st.session_state.score["W"] += 1
    elif check_draw(board):
        st.session_state.done = True
        st.session_state.winner = 0
        st.session_state.score["D"] += 1
    else:
        st.session_state.current_player = AI
        ai_move()

# If AI goes first and it's AI's turn at start of render
if not st.session_state.done and st.session_state.current_player == AI:
    ai_move()

# ──────────────────────────────────────────────────────────────────────────────
# SIDEBAR
# ──────────────────────────────────────────────────────────────────────────────

with st.sidebar:
    st.markdown("### ⚙️ Settings")

    mode = st.radio(
        "AI Opponent",
        ["Minimax", "Q-Learning", "Random"],
        index=["Minimax","Q-Learning","Random"].index(st.session_state.ai_mode),
    )
    if mode != st.session_state.ai_mode:
        st.session_state.ai_mode = mode
        new_game()

    if mode == "Q-Learning":
        if not st.session_state.q_trained:
            if st.button("🧠 Train Q-Agent (30k episodes)"):
                with st.spinner("Training... ~10 sec"):
                    st.session_state.q_agent = train_q_agent(30_000)
                    st.session_state.q_trained = True
                st.success("Q-Agent trained!")
        else:
            st.success("Q-Agent ready ✓")

    goes_first = st.radio("You play as", ["X (First)", "O (Second)"])
    human_first = goes_first.startswith("X")
    if human_first != st.session_state.human_goes_first:
        st.session_state.human_goes_first = human_first
        new_game()

    st.markdown("---")
    st.markdown("### 📖 How to Play")
    st.markdown("""
- Click any empty cell to make your move
- **X** always goes first
- **Minimax** plays perfectly — it never loses
- **Q-Learning** learns from self-play (train first!)
- **Random** makes random moves
    """)
    st.markdown("---")
    st.markdown("### 📊 About")
    st.caption("Built with Streamlit · Minimax + Q-Learning AI")

# ──────────────────────────────────────────────────────────────────────────────
# MAIN UI
# ──────────────────────────────────────────────────────────────────────────────

st.markdown("""
<div class="title-block">
  <h1>Tic‑Tac‑Toe AI</h1>
  <div class="subtitle">Minimax · Q-Learning · Reinforcement Learning</div>
</div>
""", unsafe_allow_html=True)

# Score strip
sc = st.session_state.score
st.markdown(f"""
<div class="score-strip">
  <div class="score-item wins">
    <div class="label">Wins</div>
    <div class="value">{sc["W"]}</div>
  </div>
  <div class="score-item draws">
    <div class="label">Draws</div>
    <div class="value">{sc["D"]}</div>
  </div>
  <div class="score-item losses">
    <div class="label">Losses</div>
    <div class="value">{sc["L"]}</div>
  </div>
</div>
""", unsafe_allow_html=True)

# Status banner
board = st.session_state.board
if st.session_state.done:
    w = st.session_state.winner
    if w == HUMAN:
        st.markdown('<div class="status-banner win">🎉 You win!</div>', unsafe_allow_html=True)
    elif w == AI:
        st.markdown('<div class="status-banner loss">😈 AI wins</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="status-banner draw">🤝 Draw</div>', unsafe_allow_html=True)
else:
    if st.session_state.current_player == HUMAN:
        st.markdown('<div class="status-banner">Your turn — pick a cell</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="status-banner">AI is thinking…</div>', unsafe_allow_html=True)

# Winning cells
win_cells = set()
w = st.session_state.winner
if w in (HUMAN, AI):
    combo = winning_combo(board, w)
    if combo:
        win_cells = set(combo)

# Board grid — 3 columns of 3 buttons each
SYMBOLS = {1: "X", -1: "O", 0: "·"}

for row in range(3):
    cols = st.columns(3)
    for col in range(3):
        idx = row * 3 + col
        val = board[idx]
        sym = SYMBOLS[val]
        with cols[col]:
            label = sym if val != 0 else " "
            disabled = (val != 0) or st.session_state.done or st.session_state.current_player == AI
            if st.button(
                label,
                key=f"cell_{idx}",
                disabled=disabled,
                use_container_width=True,
            ):
                human_move(idx)
                st.rerun()

# New game button
st.markdown("<br>", unsafe_allow_html=True)
c1, c2, c3 = st.columns([1, 2, 1])
with c2:
    if st.button("↺  New Game", use_container_width=True):
        new_game()
        st.rerun()

# Move log
if st.session_state.move_log:
    st.markdown("<hr class='divider'>", unsafe_allow_html=True)
    st.markdown("**Move Log**")
    log_html = ""
    for i, entry in enumerate(st.session_state.move_log[:10]):
        log_html += f'<div class="log-entry"><span>#{len(st.session_state.move_log)-i}</span> {entry}</div>'
    st.markdown(log_html, unsafe_allow_html=True)

# Board position legend in expander
with st.expander("Board positions"):
    st.code("0 | 1 | 2\n3 | 4 | 5\n6 | 7 | 8")

# ──────────────────────────────────────────────────────────────────────────────
# FOOTER
# ──────────────────────────────────────────────────────────────────────────────
st.markdown("""
<hr class='divider'>
<p style='text-align:center;font-size:0.65rem;color:#444;letter-spacing:0.1em;'>
TIC-TAC-TOE AI · MINIMAX + Q-LEARNING · STREAMLIT
</p>
""", unsafe_allow_html=True)
