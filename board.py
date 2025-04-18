class SmallBoard:
    """
    Represents one of the nine the small boards in the game.

    By default the board is full of empty squares.

    Keeps track of moving and winning state.
    """
    def __init__(self):
        """
        Initialize small board status
        """
        self.grid = [[' ' for _ in range(3)] for _ in range(3)]  
        self.winner = None 
        self.is_full = False

    def make_move(self, row, col, player):
        """
        Track the movements
        """
        if self.grid[row][col] == ' ' and self.winner == None:
            self.grid[row][col] = player
            self.check_winner()
            self.check_full()
            return True
        else:
            return False  

    def check_winner(self):
        """
        Track the small winner
        """
        lines = self.grid + [list(col) for col in zip(*self.grid)]  #
        diagonals = [[self.grid[i][i] for i in range(3)],
                     [self.grid[i][2 - i] for i in range(3)]]
        for line in (lines + diagonals):
            if line == ['X', 'X', 'X']:
                self.winner = 'X'
                return
            elif line == ['O', 'O', 'O']:
                self.winner = 'O'
                return

    def check_full(self):
        """
        check if the board is full (so no one wins and its a draw)
        """
        for row in self.grid:
            if ' ' in row:
                return False
        self.is_full = True
        return True


class BigBoard:
    """
    Large board, made up of 3x3 small boards

    By default the board is full of empty small boards.

    Keeps track of winning state.
    """
    def __init__(self):
        """
        Initialize large board status
        """
        self.boards = [[SmallBoard() for _ in range(3)] for _ in range(3)]
        self.winner = None

    def check_winner(self):
        """
        Track the game winner
        """
        status = [[self.boards[i][j].winner for j in range(3)] for i in range(3)]
        lines = status + [list(col) for col in zip(*status)]
        diagonals = [[status[i][i] for i in range(3)],
                     [status[i][2 - i] for i in range(3)]]
        for line in lines + diagonals:
            if line == ['X', 'X', 'X']:
                self.winner = 'X'
                return
            elif line == ['O', 'O', 'O']:
                self.winner = 'O'
                return

    def is_full(self):
        """
        check if board is fully occupied
        """
        for row in self.boards:
            for board in row:
                if board.winner is None and not board.is_full:
                    return False
        return True

