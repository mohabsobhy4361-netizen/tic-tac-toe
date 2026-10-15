
import tkinter as tk
import sys
import subprocess

# =========================
# Colors
# =========================
BG_COLOR = "#080808"
CELL_COLOR = "#191919"
BORDER_COLOR = "#444444"
WINNING_CELL_COLOR = "#665500"
DRAW_BACKGROUND_COLOR = "#660000"
X_COLOR = "#FF3333"
O_COLOR = "#22CC66"
TEXT_COLOR = "#FFFFFF"
MUTED_COLOR = "#AAAAAA"

# Winning combinations
WINNING_LINES = [
    (0, 1, 2),
    (3, 4, 5),
    (6, 7, 8),
    (0, 3, 6),
    (1, 4, 7),
    (2, 5, 8),
    (0, 4, 8),
    (2, 4, 6)
]


class TicTacToe:

    def __init__(self, root):
        self.root = root
        self.root.title("TIC TAC TOE")
        self.root.configure(bg=BG_COLOR)
        self.root.resizable(False, False)

        self.cells = [""] * 9
        self.current_player = "X"
        self.game_over = False
        self.winning_combination = []
        self.buttons = []
        self.x_wins = 0
        self.o_wins = 0
        self.draws = 0

        # Title
        tk.Label(
            root,
            text="TIC TAC TOE",
            font=("Arial", 24, "bold"),
            bg=BG_COLOR,
            fg=TEXT_COLOR
        ).pack(pady=(22, 4))

        tk.Label(
            root,
            text="Player X vs Player O",
            font=("Arial", 11),
            bg=BG_COLOR,
            fg=MUTED_COLOR
        ).pack(pady=(0, 10))

        # Scoreboard
        self.score_label = tk.Label(
            root,
            text="X Wins: 0    O Wins: 0    Draws: 0",
            font=("Arial", 12, "bold"),
            bg=BG_COLOR,
            fg=MUTED_COLOR
        )
        self.score_label.pack(pady=(0, 18))

        # Game board
        board = tk.Frame(root, bg=BG_COLOR)
        board.pack(padx=22, pady=2)

        for i in range(9):

            button = tk.Button(
                board,
                text="",
                font=("Arial", 34, "bold"),
                width=3,
                height=1,
                bg=CELL_COLOR,
                fg=TEXT_COLOR,
                activebackground="#292929",
                activeforeground=TEXT_COLOR,
                relief="flat",
                bd=0,
                highlightthickness=1,
                highlightbackground=BORDER_COLOR,
                cursor="hand2",
                command=lambda index=i: self.make_move(index)
            )

            button.grid(
                row=i // 3,
                column=i % 3,
                padx=4,
                pady=4,
                ipadx=8,
                ipady=8
            )

            self.buttons.append(button)

        # Bind number-row and number-pad keys to board cells.
        key_bindings = {
            "1": 6, "2": 7, "3": 8,
            "4": 3, "5": 4, "6": 5,
            "7": 0, "8": 1, "9": 2,
            "KP_1": 6, "KP_2": 7, "KP_3": 8,
            "KP_4": 3, "KP_5": 4, "KP_6": 5,
            "KP_7": 0, "KP_8": 1, "KP_9": 2
        }

        for key, index in key_bindings.items():
            root.bind(f"<{key}>", lambda event, index=index: self.make_move(index))

        # Game status
        self.status_label = tk.Label(
            root,
            text="Turn: Player X",
            font=("Arial", 15, "bold"),
            bg=BG_COLOR,
            fg=TEXT_COLOR
        )

        self.status_label.pack(pady=18)

        # Restart button
        tk.Button(
            root,
            text="Restart Game",
            font=("Arial", 12, "bold"),
            bg=CELL_COLOR,
            fg=TEXT_COLOR,
            activebackground="#333333",
            activeforeground=TEXT_COLOR,
            relief="flat",
            bd=0,
            cursor="hand2",
            command=self.restart_game
        ).pack(
            fill="x",
            padx=26,
            pady=(0, 22),
            ipady=9
        )

    def play_sound(self, sound_type):
        try:
            if sys.platform.startswith("win"):
                import winsound

                if sound_type == "move":
                    winsound.Beep(700, 100)
                elif sound_type == "win":
                    winsound.Beep(1000, 180)
                    winsound.Beep(1300, 220)
                elif sound_type == "draw":
                    winsound.Beep(300, 250)

            elif sys.platform == "darwin":
                sound_map = {
                    "move": "/System/Library/Sounds/Tink.aiff",
                    "win": "/System/Library/Sounds/Glass.aiff",
                    "draw": "/System/Library/Sounds/Basso.aiff"
                }
                subprocess.Popen(
                    ["afplay", sound_map[sound_type]],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )

            else:
                sound_map = {
                    "move": "message",
                    "win": "complete",
                    "draw": "dialog-error"
                }
                subprocess.Popen(
                    ["paplay", f"/usr/share/sounds/freedesktop/stereo/{sound_map[sound_type]}.oga"],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )

        except (FileNotFoundError, ImportError):
            self.root.bell()

    def make_move(self, index):

        if self.cells[index] != "" or self.game_over:
            return

        self.play_sound("move")

        self.cells[index] = self.current_player

        color = X_COLOR if self.current_player == "X" else O_COLOR

        self.buttons[index].config(
            text=self.current_player,
            fg=color
        )

        # Check winner
        self.winning_combination = self.check_winner()

        if self.winning_combination:

            self.play_sound("win")

            for winning_index in self.winning_combination:
                self.buttons[winning_index].config(
                    bg=WINNING_CELL_COLOR,
                    activebackground=WINNING_CELL_COLOR
                )

            if self.current_player == "X":
                self.x_wins += 1
            else:
                self.o_wins += 1

            self.update_scoreboard()

            self.status_label.config(
                text=f"Player {self.current_player} WINS!",
                fg=color
            )

            self.game_over = True
            return

        # Check draw
        if all(cell != "" for cell in self.cells):

            self.play_sound("draw")

            self.draws += 1
            self.update_scoreboard()

            self.root.configure(bg=DRAW_BACKGROUND_COLOR)
            self.status_label.config(
                text="DRAW!",
                fg=TEXT_COLOR,
                bg=DRAW_BACKGROUND_COLOR
            )

            self.game_over = True
            return

        # Switch player
        if self.current_player == "X":
            self.current_player = "O"
        else:
            self.current_player = "X"

        self.status_label.config(
            text=f"Turn: Player {self.current_player}",
            fg=TEXT_COLOR
        )

    def update_scoreboard(self):
        self.score_label.config(
            text=f"X Wins: {self.x_wins}    O Wins: {self.o_wins}    Draws: {self.draws}"
        )

    def check_winner(self):

        for combination in WINNING_LINES:

            a, b, c = combination

            if (
                self.cells[a] != ""
                and self.cells[a] == self.cells[b] == self.cells[c]
            ):
                return combination

        return []

    def restart_game(self):

        self.cells = [""] * 9
        self.current_player = "X"
        self.game_over = False
        self.winning_combination = []

        self.root.configure(bg=BG_COLOR)
        self.status_label.config(bg=BG_COLOR)

        for button in self.buttons:
            button.config(
                text="",
                fg=TEXT_COLOR,
                bg=CELL_COLOR,
                activebackground="#292929"
            )

        self.status_label.config(
            text="Turn: Player X",
            fg=TEXT_COLOR
        )


# Run the game
if __name__ == "__main__":

    window = tk.Tk()
    game = TicTacToe(window)

    window.mainloop()
