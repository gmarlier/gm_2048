import logging
from math import inf
from unittest import TestCase, main
from game import game_over
from grid import fitness_snake_like_pattern, move_generator, spawn_generator, sum_square, Action
from ai import Expectimax

class AITestCase(TestCase):

    def setUp(self):
        logging.basicConfig(level=logging.DEBUG, format="%(asctime)s [%(levelname)s] %(message)s")

        self.ai_model = Expectimax(2, move_generator, spawn_generator, game_over=game_over, fitness=sum_square)

    def test_fitness_function(self):

        
        grid = [
            [2,       4],
            [None,    4],
        ]

        self.assertEqual(36, sum_square(grid))
        #self.assertEqual(10, fitness_snake_like_pattern(grid))
        
        grid = [
            [None, None],
            [None, None],
        ]

        self.assertEqual(-inf, sum_square(grid))
        #self.assertEqual(-inf, fitness_snake_like_pattern(grid))

    def test_expectimax_suggestion(self):
        
        grid = [
                [2,       4],
                [None,    4],
            ]
        
        expected_scores = {
            Action.UP: 116,
            Action.RIGHT: 80,
            Action.DOWN: 116,
            Action.LEFT: -inf
        }

        score_actions = self.ai_model.score_actions(grid)
        self.assertDictEqual(expected_scores , score_actions)

        best_action = self.ai_model.best_move(grid)
        self.assertEqual(Action.UP, best_action)

        score_actions = self.ai_model.score_actions(grid)
        self.assertDictEqual(expected_scores , score_actions)
        self.assertEqual(Action.UP, best_action)

        score_actions = self.ai_model.score_actions(grid)
        self.assertDictEqual(expected_scores , score_actions)
        self.assertEqual(Action.UP, best_action)



if __name__ == '__main__':
    main()
