# Tic-Tac-Toe Game
def print_board(board):
    print("\n")
    print(f" {board[0]} | {board[1]} | {board[2]} ")
    print("---|---|---")
    print(f" {board[3]} | {board[4]} | {board[5]} ")
    print("---|---|---")
    print(f" {board[6]} | {board[7]} | {board[8]} ")
    print("\n")


def check_win(board, player):
    win_conditions = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Horizontal (Rows)
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Vertical (Columns)
        [0, 4, 8], [2, 4, 6]  # Diagonals
    ]
    for condition in win_conditions:
        if board[condition[0]] == board[condition[1]] == board[condition[2]] == player:
            return True
    return False


def check_draw(board):
    return all(cell == 'X' or cell == 'O' for cell in board)


def play_game():
    print("Welcome to Tic-Tac-Toe !")
    player1_name = input("Enter Name for Player 1 (X): ").strip() or "Player 1"
    player2_name = input("Enter Name for Player 2 (O): ").strip() or "Player 2"

    while True:
        board = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
        current_symbol = 'X'
        current_name = player1_name
        game_active = True

        while game_active:
            print_board(board)
            print(f"{current_name}'s turn ({current_symbol}).")

            # Input handling
            move = input("Choose an empty cell number (1-9): ").strip()

            if not move.isdigit():
                print("❌ Invalid input! Please enter a number between 1 and 9.")
                continue

            move_num = int(move)

            if move_num < 1 or move_num > 9:
                print("❌ Out of range! Please choose a number between 1 and 9.")
                continue

            index = move_num - 1

            if board[index] == 'X' or board[index] == 'O':
                print("❌ That cell is already occupied! Choose another one.")
                continue

            board[index] = current_symbol

            if check_win(board, current_symbol):
                print_board(board)
                print(f"🎉 Congratulations! {current_name} wins the game!")
                game_active = False
                break

            if check_draw(board):
                print_board(board)
                print("🤝 It's a draw! The board is full.")
                game_active = False
                break

            if current_symbol == 'X':
                current_symbol = 'O'
                current_name = player2_name
            else:
                current_symbol = 'X'
                current_name = player1_name

        play_again = input("\nDo you want to play another round? (yes/no): ").strip().lower()
        if play_again not in ['yes', 'y']:
            print("Thanks for playing! Goodbye.")
            break


if __name__ == "__main__":
    play_game()