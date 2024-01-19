"""
Minesweeper Game

This module implements a Minesweeper game using the Pygame library, board generation from board.py and configs from configs.py.

"""

import pygame
import sys
import board
from configs import *

# Pygame initialization
pygame.init()
pygame.display.set_caption("Minesweeper")
font = pygame.font.Font(None, 25)

# Load images
empty_image = pygame.image.load(GRID_CELL_PATH)
smiley_image = pygame.image.load(SMILEY_CELL_PATH)
plus_image = pygame.image.load("cell_types/plus.png")
minus_image = pygame.image.load("cell_types/minus.png")

# Game state variables
game_is_running = True
game_won = False
game_lost = False

# Game parameters
ROWS = 6
COLS = 10
MINES = 10
WIDTH, HEIGHT = (COLS + 2) * BUTTON_SIZE, (ROWS + 5) * BUTTON_SIZE
TIME_LIMIT = ROWS * COLS + 3 * MINES

# User input parameters
height_input = ROWS
width_input = COLS
mines_input = MINES

# Game initialization
button_matrix = [[(col * BUTTON_SIZE, row * BUTTON_SIZE) for col in range(1, width_input + 1)] for row in range(4, height_input + 4)]
grid = board.create_grid(width_input, height_input, mines_input)
path_matrix = [[GRID_CELL_PATH for _ in range(width_input)] for _ in range(height_input)]


def get_cell_path(cell):
    """
    Returns the file path for the given cell.

    Parameters:
    - cell: The value of the cell in the Minesweeper grid.

    Returns:
    - str: File path of the corresponding image for the cell.
    """
    path = "cell_types/"
    if cell == 0:
        path += "empty.png"
    elif cell == 'x':
        path += "mine_click.png"
    else:
        path += str(cell) + ".png"
    return path


def reveal_cells(row, col, path_matrix):
    """
    Recursively reveals neighboring cells.

    Parameters:
    - row (int): Row index of the clicked cell.
    - col (int): Column index of the clicked cell.
    - path_matrix (list): Matrix representing the state of revealed cells.

    Returns:
    - list: Updated path_matrix after revealing cells.
    """
    for i in range(max(0, row - 1), min(row + 2, ROWS)):
        for j in range(max(0, col - 1), min(col + 2, COLS)):
            if grid[i][j] == 0 and path_matrix[i][j] != EMPTY_CELL_PATH:
                path_matrix[i][j] = EMPTY_CELL_PATH
                reveal_cells(i, j, path_matrix)
            elif grid[i][j] != 'x':
                path_matrix[i][j] = get_cell_path(grid[i][j])
    return path_matrix


def end_game(path_matrix):
    """
    Reveals all mines and flags in case of game over.

    Parameters:
    - path_matrix (list): Matrix representing the state of revealed cells.

    Returns:
    - list: Updated path_matrix after revealing mines and flags.
    """
    for i in range(ROWS):
        for j in range(COLS):
            if path_matrix[i][j] == GRID_CELL_PATH and grid[i][j] == 'x':
                path_matrix[i][j] = MINE_PATH
            elif path_matrix[i][j] == FLAG_CELL_PATH and grid[i][j] != 'x':
                path_matrix[i][j] = WRONG_FLAG_PATH
    return path_matrix


def restart_game():
    """
    Restarts the game with the specified user inputs.
    """
    global grid, path_matrix, width_input, height_input, button_matrix, ROWS, COLS, MINES, WIDTH, HEIGHT

    ROWS = height_input
    COLS = width_input
    MINES = mines_input

    button_matrix = [[(col * BUTTON_SIZE, row * BUTTON_SIZE) for col in range(1, width_input + 1)] for row in
                     range(4, height_input + 4)]
    grid = board.create_grid(width_input, height_input, mines_input)
    path_matrix = [[GRID_CELL_PATH for _ in range(width_input)] for _ in range(height_input)]

    HEIGHT, WIDTH = (height_input + 5) * BUTTON_SIZE, (width_input + 2) * BUTTON_SIZE
    HEIGHT = max((6 + 5) * BUTTON_SIZE, HEIGHT)
    WIDTH = max((10 + 2) * BUTTON_SIZE, WIDTH)

    pygame.display.set_mode((WIDTH, HEIGHT))


# Pygame screen and clock initialization
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
start_time = pygame.time.get_ticks()
bomb_count = MINES

# Main game loop
while True:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Restart button
            smiley_x = (WIDTH - BUTTON_SIZE) // 2
            if event.button == 1 and smiley_x < event.pos[0] < smiley_x + BUTTON_SIZE and 10 < event.pos[1] < 10 + BUTTON_SIZE:
                restart_game()
                start_time = pygame.time.get_ticks()
                game_is_running = True
                game_won = False
                game_lost = False
                smiley_x = (WIDTH - BUTTON_SIZE) // 2
                TIME_LIMIT = ROWS * COLS + 3 * MINES
                bomb_count = MINES
            #  Buttons for adjusting parameters
            elif event.button == 1 and 110 < event.pos[0] < 110 + minus_image.get_width():
                if 10 < event.pos[1] < 10 + minus_image.get_height():
                    width_input = max(width_input - 1, 2)
                    mines_input = min(mines_input, width_input * height_input - 1)
                elif 35 < event.pos[1] < 35 + minus_image.get_height():
                    height_input = max(height_input - 1, 2)
                    mines_input = min(mines_input, width_input * height_input - 1)
                elif 60 < event.pos[1] < 60 + minus_image.get_height():
                    mines_input = max(mines_input - 1, 1)
            elif event.button == 1 and 110 + minus_image.get_width() < event.pos[0] < 110 + 2 * minus_image.get_width():
                if 10 < event.pos[1] < 10 + plus_image.get_height():
                    width_input = min(width_input + 1, MAX_WIDTH)
                elif 35 < event.pos[1] < 35 + plus_image.get_height():
                    height_input = min(height_input + 1, MAX_HEIGHT)
                elif 60 < event.pos[1] < 60 + plus_image.get_height():
                    mines_input = min(mines_input + 1, width_input*height_input - 1)
            # Handling clicks on game cells
            if game_is_running:
                for row in range(ROWS):
                    for col in range(COLS):
                        x, y = button_matrix[row][col]
                        if x < event.pos[0] < x + BUTTON_SIZE and y < event.pos[1] < y + BUTTON_SIZE:
                            if event.button == 1 and path_matrix[row][col] != FLAG_CELL_PATH:
                                path = get_cell_path(grid[row][col])
                                path_matrix[row][col] = path
                                if grid[row][col] == 0:
                                    path_matrix = reveal_cells(row, col, path_matrix)
                                elif grid[row][col] == 'x':
                                    path_matrix = end_game(path_matrix)
                                    game_lost = True
                                    game_is_running = False
                            elif event.button == 3:
                                if path_matrix[row][col] == GRID_CELL_PATH:
                                    path_matrix[row][col] = FLAG_CELL_PATH
                                    bomb_count -= 1
                                elif path_matrix[row][col] == FLAG_CELL_PATH:
                                    path_matrix[row][col] = GRID_CELL_PATH
                                    bomb_count += 1

    # Game logic and rendering
    elapsed_time = (pygame.time.get_ticks() - start_time) // 1000
    timer = max(TIME_LIMIT - elapsed_time, 0)

    screen.fill(GREY)

    # Display restart button
    screen.blit(smiley_image, ((WIDTH - BUTTON_SIZE) // 2, 10))

    # Display user input parameters
    width_text = font.render(f"width:  {width_input}", True, WHITE)
    height_text = font.render(f"height: {height_input}", True, WHITE)
    mines_text = font.render(f"mines: {mines_input}", True, WHITE)

    screen.blit(width_text, (10, 15))
    screen.blit(height_text, (10, 40))
    screen.blit(mines_text, (10, 65))

    # Display buttons for adjusting parameters
    screen.blit(minus_image, (110, 10))
    screen.blit(plus_image, (110 + minus_image.get_width(), 10))
    screen.blit(minus_image, (110, 35))
    screen.blit(plus_image, (110 + minus_image.get_width(), 35))
    screen.blit(minus_image, (110, 60))
    screen.blit(plus_image, (110 + minus_image.get_width(), 60))

    # Display Minesweeper grid cells
    grid_cell_counter = 0
    for row in range(ROWS):
        for col in range(COLS):
            if path_matrix[row][col] == GRID_CELL_PATH:
                grid_cell_counter += 1
            image = pygame.image.load(path_matrix[row][col])
            screen.blit(image, ((col + 1) * BUTTON_SIZE, (row + 4) * BUTTON_SIZE))

    # Check if the game is won
    if grid_cell_counter == 0 and bomb_count == 0:
        game_is_running = False
        game_won = True

    # Display bomb count and timer
    bomb_text = font.render(f"mines: {bomb_count}", True, WHITE)
    timer_text = font.render(f"time left: {timer}", True, WHITE)
    screen.blit(bomb_text, (10, HEIGHT - 25))
    if game_is_running:
        screen.blit(timer_text, (WIDTH - timer_text.get_width() - 10, HEIGHT - 25))

    # Display game over messages
    if timer == 0 and not game_won and not game_lost:
        game_is_running = False
        popup_text = font.render("Time's up! You lost!", True, RED)
        screen.blit(popup_text, ((WIDTH - popup_text.get_width()) // 2, 100))
    elif game_won:
        popup_text = font.render("Congratulations! You won!", True, GREEN)
        screen.blit(popup_text, ((WIDTH - popup_text.get_width()) // 2, 100))
    elif game_lost:
        popup_text = font.render("Mine clicked! You lost!", True, RED)
        screen.blit(popup_text, ((WIDTH - popup_text.get_width()) // 2, 100))

    pygame.display.flip()
    clock.tick(30)
