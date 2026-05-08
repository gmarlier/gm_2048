import math
import logging
from abc import abstractmethod
from typing import Callable
from grid import Action
from random import choice

class AbstractAI:
    ''' my comment '''

    def __init__(self, max_depth, move_generator, spawn_generator, game_over: Callable, fitness: Callable):
        self.max_depth = max_depth
        self.move_generator = move_generator
        self.spawn_generator = spawn_generator
        self.game_over = game_over
        self.fitness = fitness

    @abstractmethod
    def score_actions(self, board) -> dict[Action, float]:
        raise NotImplementedError

    @abstractmethod
    def best_move(self, board, move_generator, spawn_generator, game_over: Callable, fitness: Callable) -> Action:
        raise NotImplementedError
    
    def search(self, board, depth, is_player):
    
        if depth == 0 or (is_player and self.game_over(board)):
            return self.fitness(board)

        score = self.fitness(board)

        # if player, select a player iterator, otherwise, select empty-tiles iterator
        if is_player:
            for child_board, action in self.move_generator(board):
                child_score = self.search(child_board, depth-1, False)
                score = max(score, child_score)
                logging.debug(f'depth={depth} score={score} action={action}')

        else:  
            scores = []
            child_score = 0
            for child_board, proba in self.spawn_generator(board):
                child_score += self.search(child_board, depth-1, True)
                scores.append(child_score)
            if scores:
                score = sum(scores) / len(scores)
            logging.debug(f'depth={depth} score={score} spawn new tile')
            
        return score

class Expectimax(AbstractAI):

    def __init__(self, max_depth, move_generator, spawn_generator, game_over: Callable, fitness: Callable):
        super().__init__(max_depth, move_generator, spawn_generator, game_over, fitness)

    def score_actions(self, board) -> dict[Action, float]:
        score_actions = {}
        for child_board, action in self.move_generator(board):
            score_actions[action] = self.search(child_board, self.max_depth, False)
        return score_actions

    def best_move(self, board) -> Action:
        
        best_score = -math.inf
        best_action = None
        for action, score in self.score_actions(board).items():
            logging.debug(f'best move score={score} action={action}')
            if score > best_score:
                best_score = score
                best_action = action
        return best_action

    
    
class DummyAI(AbstractAI):
    '''
    Dummy implementation of AI suggestion.

    The model picks one move randomly. For integration test purpose only
    '''

    def best_move(self, board, move_generator, spawn_generator, fitness: Callable) -> Action:
        return choice([Action.LEFT, Action.RIGHT, Action.UP, Action.DOWN])