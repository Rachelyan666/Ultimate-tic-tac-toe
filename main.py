import pygame
from minimax import UltimateTicTacToeAI
from monte import MonteCarloAI
from board import BigBoard, SmallBoard
from gui import draw_board, get_cell, show_winner, starting_page, show_draw

def get_board_choice(player, big_board):
    """
    prompt the player to get their choices of which board to play on
    """
    while True:
        try:
            print("Player {player}, Step 1: Choose the board you want to play.")
            board_row = int(input(f"Enter the row of the big board (0-2): "))
            board_col = int(input(f"Enter the column of the big board (0-2): "))
            if 0 <= board_row <=2 and 0 <= board_col <=2:
                board = big_board.boards[board_row][board_col]
                if board.winner is None and not board.is_full:
                    return board_row, board_col
                else:
                    print("This board is already won or full. Choose another one.")
            else:
                print("Invalid board coordinates. Try again.")
        except ValueError:
            print("Invalid input. Please enter numbers between 0 and 2.")


def get_move_choice(player, board):
    """
    prompt the player to get which grid they play on for each small board
    """
    while True:
        try:
            print(f"Player {player}, Step 2: Choose the grid you want to play on.")
            move_row = int(input(f"Enter the row of the small board (0-2): "))
            move_col = int(input(f"Enter the column of the small board (0-2): "))
            if 0 <= move_row <=2 and 0 <= move_col <=2:
                if board.grid[move_row][move_col] == ' ':
                    return move_row, move_col
                else:
                    print("This grid is already taken. Choose another one.")
            else:
                print("Invalid grid coordinates. Try again.")
        except ValueError:
            print("Invalid input. Please enter numbers between 0 and 2.")

def print_board(big_board):
    """
    command line drawing
    """
    boards = big_board.boards
    for small_board_row in range(3):
        for cell_row in range(3):
            line = ''
            for small_board_col in range(3):
                board = boards[small_board_row][small_board_col]
                line += ' ' + ' | '.join(board.grid[cell_row]) + ' '
                if small_board_col != 2:
                    line += '||'
            print(line)
            if cell_row != 2:
                print('---+---+---++---+---+---++---+---+---')
        if small_board_row != 2:
            print('==========++===========++==========')


def convert_to_9x9(big_board):
    """
    Converts the BigBoard to a 9x9 flattened representation.
    """
    board = []
    for small_row in big_board.boards:
        for row_idx in range(3):
            row = []
            for small_board in small_row:
                row.extend(small_board.grid[row_idx])
            board.append(row)
    return board


def apply_ai_move(big_board, move, player):
    """
    Converts the AI's move (9x9) into a BigBoard move and applies it.
    """
    flat_row, flat_col = move
    board_row, cell_row = divmod(flat_row, 3)
    board_col, cell_col = divmod(flat_col, 3)
    big_board.boards[board_row][board_col].make_move(cell_row, cell_col, player)
    return board_row, board_col, cell_row, cell_col

def check_smallboard(big_board, next_row, next_col):
    """
    check if the small board has a winner or is full, so to avoid it as a next step
    """
    if next_row != None and next_col != None:
            next_board = big_board.boards[next_row][next_col]
            if (next_board.winner != None):
                next_row, next_col = None, None
                return next_row, next_col
            elif (next_board.is_full):
                next_row, next_col = None, None
                return next_row, next_col
            else:
                return next_row, next_col
    else:
        return next_row, next_col

def main():
    pygame.init()
    screen = pygame.display.set_mode((600, 650))
    pygame.display.set_caption("Ultimate Tic-Tac-Toe")

    big_board = BigBoard()
    ai = UltimateTicTacToeAI(max_depth=3)  # Create AI instance
    current_player = 'X'
    next_board_row = None
    next_board_col = None
    player_types = {'X': 'AI', 'O': 'Human'}  # Define player types: 'AI' or 'Human'
    subtitle = ""  # Text to display in the subtitle area

    windows = int(input(f"Choose playing with command line (1) or GUI (2): "))
    cmdln = False
    run_gui = False

    if windows == 1:
        cmdln = True
        run_gui = False
    elif windows == 2:
        run_gui = True
        cmdln = False
    else:
        print ("invalid choice, please choose 1 or 2")

    if cmdln:
        ai_algorithm = int(input(f"Choose playing with one of the two different AI models: Minimax (1) or Monte Carlo (2): "))

        if ai_algorithm == 1:
            ai = UltimateTicTacToeAI(max_depth=3)
        elif ai_algorithm == 2:
            ai = MonteCarloAI(simulations=100)
    while cmdln:
        print_board(big_board)
        # Choose the AI algorithm
        
        if big_board.winner is not None:
            print(f"Player {big_board.winner} wins the game!")
            break
        if big_board.is_full():
            print("The game is a draw!")
            break

        # Get move for the current player
        if player_types[current_player] == 'Human':
            next_board_row, next_board_col = check_smallboard(big_board, next_board_row, next_board_col)
            if next_board_row is not None and next_board_col is not None:
                required_board = big_board.boards[next_board_row][next_board_col]
                if required_board.winner is None and not required_board.is_full:
                    board_row, board_col = next_board_row, next_board_col
                    print(f"Player {current_player}, you must play in board ({board_row}, {board_col}).")
                else:
                    print(f"Player {current_player}, you can choose any board.")
                    board_row, board_col = get_board_choice(current_player, big_board)
            else:
                print(f"Player {current_player}, you can choose any board.")
                board_row, board_col = get_board_choice(current_player, big_board)
            if board_row == 'quit':
                print(f"Player {current_player} has quit the game.")
                break
            current_board = big_board.boards[board_row][board_col]
            move_row, move_col = get_move_choice(current_player, current_board)
            if move_row == 'quit':
                print(f"Player {current_player} has quit the game.")
                break
            current_board.make_move(move_row, move_col, current_player)
        else:
            # AI's turn
            print(f"AI ({current_player}) is thinking...")
            game_state = convert_to_9x9(big_board)
            next_board_row, next_board_col = check_smallboard(big_board, next_board_row, next_board_col)
            if (next_board_row == None) and (next_board_col == None):
                ai_move = ai.get_best_move(game_state, None)
            else:
                ai_move = ai.get_best_move(game_state, (next_board_row, next_board_col))
            board_row, board_col, move_row, move_col = apply_ai_move(big_board, ai_move, current_player)
            print(f"AI ({current_player}) played at big board ({board_row}, {board_col}), small board ({move_row}, {move_col}).")

        big_board.check_winner()
        next_board_row = move_row
        next_board_col = move_col
        current_player = 'O' if current_player == 'X' else 'X'
    
    if run_gui:
    # Starting Page
        button1_rect, button2_rect = starting_page(screen)
        algo_dec = None

        while algo_dec is None:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if button1_rect.collidepoint(event.pos):
                        ai = UltimateTicTacToeAI(max_depth=3)
                        algo_dec = True
                    elif button2_rect.collidepoint(event.pos):
                        ai = MonteCarloAI(simulations=100)
                        algo_dec = True
    #gui
    run_gui = True
    while run_gui:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run_gui = False

            if event.type == pygame.MOUSEBUTTONDOWN and player_types[current_player] == 'Human':
                next_board_row, next_board_col = check_smallboard(big_board, next_board_row, next_board_col)
                # Handle human move
                cell_row, cell_col = get_cell(event.pos)
                board_row, board_col = cell_row // 3, cell_col // 3
                move_row, move_col = cell_row % 3, cell_col % 3
                small_board = big_board.boards[board_row][board_col]

                # Check if the move is valid
                if (next_board_row is None or (board_row, board_col) == (next_board_row, next_board_col)) \
                        and small_board.make_move(move_row, move_col, current_player):
                    # Update game state
                    subtitle = f"Player {current_player} played in box ({board_row}, {board_col})."
                    big_board.check_winner()
                    next_board_row, next_board_col = move_row, move_col
                    current_player = 'O' if current_player == 'X' else 'X'
                else:
                    subtitle = "Invalid move! You must play in the correct box."

        # AI's move
        if player_types[current_player] == 'AI' and run_gui:
            game_state = convert_to_9x9(big_board)
            next_board_row, next_board_col = check_smallboard(big_board, next_board_row, next_board_col)
            if next_board_row is None and next_board_col is None:
                ai_move = ai.get_best_move(game_state, None)
            else:
                ai_move = ai.get_best_move(game_state, (next_board_row, next_board_col))
            apply_ai_move(big_board, ai_move, current_player)
            subtitle = f"AI ({current_player}) played in box ({ai_move[0] // 3}, {ai_move[1] // 3})."
            big_board.check_winner()
            next_board_row, next_board_col = ai_move[0] % 3, ai_move[1] % 3
            subtitle = f"Next should play in box ({ai_move[0] % 3}, {ai_move[1] % 3})."
            current_player = 'O' if current_player == 'X' else 'X'
        

        # Draw the board and update the display
        draw_board(screen, big_board)
        font = pygame.font.Font(None, 30)
        pygame.draw.rect(screen, (200, 200, 200), pygame.Rect(0, 600, 600, 50))
        subtitle_text = font.render(subtitle, True, (0, 0, 0))
        screen.blit(subtitle_text, (10, 610))
        pygame.display.flip()

        # Check for winner
        if big_board.winner:
            show_winner(screen, big_board.winner)
            subtitle = f"Player {big_board.winner} wins the game!"
            run_gui = False

        # Check for draw
        if big_board.is_full():
            show_draw(screen)
            run_gui = False

    pygame.quit()

if __name__ == "__main__":
    main()