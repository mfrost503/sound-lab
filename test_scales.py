import unittest
from scales import get_scale

class TestScales(unittest.TestCase):

    def test_get_major_scale(self):
        self.assertEqual(get_scale('C', 'major'), ['C', 'D', 'E', 'F', 'G', 'A', 'B', 'C'])
        self.assertEqual(get_scale('G', 'major'), ['G', 'A', 'B', 'C', 'D', 'E', 'F#', 'G'])
        self.assertEqual(get_scale('F', 'major'), ['F', 'G', 'A', 'Bb', 'C', 'D', 'E', 'F'])
        self.assertEqual(get_scale('Db', 'major'), ['Db', 'Eb', 'F', 'Gb', 'Ab', 'Bb', 'C', 'Db'])
        with self.assertRaises(ValueError):
            get_scale('Z', 'major')

    def test_get_minor_scale(self):
        self.assertEqual(get_scale('A', 'minor'), ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'A'])
        self.assertEqual(get_scale('E', 'minor'), ['E', 'F#', 'G', 'A', 'B', 'C', 'D', 'E'])
        self.assertEqual(get_scale('C', 'minor'), ['C', 'D', 'Eb', 'F', 'G', 'Ab', 'Bb', 'C'])
        self.assertEqual(get_scale('G', 'minor'), ['G', 'A', 'Bb', 'C', 'D', 'Eb', 'F', 'G'])
        with self.assertRaises(ValueError):
            get_scale('X', 'minor')

    def test_get_mixolydian_scale(self):
        self.assertEqual(get_scale('G', 'mixolydian'), ['G', 'A', 'B', 'C', 'D', 'E', 'F', 'G'])
        self.assertEqual(get_scale('C', 'mixolydian'), ['C', 'D', 'E', 'F', 'G', 'A', 'Bb', 'C'])
        self.assertEqual(get_scale('D', 'mixolydian'), ['D', 'E', 'F#', 'G', 'A', 'B', 'C', 'D'])

    def test_get_phrygian_scale(self):
        self.assertEqual(get_scale('E', 'phrygian'), ['E', 'F', 'G', 'A', 'B', 'C', 'D', 'E'])
        self.assertEqual(get_scale('A', 'phrygian'), ['A', 'Bb', 'C', 'D', 'E', 'F', 'G', 'A'])
        self.assertEqual(get_scale('B', 'phrygian'), ['B', 'C', 'D', 'E', 'F#', 'G', 'A', 'B'])

if __name__ == '__main__':
    unittest.main()