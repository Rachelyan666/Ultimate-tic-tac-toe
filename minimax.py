import math
from copy import deepcopy

class UltimateTicTacToeAI:
    """
    For minimax algorithm
    """
    def __init__(self, max_depth=3):
        """
        Initialize parameter for minimax
        """
        self.max_depth = max_depth

    def minimax(self, game_state, depth, alpha, beta, maximizing_player, active_box):
        """
        the main logic of minimax, minimizing the opponent and maximize current 
        player’s performance to get the best result of play
        """
        winner = self.check_winner(game_state)
        if winner or depth == 0 or self.is_full(game_state):
            return self.evaluate(game_state, winner)

        valid_moves = self.get_valid_moves(game_state, active_box)
        if maximizing_player:
            max_eval = -math.inf
            for move in valid_moves:
                new_state = self.apply_move(deepcopy(game_state), move, 'X')
                next_active_box = (move[0] % 3, move[1] % 3)
                eval = self.minimax(new_state, depth - 1, alpha, beta, False, next_active_box)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break  # Alpha-Beta Pruning
            return max_eval
        else:
            min_eval = math.inf
            for move in valid_moves:
                new_state = self.apply_move(deepcopy(game_state), move, 'O')
                next_active_box = (move[0] % 3, move[1] % 3)
                eval = self.minimax(new_state, depth - 1, alpha, beta, True, next_active_box)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break  # Alpha-Beta Pruning
            return min_eval

    def get_best_move(self, game_state, active_box):
        """
        Find the best move of all the moves that the search tree leaves have.
        """
        best_eval = -math.inf
        best_move = None
        valid_moves = self.get_valid_moves(game_state, active_box)
        for move in valid_moves:
            new_state = self.apply_move(deepcopy(game_state), move, 'X')
            next_active_box = (move[0] % 3, move[1] % 3)
            move_eval = self.minimax(new_state, self.max_depth, -math.inf, math.inf, False, next_active_box)
            if move_eval > best_eval:
                best_eval = move_eval
                best_move = move
        return best_move

    def get_valid_moves(self, game_state, active_box):
        """
        Returns all available moves as tuples so they play in the target box.
        """
        if active_box is not None:
            box_row, box_col = active_box
            valid_moves = [
                (box_row * 3 + i, box_col * 3 + j)
                for i in range(3) for j in range(3)
                if game_state[box_row * 3 + i][box_col * 3 + j] == ' '
            ]
            if valid_moves:
                return valid_moves
        #if active box is None, check all possible moves in the board
        #however, even though there are 9 boxes on the board, make sure that the box isn't full or already has a winner, 
        #if the box already has a winner or is full, any empty cells in the full/winner box should not be included in the valid moves
        valid_moves = []
        for box_row in range(3):
            for box_col in range(3):
                box_start_row, box_start_col = box_row * 3, box_col * 3
                box_winner = self.check_small_board(
                    [row[box_start_col:box_start_col + 3] for row in game_state[box_start_row:box_start_row + 3]]
                )
                if box_winner is None:
                    valid_moves.extend(
                        [
                            (box_start_row + i, box_start_col + j)
                            for i in range(3) for j in range(3)
                            if game_state[box_start_row + i][box_start_col + j] == ' '
                        ]
                    )
        return valid_moves

    def apply_move(self, game_state, move, player):
        """
        Applies a move to the board.
        """
        i, j = move
        game_state[i][j] = player
        return game_state

    def check_winner(self, board):
        """
        Checks for a winner in any small board of the big board.
        """
        for i in range(3):
            for j in range(3):
                small_board = [row[j * 3:(j + 1) * 3] for row in board[i * 3:(i + 1) * 3]]
                winner = self.check_small_board(small_board)
                if winner:
                    return winner
        return None

    def check_small_board(self, board):
        """
        Checks if there is a winner in a small board.
        """
        for i in range(3):
            if board[i][0] == board[i][1] == board[i][2] != ' ':
                return board[i][0]
            if board[0][i] == board[1][i] == board[2][i] != ' ':
                return board[0][i]

        # Check diagonals
        if board[0][0] == board[1][1] == board[2][2] != ' ':
            return board[0][0]
        if board[0][2] == board[1][1] == board[2][0] != ' ':
            return board[0][2]

        return None

    def is_full(self, game_state):
        """
        Checks if the entire board is full.
        """
        return all(cell != ' ' for row in game_state for cell in row)

    def evaluate(self, game_state, winner):
        """
        Dynamic evaluation function for game state.
        """
        if winner == 'X':
            return 100  # AI wins
        elif winner == 'O':
            return -100  # Opponent wins
        else:
            # Heuristic for ongoing game
            x_score = self.count_lines(game_state, 'X')
            o_score = self.count_lines(game_state, 'O')
            return x_score - o_score

    def count_lines(self, game_state, player):
        """
        Count potential winning lines for a player.
        """
        score = 0
        for i in range(3):
            for j in range(3):
                small_board = [row[j * 3:(j + 1) * 3] for row in game_state[i * 3:(i + 1) * 3]]
                if self.check_small_board(small_board) is None:  # No winner yet
                    for line in small_board:
                        if line.count(player) > 0 and line.count(' ') > 0:
                            score += 1
        return score
