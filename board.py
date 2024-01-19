"""
Minesweeper Grid Generator

This module provides functions to generate Minesweeper grids with mines placed randomly.

"""

import random


def place_mines(grid, cols, rows, mines):
    """
    Randomly places mines on the Minesweeper grid.

    Parameters:
    - grid (list): The Minesweeper grid represented as a 2D list.
    - cols (int): Number of columns in the grid.
    - rows (int): Number of rows in the grid.
    - mines (int): Number of mines to be placed on the grid.

    Returns:
    - list: Updated Minesweeper grid with mines placed.
    """
    for _ in range(mines):
        row = random.randint(0, rows - 1)
        col = random.randint(0, cols - 1)

        while grid[row][col] == 'x':
            row = random.randint(0, rows - 1)
            col = random.randint(0, cols - 1)

        grid[row][col] = 'x'

    return grid


def mark_neighbours(grid, rows, cols):
    """
    Marks the number of adjacent mines for each cell in the Minesweeper grid.

    Parameters:
    - grid (list): The Minesweeper grid represented as a 2D list.
    - rows (int): Number of rows in the grid.
    - cols (int): Number of columns in the grid.

    Returns:
    - list: Updated Minesweeper grid with numbers indicating adjacent mines.
    """
    for row in range(rows):
        for col in range(cols):
            if grid[row][col] == 'x':
                for i in range(max(0, row - 1), min(row + 2, rows)):
                    for j in range(max(0, col - 1), min(col + 2, cols)):
                        if grid[i][j] != 'x':
                            grid[i][j] += 1
    return grid


def create_grid(cols, rows, mines):
    """
    Creates a Minesweeper grid with the specified dimensions and number of mines.

    Parameters:
    - cols (int): Number of columns in the grid.
    - rows (int): Number of rows in the grid.
    - mines (int): Number of mines to be placed on the grid.

    Returns:
    - list: Minesweeper grid with mines and numbers indicating adjacent mines.
    """
    grid = [[0 for _ in range(cols)] for _ in range(rows)]
    grid = place_mines(grid, cols, rows, mines)
    grid = mark_neighbours(grid, rows, cols)
    return grid
