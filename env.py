# env.py

class TicTacToeEnv:
    """
    Simple Tic-Tac-Toe environment.

    Board representation:
      1  -> X
     -1  -> O
      0  -> empty

    Board indices:
      0 | 1 | 2
      ---------
      3 | 4 | 5
      ---------
      6 | 7 | 8
    """

    def __init__(self):
        self.reset()

    def reset(self):
        """Reset the board and return the initial state."""
        self.board = [0] * 9
        self.done = False
        self.winner = None
        return self._get_state()

    # ── Core API ────────────────────────────────────────────────────────────

    def step(self, action: int, player: int):
        """
        Apply `player`'s move at position `action`.

        Returns:
            state, reward, done, info
        """
        if self.done:
            raise ValueError("Game is already over.")

        # Invalid move
        if self.board[action] != 0:
            self.done = True
            self.winner = -player
            return self._get_state(), -1, True, {"invalid": True}

        # Apply move
        self.board[action] = player

        # Check terminal conditions
        if self._check_win(player):
            self.done = True
            self.winner = player
            return self._get_state(), 1, True, {"winner": player}

        if self._check_draw():
            self.done = True
            self.winner = 0
            return self._get_state(), 0, True, {"draw": True}

        # Non-terminal move
        return self._get_state(), 0, False, {}

    # ── Helpers ─────────────────────────────────────────────────────────────

    def available_actions(self):
        """Return a list of valid move indices."""
        return [i for i, v in enumerate(self.board) if v == 0]

    def _get_state(self):
        """Return a hashable state representation."""
        return tuple(self.board)

    def _check_win(self, player: int) -> bool:
        """Check if `player` has won."""
        wins = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8),  # rows
            (0, 3, 6), (1, 4, 7), (2, 5, 8),  # cols
            (0, 4, 8), (2, 4, 6),             # diagonals
        ]
        return any(
            self.board[a] == self.board[b] == self.board[c] == player
            for a, b, c in wins
        )

    def _check_draw(self) -> bool:
        """Draw if board full and no winner."""
        return all(v != 0 for v in self.board)

    # ── Rendering ───────────────────────────────────────────────────────────

    def render(self):
        """Print the board."""
        symbols = {1: "X", -1: "O", 0: "."}
        for i in range(0, 9, 3):
            row = " ".join(symbols[self.board[i + j]] for j in range(3))
            print(row)
        print()
    def clone(self):
        new_env = TicTacToeEnv()
        new_env.board = self.board.copy()
        new_env.done = self.done
        new_env.winner = self.winner
        return new_env