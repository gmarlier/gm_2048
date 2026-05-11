"""
Implementation of the command line mode of 2048 game
"""

import argparse
import logging
import sys

from game import MESSAGE_LOSE, MESSAGE_WIN, game_init, game_controller
from grid import print_pretty
from grid import Action

MESSAGE_PROMPT = (
    "Enter your next move on numerical keypad UP(8), RIGHT(6), DOWN(2), LEFT(4), AI(5) "
)
ERROR_KEYPRESSED = "Key pressed not accepted !"

if __name__ == "__main__":

    # Configure board size in command line
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-r", "--rows", type=int, default=4, help="number of rows, must be > 0"
    )
    parser.add_argument(
        "-c", "--cols", type=int, default=4, help="number of columns, must be > 0"
    )
    parser.add_argument(
        "-i", "--init", type=int, default=2, help="initial number, must be > 0"
    )
    parser.add_argument(
        "-d",
        "--depth",
        type=int,
        default=3,
        help="maximum depth of best move search, default is 5",
    )
    parser.add_argument(
        "--debug",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        default="INFO",
        help="Set the debug level (default: INFO)",
    )

    args = parser.parse_args()

    # Configure logging based on the chosen level
    logging.basicConfig(level=getattr(logging, args.debug))
    logging.debug("Debugging enabled")
    logging.info("Starting program...")

    grid, ai_model = game_init(args.rows, args.cols, args.init, args.depth)

    print_pretty(grid)

    # Run the main controller as standalone game
    while key_pressed := input(MESSAGE_PROMPT):
        try:
            action = Action(key_pressed)
        except Exception:
            print(ERROR_KEYPRESSED)
        else:
            grid, message = game_controller(action, grid, ai_model)
            print_pretty(grid, message)
            if message in [MESSAGE_WIN, MESSAGE_LOSE]:
                sys.exit(0)
