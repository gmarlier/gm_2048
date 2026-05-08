import argparse
import logging

from game import game_init, game_controller
from grid import print_pretty
from grid import Action, MESSAGE_PROMPT,ERROR_KEYPRESSED

if __name__ == '__main__':

    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s [%(levelname)s] %(message)s")

    # Configure board size in command line
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--rows", type=int, default=4, help="number of rows, must be > 0")
    parser.add_argument("-c", "--cols", type=int, default=4, help="number of columns, must be > 0")
    parser.add_argument("-i", "--init", type=int, default=2, help="initial number, must be > 0")
    parser.add_argument("-d", "--depth", type=int, default=5, help="maximum depth of best move search, default is 5")
    args = parser.parse_args()

    grid, controllers, ai_model = game_init(args.rows, args.cols, args.init, args.depth)
    
    print_pretty(grid)

    # Run the main controller as standalone game
    while key_pressed := input(MESSAGE_PROMPT):
        try:
            action = Action(key_pressed)
        except Exception:
            print(ERROR_KEYPRESSED)
        else:
            grid, message = game_controller(action, grid, controllers, ai_model)
            print_pretty(grid, message)
            
            
            

                



        




