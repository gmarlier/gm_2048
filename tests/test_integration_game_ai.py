import logging

from unittest import TestCase
from unittest.mock import patch
from game import game_over, game_controller
from grid import Action, left_move, move_generator, right_move, spawn_generator, sum_square
from ai import Expectimax

class IntegrationAITest(TestCase):

    def setUp(self):
        logging.basicConfig(level=logging.DEBUG, format="%(asctime)s [%(levelname)s] %(message)s")
        self.ai_model = Expectimax(3, move_generator, spawn_generator, dead_end_function=game_over, fitness=sum_square)
    
    @patch("game.random_tile", return_value=(0,1))
    @patch("game.random_value", return_value=2)
    def test_end_to_end(self,  mock_tile, mock_value):

        grid = [
            [2, 2],
            [2, 2]
        ]

        expected = [
            [4, 2],
            [4, None]
        ]

        grid, message = game_controller(Action.LEFT, grid, ai_model=self.ai_model)
        self.assertEqual(expected, grid)    
        self.assertEqual('', message)    
       
