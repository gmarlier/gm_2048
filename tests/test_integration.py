import logging

from unittest import TestCase
from unittest.mock import patch
from game import MESSAGE_LOSE, game_over, game_controller
from grid import (
    Action,
    move_generator,
    spawn_generator,
    sum_square,
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
            fitness=sum_square,
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

    @patch("game.random_tile", return_value=(0, 1))
    @patch("game.random_value", return_value=2)
    def _test_end_to_end(self, mock_tile, mock_value):

        grid = [
            [2, 4, 2],
            [4, 2, 4],
            [2, 4, 2],
        ]

        expected = [[4, 2], [4, None]]

        grid, message = game_controller(Action.AI, grid, ai_model=self.ai_model)
        self.assertEqual(expected, grid)
        self.assertEqual("", message)
