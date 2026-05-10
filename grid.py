"""module to manage common operations on a game board

Available functions:
- left_move: determine a new board after a left move
- right_move: determine a new board after a right move
- up_move: determine a new board after a up move
- down_move: determine a new board after a down move
- transpose_matrix: execute the mathematical transposition of a board game
- flip_matrix: execute the mathematical horizontal reverse of a board game
- move_matrix: execute the compression, merging and re-compression of all rows horizontally and to the left
- compress: removing empty slots in the board by moving horizontally elements from the right to the left
- merge: add any 2 consecutive and equal elements in the board by starting from the right elements to the left
- print_pretty: provides a user friendly view of the board when you launch the game in command line
- random_grid: generates a random board
- empty_tiles: return a list of available tiles without value
- grid_contains: check if the board contains at least a specific value
- cannot_change: check if any move can change the state of the current board
- move_generator: provides a generator to iterate though all possible player move and board
- spawn_generator: provides a generator to iterate though all possible random spawn tile of a board.
- sum_square: determine the score of the current board, used as a fitness function for ai decision

"""

from copy import deepcopy
from enum import Enum
import math
from random import randint, sample


class Action(Enum):
    """
    Enum type to list all player moves applicable to a board
    """

    UP = "8"
    RIGHT = "6"
    DOWN = "2"
    LEFT = "4"
    AI = "5"


def left_move(grid: list[list[int]]) -> tuple[list[list[int]], bool]:
    """Determine a new board after a left move as described hereunder:
                 move
    [1    2]   [1  2  ]
    [     3]   [3     ]
    [     4]   [4     ]

    Args:
        grid: list of list of integers

    Returns:
        tuple including the modified grid and a boolean to indicate if the grid has changed

    """
    next_grid = move_matrix(grid)
    return next_grid, next_grid != grid


def right_move(grid: list[list[int]]) -> tuple[list[list[int]], bool]:
    """Determine a new board after a right move as described hereunder:
                flip          move         flip
    [1    2]   [2     1]    [2  1  ]    [   1  2]
    [3  4  ]   [   4  3]    [4  3  ]    [   3  4]
    [6  5  ]   [   5  6]    [5  6  ]    [   6  5]

    Args:
        grid: list of list of integers

    Returns:
        tuple including the modified grid and a boolean to indicate if the grid has changed

    """
    next_grid = flip_matrix(grid)
    next_grid = move_matrix(next_grid)
    next_grid = flip_matrix(next_grid)
    return next_grid, next_grid != grid


def up_move(grid: list[list[int]]) -> tuple[list[list[int]], bool]:
    """Determine a new board after a up move as described hereunder:
           -> trans. ->  move  ->  trans.
    [    3]   [   1]    [1   ]    [1 2 3]
    [1 2 6]   [   2]    [2   ]    [    6]
              [3  6]    [3  6]
    Args:
        grid: list of list of integers

    Returns:
        tuple including the modified grid and a boolean to indicate if the grid has changed

    """
    next_grid = transpose_matrix(grid)
    next_grid = move_matrix(next_grid)
    next_grid = transpose_matrix(next_grid)
    return next_grid, next_grid != grid


def down_move(grid: list[list[int]]) -> tuple[list[list[int]], bool]:
    """Determine a new board after a down move as described hereunder:
              trans.     flip      move     flip      trans.
    [1 2 3]   [1   ]    [   1]    [1   ]    [   1]    [    3]
    [    6]   [2   ]    [   2]    [2   ]    [   2]    [1 2 6]
              [3  6]    [6  3]    [6  3]    [3  6]
    Args:
        grid: list of list of integers

    Returns:
        tuple including the modified grid and a boolean to indicate if the grid has changed

    """
    next_grid = transpose_matrix(grid)
    next_grid = flip_matrix(next_grid)
    next_grid = move_matrix(next_grid)
    next_grid = flip_matrix(next_grid)
    next_grid = transpose_matrix(next_grid)
    return next_grid, next_grid != grid


def transpose_matrix(grid: list[list[int]]) -> list[list[int]]:
    """transform the current grid into a new grid (cloned) where rows, and columns are swapped.
       Example:
       grid     new grid
    [1 2 3]      [1   ]
    [    6]      [2   ]
                 [3  6]

    Args:
        grid as the game board

    Returns:
        the new grid transposed

    """
    return [list(row) for row in zip(*grid)]


def flip_matrix(grid: list[list[int]]) -> list[list[int]]:
    """transform the current grid into a new grid (cloned) where all rows are reversed.
       Example:
       grid      new grid
    [1 2 3]      [3 2 1]
    [    6]      [6   ]

    Args:
        grid as the game board

    Returns:
        the new grid flipped

    """

    return [row[::-1] for row in grid]


def move_matrix(grid: list[list[int]]) -> list[list[int]]:
    """compress, merge and compress again the current grid
    Example:
      grid     compressed    merged    compressed
    [2 2 4]     [2 2 4]     [4 . 4]    [4 4 .]
    [2 . 2]     [2 2 .]     [4 . .]    [4 . .]

    Args:
        grid as the game board

    Returns:
        the new grid moved
    """
    return [compress(merge(compress(row))) for row in grid]


def compress(row: list[int]) -> list[int]:
    """removing empty slots of the current row by moving its non null elements from the right
        to the left
    Example:
       current row      new row
       [. 2 . 4 .]     [2 4 . . .]

    Args:
        current row to compress

    Returns:
        a new row compressed
    """

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
    """add any 2 consecutive and equal elements in the board by starting from the right elements to the left
    Example:
       current row      new row
       [. 2 2 8 8]     [. 4 . 16 .]

    Args:
        current row to merge

    Returns:
        a new row merged
    """

    new_row = row.copy()
    index = 0
    while index < len(row) - 1:
        if row[index + 1] == row[index] and row[index]:
            new_row[index] = row[index + 1] + row[index]
            new_row[index + 1] = None
            index += 1
        index += 1
    return new_row


def print_pretty(grid: list[list[int]], message=None):
    """user friendly representation of a board when the game is in command line

    Args:
        grid: the current board
        message: optional message to display
    """
    repr = ""
    for row in grid:
        for value in row:
            repr += f"{value or '.':^4} "
        repr += "\n"
    print(repr)
    print(message)


def random_grid(rows, columns, init=2) -> list[list[int]]:
    """generates a grid of size (rows * columns) with a random number of tiles
    initialized with init value

    Args:
        rows: number of rows
        columns: number of columns
        init: value to initialize some of board tiles, default value is 2

    Returns:
        a new initialized board
    """

    assert rows > 0, columns > 0
    assert init > 0

    grid = [[None for _ in range(columns)] for _ in range(rows)]
    size_grid = rows * columns

    # choose the number of 2s to initialize the grid
    number_of_twos = randint(1, size_grid)

    # choose distinct tiles to assign those 2s
    tiles = [(row, col) for row in range(rows) for col in range(columns)]
    for row, col in sample(tiles, number_of_twos):
        grid[row][col] = init

    return grid


def empty_tiles(grid) -> list[tuple[int, int]]:
    """
    return a list of empty tiles in the current grid

    Args:
        grid: current board

    Returns:
        a list of tuples (row, colum)

    """
    rows = len(grid)
    cols = len(grid[0])
    return [
        (row, col)
        for row in range(rows)
        for col in range(cols)
        if grid[row][col] is None
    ]


def grid_contains(grid: list[list[int]], value: int) -> bool:
    """determines if the current board contains a specific value

    Args:
        grid: current board

    Returns:
        True if value is included, False otherwise

    """
    for row in grid:
        if value in row:
            return True
    return False


def cannot_change(grid: list[list[int]]) -> bool:
    """
    True if no move can change the current board
    (Although the method is not optimal, we try to keep the code as readable as possible.)

    Args:
        grid: current board

    Returns:
        True if any move can change the board, otherwise False

    """
    for _, changed in left_move(grid), right_move(grid), up_move(grid), down_move(grid):
        if changed:
            return False
    return True


def move_generator(board: list[list[int]]):
    """a generator to iterate though all player moves. Used to hide move logic in the decision search algo

    Args:
        board: the current board

    Returns:
        yield the new board along with the corresponding move applied

    """
    actions = {
        Action.UP: up_move,
        Action.RIGHT: right_move,
        Action.LEFT: left_move,
        Action.DOWN: down_move,
    }
    for action in actions.keys():
        tmp_board, _ = actions[action](board)
        yield tmp_board, action


def spawn_generator(board: list[list[int]]):
    """a generator to iterate though all possible random state of a
       current board, while spawning a new tile with 2 possible values
       (with equi-probability). Used to hide spawning logic in the
       decision search algo

    Args:
        board: the current board

    Returns:
        yield a new board including the new spawn tile and the corresponding probability

    """

    probability_random_value = 0.5
    tiles = empty_tiles(board)
    for row, col in tiles:
        for value in [2, 4]:
            tmp_board = deepcopy(board)
            tmp_board[row][col] = value
            yield tmp_board, probability_random_value


def sum_square(grid: list[list[int]]) -> int:
    """to provide an estimate of board total points. Used a fitness function for ai decision search

    Args:
        board: the current board

    Returns:
        score of the current board

    """
    if cannot_change(grid):
        return -float("inf")
    return sum(sum(val * val for val in row if val) for row in grid)


def fitness_snake_like_pattern(grid: list[list[int]]) -> int:
    """another fitness function using "snake line pattern" (http://tinyurl.com/l9bstk6)

    Args:
        board: the current board

    Returns:
        score of the current board

    """

    if cannot_change(grid):
        return -float("inf")

    snake = []
    for i, col in enumerate(zip(*grid)):
        snake.extend(reversed(col) if i % 2 == 0 else col)

    m = max(snake)

    return sum(x / 10**n for n, x in enumerate(snake)) - math.pow(
        (grid[len(grid) - 1][0] != m) * abs(grid[len(grid) - 1][0] - m), 2
    )
