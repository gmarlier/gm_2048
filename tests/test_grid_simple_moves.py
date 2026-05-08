import logging
from unittest import TestCase, main
from grid import transpose_matrix, flip_matrix, left_move, right_move, down_move, up_move

class GridMoveTestCase(TestCase):

    def setUp(self):
        logging.basicConfig(level=logging.DEBUG, format="%(asctime)s [%(levelname)s] %(message)s")
    
    def test_edge_cases(self):
        
        cases = [
            ([[2]], [[2]]),
            ([[2,4]], [[2],[4]]),
            ([[None, None]], [[None],[None]]),
        ]
        for value, expected in cases:
            with self.subTest(value):
                self.assertEqual(expected, transpose_matrix(value))



    def test_transpose_matrix(self):

        initial_grid = [
            [1, None, 2, None],
            [None, 3, None, 4],
            [5, None, 6, None],
        ]

        expected_grid = [
            [1,     None,    5],
            [None,  3,    None],
            [2,     None,    6],
            [None,  4,    None],
        ]
        self.assertEqual(expected_grid, transpose_matrix(initial_grid))

    def test_flip_matrix(self):

        initial_grid = [
            [1, None, 2, None],
            [None, 3, None, 4],
            [5, None, 6, None],
        ]

        expected_grid = [
            [None, 2, None, 1],
            [4   , None,3, None],
            [None, 6, None, 5],
        ]
        self.assertEqual(expected_grid, flip_matrix(initial_grid))

    def test_left_move(self):

        initial_grid = [
            [2, None, 2, None],
            [None, 2, None, 2],
            [2, None, 2, None],
            [None, 2, None, 2],
        ]

        expected_grid = [
            [4, None, None, None],
            [4, None, None, None],
            [4, None, None, None],
            [4, None, None, None],
        ]

        self.assertEqual((expected_grid, True), left_move(initial_grid))

    def test_right_move(self):

        initial_grid = [
            [2, None, 2, None],
            [None, 2, None, 2],
            [2, None, 2, None],
            [None, 2, None, 2],
        ]

        expected_grid = [
            [None, None, None, 4],
            [None, None, None, 4],
            [None, None, None, 4],
            [None, None, None, 4],
        ]
        self.assertEqual((expected_grid, True), right_move(initial_grid))

    def test_down_move(self):

        initial_grid = [
            [2, None, 2, None],
            [None, 2, None, 2],
            [2, None, 2, None],
            [None, 2, None, 2],
        ]

        expected_grid = [
            [None, None, None, None],
            [None, None, None, None],
            [None, None, None, None],
            [4   , 4,    4,       4],
        ]
        self.assertEqual((expected_grid, True), down_move(initial_grid))

    def test_up_move(self):

        initial_grid = [
            [2, None, 2, None],
            [None, 2, None, 2],
            [2, None, 2, None],
            [None, 2, None, 2],
        ]

        expected_grid = [
            [4   , 4,    4,       4],
            [None, None, None, None],
            [None, None, None, None],
            [None, None, None, None],
        ]
        self.assertEqual((expected_grid, True), up_move(initial_grid))

    def test_change(self):

        initial_grid = [
            [2, None, 2, None],
            [None, 2, None, 2],
            [2, None, 2, None],
            [None, 2, None, 2],
        ]

        expected_grid = [
            [2, None, 2, None],
            [None, 2, None, 2],
            [2, None, 2, None],
            [None, 2, None, 2],
        ]
        self.assertTrue(initial_grid == expected_grid)

if __name__ == '__main__':
    main()
