import unittest
import sys
import os
from copy import deepcopy

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from board import SmallBoard, BigBoard
from main import get_board_choice, get_move_choice, print_board, apply_ai_move, convert_to_9x9
from unittest.mock import patch

class TestSmallBoard(unittest.TestCase):
    def setUp(self):
        self.board = SmallBoard()

    def test_initialization(self):
        self.assertEqual(self.board.grid, [[' ']*3 for _ in range(3)])
        self.assertIsNone(self.board.winner)
        self.assertFalse(self.board.is_full)

    def test_make_move(self):
        self.assertTrue(self.board.make_move(0, 0, 'X'))
        self.assertEqual(self.board.grid[0][0], 'X')
        self.assertFalse(self.board.make_move(0, 0, 'O'))  # Cell already taken

    def test_check_winner_row(self):
        self.board.grid = [['X', 'X', 'X'],
                            [' ', ' ', ' '],
                            [' ', ' ', ' ']]
        self.board.check_winner()
        self.assertEqual(self.board.winner, 'X')

    def test_check_winner_column(self):
        self.board.grid = [['O', ' ', ' '],
                            ['O', ' ', ' '],
                            ['O', ' ', ' ']]
        self.board.check_winner()
        self.assertEqual(self.board.winner, 'O')

    def test_check_winner_diagonal(self):
        self.board.grid = [['X', ' ', ' '],
                            [' ', 'X', ' '],
                            [' ', ' ', 'X']]
        self.board.check_winner()
        self.assertEqual(self.board.winner, 'X')

    def test_check_full(self):
        self.board.grid = [['X', 'O', 'X'],
                            ['O', 'X', 'O'],
                            ['O', 'X', 'O']]
        self.board.check_full()
        self.assertTrue(self.board.is_full)

    def test_no_winner(self):
        self.board.grid = [['X', 'O', 'X'],
                            ['O', 'X', 'O'],
                            ['O', 'X', ' ']]
        self.board.check_winner()
        self.assertIsNone(self.board.winner)

class TestBigBoard(unittest.TestCase):
    def setUp(self):
        self.big_board = BigBoard()

    def test_initialization(self):
        for row in self.big_board.boards:
            for board in row:
                self.assertIsInstance(board, SmallBoard)

    def test_check_winner_big_board_row(self):
        # Set up three small boards in the top row won by 'X'
        for col in range(3):
            self.big_board.boards[0][col].winner = 'X'
        self.big_board.check_winner()
        self.assertEqual(self.big_board.winner, 'X')

    def test_check_winner_big_board_column(self):
        # Set up three small boards in the first column won by 'O'
        for row in range(3):
            self.big_board.boards[row][0].winner = 'O'
        self.big_board.check_winner()
        self.assertEqual(self.big_board.winner, 'O')

    def test_check_winner_big_board_diagonal(self):
        # Set up small boards in the diagonal won by 'X'
        for i in range(3):
            self.big_board.boards[i][i].winner = 'X'
        self.big_board.check_winner()
        self.assertEqual(self.big_board.winner, 'X')

    def test_is_full(self):
        # Fill all small boards
        for row in self.big_board.boards:
            for board in row:
                board.is_full = True
        self.assertTrue(self.big_board.is_full())

    def test_not_full(self):
        self.big_board.boards[0][0].is_full = False
        self.assertFalse(self.big_board.is_full())

    def test_no_winner(self):
        self.big_board.check_winner()
        self.assertIsNone(self.big_board.winner)

class TestPrintBoard(unittest.TestCase):
    def test_print_board_runs(self):
        big_board = BigBoard()
        try:
            print_board(big_board)
        except Exception as e:
            self.fail(f"print_board raised an exception {e}")

from minimax import UltimateTicTacToeAI

class TestUltimateTicTacToeAI(unittest.TestCase):

    def setUp(self):
        """Initialize AI and sample game states."""
        self.ai = UltimateTicTacToeAI(max_depth=3)

        # Empty board state (9x9 ultimate tic-tac-toe board)
        self.empty_board = [[' ' for _ in range(9)] for _ in range(9)]

        # Game state with a win for 'X' in a 3x3 small board
        self.x_win_state = [
            ['X', 'X', 'X', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
        ]

        self.x_win_game = [
            ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
        ]

        self.x_lose_state = [
            ['O', 'O', 'O', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
        ]

        # Board state with a tie
        self.tied_board = [
            ['X', 'O', 'O', 'O', 'X', 'X', 'X', 'O', 'O'],
            ['O', 'X', 'X', 'X', 'O', 'O', 'O', 'X', 'X'],
            ['O', 'X', 'O', 'X', 'O', 'X', 'O', 'X', 'O'],
            ['O', 'X', 'X', 'X', 'O', 'O', 'O', 'X', 'X'],
            ['X', 'O', 'O', 'O', 'X', 'X', 'X', 'O', 'O'],
            ['O', 'X', 'X', 'X', 'O', 'O', 'O', 'X', 'X'],
            ['O', 'X', 'X', 'X', 'O', 'O', 'O', 'X', 'X'],
            ['X', 'O', 'O', 'O', 'X', 'X', 'X', 'O', 'O'],
            ['O', 'X', 'X', 'X', 'O', 'O', 'O', 'X', 'X'],
        ]


    def test_empty_board(self):
        """Test that AI picks a valid move on an empty board."""
        best_move = self.ai.get_best_move(self.empty_board, None)
        self.assertIn(best_move, self.ai.get_valid_moves(self.empty_board, None))

    def test_x_win_state(self):
        """Test that the AI correctly evaluates a winning state for 'X'."""
        score = self.ai.minimax(self.x_win_state, 0, -float('inf'), float('inf'), True, None)
        self.assertEqual(score, 100)  # 'X' wins

    def test_tied_board(self):
        """Test that the AI evaluates a tied board correctly."""
        score = self.ai.minimax(self.tied_board, 0, -float('inf'), float('inf'), True, None)
        self.assertEqual(score, 0)  # Tie game

    def test_lose_board(self):
        """Test that the AI evaluates a lose board correctly."""
        score = self.ai.minimax(self.x_lose_state, 0, -float('inf'), float('inf'), True, None)
        self.assertEqual(score, -100)  # lose game

    def test_alpha_beta_pruning(self):
        """Test that Alpha-Beta pruning works by comparing performance."""
        import time

        # Measure execution time with alpha-beta pruning enabled
        start_time = time.time()
        self.ai.minimax(self.empty_board, 3, -float('inf'), float('inf'), True, None)
        end_time = time.time()

        # Ensure it runs within a reasonable time
        self.assertLess(end_time - start_time, 2)
    
    def test_apply_move(self):
        move = (0, 0)
        new_state = self.ai.apply_move(deepcopy(self.empty_board), move, 'X')
        self.assertEqual(new_state[0][0], 'X')

    def test_get_valid_moves(self):
        valid_moves = self.ai.get_valid_moves(self.empty_board, None)
        self.assertEqual(len(valid_moves), 81)  # All cells should be valid moves initially
        # Test when a specific box is active
        self.empty_board[0][0] = 'X'
        valid_moves = self.ai.get_valid_moves(self.empty_board, (0, 0))
        self.assertEqual(len(valid_moves), 8)

    def test_evaluate(self):
        score = self.ai.evaluate(self.x_win_state, 'X')
        self.assertEqual(score, 100)
        score = self.ai.evaluate(self.tied_board, None)
        self.assertEqual(score, 0)

    def test_count_lines(self):
        count = self.ai.count_lines(self.empty_board, 'X')
        self.assertEqual(count, 0)  # No lines initially
        count2 = self.ai.count_lines(self.x_lose_state, 'X')
        self.assertEqual(count2, 0)

from monte import MonteCarloAI

class TestMonteCarloAI(unittest.TestCase):

    def setUp(self):
        self.ai = MonteCarloAI(simulations=10)
        self.empty_board = [[' ' for _ in range(9)] for _ in range(9)]
        self.x_winning_board = [
            ['X', 'X', 'X', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
        ]

    def test_get_valid_moves(self):
        valid_moves = self.ai.get_valid_moves(self.empty_board, None)
        self.assertEqual(len(valid_moves), 81)

        # Test active box restriction
        self.empty_board[0][0] = 'X'
        valid_moves = self.ai.get_valid_moves(self.empty_board, (0, 0))
        self.assertEqual(len(valid_moves), 8)

    def test_apply_move(self):
        move = (0, 0)
        new_state = self.ai.apply_move(deepcopy(self.empty_board), move, 'X')
        self.assertEqual(new_state[0][0], 'X')

    def test_is_over(self):
        self.assertFalse(self.ai.is_over(self.empty_board))
        self.assertTrue(self.ai.is_over(self.x_winning_board))

    def test_check_winner(self):
        winner = self.ai.check_winner(self.x_winning_board)
        self.assertEqual(winner, 'X')
        no_winner = self.ai.check_winner(self.empty_board)
        self.assertIsNone(no_winner)

    def test_check_small_board(self):
        small_board = [['X', 'X', 'X'], [' ', ' ', ' '], [' ', ' ', ' ']]
        winner = self.ai.check_small_board(small_board)
        self.assertEqual(winner, 'X')

        small_board = [['X', ' ', ' '], ['X', ' ', ' '], ['X', ' ', ' ']]
        winner = self.ai.check_small_board(small_board)
        self.assertEqual(winner, 'X')

        small_board = [['X', ' ', ' '], [' ', 'X', ' '], [' ', ' ', 'X']]
        winner = self.ai.check_small_board(small_board)
        self.assertEqual(winner, 'X')

    def test_simulate_game(self):
        result = self.ai.simulate_game(deepcopy(self.empty_board), (0, 0), 'X')
        self.assertIn(result, ['X', 'O', None])

    def test_get_best_move(self):
        # Best move on an empty board should be a valid move
        best_move = self.ai.get_best_move(deepcopy(self.empty_board), None)
        self.assertIn(best_move, self.ai.get_valid_moves(self.empty_board, None))

class TestMainFunctions(unittest.TestCase):
    @patch('builtins.input', side_effect=['1', '1'])
    def test_get_board_choice(self, mock_input):
        big_board = BigBoard()
        board_row, board_col = get_board_choice('X', big_board)
        self.assertEqual((board_row, board_col), (1, 1))

    @patch('builtins.input', side_effect=['0', '2'])
    def test_get_move_choice(self, mock_input):
        small_board = SmallBoard()
        move_row, move_col = get_move_choice('O', small_board)
        self.assertEqual((move_row, move_col), (0, 2))

    def test_print_board(self):
        big_board = BigBoard()
        try:
            print_board(big_board)  # Should not raise any exceptions
        except Exception as e:
            self.fail(f"print_board raised an exception: {e}")

    def test_apply_ai_move(self):
        big_board = BigBoard()
        move = (0, 0)
        player = 'X'
        board_row, board_col, cell_row, cell_col = apply_ai_move(big_board, move, player)
        self.assertEqual(big_board.boards[board_row][board_col].grid[cell_row][cell_col], player)

    def test_convert_to_9x9(self):
        big_board = BigBoard()
        board_9x9 = convert_to_9x9(big_board)
        self.assertEqual(len(board_9x9), 9)
        self.assertEqual(len(board_9x9[0]), 9)

if __name__ == '__main__':
    unittest.main()