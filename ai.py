import random
import copy


class Board:
    def __init__(self, current_player=0, p_board=None):
        self.current_player = current_player
        if not p_board:
            self.hash_key = 0
            self.hash_board = self.initial_hash()
            self.bit_board = int('0' * 64, 2)
            self.mask = int('0' * 64, 2)
            self.board = [['.' for col in range(7)] for row in range(6)]
            self.moves_remaining = 42
            self.col_heights = [0 for col in range(7)]
            self.last_played_col = None
        else:
            self.bit_board = p_board.bit_board
            self.board = p_board.board
            self.current_player = p_board.current_player
            self.hash_board = p_board.hash_board
            self.hash_key = p_board.hash_key
            self.moves_remaining = p_board.moves_remaining
            self.col_heights = p_board.col_heights
            self.last_played_col = p_board.last_played_col
            self.mask = p_board.mask

    def __hash__(self):
        return self.hash_key

    def __eq__(self, other):
        return True if self.bit_board == other.bit_board and self.moves_remaining == other.moves_remaining and \
                       self.mask == other.mask else False

    def __str__(self):
        t = ""
        for i in reversed(self.board):
            for j in i:
                t+=j
            t+='\n'
        t+='\n'
        return t

    @classmethod
    def copy_board(cls, prev_board):
        return Board(prev_board.current_player, prev_board)

    def initial_hash(self):
        board = [[random.getrandbits(64) for i in range(2)] for j in range(42)]
        return board

    def can_play(self, col):
        if self.col_heights[col] != 6:
            return True
        return False

    def play(self, col):
        if self.can_play(col):
            self.col_heights[col] += 1
            self.last_played_col = col
            piece = 'x' if self.get_current_player() else 'o'
            self.board[self.col_heights[col]-1][col] = piece
            # finds it in hashing based on 42 - weird numerics in the 42 section
            self.hash_key ^= \
                self.hash_board[self.last_played_col * 6 +
                                self.col_heights[self.last_played_col] - 1][self.get_current_player()]
            self.bit_board ^= self.mask
            self.mask |= self.mask + self.bottom_mask(col)
            self.moves_remaining -= 1

        else:
            raise ValueError('Cannot play that move -- check before action')
        self.current_player = 1 if self.get_current_player() == 0 else 0

    def bottom_mask(self, col):
        return 1 << col*7

    def is_winning_move(self,col):
        pos = self.bit_board
        pos |= (self.mask + self.bottom_mask(col)) & self.column_mask(col)
        m = pos & (pos >> 7)
        if m & (m >> (2*7)):
            return True
        m = pos & (pos >> 6)
        if m & (m >> (2 * 6)):
            return True
        m = pos & (pos >> (6 + 2))
        if m & (m >> (2 * (6 + 2))):
            return True
        m = pos & (pos >> 1)
        if m & (m >> 2):
            return True
        return False

    def won_game(self):
        pos = self.bit_board
        m = pos & (pos >> 7)
        if m & (m >> (2 * 7)):
            return True
        m = pos & (pos >> 6)
        if m & (m >> (2 * 6)):
            return True
        m = pos & (pos >> (6 + 2))
        if m & (m >> (2 * (6 + 2))):
            return True
        m = pos & (pos >> 1)
        if m & (m >> 2):
            return True
        return False

    def column_mask(self, col):
        return (1 << 6) - 1 << col*7

    def get_current_player(self):
        return self.current_player


class AI:
    def __init__(self):
        self.z_positions = {}
        self.column_order = [3, 4, 2, 5, 1, 6, 0]
        self.best_move = None

    def negamax(self, board_state):
        if board_state.moves_remaining == 0:
            return 0

        for i in range(7):
            if board_state.can_play(self.column_order[i]) and board_state.is_winning_move(self.column_order[i]):
                return (49 - (42 - board_state.moves_remaining))//2
        best_value = -float('inf')
        for i in range(7):
            if board_state.can_play(self.column_order[i]):

                new_board_state = Board(board_state.current_player, board_state)
                new_board_state.play(self.column_order[i])
                score = -self.negamax(new_board_state)

                best_value = max(score, best_value)

                '''
                alpha = max(score, alpha)
                if alpha >= beta:
                    break
                '''
        return best_value


