import math

# Constants for players
PLAYER_X = 'X'
PLAYER_O = 'O'

# Define the game board (5x6 grid)
board = [[' ' for _ in range(6)] for _ in range(5)]

# Function to print the current state of the board
def print_board():
    for row in board:
        print(' '.join(row))
    print()

# Function to check if there is a winner
def check_winner(player):
    # Check horizontally
    for row in board:
        for i in range(3):
            if all(row[i:i+4] == [player] * 4):
                return True

    # Check vertically
    for col in range(6):
        for i in range(2):
            if all(board[i+j][col] == player for j in range(4)):
                return True

    # Check diagonally (top-left to bottom-right)
    for row in range(3):
        for col in range(4):
            if all(board[row+i][col+i] == player for i in range(4)):
                return True

    # Check diagonally (top-right to bottom-left)
    for row in range(3):
        for col in range(3, 7):
            if all(board[row+i][col-i] == player for i in range(4)):
                return True

    return False

# Function to check if the board is full
def is_board_full():
    return all(cell != ' ' for row in board for cell in row)

# Minimax algorithm with alpha-beta pruning
def minimax(board, depth, max_player, alpha, beta):
    if depth == 0 or check_winner(PLAYER_X) or check_winner(PLAYER_O) or is_board_full():
        if check_winner(PLAYER_X):
            return 1000
        elif check_winner(PLAYER_O):
            return -1000
        return 0

    if max_player:
        max_eval = -math.inf
        for col in range(6):
            for row in range(5):
                if board[row][col] == ' ':
                    board[row][col] = PLAYER_X
                    eval = minimax(board, depth - 1, False, alpha, beta)
                    board[row][col] = ' '
                    max_eval = max(max_eval, eval)
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break
        return max_eval
    else:
        min_eval = math.inf
        for col in range(6):
            for row in range(5):
                if board[row][col] == ' ':
                    board[row][col] = PLAYER_O
                    eval = minimax(board, depth - 1, True, alpha, beta)
                    board[row][col] = ' '
                    min_eval = min(min_eval, eval)
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break
        return min_eval
                                                                     # Everything above is the same as player 1 implementation

# Function to find the best move for Player O
def find_best_move():
    best_move = None
    best_eval = -math.inf

    for col in range(6):
        for row in range(5):
            if board[row][col] == ' ':
                board[row][col] = PLAYER_O                           # Player X changed to Player O
                eval = minimax(board, 4, False, -math.inf, math.inf) # Depth changed to 4
                board[row][col] = ' '
                if eval > best_eval:
                    best_eval = eval
                    best_move = (row, col)

    return best_move

# Main game loop
def play_game():
    print_board()
    
    while True:
        row, col = find_best_move()
        board[row][col] = PLAYER_X
        print_board()
        if check_winner(PLAYER_X):
            print("Player X wins!")
            break
        elif is_board_full():
            print("It's a tie!")
            break

        # Let Player O make a move
        while True:
            o_col = int(input("Enter column for Player O (1-6): ")) - 1
            if 0 <= o_col < 6 and board[0][o_col] == ' ':
                for row in range(4, -1, -1):
                    if board[row][o_col] == ' ':
                        board[row][o_col] = PLAYER_O
                        break
                break
            else:
                print("Invalid move. Try again.")

        print_board()
        if check_winner(PLAYER_O):
            print("Player O wins!")
            break
        elif is_board_full():
            print("It's a tie!")
            break