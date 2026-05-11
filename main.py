"""
Implementation of the command line mode of 2048 game
"""

import keyboard
import argparse
import logging
import sys

from ai import AbstractAI
from game import MESSAGE_LOSE, MESSAGE_WIN, game_init, game_controller
from grid import pprint
from grid import Action

MESSAGE_PROMPT = (
    "Enter your next move on numerical keypad UP(8), RIGHT(6), DOWN(2), LEFT(4), AI(5) "
)
ERROR_KEYPRESSED = "Key pressed not accepted !"


def run_with_keyboard_detection(exp: bool, grid: list[list[int]], ai_model: AbstractAI):
    while True:
        print(MESSAGE_PROMPT)
        if exp:
            try:
                event = keyboard.read_event()
                if event.event_type == keyboard.KEY_DOWN and event.name.isdigit():
                    key_pressed = event.name
                print("\n")
            except ImportError:
                logging.warning(
                    "main should be launched with sudo, or do not use exp option"
                )
                sys.exit(0)
        else:
            key_pressed = input()
        try:
            action = Action(key_pressed)
        except Exception:
            print(ERROR_KEYPRESSED)
        else:
            grid, message = game_controller(action, grid, ai_model)
            pprint(grid, message)
            if message in [MESSAGE_WIN, MESSAGE_LOSE]:
                sys.exit(0)


if __name__ == "__main__":

    # Configure board size in command line
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-r",
        "--rows",
        type=int,
        metavar="",
        default=4,
        help="number of rows, must be > 0, default 4",
    )
    parser.add_argument(
        "-c",
        "--cols",
        type=int,
        metavar="",
        default=4,
        help="number of columns, must be > 0, default 4",
    )
    parser.add_argument(
        "-i",
        "--init",
        type=int,
        metavar="",
        default=2,
        help="initial number, must be > 0, default 2",
    )
    parser.add_argument(
        "-d",
        "--depth",
        metavar="",
        type=int,
        default=3,
        help="maximum depth of best move search, default is 3",
    )
    parser.add_argument(
        "-e",
        "--exp",
        action="store_true",
        help="the program will use direct event detection from keyboard (experimental), default is disable",
    )
    parser.add_argument(
        "--debug",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        default="INFO",
        help="Set the debug level, default: INFO",
    )

    args = parser.parse_args()

    # Configure logging based on the chosen level
    logging.basicConfig(level=getattr(logging, args.debug))
    logging.debug("Debugging enabled")
    logging.info("Starting program...")

    grid, ai_model = game_init(args.rows, args.cols, args.init, args.depth)
    pprint(grid)
    run_with_keyboard_detection(args.exp, grid, ai_model)
