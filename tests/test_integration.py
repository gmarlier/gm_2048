"""
Integration tests for ai + game module
"""

import logging

from unittest import TestCase
from unittest.mock import patch
from game import MESSAGE_WIN, game_over, game_controller
from grid import (
    Action,
    fitness_snake,
    move_generator,
    print_pretty,
    spawn_generator,
)
from ai import Expectimax


class IntegrationAITest(TestCase):

    def setUp(self):
        logging.basicConfig(
            level=logging.DEBUG, format="%(asctime)s [%(levelname)s] %(message)s"
        )
        self.ai_model = Expectimax(
            3,
            move_generator,
            spawn_generator,
            endgame_condition=game_over,
            fitness=fitness_snake,
        )

    def test_end_game_board(self):

        grid = [
            [2, 4, 2],
            [4, 2, 4],
            [2, 4, 2],
        ]

        new_grid = [
            [2, 4, 2],
            [4, 2, 4],
            [2, 4, 2],
        ]

        new_grid, message = game_controller(Action.AI, grid, ai_model=self.ai_model)
        self.assertEqual(new_grid, grid)

        # we dont expect any ai suggestion if end game
        self.assertIsNone(message)

    @patch("game.random_tile", return_value=(0, 2))
    @patch("game.random_value", return_value=2)
    def test_end_to_end(self, mock_tile, mock_value):

        initial_grid = [
            [256, 128, None],
            [512, 128, None],
            [1024, None, None],
        ]

        # ----------------------- STEP 1
        # Call AI suggestion, the board state does not change
        grid, ai_move = game_controller(Action.AI, initial_grid, ai_model=self.ai_model)
        self.assertEqual(Action.UP, ai_move)

        # apply ai suggestion
        grid, message = game_controller(ai_move, grid, ai_model=self.ai_model)
        self.assertEqual(message, "")

        # ----------------------- STEP 2
        # Call AI suggestion, the board state does not change
        grid, ai_move = game_controller(Action.AI, grid, ai_model=self.ai_model)
        self.assertEqual(Action.LEFT, ai_move)

        # apply ai suggestion
        grid, message = game_controller(ai_move, grid, ai_model=self.ai_model)
        self.assertEqual(message, "")

        # ----------------------- STEP 3
        # Call AI suggestion, the board state does not change
        grid, ai_move = game_controller(Action.AI, grid, ai_model=self.ai_model)
        self.assertEqual(Action.DOWN, ai_move)

        # apply ai suggestion
        grid, message = game_controller(ai_move, grid, ai_model=self.ai_model)
        self.assertEqual(message, "")

        # ----------------------- STEP 4
        # Call AI suggestion, the board state does not change
        grid, ai_move = game_controller(Action.AI, grid, ai_model=self.ai_model)
        self.assertEqual(Action.LEFT, ai_move)

        # apply ai suggestion
        grid, message = game_controller(ai_move, grid, ai_model=self.ai_model)
        self.assertEqual("", message)

        # ----------------------- STEP 5
        # Call AI suggestion, the board state does not change
        grid, ai_move = game_controller(Action.AI, grid, ai_model=self.ai_model)
        self.assertEqual(Action.LEFT, ai_move)

        # ----------------------- STEP 5
        grid, ai_move = game_controller(Action.AI, grid, ai_model=self.ai_model)
        grid, message = game_controller(ai_move, grid, ai_model=self.ai_model)
        self.assertEqual(Action.LEFT, ai_move)
        print_pretty(grid)

        # ----------------------- STEP 5
        grid, ai_move = game_controller(Action.AI, grid, ai_model=self.ai_model)
        grid, message = game_controller(ai_move, grid, ai_model=self.ai_model)
        self.assertEqual(Action.LEFT, ai_move)
        print_pretty(grid)

        # ----------------------- FINAL STEP 5
        grid, ai_move = game_controller(Action.AI, grid, ai_model=self.ai_model)
        grid, message = game_controller(ai_move, grid, ai_model=self.ai_model)
        self.assertEqual(Action.DOWN, ai_move)
        self.assertEqual(MESSAGE_WIN, message)
        print_pretty(grid)

        final_grid = [
            [None, None, None],
            [4, 2, None],
            [2048, 4, 2],
        ]

        self.assertEqual(final_grid, grid)
