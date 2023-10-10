import csv

class TicTacToe:
    def __init__(self):
        self.board = [[' ' for _ in range(6)] for _ in range(5)]
        self.moves = []
    
    def is_valid_start(self, x, y):
        return 0 <= x < 6 and 0 <= y < 5 and self.board[y][x] == ' '

    # Start Function, places the initial pieces
    def start(self, x, y, player):
        if self.is_valid_start(x, y):
            self.board[y][x] = player
            self.moves.append((player, 'Start', (x, y)))
        else:
            raise ValueError("Invalid start position")

    # Checks if next move is valid
    def is_valid_successor(self, x, y):
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]
        if self.board[y][x] != ' ':
            return False
        for dx, dy in directions:
            if 0 <= x + dx < 6 and 0 <= y + dy < 5 and self.board[y + dy][x + dx] != ' ':
                return True
        return False
    
    # Next move function, 
    def successor(self, x, y, player):
        if self.is_valid_successor(x, y):
            self.board[y][x] = player
            self.moves.append((player, 'Move', (x, y)))
        else:
            raise ValueError("Invalid move")
    
    # Returns the board state for AI use
    def descriptor(self):
        return self.board

    # Checks if a player has won the game
    # Needs further testing
    def has_won(self, player):
        # Check rows, columns and diagonals
        for i in range(5):
            for j in range(6):
                if self.board[i][j] == player:
                    # Horizontal
                    if j <= 2 and all(self.board[i][j + k] == player for k in range(4)):
                        return True
                    # Vertical
                    if i <= 1 and all(self.board[i + k][j] == player for k in range(4)):
                        return True
                    # Diagonal Right
                    if i <= 1 and j <= 2 and all(self.board[i + k][j + k] == player for k in range(4)):
                        return True
                    # Diagonal Left
                    if i <= 1 and j >= 3 and all(self.board[i + k][j - k] == player for k in range(4)):
                        return True
        return False

    # Checks if the board is completely filled
    def is_full(self):
        for row in self.board:
            for cell in row:
                if cell == ' ':
                    return False
        return True

    # Saves the games moves to a csv file
    def save_moves(self, filename):
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Player", "Turn", "Move"])
            for move in self.moves:
                writer.writerow(move)

    # Checks if the game has ended, saves moves if game ended
    def end_condition(self):
        if self.has_won('X'):
            game.save_moves('moves.csv')
            return 'X Wins!'
        if self.has_won('O'):
            game.save_moves('moves.csv')
            return 'O Wins!'
        if self.is_full():
            game.save_moves('moves.csv')
            return 'Tie'
        return None

    # Displays the games state in the console
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


# Initialize the game
game = TicTacToe()

# Initial moves
game.start(2, 2, 'X')  # Player X places at (2, 2)
game.display()

game.start(3, 2, 'O')  # Player O places at (3, 2)
game.display()

# Players take turns to make their moves
game.successor(3, 1, 'X')  # Player X places next to their existing piece
game.display()

game.successor(4, 2, 'O')  # Player O places next to their existing piece
game.display()

game.successor(3, 3, 'X')  # Player X makes another move
game.display()

game.successor(4, 3, 'O')  # Player O makes another move
game.display()

game.successor(2, 1, 'X')  # Player X's move
game.display()

game.successor(4, 1, 'O')  # Player O's move, now has 4 in a column vertically
game.display()

game.successor(2, 0, 'X')  # Player X's move
game.display()

game.successor(4, 0, 'O')  # Player O's move, now has 4 in a column vertically
game.display()

# Check for end condition
result = game.end_condition()
if result:
    print(f"Game over. Result: {result}")
    game.save_moves('moves.csv')
