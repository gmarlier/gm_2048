"""
Unit tests for AI module
"""

import logging
from math import inf
from unittest import TestCase, main
from game import MESSAGE_WIN, game_over
from grid import (
    down_move,
    fitness_snake,
    left_move,
    move_generator,
    pprint,
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

        self.ai_with_simple_fitness = Expectimax(
            2,
            move_generator,
            spawn_generator,
            endgame_condition=game_over,
            fitness=sum_square,
        )

        self.ai_with_snake_fitness = Expectimax(
            2,
            move_generator,
            spawn_generator,
            endgame_condition=game_over,
            fitness=fitness_snake,
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

        # ideal "snake" pattern board configuration
        grid = [
            [128, 64, 0, 0],
            [256, 32, 2, 0],
            [512, 16, 2, 0],
            [1024, 8, 4, 0],
        ]

        self.assertEqual(1077, int(fitness_snake(grid)))

        # a bit worse "snake" pattern board configuration, expect a lower score
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

        grid = [
            [32, 2, 0, 0],
            [64, 4, 256, 0],
            [128, 8, 0, 0],
            [0, 16, 2, 0],
        ]

        # the worse "snake" pattern board configuration since the lower
        #  left corner does not contain the biggest tile
        self.assertEqual(-65522, int(fitness_snake(grid)))

    def test_score_actions(self):

        grid = [
            [2, 4],
            [None, 4],
        ]

        expected_scores = {
            Action.UP: 80,
            Action.DOWN: 80,
            Action.LEFT: -inf,
        }

        score_actions = self.ai_with_simple_fitness.score_actions(grid)
        self.assertDictEqual(expected_scores, score_actions)

        score_actions = self.ai_with_simple_fitness.score_actions(grid)
        self.assertDictEqual(expected_scores, score_actions)

        score_actions = self.ai_with_simple_fitness.score_actions(grid)
        self.assertDictEqual(expected_scores, score_actions)

    def test_search(self):

        # just test with a mock random tile generator
        def dummy_spawn_generator(board):
            yield board, 1

        ai_model = Expectimax(
            6,
            move_generator,
            dummy_spawn_generator,
            endgame_condition=game_over,
            fitness=sum_square,
        )

        board = [
            [2, 4, 2],
            [4, 2, 4],
            [2, 4, 2],
        ]

        logging.info(ai_model.search(board, 6, is_player=True))

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

    def test_best_move(self):

        board = [
            [128, 64, None, None],
            [256, 32, 2, None],
            [512, 16, 2, None],
            [1024, 8, 4, None],
        ]

        expected_final = [
            [None, None, None, None],
            [None, None, None, None],
            [None, None, None, None],
            [2048, None, None, None],
        ]
        best = self.ai_with_snake_fitness.best_move(board)
        self.assertEqual(Action.DOWN, self.ai_with_snake_fitness.best_move(board))
        board, message = self.controllers[best](board)
        pprint(board, message)

        best = self.ai_with_snake_fitness.best_move(board)
        self.assertEqual(Action.DOWN, self.ai_with_snake_fitness.best_move(board))
        board, message = self.controllers[best](board)
        pprint(board, message)

        best = self.ai_with_snake_fitness.best_move(board)
        self.assertEqual(Action.LEFT, self.ai_with_snake_fitness.best_move(board))
        board, message = self.controllers[best](board)
        pprint(board, message)

        best = self.ai_with_snake_fitness.best_move(board)
        self.assertEqual(Action.UP, self.ai_with_snake_fitness.best_move(board))
        board, message = self.controllers[best](board)
        pprint(board, message)

        best = self.ai_with_snake_fitness.best_move(board)
        self.assertEqual(Action.UP, self.ai_with_snake_fitness.best_move(board))
        board, message = self.controllers[best](board)
        pprint(board, message)

        best = self.ai_with_snake_fitness.best_move(board)
        self.assertEqual(Action.UP, self.ai_with_snake_fitness.best_move(board))
        board, message = self.controllers[best](board)
        pprint(board, message)

        best = self.ai_with_snake_fitness.best_move(board)
        self.assertEqual(Action.LEFT, self.ai_with_snake_fitness.best_move(board))
        board, message = self.controllers[best](board)
        pprint(board, message)

        best = self.ai_with_snake_fitness.best_move(board)
        self.assertEqual(Action.DOWN, self.ai_with_snake_fitness.best_move(board))
        board, message = self.controllers[best](board)
        pprint(board, message)

        best = self.ai_with_snake_fitness.best_move(board)
        self.assertEqual(Action.DOWN, self.ai_with_snake_fitness.best_move(board))
        board, message = self.controllers[best](board)
        pprint(board, message)

        best = self.ai_with_snake_fitness.best_move(board)
        self.assertEqual(Action.DOWN, self.ai_with_snake_fitness.best_move(board))
        board, message = self.controllers[best](board)
        pprint(board, message)

        self.assertEqual(expected_final, board)


if __name__ == "__main__":
    main()
