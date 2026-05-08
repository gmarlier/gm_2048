import logging
from copy import deepcopy
from enum import Enum
import math
from random import choice, randint, sample

MESSAGE_PROMPT = "Enter your next move on numerical keypad UP(8), RIGHT(6), DOWN(2), LEFT(4), AI(5) "
MESSAGE_AI = "AI is suggesting this move:"
MESSAGE_NEW_GAME = "New random game launched !"
ERROR_KEYPRESSED = "Key pressed not accepted !"
MESSAGE_WIN = "You win !"
MESSAGE_LOSE = "You lose !"

class Action(Enum):
    UP = '8'
    RIGHT = '6'
    DOWN = '2'
    LEFT = '4'
    AI = '5'

class GridException(Exception):
    pass

def left_move(grid: list[list[int]]) -> tuple[list[list[int]], bool]:
    '''
                 move
    [1    2]   [1  2  ]
    [     3]   [3     ]
    [     4]   [4     ]
    '''
    next_grid = move_matrix(grid)
    return next_grid, next_grid != grid

def right_move(grid: list[list[int]]) -> list[list[int]]:
    '''
                flip          move         flip
    [1    2]   [2     1]    [2  1  ]    [   1  2]
    [3  4  ]   [   4  3]    [4  3  ]    [   3  4]
    [6  5  ]   [   5  6]    [5  6  ]    [   6  5]
    '''
    next_grid = flip_matrix(grid)
    next_grid = move_matrix(next_grid)
    next_grid = flip_matrix(next_grid)
    return next_grid,  next_grid != grid

def up_move(grid: list[list[int]]) -> list[list[int]]:
    '''
           -> trans. ->  move  ->  trans.
    [    3]   [   1]    [1   ]    [1 2 3]
    [1 2 6]   [   2]    [2   ]    [    6]
              [3  6]    [3  6]    
    '''
    next_grid = transpose_matrix(grid)
    next_grid = move_matrix(next_grid)
    next_grid = transpose_matrix(next_grid)
    return next_grid, next_grid != grid

def down_move(grid: list[list[int]]) -> list[list[int]]:
    '''
              trans.     flip      move     flip      trans.
    [1 2 3]   [1   ]    [   1]    [1   ]    [   1]    [    3]
    [    6]   [2   ]    [   2]    [2   ]    [   2]    [1 2 6]
              [3  6]    [6  3]    [6  3]    [3  6]
    '''
    next_grid = transpose_matrix(grid)
    next_grid = flip_matrix(next_grid)
    next_grid = move_matrix(next_grid)
    next_grid = flip_matrix(next_grid)
    next_grid = transpose_matrix(next_grid)
    return next_grid, next_grid != grid

def transpose_matrix(grid: list[list[int]]) -> list[list[int]]:
    return [list(row) for row in zip(*grid)]

def flip_matrix(grid: list[list[int]]) -> list[list[int]]:
    return [row[::-1] for row in grid]

def move_matrix(grid: list[list[int]]) -> list[list[int]]:
    return [compress(merge(compress(row))) for row in grid]

def compress(row: list[int]) -> list[int]:

    write_index = 0
    read_index = 0
    new_row = [None] * len(row)
    while read_index < len(row):
        if row[read_index]:
            new_row[write_index] = row[read_index]
            write_index += 1
        read_index += 1
    return new_row

def merge(row: list[int]) -> list[int]:
    new_row = row.copy()
    index = 0
    while index < len(row)-1:
        if row[index + 1] == row[index] and row[index]:
            new_row[index] = row[index + 1] + row[index]
            new_row[index + 1] = None
            index += 1
        index += 1
    return new_row

def print_pretty(grid: list[list[int]], message=None):
    repr = ''
    for row in grid:
        for value in row:
            repr += f'{value or '.':^2} '
        repr += '\n'
    print(repr)
    print(message)

def random_grid(rows, columns, init=2) -> list[list[int]]:
    
    assert rows > 0, columns > 0
    assert init > 0
    
    grid = [[None for _ in range(columns)] for _ in range(rows)]
    size_grid = rows * columns

    # choose the number of 2s to initialize the grid
    number_of_twos = randint(1, size_grid)

    # choose distinct tiles to assign those 2s
    tiles = [(row, col) for row in range(rows) for col in range(columns)]
    for (row, col) in sample(tiles, number_of_twos):
        grid[row][col] = init

    return grid

def empty_tiles(grid):
    '''
        return a list of empty tiles in the current grid
    '''
    rows = len(grid)
    cols = len(grid[0])
    return [(row, col) for row in range(rows) for col in range(cols) if grid[row][col] is None]

def add_new_tile(grid, row, col, value):
    new_grid = deepcopy(grid)
    new_grid[row][col] = value
    return new_grid

def select_random_tile(tiles: list, authorized_values: list[int]):
    if tiles and authorized_values:
        return choice(tiles), choice(authorized_values)
    

def add_random_tile(grid: list[list[int]], authorized_values=list[int]):
    '''
        insert a new value in the grid
    '''
    new_grid = deepcopy(grid)
    if tile := select_random_tile(empty_tiles(grid), authorized_values):
        (row, col), val = tile
        new_grid[row][col] = val
        logging.debug(f'new value={val} inserted at (row, col)=({row}, {col})')
    return new_grid

def grid_contains(grid, value=2048) -> bool:
    for row in grid:
        if value in row:
            return True
    return False

def cannot_change(grid) -> bool:
    '''
        True if no move can change the current board
    '''
    for _, changed in left_move(grid), right_move(grid), up_move(grid), down_move(grid):
        if changed:
            return False
    return True

def move_generator(board):
       
    actions = {
            Action.UP: up_move,
            Action.RIGHT: right_move,
            Action.LEFT: left_move,
            Action.DOWN: down_move,
        }
    for action in actions.keys():
        tmp_board, _ = actions[action](board)
        yield tmp_board, action

def spawn_generator(board):
    #Change here proba
    probability_random_value = 1
    tiles = empty_tiles(board)
    for (row, col) in tiles:
        for value in [2]:
            tmp_board = deepcopy(board)
            tmp_board[row][col] = value
            yield tmp_board, probability_random_value

def sum_square(grid) -> int:
    if cannot_change(grid):
        return -float("inf")
    return sum(sum(val * val for val in row if val) for row in grid)

def fitness_snake_like_pattern(grid) -> int:
    
    """
    Returns the heuristic value of b
     Snake refers to the "snake line pattern" (http://tinyurl.com/l9bstk6)
    Here we only evaluate one direction; we award more points if high valued tiles
    occur along this path. We penalize the board for not having
    the highest valued tile in the lower left corner
    """
    if cannot_change(grid):
        return -float("inf")
    
    snake = []
    for i, col in enumerate(zip(*grid)):
        snake.extend(reversed(col) if i % 2 == 0 else col)

    m = max(snake)

    return sum(x/10**n for n, x in enumerate(snake)) - \
           math.pow((grid[len(grid) - 1][0] != m)*abs(grid[len(grid) - 1][0] - m), 2)