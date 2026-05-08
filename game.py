from ai import AbstractAI, Expectimax
from grid import down_move, empty_tiles, left_move, move_generator, random_grid, right_move, spawn_generator, sum_square, up_move
from grid import add_random_tile, grid_contains, cannot_change
from grid import Action, MESSAGE_WIN, MESSAGE_LOSE

def game_win(grid: list[list[int]]):
    '''
        players wins when the board contains the default value 2048
    '''
    return grid_contains(grid, value=2048)

def game_lose(grid):
    return cannot_change(grid)

def game_over(grid):
    return game_win(grid) or game_lose(grid)

def game_init(rows: int, cols: int, init: int, depth: int):

    grid = random_grid(rows, cols , init)
    
    # Instantiate ai model
    ai_model = Expectimax(depth, move_generator, spawn_generator, game_over=game_over, fitness=sum_square)

     # Configure game actions
    controllers = {
         Action.UP : up_move,
         Action.DOWN : down_move,
         Action.RIGHT: right_move,
         Action.LEFT: left_move,
    }

    return grid, controllers, ai_model


def game_controller(action: str, grid: list[list[int]], controllers, ai_model: AbstractAI):
    
    message = ''

    # User requesting AI Suggestion
    if action == Action.AI:
        best_move = ai_model.best_move(grid)
        return grid, best_move
    
    # Trigger end user move
    grid, _  = controllers[action](grid)
    
    # Next action user could spawn a 2048
    if game_win(grid):
        return grid, MESSAGE_WIN
    
    # Otherwise, check if a tile can be spawn
    if len(empty_tiles(grid)) > 0:
        grid = add_random_tile(grid, authorized_values=[2, 4])
    
    # should be checked after spawning a new tile
    if game_lose(grid):
        return grid, MESSAGE_LOSE
    
    return grid, message