class Board:
    def __init__(self,current_player):
        self.current_player = current_player
        self.bit_board = '0' * 64
        self.board = [['.' for i in range(7)] for j in range(6)]
        pass

    def __hash__(self):
        pass

    def can_play(self,col):
        pass

    def play(self,col):
        if self.can_play(col):
            pass

        else:
            raise 'Invalid Move'
        self.current_player = 1 if self.current_player == 0 else 0


class AI:
    def __init__(self, board_state):
        pass

if __name__ == '__main__':
    newBoard = Board(1)
    for i in newBoard.board:
        for j in i:
            print(j, end='')
        print()
