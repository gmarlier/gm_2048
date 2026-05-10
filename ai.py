"""
Module to provide ai generic class and specific ai resolvers

Available classes:
- AbstractAI: base class implementing search framework of game configuration
- Expectimax: specialized class to select the most efficient move
- DummyAI: specialized class to select random move

"""

import math
import logging
from abc import abstractmethod
from typing import Callable
from grid import Action
from random import choice


class AbstractAI:
    """Generic class that implements a seach method to find all configuration of any game

    Public attributes:
    - max_depth: The maximum level to estimate a game configuration
    - move_generator: an iterator over all states of possible player move
      for example: in 2048, it will provides 4 different board states for each move Up, Right, Down, Left
    - spawn_generator: an interator over all states of random game event.
      for exemple: in 2048, it will generate the sequence of all board states for tiles spawn randomly
    - dead_end_function: function used to indicates a game configuration should not be explored further
    - fitness_function: function to assess the score of a game configuration
    """

    def __init__(
        self,
        max_depth,
        move_generator,
        spawn_generator,
        dead_end_function: Callable,
        fitness: Callable,
    ):
        self.max_depth = max_depth
        self.move_generator = move_generator
        self.spawn_generator = spawn_generator
        self.endgame_condition = dead_end_function
        self.fitness = fitness

    @abstractmethod
    def score_actions(self, board) -> dict[Action, float]:
        raise NotImplementedError

    @abstractmethod
    def best_move(
        self,
        board,
        move_generator,
        spawn_generator,
        endgame_condition: Callable,
        fitness: Callable,
    ) -> Action:
        raise NotImplementedError

    def search(self, board, depth, is_player):

        indent = " " * ((self.max_depth - depth) * 3)
        if depth == 0 or (is_player and self.endgame_condition(board)):
            score = self.fitness(board)
            logging.debug(f"{indent} depth={depth} score={score}")
            return score

        score = self.fitness(board)

        # if player, select a player iterator, otherwise, select empty-tiles iterator
        if is_player:
            scores = []
            for child_board, action in self.move_generator(board):
                logging.debug(f"{indent} depth={depth} action={action}")
                child_score = self.search(child_board, depth - 1, False)
                scores.append(child_score)
            if scores:
                score = max(scores)

        else:
            scores = []
            accumulated_score = 0
            for index, (child_board, proba) in enumerate(self.spawn_generator(board)):
                logging.debug(f"{indent} depth={depth} action=random")
                child_score = self.search(child_board, depth - 1, True)
                accumulated_score += proba * child_score
                # logging.debug(f"{indent} depth={depth-1} score={child_score}\n")
                scores.append(child_score)
            if scores:
                score = sum(scores) / len(scores)
                # logging.debug(f"depth={depth-1} average score expectancy={score}\n")

        logging.debug(f"{indent} depth={depth} best score={score}")
        return score


class Expectimax(AbstractAI):

    def __init__(
        self,
        max_depth,
        move_generator,
        spawn_generator,
        endgame_condition: Callable,
        fitness: Callable,
    ):
        super().__init__(
            max_depth, move_generator, spawn_generator, endgame_condition, fitness
        )

    def score_actions(self, board) -> dict[Action, float]:
        score_actions = {}
        for child_board, action in self.move_generator(board):
            score_actions[action] = self.search(child_board, self.max_depth, False)
        logging.info(f"depth={self.max_depth} scores={score_actions}")
        return score_actions

    def best_move(self, board) -> Action:

        best_score = -math.inf
        best_action = None
        for action, score in self.score_actions(board).items():
            logging.debug(f"best move score={score} action={action}")
            if score > best_score:
                best_score = score
                best_action = action
        return best_action


class DummyAI(AbstractAI):
    """
    Dummy implementation of AI suggestion.

    The model picks one move randomly. For integration test purpose only
    """

    def best_move(
        self,
        board,
        move_generator,
        spawn_generator,
        dead_end_function,
        fitness: Callable,
    ) -> Action:
        return choice([Action.LEFT, Action.RIGHT, Action.UP, Action.DOWN])
