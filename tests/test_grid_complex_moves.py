from unittest import TestCase, main
from grid import down_move

class GridMoveTestCase(TestCase):

    def test_down_move(self):

        initial_grid = [
            [2],
            [2],
            [4],
            [4],
            [4]
        ]

        expected_grid = [
            [None],
            [None],
            [4],
            [4],
            [8]
        ]
        self.assertEqual((expected_grid, True), down_move(initial_grid))

if __name__ == '__main__':
    main()
