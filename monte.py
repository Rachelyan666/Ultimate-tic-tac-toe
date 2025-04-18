import random
from copy import deepcopy

class MonteCarloAI:
    """
    For Monte Carlo algoritm
    """
    def __init__(self, simulations=100):
        """
        Initialize parameter for monte carlo algorithm
        """
        self.simulations = simulations

    def get_best_move(self, game_state, active_box):
        """
        Find the best move using Monte Carlo simulations.
        """
        valid_moves = self.get_valid_moves(game_state, active_box)
        if not valid_moves:
            return None

        move_scores = {move: 0 for move in valid_moves}

        for move in valid_moves:
            for _ in range(self.simulations):
                result = self.simulate_game(game_state, move, 'X')
                if result == 'X':
                    move_scores[move] += 1
                elif result == 'O':
                    move_scores[move] -= 1

        best_move = max(move_scores, key=move_scores.get)
        return best_move

    def simulate_game(self, game_state, first_move, player):
        """
        Simulates a random game starting with the given move.
        """
        sim_state = deepcopy(game_state)
        self.apply_move(sim_state, first_move, player)
        current_player = 'O' if player == 'X' else 'X'

        while not self.is_over(sim_state):
            valid_moves = self.get_valid_moves(sim_state, None)
            random_move = random.choice(valid_moves)
            self.apply_move(sim_state, random_move, current_player)
            current_player = 'O' if current_player == 'X' else 'X'

        return self.check_winner(sim_state)

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

    def is_over(self, game_state):
        """
        Checks if the game is over.
        """
        return self.check_winner(game_state) is not None or all(
            cell != ' ' for row in game_state for cell in row
        )

    def check_winner(self, game_state):
        """
        Checks for a winner in any small board of the big board.
        """
        for i in range(3):
            for j in range(3):
                small_board = [row[j * 3:(j + 1) * 3] for row in game_state[i * 3:(i + 1) * 3]]
                winner = self.check_small_board(small_board)
                if winner:
                    return winner
        return None

    def check_small_board(self, board):
        """
        Checks for a winner in a small board.
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
