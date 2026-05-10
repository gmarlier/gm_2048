import logging
from math import inf
from unittest import TestCase, main
from game import game_over
from grid import (
    down_move,
    fitness_snake,
    left_move,
    move_generator,
    right_move,
    spawn_generator,
    sum_square,
    Action,
    up_move,
)
from ai import Expectimax


class AITestCase(TestCase):

    def setUp(self):
        logging.basicConfig(
            level=logging.DEBUG, format="%(asctime)s [%(levelname)s] %(message)s"
        )

        self.ai_model = Expectimax(
            2,
            move_generator,
            spawn_generator,
            endgame_condition=game_over,
            fitness=sum_square,
        )
        self.controllers = {
            Action.UP: up_move,
            Action.DOWN: down_move,
            Action.RIGHT: right_move,
            Action.LEFT: left_move,
        }

    def test_fitness_function(self):

        grid = [
            [2, 4],
            [None, 4],
        ]

        self.assertEqual(36, sum_square(grid))
        self.assertEqual(-15.756, fitness_snake(grid))

        grid = [
            [None, None],
            [None, None],
        ]

        self.assertEqual(-inf, sum_square(grid))
        self.assertEqual(-inf, fitness_snake(grid))

        # ideal "snake" board configuration
        grid = [
            [128, 64, 0, 0],
            [256, 32, 2, 0],
            [512, 16, 2, 0],
            [1024, 8, 4, 0],
        ]

        self.assertEqual(1077, int(fitness_snake(grid)))

        # a bit worse "snake" board configuration, expect a lower score
        grid = [
            [64, 4, 0, 0],
            [128, 8, 0, 0],
            [256, 16, 2, 0],
            [512, 32, 2, 0],
        ]

        # a bit worse "snake" board configuration, expect a lower score
        self.assertEqual(538, int(fitness_snake(grid)))

        grid = [
            [32, 2, 0, 0],
            [64, 4, 0, 0],
            [128, 8, 0, 0],
            [256, 16, 2, 0],
        ]

        # a bit worse "snake" board configuration, expect a lower score
        self.assertEqual(269, int(fitness_snake(grid)))

    def test_expectimax_suggestion(self):

        grid = [
            [2, 4],
            [None, 4],
        ]

        expected_scores = {
            Action.UP: 80,
            Action.DOWN: 80,
            Action.LEFT: -inf,
        }

        score_actions = self.ai_model.score_actions(grid)
        self.assertDictEqual(expected_scores, score_actions)

        best_action = self.ai_model.best_move(grid)
        self.assertEqual(Action.UP, best_action)

        score_actions = self.ai_model.score_actions(grid)
        self.assertDictEqual(expected_scores, score_actions)
        self.assertEqual(Action.UP, best_action)

        score_actions = self.ai_model.score_actions(grid)
        self.assertDictEqual(expected_scores, score_actions)
        self.assertEqual(Action.UP, best_action)

    def test_end_to_end_expectimax_decisions(self):

        def spawn_generator(board):
            yield board, 1

        ai_model = Expectimax(
            6,
            move_generator,
            spawn_generator,
            endgame_condition=game_over,
            fitness=sum_square,
        )

        board = [
            [2, 4, 2],
            [4, 2, 4],
            [2, 4, 2],
        ]

        expected_scores = {
            Action.UP: -inf,
            Action.DOWN: -inf,
            Action.LEFT: -inf,
            Action.RIGHT: -inf,
        }
        logging.info(ai_model.search(board, 6, is_player=True))
        logging.info(f"action scores={ai_model.score_actions(board)}")
        self.assertEqual({}, ai_model.score_actions(board))
        self.assertEqual(None, ai_model.best_move(board))

        board = [
            [4, 2, 8],
            [2, 4, 4],
            [4, 2, None],
            [2, 4, 2],
        ]

        # calculate the score of the current boart
        ai_model.max_depth = 0
        final_score = ai_model.search(board, ai_model.max_depth, is_player=True)
        logging.info(f"max depth={ai_model.max_depth} final score={final_score}")
        self.assertEqual(164, final_score)

        # calculate the max score after 1 move in each direction
        ai_model.max_depth = 1
        final_score = ai_model.search(board, ai_model.max_depth, is_player=True)
        logging.info(f"max depth={ai_model.max_depth} final score={final_score}")
        self.assertEqual(196, final_score)

        # calculate the max score after 2 recursive moves in each direction
        ai_model.max_depth = 2
        final_score = ai_model.search(board, ai_model.max_depth, is_player=True)
        logging.info(f"max depth={ai_model.max_depth} final score={final_score}")
        self.assertEqual(196, final_score)

        ai_model.max_depth = 3
        board = [
            [None, 16, 16],
            [32, 1024, 512],
            [64, 128, 256],
        ]
        self.assertEqual(Action.LEFT, ai_model.best_move(board))

        board = [
            [32, 16, None],
            [32, 1024, 512],
            [64, 128, 256],
        ]
        self.assertEqual(Action.UP, ai_model.best_move(board))

        board = [
            [64, 16, 512],
            [64, 1024, 256],
            [None, 128, None],
        ]
        self.assertEqual(Action.DOWN, ai_model.best_move(board))

        board = [
            [None, 16, None],
            [None, 1024, 512],
            [128, 128, 256],
        ]
        self.assertEqual(Action.RIGHT, ai_model.best_move(board))

        board = [
            [None, None, 16],
            [None, 1024, 512],
            [None, 256, 256],
        ]
        self.assertEqual(Action.RIGHT, ai_model.best_move(board))

        board = [
            [None, None, 16],
            [None, 1024, 512],
            [None, None, 512],
        ]
        self.assertEqual(Action.DOWN, ai_model.best_move(board))

        board = [
            [None, None, None],
            [None, None, 16],
            [None, 1024, 1024],
        ]
        self.assertEqual(Action.RIGHT, ai_model.best_move(board))


if __name__ == "__main__":
    main()
