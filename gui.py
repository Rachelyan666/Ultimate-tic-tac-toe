import pygame
from board import BigBoard

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 600, 600
GRID_COLOR = (200, 200, 200)
FONT_COLOR = (0, 0, 0)
BG_COLOR = (255, 255, 255)
LINE_WIDTH = 5
CELL_SIZE = SCREEN_WIDTH // 9

pygame.init()
FONT = pygame.font.Font(None, 40)

def draw_board(screen, big_board):
    """
    Draws the BigBoard and its SmallBoards on the screen.
    """
    screen.fill(BG_COLOR)

    # Draw grid lines
    for i in range(1, 9):
        line_width = LINE_WIDTH if i % 3 == 0 else 2
        pygame.draw.line(screen, GRID_COLOR, (i * CELL_SIZE, 0), (i * CELL_SIZE, SCREEN_HEIGHT), line_width)
        pygame.draw.line(screen, GRID_COLOR, (0, i * CELL_SIZE), (SCREEN_WIDTH, i * CELL_SIZE), line_width)

    # Draw symbols
    boards = big_board.boards
    for small_row in range(3):
        for small_col in range(3):
            small_board = boards[small_row][small_col]
            for cell_row in range(3):
                for cell_col in range(3):
                    cell_value = small_board.grid[cell_row][cell_col]
                    if cell_value != ' ':
                        center_x = (small_col * 3 + cell_col + 0.5) * CELL_SIZE
                        center_y = (small_row * 3 + cell_row + 0.5) * CELL_SIZE
                        text = FONT.render(cell_value, True, FONT_COLOR)
                        screen.blit(text, text.get_rect(center=(center_x, center_y)))

def get_cell(pos):
    """
    Converts mouse position to board and cell coordinates.
    """
    x, y = pos
    return y // CELL_SIZE, x // CELL_SIZE

def show_winner(screen, winner):
    """
    Displays the winner on the screen.
    """
    screen.fill(BG_COLOR)
    text = FONT.render(f"Player {winner} wins!", True, FONT_COLOR)
    screen.blit(text, text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)))
    pygame.display.flip()
    pygame.time.wait(3000)

def show_draw(screen):
    """
    Displays the winner on the screen.
    """
    text = FONT.render("It's a draw!", True, FONT_COLOR)
    screen.blit(text, text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)))
    pygame.display.flip()
    pygame.time.wait(3000)

def starting_page(screen):
    """
    draws the starting page choosing the algorithms
    """
    screen.fill((255, 255, 255))
    font = pygame.font.Font(None, 50)

    # Button 1: Minimax
    button1_rect = pygame.Rect(200, 200, 200, 50)
    pygame.draw.rect(screen, (0, 0, 255), button1_rect)
    text1 = font.render("Minimax", True, (255, 255, 255))
    screen.blit(text1, text1.get_rect(center=button1_rect.center))

    # Button 2: Monte Carlo
    button2_rect = pygame.Rect(200, 300, 200, 50)
    pygame.draw.rect(screen, (0, 255, 0), button2_rect)
    text2 = font.render("Monte Carlo", True, (255, 255, 255))
    screen.blit(text2, text2.get_rect(center=button2_rect.center))

    pygame.display.flip()
    return button1_rect, button2_rect
