import logging
from math import inf
from unittest import TestCase, main
from game import game_over
from grid import down_move, fitness_snake_like_pattern, left_move, move_generator, right_move, spawn_generator, sum_square, Action, up_move
from ai import Expectimax

class AITestCase(TestCase):

    def setUp(self):
        logging.basicConfig(level=logging.DEBUG, format="%(asctime)s [%(levelname)s] %(message)s")

        self.ai_model = Expectimax(2, move_generator, spawn_generator, dead_end_function=game_over, fitness=sum_square)
        self.controllers = {
            Action.UP : up_move,
            Action.DOWN : down_move,
            Action.RIGHT: right_move,
            Action.LEFT: left_move,
        }

    def _test_fitness_function(self):

        
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

    def _test_expectimax_suggestion(self):
        
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

    def test_end_to_end_expectimax_decisions(self):

        def spawn_generator(board):
            yield board, 1

        ai_model = Expectimax(6, move_generator, spawn_generator, dead_end_function=game_over, fitness=sum_square)

        board = [
                [16,     8,      8 ],
                [32,    1024,   512],
                [64,    128,     256],
            ]
        self.assertEqual(Action.RIGHT, ai_model.best_move(board))
            
        board = [
                [None,    16,      16],
                [32,    1024,   512],
                [64,    128,     256],
            ]
        self.assertEqual(Action.LEFT, ai_model.best_move(board))

        board = [
                [32,    16,      None],
                [32,    1024,    512],
                [64,    128,     256],
            ]
        self.assertEqual(Action.UP, ai_model.best_move(board))

        board = [
                [64,    16,      512],
                [64,    1024,    256],
                [None,  128  ,  None],
            ]
        self.assertEqual(Action.DOWN, ai_model.best_move(board))

        board = [
                [None,    16,    None],
                [None,    1024,    512],
                [128,     128  ,   256],
            ]
        self.assertEqual(Action.RIGHT, ai_model.best_move(board))

        board = [
                [None,    None,    16],
                [None,    1024,    512],
                [None,     256,   256],
            ]
        self.assertEqual(Action.RIGHT, ai_model.best_move(board))

        board = [
                [None,    None,    16],
                [None,    1024,    512],
                [None,     None,   512],
            ]
        self.assertEqual(Action.UP, ai_model.best_move(board))

        board = [
                [None,    1024,      16],
                [None,    None,    1024],
                [None,     None,    512],
            ]
        self.assertEqual(Action.UP, ai_model.best_move(board))


if __name__ == '__main__':
    main()
