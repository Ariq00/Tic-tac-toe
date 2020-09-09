from math import inf

board = [["1", "2", "3"],
         ["4", "5", "6"],
         ["7", "8", "9"]]


def player_setup():
    """Initialises the symbols for the human player and computer"""
    global player_1, computer
    player_1 = ""
    while player_1 not in ("X", "O"):
        player_1 = input("\nEnter X or O: ").upper()

    if player_1 == "X":
        computer = "O"
    else:
        computer = "X"


def display_board(board):
    print()
    for i in range(3):
        print(board[i][0] + " | " + board[i][1] + " | " + board[i][2])


def available_spaces(board):
    """Returns a list containing positions on the board which are still unoccupied"""
    options = []
    for x in range(3):
        for y in range(3):
            if board[x][y].isnumeric():  # available spaces will still be numbered
                options.append(int(board[x][y]))
    return options


def evaluate(board):
    """Returns an integer which represents the value of the game for the winner"""
    # Checking rows are the same
    for x in range(3):
        if len(set(board[x])) == 1:  # set will only contain 1 element if row is same
            if player_1 in set(board[x]):
                return -10
            else:
                return 10

    win_condition = [
        # Checking diagonals
        [board[0][0], board[1][1], board[2][2]],
        [board[0][2], board[1][1], board[2][0]],

        # Checking columns
        [board[0][0], board[1][0], board[2][0]],
        [board[0][1], board[1][1], board[2][1]],
        [board[0][2], board[1][2], board[2][2]],
    ]
    if [player_1] * 3 in win_condition:
        return -10
    elif [computer] * 3 in win_condition:
        return 10

    # Checking for draw
    if len(available_spaces(board)) == 0:
        return 0


def game_over(board):
    """Returns a boolean value indicating if there has been a win"""
    if evaluate(board) == -10 or evaluate(board) == 10:  # Checking for a win
        return True
    else:
        return False


def user_move(board):
    """Returns a list which is the updated game board containing the user input"""
    global moves
    user_input = int()
    while user_input not in available_spaces(board):
        if 1 <= user_input <= 9:
            print("\nThat space is already occupied! ")
        try:
            user_input = int(input("\nWhere would you like to place your counter? "))
        except ValueError:
            print("\nEnter a valid number!")

    moves = {  # Translates user input to coordinates
    1: [0, 0], 2: [0, 1], 3: [0, 2],
    4: [1, 0], 5: [1, 1], 6: [1, 2],
    7: [2, 0], 8: [2, 1], 9: [2, 2],
    }

    x, y = moves[user_input][0], moves[user_input][1]
    board[x][y] = player_1

    return board


def play_game(board):
    """Main function which controls the sequence of turns and when the game ends"""
    while not game_over(board) and len(available_spaces(board)) > 0:
        display_board(board)

        board = user_move(board)

        if evaluate(board) == -10:
            display_board(board)
            print("\nCongratulations, you win!")
            return

        else:
            if len(available_spaces(board)) >= 1:
                x, y = computer_move(board)
                board[x][y] = computer
            if evaluate(board) == 10:
                display_board(board)
                print("\nYou lose!")
                return

            if evaluate(board) == 0:
                display_board(board)
                print("\nIt's a tie!")


def computer_move(board):
    """Returns a list with the coordinates of the optimal move for the computer"""
    depth = len(available_spaces(board))
    move = minimax(board, depth, True)
    x, y = move[0], move[1]
    return x, y


def minimax(board, depth, maximising_player):
    """Function which finds the optimal play for the computer and returns
     a list containing the optimal next move for the computer and its coordinates"""
    if maximising_player:       # computer player
        best_score = [0, 0, -inf]  # Note: (0,0) are arbitrary coordinates
        player = computer
    else:
        best_score = [0, 0, +inf]
        player = player_1

    if depth == 0 or game_over(board):
        score = evaluate(board)
        return [0, 0, score]

    for position in available_spaces(board):
        x, y = moves[position][0], moves[position][1]
        board[x][y] = player

        if maximising_player:
            score = minimax(board, depth - 1, False)

        else:
            score = minimax(board, depth - 1, True)

        board[x][y] = str(position)
        score[0], score[1] = x, y

        if maximising_player:
            if score[2] > best_score[2]:
                best_score = score
        else:
            if score[2] < best_score[2]:
                best_score = score

    return best_score


player_setup()
play_game(board)
