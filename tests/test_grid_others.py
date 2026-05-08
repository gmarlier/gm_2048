import logging
from unittest import TestCase, main
from unittest.mock import patch
from grid import add_random_tile, empty_tiles, cannot_change

class GridRandomsTestCase(TestCase):

    def setUp(self):
        logging.basicConfig(level=logging.DEBUG, format="%(asctime)s [%(levelname)s] %(message)s")

    def test_random_new_tiles(self):

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

        with patch("grid.select_random_tile", return_value=((1,2),4)):
            next_grid = add_random_tile(grid)
            self.assertEqual(next_grid, expected_grid)

        # testing a different size 3*4
        grid = [
            [2, None,    2],
            [None, 2, None],
            [2, None,    2],
            [None, 2, None],
        ]

        expected_grid = [
            [2, None,    2],
            [None, 2,    4],
            [2, None,    2],
            [None, 2, None],
        ]

        with patch("grid.select_random_tile", return_value=((1,2),4)):
            next_grid = add_random_tile(grid)
            self.assertEqual(next_grid, expected_grid)

    def test_is_any_move_blocked(self):

        blocked = [
            [2, 4, 2, 4],
            [4, 2, 4, 2],
            [2, 4, 2, 4],
            [4, 2, 4, 2],
        ]
        self.assertTrue(cannot_change(blocked))

        not_blocked = [
            [2, 4, 2, 4],
            [4, 2, 2, 2],
            [2, 4, 2, 4],
            [4, 2, 4, 2],
        ]
        self.assertFalse(cannot_change(not_blocked))

        not_blocked = [
            [2, 4, 2, 4],
            [4, 2, None, 2],
            [2, 4, 2, 4],
            [4, 2, 4, 2],
        ]
        self.assertFalse(cannot_change(not_blocked))

    def test_empty_tiles(self):
        initial_grid = [
            [2, None, 2   ],
            [None, 2, None],
            [2, None, 2   ],
            [None, 2, None],
        ]

        expected_tiles = [(0,1),(1,0),(1,2),(2,1),(3,0),(3,2)]
        self.assertEqual(expected_tiles, empty_tiles(initial_grid))

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
        self.assertEqual(initial_grid, expected_grid)

if __name__ == '__main__':
    main()
