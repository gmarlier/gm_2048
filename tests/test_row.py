from unittest import TestCase, main
from grid import compress, merge

class RowTestCase(TestCase):

    def test_merge(self):

        before = [2 , 2 , None, None]
        expected = [4 , None , None, None]
        self.assertEqual(expected, merge(before))

    def test_compress(self):

        before = [None, 2, None, 2]
        expected = [2 , 2 , None, None]
        self.assertEqual(expected, compress(before))

    def test_move(self):

        before = [2 , 2 , None, None]
        expected = [4 , None , None, None]
        self.assertEqual(expected, merge(before))


if __name__ == '__main__':
    main()
