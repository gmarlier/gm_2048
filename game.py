"""
Defines game workflow
"""

import logging
from copy import deepcopy
from random import choice
from typing import Tuple

from ai import AbstractAI, Expectimax
from grid import (
    down_move,
    empty_tiles,
    fitness_snake,
    left_move,
    move_generator,
    random_grid,
    right_move,
    spawn_generator,
    sum_square,
    up_move,
)
from grid import grid_contains, cannot_change
from grid import Action

MESSAGE_WIN = "You win !"
MESSAGE_LOSE = "You lose !"
ERROR_GAME_CONTROLLER = "Error in game controller"


def player_win(grid: list[list[int]], value=2048) -> bool:
    """the player wins if there is at least one value 2048 in the board

    Args:
        grid: data structure of the game state

    Returns:
        True if the player wins, False otherwise
    """
    return grid_contains(grid, value)


def player_lose(grid: list[list[int]], value=2048) -> bool:
    """The player loses if no 2048 tile exists and no further moves are possible

    Args:
        grid: current game state

    Returns:
        True if the player loses, False otherwise
    """
    # logging.info(f"player_lose {grid_contains(grid, value)} {cannot_change(grid)}")
    return grid_contains(grid, value) is False and cannot_change(grid)


def game_over(grid: list[list[int]]) -> bool:
    """the game is over if the player wins or lose

    Args:
        grid: current game board

    Returns:
        True if the current game is over, False otherwise
    """
    return player_win(grid) or player_lose(grid)


def random_tile(tiles: list[tuple[int, int]]) -> Tuple[int, int]:
    """select a random tile among the tiles board

    Args:
        grid: current game board

    Returns:
        return a random tile (row, col)
    """
    return choice(tiles)


def random_value(values: list[int]) -> int:
    """select a random value from values list

    Args:
        values: possible values

    Returns:
        return a random number
    """
    return choice(values)


def game_with_random_tile(
    grid: list[list[int]], authorized_values: list[int] = [2, 4]
) -> list[list[int]]:
    """Insert a new value in the grid. The method is stateless

    Args:
        grid: the current board
        authorized_values: the value that can be selected randomly

    Returns:
        a new grid with the new random tile added

    """
    new_grid = deepcopy(grid)
    if tiles := empty_tiles(grid):
        logging.debug(f"empty tile={tiles}")
        row, col = random_tile(tiles)
        new_grid[row][col] = random_value(authorized_values)
        logging.debug(f"random value={new_grid[row][col]} added here {(row, col)}")
    else:
        logging.warning(f"no random tile can be added")
    return new_grid


def game_init(
    rows: int, cols: int, init: int, depth: int
) -> tuple[list[list[int]], AbstractAI]:
    """initialize game with few parameters: board size, random initial number
        or maximum depth of ai search

    Args:
        rows: number of rows of game board
        cols: number of columns of game board
        init: number used to initialize a random board
        depth: maximum depth used to explore game combination

    Returns:
        un tuple of new board and instance of ai model
    """
    grid = random_grid(rows, cols, init)

    # Instantiate ai model
    ai_model = Expectimax(
        depth,
        move_generator,
        spawn_generator,
        endgame_condition=game_over,
        # fitness=sum_square,
        fitness=fitness_snake,
    )

    return grid, ai_model


def game_controller(
    action: str, grid: list[list[int]], ai_model: AbstractAI = None
) -> tuple[list[list[int]], str]:
    """
    this method defines the game workflow.
    This controller is shared between 2 modes: command line and web modes

    Args:
        action: user action identifier
        grid: current board
        ai_model: ai algo to select the best move

    Returns:
        a tuple with the new board state and eventual message
    """
    try:
        message = ""

        # User requesting AI Suggestion
        if action == Action.AI and ai_model:
            best_move = ai_model.best_move(grid)
            return grid, best_move

        # Trigger end user move
        controllers = {
            Action.UP: up_move,
            Action.DOWN: down_move,
            Action.RIGHT: right_move,
            Action.LEFT: left_move,
        }

        grid, changed = controllers[action](grid)

        # Next action user could spawn a 2048
        if player_win(grid):
            return grid, MESSAGE_WIN

        # we select a new random tile if game is modified
        if changed:
            grid = game_with_random_tile(grid)

        # should be checked after spawning a new tile
        if player_lose(grid) is True:
            return grid, MESSAGE_LOSE

        return grid, message

    except KeyError as exception:
        logging.error(ERROR_GAME_CONTROLLER, exception)
