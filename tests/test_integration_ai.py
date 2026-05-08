from unittest import TestCase
from game import game_over
from grid import Action, left_move, move_generator, right_move, spawn_generator, sum_square
from ai import Expectimax

class IntegrationAITest(TestCase):

    def setUp(self):
        self.ai_model = Expectimax(3, move_generator, spawn_generator, game_over=game_over, fitness=sum_square)

    def test_end_to_end(self):

        grid = [
            [2, 2, 2, 2, None]
        ]

        controllers = {
            Action.LEFT: left_move,
            Action.RIGHT: right_move
        }

        def score():
            return 1
        
        #ai.suggest(grid, controllers, score_func=score, empty_tiles_func= )