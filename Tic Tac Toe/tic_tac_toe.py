import tkinter as tk
from tkinter import messagebox

class TicTacToe:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Tic-Tac-Toe")
        self.board = [""] * 9
        self.buttons = []
        self.current_player = "X"
        self.point_x = 0
        self.point_o = 0
        self.colors = {"X": "#023374", "O": "#D34202"}
        self.create_board()

    def create_board(self):
        for i in range(9):
            button = tk.Button(self.window, text="", width=10, height=3,
                               font=('Arial', 24, 'bold'),
                               command=lambda i=i: self.on_button_click(i))
            button.grid(row=i//3, column=i%3)
            self.buttons.append(button)
        self.info_label = tk.Label(self.window, text="X's turn", font=('Arial', 12))
        self.info_label.grid(row=3, column=0, columnspan=3)
        self.window.mainloop()

    def on_button_click(self, index):
        if self.buttons[index]["text"] == "":
            self.buttons[index]["text"] = self.current_player
            self.buttons[index]["fg"] = self.colors[self.current_player]
            self.board[index] = self.current_player
            if self.check_winner():
                messagebox.showinfo("Game Over", f"{self.current_player} won!")
                if self.current_player == "X":
                    self.point_x += 1
                else:
                    self.point_o += 1
                self.ask_play_again()
            elif all(self.board):
                messagebox.showinfo("Game Over", "It's a tie!")
                self.ask_play_again()
            else:
                self.current_player = "O" if self.current_player == "X" else "X"
                self.info_label.config(text=f"{self.current_player}'s turn")

    def check_winner(self):
        win_conditions = [(0, 1, 2), (3, 4, 5), (6, 7, 8),
                          (0, 3, 6), (1, 4, 7), (2, 5, 8),
                          (0, 4, 8), (2, 4, 6)]
        for condition in win_conditions:
            if self.board[condition[0]] == self.board[condition[1]] == self.board[condition[2]] != "":
                return True
        return False

    def ask_play_again(self):
        play_again = messagebox.askyesno("Play Again", "Would you like to play again?")
        if play_again:
            self.reset_board()
        else:
            self.window.quit()

    def reset_board(self):
        self.board = [""] * 9
        for button in self.buttons:
            button["text"] = ""
            button["fg"] = "black"
        self.current_player = "X"
        self.info_label.config(text="X's turn")

if __name__ == "__main__":
    TicTacToe()
