import csv
import time
import math

class TicTacToe:
    def __init__(self):
        self.board = [[' ' for _ in range(6)] for _ in range(5)]
        self.moves = []
        self.finished = False
        self.winner = ''
        self.metrics = []

    def is_valid_start(self, x, y):
        return not self.finished and 0 <= x < 6 and 0 <= y < 5 and self.board[y][x] == ' '

    def start(self, x, y, player):
        if self.is_valid_start(x, y):
            self.board[y][x] = player
            self.moves.append((player, 'Start', (x, y)))
        else:
            raise ValueError("Invalid start position")

    def is_valid_successor(self, x, y, player):
        if self.board[y][x] != ' ' or self.finished:
            return False
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]
        for dx, dy in directions:
            if 0 <= x + dx < 6 and 0 <= y + dy < 5 and self.board[y + dy][x + dx] == player:
                return True
        return False

    def successor(self, x, y, player, time, nodes):
        if self.is_valid_successor(x, y, player):
            self.board[y][x] = player
            self.moves.append((player, 'Move', (x, y), time, nodes))
            self.end_condition()
        else:
            print(f"Player {player}: {x}, {y}")
            raise ValueError("Invalid move")

    def descriptor(self):
        return self.board

    def has_won(self, player):
        for i in range(5):
            for j in range(6):
                if self.board[i][j] == player:
                    if j <= 2 and all(self.board[i][j + k] == player for k in range(4)):
                        return True
                    if i <= 1 and all(self.board[i + k][j] == player for k in range(4)):
                        return True
                    if i <= 1 and j <= 2 and all(self.board[i + k][j + k] == player for k in range(4)):
                        return True
                    if i <= 1 and j >= 3 and all(self.board[i + k][j - k] == player for k in range(4)):
                        return True
        return False

    def is_full(self):
        return all(cell != ' ' for row in self.board for cell in row)

    def save_moves(self, filename):
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Player", "Turn", "Move", "Time", "Nodes Generated"])
            writer.writerows(self.moves)

    def end_condition(self):
        for player in ['X', 'O']:
            if self.has_won(player):
                self.save_moves('moves.csv')
                self.finished = True
                self.winner = player
                print(f"{player} Wins!")
                return
        if self.is_full():
            self.save_moves('moves.csv')
            self.finished = True
            self.winner = 'Tie'
            print("Tie!")

    def display(self):
        # Print column numbers
        print("  ", end='')
        for j in range(6):
            print(f" {j} ", end='')
        print("\n  " + "-"*19)

        for i, row in enumerate(self.board):
            print(f"{i}|", end='')
            for cell in row:
                print(f" {cell} ", end='')
            print("|")
        print("  " + "-"*19)

    def minimax(self, depth, max_player, alpha, beta, player, counter=None):
        if counter is None:
            counter = [0]
        counter[0] += 1
        
        if depth == 0 or self.has_won('X') or self.has_won('O') or self.is_full():
            if self.has_won(player):
                return 1000, counter
            elif self.has_won(opp_player(player)):
                return -1000, counter
            else:
                return 0, counter
            
        if max_player:
            max_eval = -math.inf
            for col in range(6):
                for row in range(5):
                    if self.board[row][col] == ' ':
                        self.board[row][col] = 'X'
                        eval, _ = self.minimax(depth - 1, False, alpha, beta, player)
                        self.board[row][col] = ' '
                        max_eval = max(max_eval, eval)
                        alpha = max(alpha, eval)
                        if beta <= alpha:
                            break
            return max_eval, counter
        else:
            min_eval = math.inf
            for col in range(6):
                for row in range(5):
                    if self.board[row][col] == ' ':
                        self.board[row][col] = 'O'
                        eval, _ = self.minimax(depth - 1, True, alpha, beta, player)
                        self.board[row][col] = ' '
                        min_eval = min(min_eval, eval)
                        beta = min(beta, eval)
                        if beta <= alpha:
                            break
            return min_eval, counter

    def find_best_move(self, player, depth):
        best_row = None
        best_col = None
        best_eval = -math.inf if player == 'X' else math.inf
        nodes = 0
        for col in range(6):
            for row in range(5):
                if self.board[row][col] == ' ' and self.is_valid_successor(col, row, player):
                    self.board[row][col] = player
                    eval, gen_nodes = self.minimax(depth, player != 'X', -math.inf, math.inf, player)
                    nodes += gen_nodes[0]
                    self.board[row][col] = ' '
                    is_better_move = (eval > best_eval) if player == 'X' else (eval < best_eval)
                    if is_better_move:
                        best_eval = eval
                        best_row = row
                        best_col = col
        return best_row, best_col, nodes

def opp_player(player):
    if player == 'X':
        return 'O'
    else:
        return 'X'
    
def play_tic_tac_toe():
    game = TicTacToe()
    current_player = True  # True -> X, False -> O
    game.start(4, 3, 'X')
    game.start(3, 3, 'O')
    while not game.finished:
        game.display()
        if current_player:
            start_time = time.time()
            y, x, gen_nodes = game.find_best_move('X', 2)
            stop_time = time.time()
            print(x, y)
            if x is None:
                print("No valid move found! Exiting game.")
                return
            game.successor(x, y, 'X', stop_time - start_time, gen_nodes)
        else:  # Computer's turn
            start_time = time.time()
            y, x, gen_nodes = game.find_best_move('O', 4) 
            stop_time = time.time()
            if x is None:
                print("No valid move found! Exiting game.")
                return
            game.successor(x, y, 'O', stop_time - start_time, gen_nodes)
        current_player = not current_player
        game.display()

if __name__ == "__main__":
    play_tic_tac_toe()