"""
Unit tests for game module
"""

import logging
from math import inf
from unittest import TestCase, main
from unittest.mock import patch
from game import (
    game_controller,
    game_over,
    game_with_random_tile,
    player_win,
    player_lose,
)
from grid import Action, left_move, right_move


class GameTestCase(TestCase):

    def setUp(self):
        logging.basicConfig(
            level=logging.DEBUG, format="%(asctime)s [%(levelname)s] %(message)s"
        )

    def test_game_states(self):

        # testing no further moves possible
        grid = [[2]]
        self.assertTrue(game_over(grid))
        self.assertFalse(player_win(grid))
        self.assertTrue(player_lose(grid))

        # testing no further moves possible
        grid = [[2, 4, 2, 4], [4, 2, 4, 2], [2, 4, 2, 4], [4, 2, 4, 2]]
        self.assertTrue(game_over(grid))
        self.assertFalse(player_win(grid))
        self.assertTrue(player_lose(grid))

        # testing game with possible move
        grid = [[2, None]]
        self.assertFalse(game_over(grid))
        self.assertFalse(player_win(grid))
        self.assertFalse(player_lose(grid))

        # testing game with possible move
        grid = [
            [2, 2, 8],
            [16, 32, 65],
        ]
        self.assertFalse(game_over(grid))
        self.assertFalse(player_win(grid))
        self.assertFalse(player_lose(grid))

        # testing winning game
        grid = [[2048]]
        self.assertTrue(game_over(grid))
        self.assertTrue(player_win(grid))
        self.assertFalse(player_lose(grid))

        grid = [
            [4, None, None, 2],
            [2048, None, None, None],
            [4, 2, None, None],
            [4, None, None, None],
        ]
        self.assertTrue(game_over(grid))
        self.assertTrue(player_win(grid))
        self.assertFalse(player_lose(grid))

    @patch("game.random_tile", return_value=(1, 2))
    @patch("game.random_value", return_value=4)
    def test_game_random_new_tiles(self, mock_tile, mock_value):

        grid = [
            [2, None, 2, None],
            [None, 2, None, 2],
            [2, None, 2, None],
            [None, 2, None, 2],
        ]

        expected_grid = [
            [2, None, 2, None],
            [None, 2, 4, 2],
            [2, None, 2, None],
            [None, 2, None, 2],
        ]

        # test a new tile '4' is added into an empty cell
        next_grid = game_with_random_tile(grid)
        self.assertEqual(next_grid, expected_grid)

    @patch("game.random_tile", return_value=(0, 0))
    @patch("game.random_value", return_value=2)
    def test_controller_down(self, mock_tile, mock_value):

        grid = [
            [2, 2, None],
            [2, 2, None],
            [2, 2, None],
        ]

        expected = [
            [2, None, None],
            [2, 2, None],
            [4, 4, None],
        ]

        grid, message = game_controller(Action.DOWN, grid)
        self.assertEqual(expected, grid)
        self.assertEqual("", message)

    @patch("game.random_tile", return_value=(0, 0))
    @patch("game.random_value", return_value=4)
    def test_controller_right(self, mock_tile, mock_value):

        grid = [
            [2, 2, None],
            [2, 2, None],
            [2, 2, None],
        ]

        expected = [
            [4, None, 4],
            [None, None, 4],
            [None, None, 4],
        ]

        grid, message = game_controller(Action.RIGHT, grid)
        self.assertEqual(expected, grid)
        self.assertEqual("", message)

    @patch("game.random_tile", return_value=(0, 1))
    @patch("game.random_value", return_value=2)
    def test_controller_left(self, mock_tile, mock_value):

        grid = [
            [2, 2, None],
            [2, 2, None],
            [2, 2, None],
        ]

        expected = [
            [4, 2, None],
            [4, None, None],
            [4, None, None],
        ]

        grid, message = game_controller(Action.LEFT, grid)
        self.assertEqual(expected, grid)
        self.assertEqual("", message)

    @patch("game.random_tile", return_value=(2, 2))
    @patch("game.random_value", return_value=4)
    def test_controller_left(self, mock_tile, mock_value):

        grid = [
            [2, 2, None],
            [2, 2, None],
            [2, 2, None],
        ]

        expected = [
            [4, 4, None],
            [2, 2, None],
            [None, None, 4],
        ]

        grid, message = game_controller(Action.UP, grid)
        self.assertEqual(expected, grid)
        self.assertEqual("", message)
