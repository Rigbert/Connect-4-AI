from ai import Board, AI

artInt = AI()
cur_board = Board(0)
print("Welcome to Connect-4 AI")
while not cur_board.won_game():
    print(cur_board)
    print("Please make a move based on a zero-indexed column: ")
    user_input = int(input())
    while user_input > 6 or user_input < 0 or not cur_board.can_play(user_input):
        print("Please enter a valid option")
        user_input = int(input())
    cur_board.play(user_input)
    print(artInt.negamax(cur_board, -float("inf"), float("inf")))



